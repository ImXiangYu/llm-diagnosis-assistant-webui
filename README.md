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

本项目是一个基于 Gradio 构建的 WebUI 页面，旨在为医疗从业者提供智能化的辅助诊疗工具。系统集成了自然语言处理、医学影像分析和知识库检索等功能，帮助医生快速生成病历、进行诊断推理，并支持历史病例查询与医学影像报告输出。

### 核心功能模块

1. **文本诊疗**
   - 支持通过文本或语音输入患者现病史。
   - 基于大语言模型（LLM）生成结构化病历（主诉、现病史、辅助检查、诊断结果、处置意见）。
   - 提供“深度思考”、“联网搜索”、“检索增强”等模型增强选项以提高诊断准确性。
   - 支持导出完整病历为 PDF 文件。

2. **医学影像分析**
   - 支持上传医学影像图片（如 X 光、CT 等）。
   - 利用图像识别模型对影像进行解读，输出“影像所见”和“影像诊断”。
   - 可将分析结果导出为 PDF 影像报告。

3. **历史病例查询**
   - 支持查看、下载过往创建的病历与影像报告。
   - 提供病例导入功能，可快速载入历史信息用于新对话。
   - 支持删除历史病例记录。

4. **知识库上传与预览**
   - 用户可上传本地文件（PDF、Word、TXT、Markdown、图片等）构建私有医学知识库。
   - 提供“预览模型效果”功能，测试模型对知识库内容的理解能力。
   - 启用“检索增强”后，模型可在诊疗过程中引用知识库内容辅助决策。

5. **用户管理**
   - 包含登录与注册功能，支持多用户使用。
   - 所有病历与报告均与用户绑定，确保数据安全与隐私保护。

### 技术架构

- **前端界面**：使用 [Gradio](https://www.gradio.app/) 构建交互式 UI。
- **样式设计**：通过 [CustomCss.py](file://D:\PythonWebUI\llm-diagnosis-assistant-webui\src\CustomCss.py) 自定义 CSS 实现美观界面。
- **语音识别**：采用阿里通义实验室的 SenseVoice 模型实现高精度中文语音转文字。
- **语言模型**：调用本地运行的 LLM（如 Qwen）完成病历生成与诊断推理。
- **图像模型**：结合 Ollama 和本地部署的视觉模型处理医学影像。
- **文档生成**：使用 `docxtpl` 和 `python-docx` 动态生成 Word 文档并转换为 PDF。
- **数据库**：SQLite 存储用户、病人信息及文件路径，便于管理和检索。
- **文件存储**：支持保存病历 PDF、影像报告 PDF、上传的医学影像和知识库文件。

### 应用场景

适用于医院门诊、远程会诊、医学教育等场景，提升医生工作效率，减少重复性劳动，同时保证病历书写的规范性和专业性。

