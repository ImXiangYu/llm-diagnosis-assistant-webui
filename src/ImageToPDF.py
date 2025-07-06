# ImageToPDF.py
import os
import time
import pythoncom
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
import win32com.client

import random


def ImageToPDF(
    name,
    gender,
    age,
    username,
    clinical_diagnosis="无",
    image="无",
    description="无",
    imaging_diagnosis="无",
):
    doc = DocxTemplate("../Template/ImageTemplate.docx")

    if not image:
        insert_image = "无"
    else:
        insert_image = InlineImage(doc, image, width=Mm(140))

    context = {
        "time": time.strftime("%Y.%m.%d %H:%M", time.localtime()),
        "random": random.randint(1, 100),
        "name": name,
        "gender": gender,
        "username": username,
        "age": age,
        "part": "胸片",
        "clinical_diagnosis": clinical_diagnosis,
        "image": insert_image,
        "description": description,
        "imaging_diagnosis": imaging_diagnosis,
    }

    doc.render(context)

    local_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    word_filename = f"医学影像报告_{name}_{local_time}.docx"
    pdf_filename = f"医学影像报告_{name}_{local_time}.pdf"
    word_path = "../SavedImageRecords/" + word_filename
    pdf_path = "../SavedImageRecords/" + pdf_filename

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
