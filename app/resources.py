import pydash
import json
import time
from flask_restx import Resource, Namespace
from app.blaze import BlazeSql
from flask import jsonify, make_response
from .extensions import response_model_for_prediction, request_model_for_prediction, request_model_for_prophet_prediction, prophet_forecast_model, request_model_for_news, response_model_for_news
from .ai_prediction.annual_report_copilot import annual_report_copilot
from .ai_prediction.stock_market_prediction import get_news_data, get_stock_market_prediction_prophet, get_stock_market_prediction_prophet_plus_news_sentiments
from utils import get_files_list

ns = Namespace("api")
global blaze_db
DATA_DIR = "input_csv"

@ns.route('/query')
class Query(Resource):
    @ns.doc(description='API to get response from ai model for prediction')
    @ns.marshal_with(response_model_for_prediction, code=200)
    @ns.expect(request_model_for_prediction)
    def post(self):
        print('entered query')
        query = ns.payload['query']
        symbol = ns.payload['symbol']
        model_type = pydash.get(ns.payload, 'model_type') or "azure_openai"
        response = annual_report_copilot(query, model_type, symbol)
        print(response)
        return {
                    "query": query,
                    "answer": response
            }

# get_stock_market_prediction_prophet
@ns.route('/get_stock_market_prediction_prophet')
class Get_Stock_Market_Prediction_Prophet(Resource):
    @ns.doc(description='API to get prophet response from ai model for prediction')
    @ns.marshal_with(prophet_forecast_model, code=200)
    @ns.expect(request_model_for_prophet_prediction)
    def post(self):
        print('entered Get_Stock_Market_Prediction_Prophet')
        symbol = ns.payload['symbol']
        periods = ns.payload['periods']
        frequency_type = ns.payload['frequency_type']
        frequency = ns.payload['frequency']
        # symbol = "IBM", periods = 20, Frequency_type = "Day", Frequency = 1
        json_response_string = get_stock_market_prediction_prophet(symbol, periods, frequency_type, frequency)
        json_response = json.loads(json_response_string)
        print(type(json_response), json_response)
        # response_answer = get(response, 'choices[0].text')
        return json_response

@ns.route('/get_stock_market_prediction_prophet_plus_sentiment')
class Get_Stock_Market_Prediction_Prophet_Plus_Sentiment(Resource):
    @ns.doc(description='API to get prophet response from ai model for prediction')
    @ns.marshal_with(prophet_forecast_model, code=200)
    @ns.expect(request_model_for_prophet_prediction)
    def post(self):
        print('entered Get_Stock_Market_Prediction_Prophet_Plus_Sentiment')
        symbol = ns.payload['symbol']
        periods = ns.payload['periods']
        frequency_type = ns.payload['frequency_type']
        frequency = ns.payload['frequency']
        model_type = pydash.get(ns.payload, 'model_type') or "azure_openai"
        json_response_string = get_stock_market_prediction_prophet_plus_news_sentiments(model_type, symbol, periods, frequency_type, frequency)
        json_response = json.loads(json_response_string)
        print(type(json_response), json_response)
        return json_response

@ns.route('/get_news')
class Get_News(Resource):
    @ns.doc(description='API to get news')
    @ns.expect(request_model_for_news)
    @ns.marshal_with(response_model_for_news, code=200)
    def post(self):
        print('entered Get_News')
        symbol = ns.payload['symbol']
        json_response_string = get_news_data(symbol)
        json_response = json.loads(json_response_string)
        print(type(json_response), json_response)
        return json_response

@ns.route('/init-db')
class InitDb(Resource):
    # @ns.doc(description='API to get news')
    # @ns.expect(request_model_for_news)
    # @ns.marshal_with(response_model_for_news, code=200)
    def post(self):
        print('entered InitDb')
        file_name_from_payload = ns.payload['source']
        file_name = file_name_from_payload or 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
        try:
            blaze_db = BlazeSql(DATA_DIR, file_name)
            return make_response(jsonify(blaze_db.get_metadata()), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 200)

@ns.route('/run-query')
class RunQuery(Resource):
    # @ns.doc(description='API to get news')
    # @ns.expect(request_model_for_news)
    # @ns.marshal_with(response_model_for_news, code=200)
    def post(self):
        print('entered RunQuery')
        file_name_from_payload = ns.payload['query']
        file_name = file_name_from_payload or 'TIME_SERIES_INTRADAY_symbol-AMZN_interval-15min_adjusted-true_extended_hours-true_outputsize-full_datatype-csv.csv'
        try:
            blaze_db = BlazeSql(DATA_DIR, file_name)
            return make_response(jsonify(blaze_db.get_metadata()), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 200)

@ns.route('/get-companies')
class GetCompanies(Resource):
    # @ns.doc(description='API to get news')
    # @ns.expect(request_model_for_news)
    # @ns.marshal_with(response_model_for_news, code=200)
    def get(self):
        print('entered GetCompanies')
        file_name_from_payload = ns.payload['query']
        files = get_files_list('./ai_prediction/output_data/result/csv')
        return make_response(jsonify({"files": files}), 200)

