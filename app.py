from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontPage.html')
@app.route('/emailVerification')
def emailVerification():
    return render_template('emailVerification.html')
@app.route('/homePage')
def emailVerification():
    return render_template('homePage.html')
@app.route('/PasswordPage')
def emailVerification():
    return render_template('PasswordPage.html')
@app.route('/personalDetails')
def emailVerification():
    return render_template('personalDetails.html')
@app.route('/register')
def emailVerification():
    return render_template('register.html')
@app.route('/sizePreference')
def emailVerification():
    return render_template('sizePreference.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)