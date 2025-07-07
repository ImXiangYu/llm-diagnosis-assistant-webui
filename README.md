# llm-diagnosis-assistant-webui

基于Gradio构建的WebUI页面，包含[待完善]

主要用于重庆大学2022级校内实习项目  

## 项目结构
```
.
├── README.md
├── SavedImageRecords
│   └── README.md
├── SavedMedicalRecords
│   └── README.md
├── Template
│   ├── ImageTemplate.docx
│   └── MedicalReportTemplate.docx
├── app.py
├── requirements.txt
└── src
    ├── CustomCss.py
    ├── ImageModel.py
    ├── ImageToPDF.py
    ├── Model.py
    ├── OperationFunc.py
    ├── TextToPDF.py
    ├── UploadedFiles
    │   └── README.md
    ├── UploadedImages
    │   └── README.md
    ├── VoiceToText.py
    ├── app.db
    └── database.py
```
## 如何使用
### Requirements
先在根目录下运行指令进行环境安装  
`pip install -r requirements.txt`

### 模型加载
运行项目前需先启动ollama服务  
`ollama serve`  
在`src/model.py`中修改模型与模型参数  
运行`app.py`会自动下载需要的语言识别模型

### 运行
直接使用`python app.py`即可运行

也可以使用`gradio app.py`进行热部署  
但部分情况下会出现Bug，仅推荐开发时使用

## 项目介绍
待完善
