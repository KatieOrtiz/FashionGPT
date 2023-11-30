from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontPage.html')
@app.route('/emailVerification')
def emailVerification():
    return render_template('emailVerification.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)