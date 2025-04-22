# tests/test_voice_tts.py

import pytest
import numpy as np
import torch
import scipy.io.wavfile as wavfile
from tang_yuan_mlops_sdk.voice.tts import TTSClient

@pytest.mark.asyncio
async def test_tts():
    client = TTSClient(base_url="http://222.186.32.152:10004")

    tts_text = "你好，我是通义千问语音合成大模型.哈哈哈哈"
    spk_id = "中文女"
    audio_bytes = await client.synthesize(tts_text, spk_id, endpoint="inference_sft", params={})

    # 转换为 tensor
    tts_speech = torch.from_numpy(np.frombuffer(audio_bytes, dtype=np.int16)).unsqueeze(dim=0)
    # 写出到本地
    wavfile.write("demo_tts.wav", 22050, tts_speech.numpy().squeeze().astype(np.int16))

    assert len(audio_bytes) > 0
    print("Status:", "ok")
    print("Audio length:", len(audio_bytes))