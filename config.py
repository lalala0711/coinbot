import os

def load_environment_variables():
    apppass = os.environ.get('APP_PASSWORD')
    googleapikey = os.environ.get('GOOGLE_API_KEY')
    mongodbpass = os.environ.get('MONGODB_PASSWORD')
    coinapikey = os.environ.get('COINGECKO_API_KEY')
    return {
        'APP_PASSWORD': apppass,
        'GOOGLE_API_KEY': googleapikey,
        'MONGODB_PASSWORD': mongodbpass,
        'COINGECKO_API_KEY': coinapikey
    }