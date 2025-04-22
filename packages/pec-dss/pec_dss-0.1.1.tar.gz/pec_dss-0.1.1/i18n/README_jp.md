# PEC-DSS 🎵🔊

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[English](../README.md) | [한국어](README_ko.md) | [中文](README_zh.md) | [日本語](README_jp.md)

**話者分離セグメントからの準言語イベント分類**

PEC-DSSは、高度な話者分離と神経音声処理を通じて、準言語的な音声イベント（笑い声、ため息など）を識別し、特定の話者に帰属させる先進的な音声分析システムです。

## ✨ 特徴

* 🎙️ 神経音声エンコーダーを使用した高度な話者識別
* 😀 準言語イベントを特定の話者に帰属
* 🔍 高精度SNAC（Scalable Neural Audio Codec）モデルの統合
* 🔊 音声埋め込みと類似性ベースの話者マッチング
* 📊 包括的な音声コードブック分析
* 🔄 カスタマイズが容易なモジュラーアーキテクチャ

## 🚀 インストール

依存関係のインストール：

```bash
pip install torch torchaudio librosa soundfile numpy transformers huggingface_hub
pip install snac
```

またはリポジトリをクローン：

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -r requirements.txt
```

> **注意**：現在の実装ではSNACを一時的なソリューションとして使用しています。システムの改善を続けるにつれて、今後のバージョンではこの部分が置き換えられたり修正されたりする可能性があります。

## 📖 クイックスタート

### 基本的な使用法

```python
from snac_model import load_snac_model
from audio_encoder import get_codebook_vectors
from speaker_identification import assign_speakers_to_laughs
import librosa

# SNACモデルをロード
snac_model = load_snac_model(device="cpu")  # またはGPUの場合は"cuda"

# 話者参照サンプルの準備
speaker_samples = {
    "speaker1": [audio1, audio2],  # numpy配列としての音声波形
    "speaker2": [audio3, audio4]
}

# 未識別の音声イベントを処理
unidentified_events = [event1, event2]  # numpy配列としての音声波形

# 各音声イベントの話者を識別
results = assign_speakers_to_laughs(speaker_samples, unidentified_events, snac_model)

# 結果を表示
for speaker, events in results.items():
    print(f"話者 {speaker} には {len(events)} の帰属イベントがあります")
```

## 🧩 システムアーキテクチャ

PEC-DSSは以下のコンポーネントで構成されています：

* **snac_model.py**：SNACモデルの初期化と管理
* **audio_encoder.py**：音声エンコーディングとベクトル化
* **codebook_analysis.py**：音声コードブックの統計分析
* **speaker_identification.py**：話者識別アルゴリズム
* **main.py**：統合と実行フレームワーク

## 🔊 音声イベントタイプ

システムは以下のようなさまざまな準言語イベントを識別できます：

* 笑い声
* ため息
* 泣き声
* 咳
* その他の非言語的な音声表現

## 🚀 今後の開発

* 🧠 より多くの音声エンコーダーモデルとの統合
* 😢 拡張された準言語イベント認識
* 🎵 感情トーンの分類
* ⚡ リアルタイム処理のためのパフォーマンス最適化

## 🤝 貢献

貢献は歓迎します！Pull Requestを自由に提出してください。

## 📄 ライセンス

このプロジェクトはGNU General Public License v3.0の下でライセンスされています。

## 🙏 謝辞

* [SNAC](https://github.com/hubertsiuzdak/snac) - Scalable Neural Audio Codec
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) - 機械学習ツール
* [Llama](https://ai.meta.com/llama/) - テキスト処理のための言語モデル 