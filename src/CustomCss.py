# 预设的css样式，可以应用到gradio程序中
custom_css ="""
/* 背景页面淡蓝色 */
.gradio-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;

    background-image: url('https://www.cqu.edu.cn/images/23/10/11/1ucry5xfsw/%E8%99%8E%E6%BA%AA%E4%BA%91%E6%B9%96%E6%B0%B4%E5%BD%B1.jpg'); /* 替换为你的背景图片URL */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: #f2f6fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 主体内容自动占据剩余空间 */
#main-content {
    flex: 1;
    min-height: 670px;
}


/* 添加一个半透明遮罩层 */
.gradio-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(255, 255, 255, 0.5); /* 白色半透明遮罩，透明度可调 */
    z-index: 0;
}

/* 确保容器内其他内容在遮罩上方 */
.gradio-container > * {
    position: relative;
    z-index: 1;
}

/* 清空按钮 */
#clear-btn {
    background-color: red;
    color: white;
}

/* 登出按钮 */
#logout-btn {
    background-color: red;
    color: white;
}

#normal-btn {
    background-color: #90EE90;
    color: #1D4ED8;
}

/* Markdown 标题样式 */
h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
}

/* Markdown 标题样式 */
h2 {
    text-align: center;
    color: #1e40af;
    margin-bottom: 20px;
}

/* Markdown 标题样式 */
h3 {
    color: #1e40af;
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

#card {
    position: fixed;         /* 脱离文档流，基于窗口定位 */
    top: 20%;                /* 顶部 20% */
    left: 60%;               /* 左边 60% */
    margin-left: auto;
    margin-right: 5vw;
    width: 400px;
    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* 页脚样式 */
#footer {
    text-align: center;
    font-size: 12px;
    color: #999;
    padding: 10px 0;
    border-top: 1px solid #ddd;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 100%;
}


/* 文本诊疗PDF下载 */
#chat-PDF-Download {
    height: 82px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

/* 医学影像报告PDF下载 */
#image-PDF-Download {
    height: 83px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

/* 医学影像上传 */
#image-upload {
    height: 188px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

/* 已上传的知识库文件 */
#files-upload {
    height: 300px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

/* 上传知识库界面的文字 */
#text-in-file-upload {
    height: 300px;
    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    width: 360px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* ============ 针对 Gradio DataFrame 的样式调整 ============ */
/* 1. 取消表格内所有单元格的边框 */
.gradio-dataframe table {
    border-collapse: collapse;       /* 合并单元格边框 */
}
.gradio-dataframe td,
.gradio-dataframe th {
    border: none !important;         /* 去掉所有内、外边框 */
}

/* 2. 让第一列占更大比例（例如占 30%）*/
.gradio-dataframe td:first-child,
.gradio-dataframe th:first-child {
    width: 150% !important;
}

/* 3. 其余列按比例分配（可选，让剩余三列平均分布）*/
.gradio-dataframe td:nth-child(n+2),
.gradio-dataframe th:nth-child(n+2) {
    width: 23.33% !important;       /* (100% - 30%) / 3 ≈ 23.33% */
}

#welcome-line .welcome-tagline {
  text-align: right;
  font-size: 3.2rem;
  color: #004A9F;
  margin-right: 40vw;
  margin-top: 17vh;
  font-weight: 600;
}
#welcome-line .zhiyu-title {
  font-size: 6rem; /* 智渝专属字体大小 */
  font-weight: 700;
  color: #004A9F;
  line-height: 2;
}
#welcome-line .welcome-image {
  width: 300px;
  height: auto;
  display: block;
  margin-left: 31vw;
}
"""