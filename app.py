from flask import Flask
from flask import render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash


# Import  Forms
from forms.forms import SignupForm,LoginForm,BlogForm


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
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(54))

    def __init__(self,username,name,email,password):
        self.username = username.lower()
        self.name = name.lower()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.pwdhash,password)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __init__(self,title,content):
        self.title = title
        self.content = content



@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html',name=index, blogs=blogs)


@app.route('/user/<int:user_id>/')
def user(user_id):
    return 'User Id : {}'.format(user_id)


@app.route('/dashboard')
def dashboard():
    blogs = Blog.query.all()
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html',name='dashboard',blogs=blogs)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if request.method=='POST':
        if form.validate() == False:
            return render_template('signup.html', name=signup, form=form)
        else:
            newuser = User(form.username.data,form.name.data,form.email.data,form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email']= newuser.email
            return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html',name=signup,form=form)



@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method=='POST':
        if form.validate() == False:
            return render_template('login.html', name=login, form=form)
        else:
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user is not None and user.check_password(password):
                session['username'] = form.username.data
                return redirect(url_for('dashboard'))
        # else:
        #     return render_template('login.html',name=login,form=form)

    elif request.method == 'GET':
        return render_template('login.html', name=login, form=form)


        return render_template('login.html',name=login,form=form)


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route('/create', methods=['GET','POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    form = BlogForm()
    if request.method=='POST':
        if form.validate() == False:
            return render_template('create.html', name=create, form=form)
        else:
            newblog = Blog(form.title.data,form.content.data)
            db.session.add(newblog)
            db.session.commit()
            flash("Blog Post Created Successfully")
            return redirect(url_for('dashboard'))
    else:
        return render_template('create.html',name=create,form=form)


@app.route('/editblog/<pk>', methods=['GET','POST'])
def editblog(pk):
    if 'username' not in session:
        return redirect(url_for('login'))
    form = BlogForm()
    blog = Blog.query.filter_by(id=pk).first_or_404()
    if request.method=='POST':
        if form.validate() == False:
            return render_template('editblog.html', name=editblog,blog=blog, form=form)
        else:
            edit = Blog(form.title.data,form.content.data)
            db.session.add(edit)
            db.session.commit()

            return redirect(url_for('index'))
    else:
        return render_template('editblog.html',name=editblog,blog=blog,form=form)


@app.route('/detail/<pk>')
def detail(pk):

        blog = Blog.query.filter_by(id=pk).first_or_404()
        return render_template('detail.html',name=detail,blog=blog)


@app.route('/delete/<pk>')
def delete(pk):
    blog = Blog.query.filter_by(id=pk).first()
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('dashboard'))


# @app.route('/detail/<pk>', methods=['GET','POST'])
# def detail(pk):
#     # if 'username' in session:
#     #     return redirect(url_for('dashboard'))
#     form = BlogForm()
#     if request.method=='POST':
#         if form.validate() == False:
#             return render_template('create.html', name=createblog, form=form)
#         else:
#             newblog = Blog(form.title.data,form.content.data)
#             db.session.add(newblog)
#             db.session.commit()
#
#             return redirect(url_for('dashboard'))
#     else:
#         blog = Blog.query.filter_by(id=pk).first_or_404()
#         return render_template('detail.html',name=detail,blog=blog,form=form)


if __name__ == '__main__':
    app.run(debug=True)