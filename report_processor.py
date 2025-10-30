# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os
import re
from openpyxl import load_workbook 


def normalize_text(text):
   
    if pd.isna(text):
        return text
    
    text = str(text).strip()
    text = re.sub('[أإآ]', 'ا', text)
    return text

def process_and_highlight_duplicates(file_path):
    """
    يحمّل ملف Excel، يطبّق التنظيف وتظليل التكرارات باستخدام xlsxwriter، ويحفظ الملف.
    (لا يقوم بعملية المسح/الـ Reset)
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at the specified path: {file_path}", file=sys.stderr)
            return

        print("Starting data cleaning and duplicate highlighting using xlsxwriter...")

        # 1. القراءة والتنظيف وتحديد التكرارات (كالمعتاد)
        df = pd.read_excel(file_path)
        
        # أعمدة المفتاح للتحقق من التكرار
        key_columns = [
            'تاريخ النشاط', 'اسم القطاع', 'الإدارة',
            'موضوع النشاط', 'اسم المقدم', 'الفئة المستهدفة'
        ]
        
        # تطبيق التنظيف على أعمدة النصوص
        text_cols_to_clean = ['موضوع النشاط', 'اسم المقدم', 'الفئة المستهدفة']
        for col in text_cols_to_clean:
            if col in df.columns:
                df[col] = df[col].apply(normalize_text)

        # تحديد التكرارات
        df['is_duplicate'] = df.duplicated(subset=key_columns, keep='first')
        
        if not df['is_duplicate'].any():
            print("No duplicates found after text cleaning.")
            # إذا لم يكن هناك تكرارات، نحفظ البيانات المنظفة فقط ونخرج
            df.drop(columns=['is_duplicate'], inplace=True)
            df.to_excel(file_path, index=False, engine='xlsxwriter')
            return

        print(f"Found {df['is_duplicate'].sum()} duplicate rows. Highlighting in red...")

        # 2. الكتابة والتظليل باستخدام xlsxwriter
        
        # نستخدم ExcelWriter لتحديد المحرك xlsxwriter
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        
        # حفظ البيانات المنظفة في الملف مؤقتاً
        df.drop(columns=['is_duplicate']).to_excel(writer, sheet_name='Sheet1', index=False)
        
        # الوصول إلى الكائنات الأصلية لـ xlsxwriter
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # تعريف التنسيق الأحمر
        red_format = workbook.add_format({
            'bg_color': '#FFC7CE', # لون أحمر فاتح للخلفية
        })
        
        # تطبيق التنسيق على الصفوف المكررة
        for row_index in df.index:
            if df.loc[row_index, 'is_duplicate']:
                # row_index في pandas يبدأ من 0، بينما في Excel يبدأ الصف الأول للبيانات من 1.
                # صف العناوين هو الصف 0 في pandas و الصف 1 في Excel.
                # لذا، row_index 0 (أول صف بيانات) هو صف 1 في pandas و الصف 2 في Excel.
                excel_row = row_index + 1 # +1 لتعويض صف العناوين
                
                # نطاق الصف بالكامل (من العمود A حتى عدد الأعمدة)
                start_col = 0
                end_col = len(df.columns) - 2 # نطرح 2 لأننا أسقطنا عمود 'is_duplicate' وعمود التكرار المؤقت
                
                # الكتابة والتظليل على الصف بالكامل
                worksheet.set_row(excel_row, None, red_format)
                
        # إغلاق الكاتب لحفظ جميع التغييرات
        writer.close()
        
        print(" Data cleaning and highlighting complete on the original file using xlsxwriter.")

    except Exception as e:
        print(f"Error during Excel processing with xlsxwriter: {e}", file=sys.stderr)
        sys.exit(1)

# نقطة الدخول: تأخذ مسار الملف من سطر الأوامر
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Excel file path not provided.", file=sys.stderr)
        sys.exit(1)
        
    excel_path = sys.argv[1]
    process_and_highlight_duplicates(excel_path)
