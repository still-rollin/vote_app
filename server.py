from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidates.db'
db = SQLAlchemy(app)
selected_position=''



class Candidate(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    position=db.Column(db.String(100),nullable=False)
    graduation_year=db.Column(db.String(100),nullable=False)
    manifesto=db.Column(db.String(100),nullable=False)
    def __repr__(self):
        return '<Candidate %r>' % self.name
with app.app_context():
    db.create_all()
    
    
def get_positions():
    positions = db.session.query(Candidate.position).distinct().all()
    values =[name[0] for name in positions]
    print(values)
    return values
def get_candidates(position):
    candidates= db.session.query(Candidate.name).filter(Candidate.position == position).distinct().all()
    values =[name[0] for name in candidates]
    print(values)
    return values
def get_candidate_row(position):
    candidates= db.session.query(Candidate).filter(Candidate.position == position).distinct().all()
    return candidates
   
def create_candidate(name,votes,position,graduation_year,manifesto):
    existing_candidate = Candidate.query.filter_by(name=name, position=position).first()

    if existing_candidate:
        return "Candidate already exists!"
    new_candidate = Candidate(name=name,votes=votes,position=position,graduation_year=graduation_year,manifesto=manifesto)
    db.session.add(new_candidate)
    db.session.commit()

def search_candidate(name,position):
    candidates = Candidate.query.filter(and_(Candidate.name.ilike(f"%{name}%"), Candidate.position.ilike(f"%{position}%"))).all()
    return candidates[0]
votes={}
bitsidlist=[]
def read_candidates():
    all_candidates=[] 
    candidates = Candidate.query.all()
    for candidate in candidates:
        print (candidate.name)
    return candidates

    

@app.route("/") 
def random():
    status_message="Welcome"
    return render_template('vote.html',status_message=status_message,positions=get_positions(),candidates=get_candidates(''))

@app.route("/add_candidates")
def add():
    position = request.args.get('positions') 
    candidate_name=request.args.get('candidate_name')
    prospectus=request.args.get('prospectus')
    graduation_year=request.args.get('graduation_year')
    print(position,candidate_name,prospectus,graduation_year)
    
    if position is None or candidate_name is None or prospectus is None or graduation_year is None:
        return render_template('add_position.html',all_candidates=read_candidates() )
    if len(position)==0 or len(candidate_name)==0  or len(prospectus)==0 or len(graduation_year)==0:
        return render_template('add_position.html',all_candidates=read_candidates())
    details=(position,candidate_name,prospectus,graduation_year)
    print(details)
    add_position(position,votes)
    add_member(position,candidate_name,votes)
    create_candidate(candidate_name,0,position,graduation_year,prospectus)
    return render_template('add_position.html', all_candidates=read_candidates())

def add_position(position, votes):
    if(position not in votes ):
        votes[position]={}
        
def add_member(position, candidate,votes):
    if(position  in votes and candidate not in votes[position] ):
        votes[position][candidate] =0

@app.route("/voting")
def vote():
    candidate_name=request.args.get('candidates')
    bitsid=request.args.get('bitsid')
    if(bitsid in bitsidlist   ):
        status_message="Already voted"
        return render_template('vote.html',status_message=status_message,positions=get_positions(),candidates=get_candidates(''))
    #if(position is None or candidate_name is None   ):
        #status_message=""
        #eturn render_template('vote.html',status_message=status_message,positions=get_positions(),candidates=get_candidates(''))
    #if(position not in votes or candidate_name not in votes[position] ):
        #status_message="Couldn't find candidate "+ candidate_name
        #return render_template('vote.html',votes=votes,status_message=status_message,positions=get_positions(),candidates=get_candidates())
    print("PRINT HERE")
    candidate_to_vote=search_candidate(candidate_name,selected_position)
    candidate_to_vote.votes=candidate_to_vote.votes + 1
    bitsidlist.append(bitsid)
    #print('HELLO')
    #print(votes)
    status_message="Voted Successfully for  "+ candidate_name
    db.session.commit()
    return render_template('vote.html',status_message=status_message,positions=get_positions(),candidates=get_candidates(''))

@app.route("/selectposition")
def selectposition():
    position=request.args.get('positions')
    print("SELECTED POSITIONS ")
    print(position)
    global selected_position
    selected_position=position
    status_message=''
    return render_template('vote.html',status_message=status_message,positions=get_positions(),candidates=get_candidates(position))
 
@app.route("/selectpositionforresult")
def selectpositionforresults(): 
    position=request.args.get('positions')
    global selected_position
    selected_position=position
    print("here")
    print(get_candidates(position))
    print(get_candidate_row(position))
    return render_template('results.html',positions=get_positions(),candidates=get_candidate_row(position))

@app.route("/results")
def results():
    return render_template('results.html',positions=get_positions(),candidates=get_candidates(''))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/name/<username>')
def greet_user(username):
    return render_template('hiname.html',username=username)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('home.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('home.html'), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
  
   