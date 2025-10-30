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
    
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at the specified path: {file_path}", file=sys.stderr)
            return

        print("Starting data cleaning and duplicate highlighting using xlsxwriter...")

        # 1. القراءة والتنظيف وتحديد التكرارات
        df = pd.read_excel(file_path)
        
        key_columns = [
            'تاريخ النشاط', 'اسم القطاع', 'الإدارة',
            'موضوع النشاط', 'اسم المقدم', 'الفئة المستهدفة'
        ]
        
        text_cols_to_clean = ['موضوع النشاط', 'اسم المقدم', 'الفئة المستهدفة']
        for col in text_cols_to_clean:
            if col in df.columns:
                df[col] = df[col].apply(normalize_text)

        df['is_duplicate'] = df.duplicated(subset=key_columns, keep='first')
        
        if not df['is_duplicate'].any():
            print("No duplicates found after text cleaning.")
            df.drop(columns=['is_duplicate'], inplace=True)
            df.to_excel(file_path, index=False, engine='xlsxwriter')
            return

        print(f"Found {df['is_duplicate'].sum()} duplicate rows. Highlighting in red...")

        # 2. الكتابة والتظليل باستخدام xlsxwriter
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        
        # استخدام اسم 'الردود' الصحيح
        df.drop(columns=['is_duplicate']).to_excel(writer, sheet_name='الردود', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['الردود']

        red_format = workbook.add_format({
            'bg_color': '#FFC7CE', 
        })
        
        for row_index in df.index:
            if df.loc[row_index, 'is_duplicate']:
                excel_row = row_index + 1
                worksheet.set_row(excel_row, None, red_format)
        
        worksheet.right_to_left()
                
        # إغلاق الكاتب لحفظ جميع التغييرات
        writer.close()
        
        print("Data cleaning and highlighting complete on the original file using xlsxwriter.")

    except Exception as e:
        print(f"Error during Excel processing with xlsxwriter: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Excel file path not provided.", file=sys.stderr)
        sys.exit(1)
        
    excel_path = sys.argv[1]
    process_and_highlight_duplicates(excel_path)
