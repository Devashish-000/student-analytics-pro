import pandas as pd

# =========================
# LOW ATTENDANCE
# =========================
def low_attendance_alert(df, threshold=75):
    if "attendance" not in df.columns:
        return pd.DataFrame()

    return df[df["attendance"] < threshold]


# =========================
# LOW PERFORMANCE (FIXED)
# =========================
def low_marks_alert(df, threshold=40):
    if "Average" not in df.columns:
        return pd.DataFrame()

    return df[df["Average"] < threshold]


# =========================
# MARKS DROP (SAFE)
# =========================
def marks_drop_alert(df):
    return pd.DataFrame()  # disable until real history system added


# =========================
# WARNING SYSTEM
# =========================
def warning_students(df):

    if "attendance" not in df.columns or "Average" not in df.columns:
        return pd.DataFrame()

    return df[
        (df["attendance"] < 75) |
        (df["Average"] < 40)
    ]
