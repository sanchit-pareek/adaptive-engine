import math
from db import questions_col

def irt_probability(theta, a, b):
    """
    3PL IRT model simplified to 2PL.
    theta: current ability estimate
    a: discrimination parameter
    b: difficulty parameter
    Returns probability of correct response.
    """
    return 1 / (1 + math.exp(-a * (theta - b)))

def update_theta(theta, responses):
    """
    Simple MLE theta update using gradient ascent.
    responses: list of dicts with keys 'irt_a', 'irt_b', 'correct'
    """
    for _ in range(20): 
        gradient = 0
        for r in responses:
            a = r["irt_a"]
            b = r["irt_b"]
            p = irt_probability(theta, a, b)
            correct = 1 if r["correct"] else 0
            gradient += a * (correct - p)
        theta += 0.1 * gradient 
        theta = max(-4.0, min(4.0, theta))  
    return round(theta, 4)

def select_next_question(theta, asked_ids):
    """
    Select the question with difficulty closest to current theta
    that hasn't been asked yet.
    """
    all_questions = list(questions_col.find(
        {"question_id": {"$nin": asked_ids}},
        {"_id": 0}
    ))

    if not all_questions:
        return None

    best = min(all_questions, key=lambda q: abs(q["irt_b"] - theta))
    return best

def evaluate_answer(question, user_answer):
    """Returns True if the user's answer matches the correct answer."""
    return user_answer.strip().upper() == question["correct"].strip().upper()