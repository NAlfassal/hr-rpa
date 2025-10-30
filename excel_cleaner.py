import pandas as pd
import sys
import xlsxwriter
import os

def clear_responses_data(file_path):
    """
    يقوم بقراءة الصف الأول (العناوين) من ملف responses.xlsx،
    ثم يعيد كتابة الملف بالصف الأول فقط.
    """
    if not os.path.exists(file_path):
        print(f"Error: Excel file not found at {file_path}")
        return

    try:
        # قراءة الصف الأول فقط (index 0) للحصول على العناوين
        # header=None لضمان أننا لا نضيع العناوين في حالة كان الملف فارغاً بالفعل
        df = pd.read_excel(file_path, sheet_name='الردود', header=None)
        
        # استخراج الصف الأول فقط (الذي يحتوي على العناوين)
        # إذا كان الملف يحتوي على صف واحد فقط، ستبقى العناوين
        header_row = df.iloc[[0]] 
        
        # إنشاء كاتب Excel جديد
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        
        # كتابة صف العناوين فقط إلى الملف
        header_row.to_excel(writer, sheet_name='الردود', index=False, header=False)
        
        # تطبيق خاصية الكتابة من اليمين لليسار
        worksheet = writer.sheets['الردود']
        worksheet.right_to_left()
        
        writer.close()
        print(f"Success: File reset completed for {file_path}.")
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred during reset: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python excel_cleaner.py <path_to_excel_file>")
        sys.exit(1)
        
    file_to_clear = sys.argv[1]
    clear_responses_data(file_to_clear)
