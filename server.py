#import flask module
from flask import Flask,render_template, request
from flask_mail import Mail, Message 
votes={}
positionslist=[]
candidateslist=[]
prospectuslist=[]
graduation_yearlist=[]
all_candidates=[] 
random=[]
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text when root url is accessed
@app.route("/") 
def random():
    status_message="Welcome"
    return render_template('vote.html',votes=votes,status_message=status_message)
 
@app.route("/add_candidates")
def add():
    position = request.args.get('positions') 
    candidate_name=request.args.get('candidate_name')
    prospectus=request.args.get('prospectus')
    graduation_year=request.args.get('graduationyear')
    if position is None or candidate_name is None or prospectus is None or graduation_year is None:
        return render_template('add_position.html', all_candidates=all_candidates)
    if len(position)==0 or len(candidate_name)==0  or len(prospectus)==0 or len(graduation_year)==0:
        return render_template('add_position.html', all_candidates=all_candidates)
    positionslist.append(position)
    candidateslist.append(candidate_name)
    prospectuslist.append(prospectus)
    graduation_yearlist.append(graduation_year)
  
    details=(position,candidate_name,prospectus,graduation_year)
    add_position(position,votes)
    add_member(position,candidate_name,votes)
    print("yes1")
    print(votes)
    all_candidates.append(details)
    print(all_candidates)
    return render_template('add_position.html', all_candidates=all_candidates)

def add_position(position,votes):
    if(position not in votes):
        votes[position]={}
        
def add_member(position, candidate,votes):
    if(position  in votes and candidate not in votes[position]):
        votes[position][candidate] =0

@app.route("/voting")
def vote():
    position=request.args.get('positions')
    candidate_name=request.args.get('candidates')
    if(position is None or candidate_name is None ):
        status_message=""
        return render_template('vote.html',votes=votes,status_message=status_message)
    if(position not in votes or candidate_name not in votes[position] ):
        status_message="Couldn't find candidate "+ candidate_name
        return render_template('vote.html',votes=votes,status_message=status_message)
    print("PRINT HERE")
    votes[position][candidate_name] =votes[position][candidate_name]+ 1
    print('HELLO')
    print(votes)
    status_message="Voted Successfully for  "+ candidate_name
    return render_template('vote.html',votes=votes,status_message=status_message)
#tried dynamic dropdown but didn't work
@app.route("/selectposition")
def selectposition():
    position=request.args.get('positions')
    print("SELECTED POSITIONS ")
    print(position)
    status_message=''
    return render_template('vote.html',votes=votes,status_message=status_message)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/results")
def about1():
    return render_template('results.html',votes=votes)

if __name__ == '__main__':  
   app.run()
   