from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime
import xlsxwriter 

app = Flask(__name__, template_folder='.')

DATA_PATH = os.path.join("data", "responses.xlsx")

@app.route("/form")
def form():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    column_order = [
        "اسم القطاع", "الإدارة", "موضوع النشاط", "نوع النشاط", 
        "هدف استراتيجي 1", "هدف استراتيجي 2", "تصنيف المقدم", 
        "تاريخ النشاط", "اسم المقدم", "مسؤول الحضور", 
        "الفئة المستهدفة", "عدد الحضور", "مدة النشاط (ساعة)", 
        "مكان الحفظ", "تاريخ الإرسال"
    ]
    
    data = {
        "اسم القطاع": [request.form.get("sector")],
        "الإدارة": [request.form.get("department")],
        "موضوع النشاط": [request.form.get("activityTopic")],
        "نوع النشاط": [request.form.get("activityType")],
        "هدف استراتيجي 1": [request.form.get("strategicGoalLevel1")],
        "هدف استراتيجي 2": [request.form.get("strategicGoalLevel2")],
        "تصنيف المقدم": [request.form.get("presenterCategory")],
        "تاريخ النشاط": [request.form.get("activityDate")],
        "اسم المقدم": [request.form.get("presenterName")],
        "مسؤول الحضور": [request.form.get("attendanceResponsible")],
        "الفئة المستهدفة": [request.form.get("targetAudience")],
        "عدد الحضور": [request.form.get("attendeeCount")],
        "مدة النشاط (ساعة)": [request.form.get("activityDuration")],
        "مكان الحفظ": [request.form.get("contentLocation")],
        "تاريخ الإرسال": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    df = pd.DataFrame(data, columns=column_order)

    if os.path.exists(DATA_PATH):
        try:
            old_df = pd.read_excel(DATA_PATH)
            
            old_df = old_df.reindex(columns=column_order)
            
            df = pd.concat([old_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error reading existing Excel file: {e}. Starting new DataFrame.")
            pass 

    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        writer = pd.ExcelWriter(DATA_PATH, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='الردود', index=False)
        
        worksheet = writer.sheets['الردود']
        worksheet.right_to_left()
        
        writer.close() 

        return "✅ تم استلام النموذج وحفظه في ملف Excel بنجاح!"
    except Exception as e:
        print(f"Error writing to Excel: {e}")
        return "❌ فشل في حفظ البيانات على الخادم. الرجاء التحقق من تسجيل الخطأ.", 500

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True)
