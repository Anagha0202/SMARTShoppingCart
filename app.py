from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World trying out flask"

if __name__ == "__main__":
    #website_url = 'anaghascu.com'
    #app.config['SERVER_NAME'] = website_url
    app.run(host='127.0.0.1', port=8080, debug=True)
