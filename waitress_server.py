from waitress import serve
from flask_main import app

if __name__=='__main__':
    serve(app, host ='0.0.0.0', port='5000')