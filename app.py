from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Anhyeuem123@localhost/typing'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/score', methods=['POST'])
def create():
  x = request.get_json()

  score = Score(wpm = x['wpm'], excerpt_id=x['excerpt_id'])

  db.session.add(score)
  db.session.commit()

  # count total score
  total_scores = Score.query.filter_by(excerpt_id=x['excerpt_id']).count()

  # find all the score of excerpts_id
  scores = Score.query.with_entities(Score.wpm).filter_by(excerpt_id=x['excerpt_id']).order_by(Score.wpm.desc()).all()
  
  # make wpm list
  ranking_list = []

  for score in scores:
    ranking_list.append(score.wpm)

  # find the rank through wpm list
  ranking = ranking_list.index(x['wpm']) + 1

  return jsonify({
    "success": True,
    "ranking": ranking,
    "total_scores": total_scores,
  }), 201


@app.route('/excerpts/random', methods=['GET'])
def random_excerpt():

    # get random excerpt
    excerpt = Excerpt.query.order_by(db.func.random()).first()

    # total scores
    scores_count = Score.query.filter_by(excerpt_id=excerpt.id).count()

    # all the scores
    scores = Score.query.filter_by(excerpt_id=excerpt.id).order_by(Score.wpm.desc()).all()
    
    # only 3 top scores
    top_scores = []

    for x in range(3 if len(scores) > 3 else len(scores)):
      top_scores.append({
        'id': scores[x].id,
        'value': scores[x].wpm
      })
    
    return jsonify({
      'excerpt': {
        'id': excerpt.id,
        'text': excerpt.text,
        'scores': {
          'top_scores': top_scores,
          'scores_count': scores_count
        }
      }
    })

                
class Score(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  wpm = db.Column(db.Integer, nullable=False)
  excerpt_id = db.Column(db.Integer, db.ForeignKey('excerpt.id'), nullable=False)

class Excerpt(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(200), unique=True, nullable=False)
  scores = db.relationship('Score', backref='excerpt', lazy='dynamic')