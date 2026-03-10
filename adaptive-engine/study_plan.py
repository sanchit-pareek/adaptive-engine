from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_study_plan(theta, topic_breakdown, user_id):
    """
    Generate a personalized GRE study plan using OpenAI.
    Falls back to rule-based plan if OpenAI is unavailable.
    """
    try:
        return _openai_study_plan(theta, topic_breakdown)
    except Exception:
        return _fallback_study_plan(theta, topic_breakdown)


def _ability_label(theta):
    if theta < -1:
        return "beginner"
    elif theta < 0:
        return "below average"
    elif theta < 1:
        return "average"
    elif theta < 2:
        return "above average"
    else:
        return "advanced"


def _openai_study_plan(theta, topic_breakdown):
    topic_summary = []
    weak_topics = []

    for topic, stats in topic_breakdown.items():
        accuracy = round(stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        topic_summary.append(f"- {topic}: {stats['correct']}/{stats['total']} correct ({accuracy}%)")
        if accuracy < 60:
            weak_topics.append(topic)

    topic_text = "\n".join(topic_summary)
    ability_level = _ability_label(theta)

    prompt = f"""You are a GRE tutor. A student just completed a diagnostic test with the following results:

Ability level (theta): {theta} ({ability_level})

Topic performance:
{topic_text}

Weak areas: {', '.join(weak_topics) if weak_topics else 'None identified'}

Based on this, generate a concise 1-week personalized GRE study plan. Include:
1. Daily focus areas (which topics to study each day)
2. Specific recommendations for weak areas
3. Practice strategies suited to their ability level
4. 2-3 recommended resource types (e.g. flashcards, practice sets, timed drills)

Keep the plan practical and actionable. Format it clearly with day-by-day breakdown."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert GRE tutor who creates personalized study plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7
    )

    return response.choices[0].message.content


def _fallback_study_plan(theta, topic_breakdown):
    """Rule-based study plan generated from performance data."""
    ability_level = _ability_label(theta)

    weak_topics = []
    strong_topics = []
    for topic, stats in topic_breakdown.items():
        accuracy = round(stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        if accuracy < 60:
            weak_topics.append((topic, accuracy))
        else:
            strong_topics.append((topic, accuracy))

    weak_topics.sort(key=lambda x: x[1])  # weakest first

    plan = f"## Personalized GRE Study Plan\n"
    plan += f"**Ability Level:** {ability_level} (θ = {theta})\n\n"
    plan += "### Performance Summary\n"

    for topic, stats in topic_breakdown.items():
        accuracy = round(stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        status = "⚠️ Needs work" if accuracy < 60 else "✅ Strong"
        plan += f"- **{topic.capitalize()}**: {accuracy}% accuracy {status}\n"

    plan += "\n### 7-Day Study Plan\n\n"

    if not weak_topics:
        plan += (
            "**Day 1-2: Advanced Vocabulary**\n"
            "- Study high-frequency GRE words (Magoosh flashcards or Barron's 333)\n"
            "- Practice 20 sentence equivalence + text completion questions daily\n\n"
            "**Day 3-4: Quantitative Reasoning**\n"
            "- Focus on data interpretation and advanced algebra\n"
            "- Timed practice sets (35 min per section)\n\n"
            "**Day 5-6: Analytical Writing**\n"
            "- Write 2 full essays (Issue + Argument tasks)\n"
            "- Review ETS scoring rubric and sample essays\n\n"
            "**Day 7: Full Mock Test**\n"
            "- Take a full timed GRE practice test\n"
            "- Review all mistakes and note patterns\n\n"
            "**Recommended Resources:** ETS Official Guide, Magoosh GRE, Manhattan Prep 5lb Book\n"
        )
    else:
        days_used = 0
        for i, (topic, accuracy) in enumerate(weak_topics):
            day_start = days_used + 1
            day_end = days_used + 2
            plan += f"**Day {day_start}-{day_end}: Focus on {topic.capitalize()} (current accuracy: {accuracy}%)**\n"

            if topic == "vocabulary":
                plan += (
                    "- Study 30 new GRE words per day using spaced repetition flashcards\n"
                    "- Practice text completion and sentence equivalence questions\n"
                    "- Use Magoosh Vocabulary Builder app\n\n"
                )
            elif topic == "quantitative":
                plan += (
                    "- Review core math concepts: algebra, geometry, data analysis\n"
                    "- Do 20 practice problems per day, untimed first then timed\n"
                    "- Use Manhattan Prep 5lb Book (Quant sections)\n\n"
                )
            elif topic == "analytical":
                plan += (
                    "- Practice identifying argument structure and logical fallacies\n"
                    "- Do 10 critical reasoning questions daily\n"
                    "- Review ETS sample Argument essays\n\n"
                )
            days_used += 2
            if days_used >= 6:
                break

        if days_used < 5:
            plan += f"**Day {days_used + 1}: Mixed Practice**\n"
            plan += "- 20 mixed questions across all topics\n"
            plan += "- Focus on timing and accuracy\n\n"
            days_used += 1

        plan += f"**Day {days_used + 1}: Full Mock Test**\n"
        plan += "- Take a full timed GRE practice test\n"
        plan += "- Review all mistakes and note patterns\n\n"

        plan += "**Recommended Resources:** ETS Official Guide, Magoosh GRE, Manhattan Prep 5lb Book\n"

    plan += "\n---\n*Note: This plan was generated based on your diagnostic performance. For an AI-personalized plan, ensure a valid OpenAI API key is configured.*"

    return plan