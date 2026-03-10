from flask import Flask, request, jsonify
from db import questions_col, sessions_col
from irt import select_next_question, update_theta, evaluate_answer
import uuid
from datetime import datetime
from study_plan import generate_study_plan

app = Flask(__name__)

MAX_QUESTIONS = 10  # number of questions per session


@app.route("/session/start", methods=["POST"])
def start_session():
    """Start a new diagnostic session."""
    data = request.json or {}
    user_id = data.get("user_id", "anonymous")

    session_id = str(uuid.uuid4())
    theta = 0.0  # start at average ability

    first_question = select_next_question(theta, [])
    if not first_question:
        return jsonify({"error": "No questions available"}), 500

    session = {
        "session_id": session_id,
        "user_id": user_id,
        "responses": [],
        "current_theta": theta,
        "question_history": [first_question["question_id"]],
        "completed": False,
        "study_plan": None,
        "created_at": datetime.utcnow()
    }
    sessions_col.insert_one(session)

    return jsonify({
        "session_id": session_id,
        "question": {
            "question_id": first_question["question_id"],
            "text": first_question["text"],
            "options": first_question["options"],
            "topic": first_question["topic"]
        },
        "question_number": 1,
        "total_questions": MAX_QUESTIONS
    })


@app.route("/session/answer", methods=["POST"])
def submit_answer():
    """Submit an answer and get the next question."""
    data = request.json or {}
    session_id = data.get("session_id")
    question_id = data.get("question_id")
    user_answer = data.get("answer")

    if not all([session_id, question_id, user_answer]):
        return jsonify({"error": "session_id, question_id, and answer are required"}), 400

    session = sessions_col.find_one({"session_id": session_id})
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if session["completed"]:
        return jsonify({"error": "Session already completed"}), 400

    question = questions_col.find_one({"question_id": question_id}, {"_id": 0})
    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = evaluate_answer(question, user_answer)

    response_entry = {
        "question_id": question_id,
        "answer": user_answer,
        "correct": is_correct,
        "irt_a": question["irt_a"],
        "irt_b": question["irt_b"],
        "timestamp": datetime.utcnow()
    }

    updated_responses = session["responses"] + [response_entry]
    new_theta = update_theta(session["current_theta"], updated_responses)

    question_number = len(updated_responses)

    # Check if session is complete
    if question_number >= MAX_QUESTIONS:
        sessions_col.update_one(
            {"session_id": session_id},
            {"$set": {
                "responses": updated_responses,
                "current_theta": new_theta,
                "completed": True
            }}
        )
        return jsonify({
            "correct": is_correct,
            "correct_answer": question["correct"],
            "theta": new_theta,
            "completed": True,
            "message": "Session complete. Call /session/result for your study plan."
        })

    # Select next question
    asked_ids = session["question_history"] + [question_id]
    next_question = select_next_question(new_theta, asked_ids)

    if not next_question:
        sessions_col.update_one(
            {"session_id": session_id},
            {"$set": {
                "responses": updated_responses,
                "current_theta": new_theta,
                "completed": True
            }}
        )
        return jsonify({
            "correct": is_correct,
            "correct_answer": question["correct"],
            "theta": new_theta,
            "completed": True,
            "message": "No more questions available. Call /session/result for your study plan."
        })

    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {
            "responses": updated_responses,
            "current_theta": new_theta,
            "question_history": asked_ids + [next_question["question_id"]]
        }}
    )

    return jsonify({
        "correct": is_correct,
        "correct_answer": question["correct"],
        "theta": new_theta,
        "completed": False,
        "next_question": {
            "question_id": next_question["question_id"],
            "text": next_question["text"],
            "options": next_question["options"],
            "topic": next_question["topic"]
        },
        "question_number": question_number + 1,
        "total_questions": MAX_QUESTIONS
    })


@app.route("/session/result", methods=["GET"])
def get_result():
    """Get session summary and trigger study plan generation."""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    session = sessions_col.find_one({"session_id": session_id}, {"_id": 0})
    if not session:
        return jsonify({"error": "Session not found"}), 404

    responses = session["responses"]
    total = len(responses)
    correct = sum(1 for r in responses if r["correct"])

    topic_breakdown = {}
    for r in responses:
        q = questions_col.find_one({"question_id": r["question_id"]}, {"_id": 0})
        if q:
            topic = q["topic"]
            if topic not in topic_breakdown:
                topic_breakdown[topic] = {"correct": 0, "total": 0}
            topic_breakdown[topic]["total"] += 1
            if r["correct"]:
                topic_breakdown[topic]["correct"] += 1

    return jsonify({
        "session_id": session_id,
        "user_id": session["user_id"],
        "completed": session["completed"],
        "theta": session["current_theta"],
        "score": f"{correct}/{total}",
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "topic_breakdown": topic_breakdown,
        "study_plan": session.get("study_plan")
    })
@app.route("/session/plan", methods=["POST"])
def get_study_plan():
    """Generate a personalized study plan for a completed session."""
    data = request.json or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    session = sessions_col.find_one({"session_id": session_id}, {"_id": 0})
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if not session["completed"]:
        return jsonify({"error": "Session not completed yet"}), 400

    # Get topic breakdown
    responses = session["responses"]
    topic_breakdown = {}
    for r in responses:
        q = questions_col.find_one({"question_id": r["question_id"]}, {"_id": 0})
        if q:
            topic = q["topic"]
            if topic not in topic_breakdown:
                topic_breakdown[topic] = {"correct": 0, "total": 0}
            topic_breakdown[topic]["total"] += 1
            if r["correct"]:
                topic_breakdown[topic]["correct"] += 1

    plan = generate_study_plan(session["current_theta"], topic_breakdown, session["user_id"])

    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"study_plan": plan}}
    )

    return jsonify({"session_id": session_id, "study_plan": plan})

if __name__ == "__main__":
    app.run(debug=True)