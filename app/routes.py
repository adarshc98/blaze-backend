from flask import Blueprint, request, jsonify, make_response
from .blaze import BlazeSql
from .utils import get_files_list

bp = Blueprint('main', __name__)

global blaze_db
DATA_DIR = "./app/csv/"

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
    file_name = 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
    try:
        blaze_db = BlazeSql(DATA_DIR, file_name)
        return make_response(jsonify(blaze_db.get_metadata()), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 200)

@bp.route('/run-query', methods=['POST'])
def run_query():
    global blaze_db
    print('entered RunQuery')
    query = request.json.get('query', None)
    try:
        response = blaze_db.run(query)
        return make_response(jsonify(response), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 200)

@bp.route('/get-companies', methods=['GET'])
def get_companies():
    print('entered GetCompanies')
    files = get_files_list(DATA_DIR)
    return make_response(jsonify({"files": files}), 200)
