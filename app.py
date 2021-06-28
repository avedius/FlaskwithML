#import libraries
import pickle
import numpy as np
from flask import Flask, render_template,flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import pymysql
pymysql.install_as_MySQLdb()




#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model/model.pkl', 'rb'))

# old SQLite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
# new mysql db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1/app.db'

app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create a model
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(250), nullable=False)
    date_added = db.Column(db.DateTime, default= datetime.utcnow)

    #create a string
    def __repr__ (self):
        return '<subject %r>' % self.subject


#create a route decorator
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/home")
def index():
    return render_template("index.html")


@app.errorhandler(404)
# Invalid Url
def page_not_found(e):
    return render_template("404.html"), 404

# Internal servor Error
def page_not_found(e):
    return render_template("500.html"), 500



@app.route("/department")
def department():
    return render_template("department.html")


# localhost:5000/user/name
# @app.route('/user/<subject>')

# def user(subject):
#     return "<h1> Hello {} </h1>".format(subject)


# create a Form Class
class CommentForm(FlaskForm):
    subject = StringField("Enter a Subject ", validators=[DataRequired()])
    comment = StringField("What's your Suggestion ", validators=[DataRequired()])
    submit = SubmitField("Submit")


 #To use the predict button in our web-app
@app.route('/comments',methods=['GET','POST'])
def model():
    subject = None
    comment = None
    form = CommentForm()
    # validate form
    if form.validate_on_submit():
        subject = form.subject.data
        form.subject.data = ''
        comment = form.subject.data
        form.comment.data = ''
        flash("Comment Submitted Successfully ")
        subjects = (Comments.query.filter_by(subject = form.subject.data).first())
        if subjects is None:
            subjects = Comments(subject=form.subject.data, comment=form.comment.data)
            db.session.add(subjects)
            db.session.commit()
            subject = form.subject.data
            form.subject.data =''
            form.comment.data =''



    #For rendering results on HTML GUI
    # int_features = [float(x) for x in request.form.values()]
    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)
    # output = round(prediction[0], 2) 
    # return render_template('model.html', prediction_text='CO2    Emission of the vehicle is :{}'.format(output))
    return render_template("model.html", subject = subject, form = form)


# db.create_all()


if __name__ == "__main__":
    app.run(debug=True)