from flask import Flask
from flask import render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash

# Import Signup Form
from forms import SignupForm


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psotgres@localhost/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
db = SQLAlchemy(app)


app.secret_key = "my-secret-key"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(54))

    def __init__(self,username,email,password):
        self.username = username.lower()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.pwdhash,password)


@app.route('/')
def index():
    return render_template('index.html',name=index)


@app.route('/user/<int:user_id>/')
def user(user_id):
    return 'User Id : {}'.format(user_id)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',name='dashboard')


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method=='POST':
        if form.validate() == False:
            return render_template('signup.html', name=signup, form=form)
        else:
            newuser = User(form.username.data,form.email.data,form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email']= newuser.email
            return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html',name=signup,form=form)


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)