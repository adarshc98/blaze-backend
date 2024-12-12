from blazingsql import BlazingContext
import cudf
import time

class BlazeSql:
    def __init__(self, data_dir, file_name):
        self.perfmon = True
        self.data_dir = data_dir
        self.file_name = file_name
        self.source_path = f"{self.data_dir}/{self.file_name}"

        self.bc = BlazingContext()

        self.cudf_df = self.optimized_load_data()
        self.register_table()

    def load_data(self):
        cudf_df = cudf.read_csv(self.source_path)
        return cudf_df

    def optimized_load_data(self):
        dtype_dict = {
            'timestamp': 'str',
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64'
        }
        start_time = time.time()
        cudf_df = cudf.read_csv(self.source_path, usecols=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
                                num_partitions=4, engine='cudf')
        loading_csv_time = time.time() - start_time
        if(self.perfmon):
            print('loading csv time', loading_csv_time)
        return cudf_df

    def register_table(self, table_name="root_table"):
        self.bc.create_table(table_name, self.cudf_df)

    def execute_query(self, query_to_be_exec):
        print(f"Executing query: {query_to_be_exec}")
        start_time = time.time()
        result = self.bc.sql(query_to_be_exec)
        loading_csv_time = time.time() - start_time
        if(self.perfmon):
            print('query exec time', loading_csv_time)
        return result

    def run(self, query_to_be_exec):
        result = self.execute_query(query_to_be_exec)
        print("Query Result:")
        print(result)
        return result

    def get_metadata(self):
        metadata = {
            "columns": list(self.cudf_df.columns),
            "dtypes": {col: str(self.cudf_df[col].dtype) for col in self.cudf_df.columns},
            "num_rows": len(self.cudf_df)
        }
        return metadata


# # Example usage:
# if __name__ == "__main__":
# data_dir = "input_csv"
# file_name = 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
# query="SELECT * FROM stock_market WHERE high = 190.91"
# stock_query = BlazeSql(data_dir, file_name)
# stock_query.run(query)
