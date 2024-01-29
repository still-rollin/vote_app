#import flask module
from flask import Flask,render_template, request
from flask_mail import Mail, Message 
votes={}
 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text when root url is accessed
@app.route("/") 
def random():
    return render_template('vote.html') 
@app.route("/addposition")
def add_position(position):
    votes[position]={}
def add_member(postion, candidate):
    votes[position][candidate] = 0  
@app.route("/voting")
def vote(position, candidate):
    votes[position][candidate] = votes[position][candidate] + 1


    


    
    
    
    
    
    
    
    
 
if __name__ == '__main__':  
   app.run()
   