#import flask module
from flask import Flask,render_template, request
from flask_mail import Mail, Message 
votes={}
positionslist=[]
candidateslist=[]
prospectuslist=[]
graduation_yearlist=[]
all_candidates=[]

 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text when root url is accessed
@app.route("/") 
def random():
    return render_template('vote.html') 
@app.route("/add_candidates")
def add():
    position = request.args.get('positions') 
    positionslist.append(position)

    candidate_name=request.args.get('candidate_name')
    candidateslist.append(candidate_name)
    prospectus=request.args.get('prospectus')
    prospectuslist.append(prospectus)
    graduation_year=request.args.get('graduationyear')
    graduation_yearlist.append(graduation_year)
  
    details=(position,candidate_name,prospectus,graduation_year)
   
    
    all_candidates.append(details)
    print(all_candidates)
    return render_template('add_position.html', all_candidates=all_candidates)

def add_position(position):
    votes[position]={}
def add_member(position, candidate):
    votes[position][candidate] = {}
    
    
@app.route("/voting")
def vote():
    position = request.args.get('positions') 
    candidate= request.args.get('candidates')
    print(position)
    print(candidate)
    votes[position][candidate] = votes[position][candidate] + 1
    return render_template('vote.html')


    


    
    
    
    
    
    
    
    
 
if __name__ == '__main__':  
   app.run()
   