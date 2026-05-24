import pandas as pd


# =========================
# AI DATA ANALYSIS ENGINE
# =========================
def analyze_data(df):

    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "numeric_columns": [],
            "missing_values": {}
        }

    report = {}

    # basic info
    report["rows"] = int(len(df))
    report["columns"] = int(len(df.columns))

    # numeric columns detection
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    report["numeric_columns"] = numeric_cols

    # missing values (clean format)
    report["missing_values"] = df.isnull().sum().to_dict()

    # extra AI insights (NEW UPGRADE)
    try:
        if "Average" in df.columns:
            report["avg_score"] = float(df["Average"].mean())

            report["top_student"] = {
                "name": df.loc[df["Average"].idxmax(), "name"]
                if "name" in df.columns else "Unknown",
                "score": float(df["Average"].max())
            }

            report["weak_students"] = int((df["Average"] < 60).sum())
        else:
            report["avg_score"] = 0
            report["top_student"] = {"name": "N/A", "score": 0}
            report["weak_students"] = 0

    except Exception as e:
        report["error"] = str(e)

    return report


# =========================
# AI GRADE PREDICTION ENGINE
# =========================
def predict_grade(avg, attendance):

    # safe conversion
    try:
        avg = float(avg)
    except:
        avg = 0.0

    try:
        attendance = float(attendance)
    except:
        attendance = 0.0

    # AI scoring model (weighted system)
    score = (avg * 0.7) + (attendance * 0.3)

    # grade mapping
    if score >= 80:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 40:
        grade = "C"
    else:
        grade = "D"

    return grade, round(score, 2)
