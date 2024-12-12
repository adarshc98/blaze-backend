from flask_restx import Api
from flask_restx import fields

api = Api()

api = Api(version='1.0', title='Prediction API',
          description='stock market prediciton api')

ns = api.namespace('api', description='API endpoints for prediction')


response_model_for_prediction = api.model('response', {
    'query': fields.String(description='query from client'),
    'answer': fields.String(description='answer from ai model')
})

# olama request
request_model_for_prediction = api.model('request', {
    'query': fields.String(description='query from client'),
})


# prophet prediction
request_model_for_prophet_prediction = api.model('request_prophet', {
    'symbol': fields.String(description='stock market company symbol(eg: IBM)'),
    'periods': fields.Integer(description='period number'),
    'frequency_type': fields.String(description='frequency(eg: Day)'),
    'frequency': fields.Integer(description='frequency interval'),
})

dynamic_model = api.model('DynamicValues', {
    'data': fields.Raw(description='Dynamic key-value pairs with float values')
})

prophet_forecast_model = api.model('response_prophet', {
    'ds': fields.Raw(description='Timestamps as dynamic key-value pairs'),
    'yhat': fields.Raw(description='Predicted values as dynamic key-value pairs'),
    'yhat_lower': fields.Raw(description='Lower bounds of predictions as dynamic key-value pairs'),
    'yhat_upper': fields.Raw(description='Upper bounds of predictions as dynamic key-value pairs'),
})



# news
request_model_for_news = api.model('request_for_news', {
    'symbol': fields.String(description='stock market company symbol(eg: IBM)'),
})

response_model_for_news = api.model('response_for_news', {
    'time_published': fields.Raw(description='Timestamps as dynamic key-value pairs'),
    'title': fields.Raw(description='Title values as dynamic key-value pairs'),
    'summary': fields.Raw(description='Summary as dynamic key-value pairs'),
    'news_category': fields.Raw(description='News category as dynamic key-value pairs'),
    'topics': fields.Raw(description='Topics as dynamic key-value pairs'),
    'relevance_score': fields.Raw(description='Relevance score as dynamic key-value pairs'),
    'sentiment_score': fields.Raw(description='Sentiment score as dynamic key-value pairs'),
    'sentiment_label': fields.Raw(description='Sentiment label as dynamic key-value pairs'),
})