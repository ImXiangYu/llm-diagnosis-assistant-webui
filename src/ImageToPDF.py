# ImageToPDF.py
import os
import time
import pythoncom
from docxtpl import DocxTemplate
import win32com.client

def ImageToPDF(name, gender, age, phone, username):
    doc = DocxTemplate("../Template/MedicalReportTemplate.docx")

    context = {
        "name": name,
        "gender": gender,
        "age": age,
        "phone": phone,
    }

    doc.render(context)

    local_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    word_filename = f"医学影像报告_{name}_{local_time}.docx"
    pdf_filename = f"医学影像报告_{name}_{local_time}.pdf"
    word_path = "SavedImageRecords/" + word_filename
    pdf_path = "SavedImageRecords/" + pdf_filename

    doc.save(word_path)

    def word_to_pdf(input_path, output_path):
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        this_doc = word.Documents.Open(os.path.abspath(input_path))
        this_doc.SaveAs(os.path.abspath(output_path), FileFormat=17)
        this_doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()

    word_to_pdf(word_path, pdf_path)
    return [pdf_path, pdf_filename]
