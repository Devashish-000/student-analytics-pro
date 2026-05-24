def predict_result(avg_marks):

    if avg_marks >= 75:
        return "🟢 Distinction"
    elif avg_marks >= 50:
        return "🟡 Pass"
    else:
        return "🔴 Fail"
