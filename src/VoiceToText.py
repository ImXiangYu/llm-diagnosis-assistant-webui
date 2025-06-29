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
    model='iic/SenseVoiceSmall',
    model_revision="master",
    device="cuda:0",)

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
        return clean_text(result[0]["text"])
    except Exception as e:
        print("识别失败：", e)
        return "语音识别失败，请重试"