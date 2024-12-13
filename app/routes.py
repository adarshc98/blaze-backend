from flask import Blueprint, request, jsonify, make_response
from .blaze import BlazeSql
from .utils import get_files_list

import cudf
import queue
import threading



bp = Blueprint('main', __name__)

global blaze_db
DATA_DIR = "./app/csv/"

# Create a queue to hold the result
global result_queue
result_queue = queue.Queue()

def init_db_in_thread(file_name):
    global blaze_db
    try:
        blaze_db = BlazeSql(DATA_DIR, file_name)
    except Exception as e:
        print('ERROR init_db_in_thread>',e)

def run_query_in_thread(query):
    global blaze_db
    global result_queue
    try:
        result = blaze_db.run(query)
        result_queue.put(result)
    except Exception as e:
        print('ERROR run_query_in_thread>',e)
        result_queue.put(e)

@bp.route('/')
def root():
    print('entered /')
    return "hello"

@bp.route('/blaze', methods=['GET'])
def blaze():
    return "Blaze endpoint is working!"

@bp.route('/init-db', methods=['POST'])
def init_db():
    global blaze_db
    print('entered InitDb')
    file_name_from_payload = request.json.get('source', None)
    file_name = file_name_from_payload or 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
    # file_name = 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
    try:
        t = threading.Thread(target=init_db_in_thread, args=(file_name,))
        t.start()
        t.join()
        return make_response(jsonify(blaze_db.get_metadata()), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 200)

@bp.route('/run-query', methods=['POST'])
def run_query():
    global blaze_db
    print('entered RunQuery')
    query = request.json.get('query', None)
    try:
        t = threading.Thread(target=run_query_in_thread, args=(query,))
        t.start()
        t.join()
        result = result_queue.get()
        response_to_send = {"query_time": result["query_time"], "result":result["result"].to_pandas().to_dict()}
        return make_response(jsonify(response_to_send), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 200)

@bp.route('/get-companies', methods=['GET'])
def get_companies():
    print('entered GetCompanies')
    files = get_files_list(DATA_DIR)
    return make_response(jsonify({"files": files}), 200)

@bp.route("/testblaze")
def test_blazing():
    from blazingsql import BlazingContext
    bc = BlazingContext()
    cudf_df = cudf.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    bc.create_table("test_table", cudf_df)
    result = bc.sql("SELECT * FROM test_table WHERE a = 2")
    return result.to_pandas().to_json()