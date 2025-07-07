# 禁用ModelScope的info和warning
import logging
import sys

logging.disable(sys.maxsize)
# 用于处理正则
import re
import numpy as np


def clean_text(raw_text):
    return re.sub(r"<\|.*?\|>", "", raw_text)


# 语音转文字
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import tempfile
import soundfile as sf

# 换成了通义的SenseVoiceSmall，效果比之前的Whisper要好很多
asr_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model="iic/SenseVoiceSmall",
    model_revision="master",
    device="cuda:0",
)
# 标点恢复模型
punc_pipeline = pipeline(
    task=Tasks.punctuation,
    model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
    model_revision="v2.0.4",
    device="cuda:0",  # 如果你想使用 GPU，确保该模型也支持
)


# 语音转文字 Function
def transcribe(audio):
    if not audio or not isinstance(audio, (tuple, list)) or len(audio) != 2:
        return "无效的音频输入，请重新录音"
    sr, y = audio
    if y is None or len(y) == 0:
        return "音频数据为空，请重新录音"
    if y.ndim > 1:
        y = y.mean(axis=1)
    y = y.astype(np.float32)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, y, sr)
        result = asr_pipeline(f.name)
    try:
        raw_text = clean_text(result[0]["text"])
        # 添加标点
        punc_result = punc_pipeline(raw_text)
        final_text = punc_result[0]["text"]
        return final_text
    except Exception as e:
        print("识别失败：", e)
        return "语音识别失败，请重试"
