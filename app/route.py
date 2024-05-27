from flask import Blueprint, render_template, request, session, redirect, url_for
from app.forms import QuestionsForm
from app.models import Questions
from datetime import datetime
import time
bp = Blueprint("route",__name__ )
# Define total allowed time in seconds, e.g., 600 seconds for 10 minutes
TOTAL_ALLOWED_TIME = 20
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/question/<int:id>", methods=["POST", "GET"])
def question(id):
    if 'score' not in session:
        session['score'] = 0
    if 'start_time' not in session:
        session['start_time'] = time.time()
    
    form = QuestionsForm()
    questions = Questions.query.filter_by(q_id=id).first()

    if not questions:
        return redirect(url_for('route.score'))

    form.options.choices = [
        (questions.a, questions.a),
        (questions.b, questions.b),
        (questions.c, questions.c),
        (questions.d, questions.d)
    ]

    if form.validate_on_submit():
        option = form.options.data
        if option == questions.ans:
            session['score'] += 10
        return redirect(url_for('route.question', id= (id + 1)))

    # Calculate remaining time
    elapsed_time = time.time() - session['start_time']
    remaining_time = TOTAL_ALLOWED_TIME - elapsed_time
    if remaining_time <= 0:
        return redirect(url_for('score'))

    return render_template("questions.html", form=form, questions=questions, remaining_time=remaining_time, total_allowed_time=TOTAL_ALLOWED_TIME)

@bp.route("/score")
def score():
    final_score = session.get('score', 0)
    session.pop('score', None)
    session.pop('start_time', None)
    return render_template("score.html", score=final_score)