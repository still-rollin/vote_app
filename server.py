#import flask module
from flask import Flask,render_template, request
from flask_mail import Mail, Message 

 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/vote") 
def random():
    return render_template('vote.html') 
@app.route("/addvote")
def addvote():
    candidate=request.args.get('candidates')
    
    
    
 
if __name__ == '__main__':  
   app.run()