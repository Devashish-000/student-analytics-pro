from reportlab.platypus import SimpleDocTemplate, Table
import sqlite3
import os

def export_pdf():

    file_path = "student_report.pdf"
    doc = SimpleDocTemplate(file_path)

    conn = sqlite3.connect("database/school.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    table = Table([["ID","Name","Class","Age"]] + data)

    doc.build([table])

    return file_path
