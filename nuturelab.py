from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, DetailsForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SECRET_KEY'] = '76ac3c1b34e08a2ac5851d7fa02bb689'

db = SQLAlchemy(app)


# @app.route("/")
# @app.route("/home")
# def home():
#     return "<h1>Home Page</h1>"

class Employees(db.Model):
    id = db.Column('employee_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    username = db.Column(db.String(100))
    Photo_url = db.Column(db.String(5000))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __init__(self, user_id, username, photo_url):
        self.user_id = user_id
        self.username = username
        self.photo_url = photo_url


@app.route("/")
@app.route("/admin")
def Admin():
    return render_template('admin.html', title='Admin')


@app.route('/add', methods=['GET', 'POST'])
def addEmployee():
    if request.method == 'POST':
        if not request.form['user_id'] or not request.form['username']:
            flash('Please enter all the fields', 'error')
        else:
            employee = Employees(request.form['user_id'], request.form['username'],
                                 request.form['photo_url'])

            db.session.add(employee)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('advisor_result'))
    return render_template('admin.html')


@app.route('/advisor', methods=['POST', 'GET'])
def advisor():
    if request.method == 'POST':
        result = request.form
        return render_template("advisor_result.html", result=result)


@app.route("/User")
def User():
    return render_template('user.html', title='User')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('User'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have been logged in!', 'success')
        return redirect(url_for('User'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/details")
# @app.route("/user/<user-id>/advisor")
def details():
    form = DetailsForm()
    if form.validate_on_submit():
        flash(f'200_OK if the request is successful')
        return redirect(url_for('advisor'))


@app.route("/user/<user_id>/advisor", methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        result = request.form
        return render_template("advisor_result.html", result=result)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
