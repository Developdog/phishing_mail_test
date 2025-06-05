from waitress import serve
import phishing_flask

if __name__=='__main__':
    serve(phishing_flask.app, host ='0.0.0.0', port='5000')