# 预设的css样式，可以应用到gradio程序中
custom_css ="""
/* 背景页面淡蓝色 */
.gradio-container {
    background-color: #f2f6fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 页脚 */
#footer {
    text-align: center;
    font-size: 12px;
    color: #999;
    margin-top: 20px;
}

/* 清空按钮 */
#clear-btn {
    background-color: red;
    color: white;
}

/* Markdown 标题样式 */
h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
}

/* Markdown 标题样式 */
h2 {
    color: #1e40af;
    margin-bottom: 20px;
}

/* 普通文本框边框样式 */
textarea, input, .gradio-textbox {
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
    padding: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 取消点击输入框后的蓝色背景 */
textarea:focus, input[type="password"]:focus, .gradio-textbox:focus {
    background-color: white !important;
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #999 !important;
}

/* ChatBot文本框边框样式 */
.gradio-chatbot {
    border-radius: 8px !important;
    border: 1px solid #ccc !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
"""