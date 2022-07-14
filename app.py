from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from models import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tvG^&5fv67F%^^&tv6p9V^&6g67GH^&(_^G&8'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db1 = Database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    mssg = None
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 == password2 and db1.isUnique(username):
            db1.create_user(username, password1, fullname)
            return redirect(url_for('login'))
        else:
            info = []
            if not db1.isUnique(username):
                info.append('Username is already in use!')
            if password1 != password2:
                info.append('Two passwords are not matching!')
            mssg = {
                'username': username,
                'fullname': fullname,
                'info': info
            }

    return render_template('signup.html', mssg=mssg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mssg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if db1.userExists(username, password):
            session['username'] = username
            session['fullname'] = db1.getFullName(username)
            return redirect(url_for('dashboard'))
        else:
            info = []
            info.append('Invalid Credentials! Please enter correct ones.')
            mssg = {
                'username': username,
                'info': info
            }
    return render_template('login.html', mssg=mssg)


@app.route('/dashboard')
def dashboard():
    context = {}
    regType = ''
    if not db1.registrationExists(session['username']):
        regType = 'new'
    else:
        if db1.isRegistrationPending(session['username']):
            regType = 'pending'
        else:
            if not db1.isRegSubmitted(session['username']):
                regType = 'finished'
            else:
                regType = 'submitted'
                context['registration_no'] = db1.getRegistrationNo(
                    session['username'])

    context['regType'] = regType
    return render_template('dashboard.html', context=context)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('fullname', None)
    return redirect(url_for('login'))


def myFormat(category, value):
    if value == None or len(value) == 0:
        return 'NULL'

    # else:
    if category == 'n':
        return value
    return f'\'{value}\''


@app.route('/newRegistration', methods=['GET', 'POST'])
def newRegistration():
    if request.method == 'POST':
        gender = myFormat('s', request.form.get('gender'))
        dob = myFormat('s', request.form.get('dob'))
        guardianname = myFormat('s', request.form.get('guardianname'))
        category = myFormat('s', request.form.get('category'))
        email = myFormat('s', request.form.get('email'))
        mobile = myFormat('s', request.form.get('mobile'))
        address = myFormat('s', request.form.get('address'))
        pin = myFormat('n', request.form.get('pin'))
        xth = myFormat('n', request.form.get('xth'))
        xiith = myFormat('n', request.form.get('xiith'))
        ugscheme = myFormat('s', request.form.get('ugscheme'))
        ugmarks = myFormat('n', request.form.get('ugmarks'))
        print(request.form)

        db1.create_registration(
            myFormat('s', session['username']), gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks)

        return redirect(url_for('dashboard'))

    return render_template('registration.html', values=None)


@app.route('/resumeRegistration', methods=['GET', 'POST'])
def resumeRegistration():
    if request.method == 'POST':
        gender = myFormat('s', request.form.get('gender'))
        dob = myFormat('s', request.form.get('dob'))
        guardianname = myFormat('s', request.form.get('guardianname'))
        category = myFormat('s', request.form.get('category'))
        email = myFormat('s', request.form.get('email'))
        mobile = myFormat('s', request.form.get('mobile'))
        address = myFormat('s', request.form.get('address'))
        pin = myFormat('n', request.form.get('pin'))
        xth = myFormat('n', request.form.get('xth'))
        xiith = myFormat('n', request.form.get('xiith'))
        ugscheme = myFormat('s', request.form.get('ugscheme'))
        ugmarks = myFormat('n', request.form.get('ugmarks'))
        print(request.form)

        db1.update_registration(
            myFormat('s', session['username']), gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks)

        return redirect(url_for('dashboard'))

    values = db1.getRegistrationProgress(session['username'])
    # print(values)
    return render_template('registration.html', values=values)


@app.route('/submitRegistration')
def submitRegistration():
    db1.submitRegistration(session['username'])
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
