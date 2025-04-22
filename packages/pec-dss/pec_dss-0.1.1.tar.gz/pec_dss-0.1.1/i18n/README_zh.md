# PEC-DSS 🎵🔊

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[English](../README.md) | [한국어](README_ko.md) | [中文](README_zh.md) | [日本語](README_jp.md)

**从分离说话人片段识别准语言事件**

PEC-DSS是一种先进的音频分析系统，通过复杂的说话人分离和神经音频处理技术，识别准语言声音事件（如笑声、叹息等）并将其归属于特定说话人。

## ✨ 特点

* 🎙️ 使用神经音频编码器进行高级说话人识别
* 😀 将准语言事件归属于特定说话人
* 🔍 高精度SNAC（可扩展神经音频编解码器）模型集成
* 🔊 语音嵌入和基于相似度的说话人匹配
* 📊 全面的音频码本分析
* 🔄 便于自定义的模块化架构

## 🚀 安装

安装依赖：

```bash
pip install torch torchaudio librosa soundfile numpy transformers huggingface_hub
pip install snac
```

或者克隆仓库：

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -r requirements.txt
```

> **注意**：当前实现使用SNAC作为临时解决方案。随着我们不断改进系统，此部分可能在未来版本中被替换或修改。

## 📖 快速开始

### 基本用法

```python
from snac_model import load_snac_model
from audio_encoder import get_codebook_vectors
from speaker_identification import assign_speakers_to_laughs
import librosa

# 加载SNAC模型
snac_model = load_snac_model(device="cpu")  # 或者GPU使用"cuda"

# 准备说话人参考样本
speaker_samples = {
    "speaker1": [audio1, audio2],  # 作为numpy数组的音频波形
    "speaker2": [audio3, audio4]
}

# 处理未识别的音频事件
unidentified_events = [event1, event2]  # 作为numpy数组的音频波形

# 为每个音频事件识别说话人
results = assign_speakers_to_laughs(speaker_samples, unidentified_events, snac_model)

# 打印结果
for speaker, events in results.items():
    print(f"说话人 {speaker} 有 {len(events)} 个归属事件")
```

## 🧩 系统架构

PEC-DSS包含以下组件：

* **snac_model.py**：SNAC模型初始化和管理
* **audio_encoder.py**：音频编码和向量化
* **codebook_analysis.py**：音频码本统计分析
* **speaker_identification.py**：说话人识别算法
* **main.py**：集成和执行框架

## 🔊 音频事件类型

系统可以识别各种准语言事件，包括：

* 笑声
* 叹息
* 哭泣
* 咳嗽
* 其他非语言声音表达

## 🚀 未来发展

* 🧠 集成更多音频编码器模型
* 😢 扩展准语言事件识别
* 🎵 情感语调分类
* ⚡ 实时处理性能优化

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

## 📄 许可证

本项目采用GNU通用公共许可证v3.0授权。

## 🙏 致谢

* [SNAC](https://github.com/hubertsiuzdak/snac) - 可扩展神经音频编解码器
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) - 机器学习工具
* [Llama](https://ai.meta.com/llama/) - 用于文本处理的语言模型 