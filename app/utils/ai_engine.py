def predict_grade(avg, attendance):

    score = (avg * 0.7) + (attendance * 0.3)

    if score >= 75:
        return "🟢 Distinction", score

    elif score >= 50:
        return "🟡 Pass", score

    else:
        return "🔴 Fail", score
