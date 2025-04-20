from collections import defaultdict
from typing import List

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.catalog import Column
from pyspark.sql.functions import when, isnull
from pyspark.sql.types import StructType, StringType, StructField

from wedata.feature_store.entities.feature import Feature
from wedata.feature_store.entities.feature_table import FeatureTable
from wedata.feature_store.entities.function_info import FunctionParameterInfo, FunctionInfo
from wedata.feature_store.utils.common_utils import unsanitize_identifier, sanitize_multi_level_name


class SparkClient:
    def __init__(self, spark: SparkSession):
        self._spark = spark


    def get_current_catalog(self):
        """
        获取当前Spark会话的catalog名称（使用spark.catalog.currentCatalog属性）

        返回:
            str: 当前catalog名称，如果未设置则返回None
        """
        try:
            return unsanitize_identifier(self._spark.catalog.currentCatalog())
        except Exception:
            return None

    def get_current_database(self):
        """
        获取Spark上下文中当前设置的数据库名称

        返回:
            str: 当前数据库名称，如果获取失败则返回None
        """
        try:
            # 使用Spark SQL查询当前数据库
            df = self._spark.sql("SELECT CURRENT_DATABASE()")
            # 获取第一行第一列的值并去除特殊字符
            return unsanitize_identifier(df.first()[0])
        except Exception:
            # 捕获所有异常并返回None
            return None




    def createDataFrame(self, data, schema) -> DataFrame:
        return self._spark.createDataFrame(data, schema)


    def read_table(self, table_name):
        """读取Spark表数据

        Args:
            table_name: 表名，支持格式: catalog.schema.table、schema.table 或 table

        Returns:
            DataFrame: 表数据

        Raises:
            ValueError: 当表不存在或读取失败时抛出
        """
        try:
            # 解析表名
            parts = table_name.split('.')
            if len(parts) == 3:
                catalog, schema, table = parts
            elif len(parts) == 2:
                schema, table = parts
            else:
                table = table_name

            # 验证表是否存在
            if not self._spark.catalog.tableExists(table):
                raise ValueError(f"表不存在: {table_name}")

            return self._spark.table(table)

        except Exception as e:
            raise ValueError(f"读取表 {table_name} 失败: {str(e)}")


    def get_features(self, table_name):
        # 解析表名
        parts = table_name.split('.')
        if len(parts) == 3:
            # 对于三部分名称(catalog.schema.table)，使用schema.table格式
            _, schema, table = parts
            full_table_name = f"{schema}.{table}"
        elif len(parts) == 2:
            # 对于两部分名称(schema.table)，直接使用
            full_table_name = table_name
        else:
            # 单表名，使用当前数据库
            current_db = self.get_current_database()
            if not current_db:
                raise ValueError("无法确定当前数据库")
            full_table_name = f"{current_db}.{table_name}"

        # 使用dbName.tableName格式查询列信息
        columns = self._spark.catalog.listColumns(tableName=full_table_name)
        return [
            Feature(
                feature_table=table_name,
                feature_id=f"{table_name}_{row.name}",
                name=row.name,
                data_type=row.dataType,
                description=row.description or ""
            ) for row in columns
        ]

    def get_feature_table(self, table_name):

        # 获取表元数据
        table = self._spark.catalog.getTable(table_name)

        parts = table_name.split('.')
        if len(parts) == 3:
            # 对于三部分名称(catalog.schema.table)，只使用表名部分
            table_to_describe = parts[2]
        elif len(parts) == 2:
            # 对于两部分名称(schema.table)，只使用表名部分
            table_to_describe = parts[1]
        else:
            # 单表名，直接使用
            table_to_describe = table_name
        # 获取表详细信息
        table_details = self._spark.sql(f"DESCRIBE TABLE EXTENDED {table_to_describe}").collect()

        table_properties = {}
        for row in table_details:
            if row.col_name == "Table Properties":
                props = row.data_type[1:-1].split(", ")
                table_properties = dict(p.split("=") for p in props if "=" in p)

        # 获取特征列信息
        features = self.get_features(table_name)

        # 构建完整的FeatureTable对象
        return FeatureTable(
            name=table_name,
            table_id=table_properties.get("table_id", table_name),
            description=table.description or table_properties.get("comment", table_name),
            primary_keys=table_properties.get("primaryKeys", "").split(",") if table_properties.get("primaryKeys") else [],
            partition_columns=table.partitionColumnNames if hasattr(table, 'partitionColumnNames') else [],
            features=features,
            creation_timestamp=None,  # Spark表元数据不包含创建时间戳
            online_stores=None,
            notebook_producers=None,
            job_producers=None,
            table_data_sources=None,
            path_data_sources=None,
            custom_data_sources=None,
            timestamp_keys=table_properties.get("timestamp_keys"),
            tags=table_properties
        )

    def _get_routines_with_parameters(self, full_routine_names: List[str]) -> DataFrame:
        """
        Retrieve the routines with their parameters from information_schema.routines, information_schema.parameters.
        Return DataFrame only contains routines that 1. exist and 2. the caller has GetFunction permission on.

        Note: The returned DataFrame contains the cartesian product of routines and parameters.
        For efficiency, routines table columns are only present in the first row for each routine.
        """
        routine_name_schema = StructType(
            [
                StructField("specific_catalog", StringType(), False),
                StructField("specific_schema", StringType(), False),
                StructField("specific_name", StringType(), False),
            ]
        )
        routine_names_df = self.createDataFrame(
            [full_routine_name.split(".") for full_routine_name in full_routine_names],
            routine_name_schema,
        )
        routines_table = self.read_table(
            "system.information_schema.routines"
        )
        parameters_table = self.read_table(
            "system.information_schema.parameters"
        )

        # Inner join routines table to filter out non-existent routines.
        # Left join parameters as routines may have no parameters.
        full_routines_with_parameters_df = routine_names_df.join(
            routines_table, on=routine_names_df.columns, how="inner"
        ).join(parameters_table, on=routine_names_df.columns, how="left")

        # Return only relevant metadata from information_schema, sorted by routine name + parameter order.
        # For efficiency, only preserve routine column values in the first of each routine's result rows.
        # The first row will have parameter.ordinal_value is None (no parameters) or equals 0 (first parameter).
        def select_if_first_row(col: Column) -> Column:
            return when(
                isnull(parameters_table.ordinal_position)
                | (parameters_table.ordinal_position == 0),
                col,
                ).otherwise(None)

        return full_routines_with_parameters_df.select(
            routine_names_df.columns
            + [
                select_if_first_row(routines_table.routine_definition).alias(
                    "routine_definition"
                ),
                select_if_first_row(routines_table.external_language).alias(
                    "external_language"
                ),
                parameters_table.ordinal_position,
                parameters_table.parameter_name,
                parameters_table.full_data_type,
            ]
        ).sort(routine_names_df.columns + [parameters_table.ordinal_position])

    def get_functions(self, full_function_names: List[str]) -> List[FunctionInfo]:
        """
        Retrieves and maps Unity Catalog functions' metadata as FunctionInfos.
        """
        # Avoid unnecessary Spark calls and return if empty.
        if not full_function_names:
            return []

        # Collect dict of routine name -> DataFrame rows describing the routine.
        routines_with_parameters_df = self._get_routines_with_parameters(
            full_routine_names=full_function_names
        )
        routine_infos = defaultdict(list)
        for r in routines_with_parameters_df.collect():
            routine_name = f"{r.specific_catalog}.{r.specific_schema}.{r.specific_name}"
            routine_infos[routine_name].append(r)

        # Mock GetFunction DNE error, since information_schema does not throw.
        for function_name in full_function_names:
            if not function_name in routine_infos:
                raise ValueError(f"Function '{function_name}' does not exist.")

        # Map routine_infos into FunctionInfos.
        function_infos = []
        for function_name in full_function_names:
            routine_info = routine_infos[function_name][0]
            input_params = [
                FunctionParameterInfo(name=p.parameter_name, type_text=p.full_data_type)
                for p in routine_infos[function_name]
                if p.ordinal_position is not None
            ]
            function_infos.append(
                FunctionInfo(
                    full_name=function_name,
                    input_params=input_params,
                    routine_definition=routine_info.routine_definition,
                    external_language=routine_info.external_language,
                )
            )
        return function_infos


