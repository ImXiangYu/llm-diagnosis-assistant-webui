# TextToPDF.py
import os
import time
import pythoncom
from docxtpl import DocxTemplate
import win32com.client

def TextToPDF(name, gender, age, phone,
              chief_complaint="无", examinations="无", diagnosis="无", disposal="无", username="wys"):
    doc = DocxTemplate("../Template/template.docx")

    context = {
        "name": name,
        "gender": gender,
        "age": age,
        "phone": phone,
        "chief_complaint": chief_complaint,
        "examinations": examinations,
        "diagnosis": diagnosis,
        "disposal": disposal,
        "username": username
    }

    doc.render(context)

    local_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    word_filename = f"病历_{name}_{local_time}.docx"
    pdf_filename = f"病历_{name}_{local_time}.pdf"
    word_path = "SavedMedicalRecords/" + word_filename
    pdf_path = "SavedMedicalRecords/" + pdf_filename

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
