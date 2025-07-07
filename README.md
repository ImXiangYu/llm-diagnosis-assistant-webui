# llm-diagnosis-assistant-webui

基于Gradio构建的WebUI页面，包含[待完善]

主要用于重庆大学2022级校内实习项目  

## 项目结构
```
.
├── app.py                              主页面
├── README.md
├── requirements.txt                    依赖列表
├── Template
│        ├── ImageTemplate.docx         影像报告模板
│        └── MedicalReportTemplate.docx 病历模板
└── src
    ├── CustomCss.py                    全局样式设置
    ├── ImageToPDF.py                   医学影像报告生成
    ├── Model.py                        大模型
    ├── OperationFunc.py                操作逻辑相关函数
    ├── SavedImageRecords               生成的医学影像保存目录
    ├── SavedMedicalRecords             病历保存目录
    │        └── README.md          
    ├── TextToPDF.py                    文本转PDF
    ├── UploadedImages                  上传的医学影像保存目录
    │        └── placeholder.txt
    ├── VoiceToText.py                  声音转文字
    ├── app.db                          数据库
    └── database.py                     数据库处理文件
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
