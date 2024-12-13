import cudf
import time
from blazingsql import BlazingContext

class BlazeSql:
    def __init__(self, data_dir, file_name):
        # Initialize with file path components
        self.perfmon = True
        self.data_dir = data_dir
        self.file_name = file_name
        self.source_path = f"{self.data_dir}/{self.file_name}"

        # Initialize BlazingSQL context
        self.bc = BlazingContext()

        # Load the data into cuDF DataFrame
        self.cudf_df = self.optimized_load_data()
        self.register_table()

    def load_data(self):
        """Read the CSV file using cuDF."""
        print(f"Loading data from {self.source_path}...")
        cudf_df = cudf.read_csv(self.source_path)
        print("Data loaded successfully.")
        return cudf_df

    def optimized_load_data(self):
        # # Predefine column data types to avoid type inference
        dtype_dict = {
            'timestamp': 'str',
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64'
        }
        start_time = time.time()
        # Read CSV with optimized parameters
        cudf_df = cudf.read_csv(self.source_path, usecols=['timestamp', 'open', 'high', 'low', 'close', 'volume'], 
                                num_partitions=4, engine='cudf')
        loading_csv_time = time.time() - start_time
        if(self.perfmon):
            print('loading csv time', loading_csv_time)
        return cudf_df

    def register_table(self):
        """Register the cuDF DataFrame as a table in BlazingSQL."""
        self.bc.create_table('stock_market', self.cudf_df)
        print("Table registered in BlazingSQL.")

    def execute_query(self, query):
        """Execute a SQL query on the registered table."""
        print(f"Executing query: {query}")
        start_time = time.time()
        result = self.bc.sql(query)
        loading_csv_time = time.time() - start_time
        if(self.perfmon):
            print('query exec time', loading_csv_time)
        return result

    def run(self, query):
        result = self.execute_query(query)
        print("Query Result:")
        print(result)


# # Example usage:
# if __name__ == "__main__":
data_dir = "./app/csv"
file_name = 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
query="SELECT * FROM stock_market WHERE high = 190.91"
query="SELECT * FROM `stock_market` WHERE CAST(SUBSTRING(`timestamp`, 1, 10) AS DATE) IN (SELECT CAST(SUBSTRING(`timestamp`, 1, 10) AS DATE) FROM `stock_market` GROUP BY CAST(SUBSTRING(`timestamp`, 1, 10) AS DATE) ORDER BY MAX(`open`) DESC LIMIT 10) ORDER BY `open` DESC"
stock_query = BlazeSql(data_dir, file_name)
stock_query.run(query)
