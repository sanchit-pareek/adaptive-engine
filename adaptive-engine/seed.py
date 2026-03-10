from db import questions_col

questions = [
    # Vocabulary (8 questions, varying difficulty)
    {
        "question_id": "q001",
        "text": "What is the meaning of 'ephemeral'?",
        "options": ["A. Lasting forever", "B. Short-lived", "C. Ancient", "D. Brilliantly lit"],
        "correct": "B",
        "topic": "vocabulary",
        "irt_b": -0.5,
        "irt_a": 1.0
    },
    {
        "question_id": "q002",
        "text": "Which word is closest in meaning to 'laconic'?",
        "options": ["A. Verbose", "B. Melancholic", "C. Brief", "D. Energetic"],
        "correct": "C",
        "topic": "vocabulary",
        "irt_b": 0.0,
        "irt_a": 1.2
    },
    {
        "question_id": "q003",
        "text": "The word 'obsequious' most nearly means:",
        "options": ["A. Stubborn", "B. Fawning", "C. Forgetful", "D. Loud"],
        "correct": "B",
        "topic": "vocabulary",
        "irt_b": 0.8,
        "irt_a": 1.3
    },
    {
        "question_id": "q004",
        "text": "Which word means 'to make worse'?",
        "options": ["A. Ameliorate", "B. Exacerbate", "C. Mitigate", "D. Placate"],
        "correct": "B",
        "topic": "vocabulary",
        "irt_b": 0.5,
        "irt_a": 1.1
    },
    {
        "question_id": "q005",
        "text": "The word 'garrulous' most nearly means:",
        "options": ["A. Silent", "B. Angry", "C. Talkative", "D. Fearful"],
        "correct": "C",
        "topic": "vocabulary",
        "irt_b": -0.2,
        "irt_a": 1.0
    },
    {
        "question_id": "q006",
        "text": "Which word is closest in meaning to 'recondite'?",
        "options": ["A. Common", "B. Obscure", "C. Bright", "D. Gentle"],
        "correct": "B",
        "topic": "vocabulary",
        "irt_b": 1.2,
        "irt_a": 1.4
    },
    {
        "question_id": "q007",
        "text": "The word 'sanguine' most nearly means:",
        "options": ["A. Pessimistic", "B. Bloody", "C. Optimistic", "D. Tired"],
        "correct": "C",
        "topic": "vocabulary",
        "irt_b": 0.6,
        "irt_a": 1.2
    },
    {
        "question_id": "q008",
        "text": "Which word means 'a strong dislike or aversion'?",
        "options": ["A. Predilection", "B. Antipathy", "C. Equanimity", "D. Probity"],
        "correct": "B",
        "topic": "vocabulary",
        "irt_b": 1.0,
        "irt_a": 1.3
    },

    # Quantitative Reasoning (7 questions, varying difficulty)
    {
        "question_id": "q009",
        "text": "If 3x + 7 = 22, what is the value of x?",
        "options": ["A. 3", "B. 4", "C. 5", "D. 6"],
        "correct": "C",
        "topic": "quantitative",
        "irt_b": -1.0,
        "irt_a": 0.9
    },
    {
        "question_id": "q010",
        "text": "What is 15% of 240?",
        "options": ["A. 24", "B. 36", "C. 48", "D. 32"],
        "correct": "B",
        "topic": "quantitative",
        "irt_b": -0.8,
        "irt_a": 1.0
    },
    {
        "question_id": "q011",
        "text": "A rectangle has length 12 and width 7. What is its area?",
        "options": ["A. 19", "B. 38", "C. 84", "D. 96"],
        "correct": "C",
        "topic": "quantitative",
        "irt_b": -0.6,
        "irt_a": 1.0
    },
    {
        "question_id": "q012",
        "text": "If the ratio of boys to girls in a class is 3:5 and there are 40 students total, how many are boys?",
        "options": ["A. 12", "B. 15", "C. 18", "D. 24"],
        "correct": "B",
        "topic": "quantitative",
        "irt_b": 0.3,
        "irt_a": 1.2
    },
    {
        "question_id": "q013",
        "text": "A car travels 180 miles in 3 hours. At the same speed, how far will it travel in 5 hours?",
        "options": ["A. 240", "B. 270", "C. 300", "D. 360"],
        "correct": "C",
        "topic": "quantitative",
        "irt_b": 0.0,
        "irt_a": 1.1
    },
    {
        "question_id": "q014",
        "text": "If x² - 5x + 6 = 0, what are the values of x?",
        "options": ["A. 1 and 6", "B. 2 and 3", "C. -2 and -3", "D. -1 and 6"],
        "correct": "B",
        "topic": "quantitative",
        "irt_b": 0.7,
        "irt_a": 1.3
    },
    {
        "question_id": "q015",
        "text": "A cylindrical tank has radius 3 and height 10. What is its volume? (Use π ≈ 3.14)",
        "options": ["A. 188.4", "B. 282.6", "C. 314.0", "D. 94.2"],
        "correct": "B",
        "topic": "quantitative",
        "irt_b": 1.0,
        "irt_a": 1.4
    },

    # Reading Comprehension / Analytical (5 questions)
    {
        "question_id": "q016",
        "text": "The author's primary purpose in a passage that describes both benefits and drawbacks of a policy is most likely to:",
        "options": ["A. Argue for the policy", "B. Argue against the policy", "C. Present a balanced analysis", "D. Entertain the reader"],
        "correct": "C",
        "topic": "analytical",
        "irt_b": 0.2,
        "irt_a": 1.0
    },
    {
        "question_id": "q017",
        "text": "Which of the following, if true, would most weaken the argument that 'exercise always improves mental health'?",
        "options": [
            "A. Many people enjoy exercising outdoors",
            "B. Some individuals experience increased anxiety after intense exercise",
            "C. Exercise reduces the risk of heart disease",
            "D. Most doctors recommend regular physical activity"
        ],
        "correct": "B",
        "topic": "analytical",
        "irt_b": 0.5,
        "irt_a": 1.2
    },
    {
        "question_id": "q018",
        "text": "An argument that concludes X because X has always been done is an example of which fallacy?",
        "options": ["A. Ad hominem", "B. Straw man", "C. Appeal to tradition", "D. False dichotomy"],
        "correct": "C",
        "topic": "analytical",
        "irt_b": 0.9,
        "irt_a": 1.3
    },
    {
        "question_id": "q019",
        "text": "If all mammals are warm-blooded, and all whales are mammals, which conclusion is valid?",
        "options": [
            "A. All warm-blooded animals are whales",
            "B. All whales are warm-blooded",
            "C. Some mammals are not warm-blooded",
            "D. Whales are not mammals"
        ],
        "correct": "B",
        "topic": "analytical",
        "irt_b": -0.3,
        "irt_a": 1.0
    },
    {
        "question_id": "q020",
        "text": "A study finds a correlation between ice cream sales and drowning rates. The most reasonable explanation is:",
        "options": [
            "A. Ice cream causes drowning",
            "B. Drowning causes people to buy ice cream",
            "C. A third variable (hot weather) causes both",
            "D. The data is fabricated"
        ],
        "correct": "C",
        "topic": "analytical",
        "irt_b": 0.4,
        "irt_a": 1.1
    }
]

def seed():
    questions_col.drop()
    questions_col.insert_many(questions)
    print(f"Seeded {len(questions)} questions successfully.")

if __name__ == "__main__":
    seed()