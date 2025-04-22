# PEC-DSS 🎵🔊

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[English](../README.md) | [한국어](README_ko.md) | [中文](README_zh.md) | [日本語](README_jp.md)

**화자 분할 세그먼트에서의 준언어적 이벤트 분류**

PEC-DSS는 고급 화자 분할 및 신경망 오디오 처리를 통해 준언어적 음성 이벤트(웃음, 한숨 등)를 식별하고 특정 화자에게 귀속시키는 고급 오디오 분석 시스템입니다.

## ✨ 특징

* 🎙️ 신경망 오디오 인코더를 사용한 고급 화자 식별
* 😀 준언어적 이벤트를 특정 화자에게 귀속
* 🔍 고정확도 SNAC(Scalable Neural Audio Codec) 모델 통합
* 🔊 음성 임베딩 및 유사도 기반 화자 매칭
* 📊 종합적인 오디오 코드북 분석
* 🔄 쉬운 커스터마이징을 위한 모듈식 아키텍처

## 🚀 설치

의존성 설치:

```bash
pip install torch torchaudio librosa soundfile numpy transformers huggingface_hub
pip install snac
```

또는 저장소 복제:

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -r requirements.txt
```

> **참고**: 현재 구현에서는 SNAC을 임시 솔루션으로 사용하고 있습니다. 시스템을 계속 개선함에 따라 향후 버전에서는 이 부분이 대체되거나 수정될 수 있습니다.

## 📖 빠른 시작

### 기본 사용법

```python
from snac_model import load_snac_model
from audio_encoder import get_codebook_vectors
from speaker_identification import assign_speakers_to_laughs
import librosa

# SNAC 모델 로드
snac_model = load_snac_model(device="cpu")  # 또는 GPU를 위한 "cuda"

# 화자 참조 샘플 준비
speaker_samples = {
    "speaker1": [audio1, audio2],  # numpy 배열로서의 오디오 파형
    "speaker2": [audio3, audio4]
}

# 미식별 오디오 이벤트 처리
unidentified_events = [event1, event2]  # numpy 배열로서의 오디오 파형

# 각 오디오 이벤트에 대한 화자 식별
results = assign_speakers_to_laughs(speaker_samples, unidentified_events, snac_model)

# 결과 출력
for speaker, events in results.items():
    print(f"화자 {speaker}는 {len(events)}개의 이벤트를 가집니다")
```

## 🧩 시스템 아키텍처

PEC-DSS는 다음 구성 요소로 이루어져 있습니다:

* **snac_model.py**: SNAC 모델 초기화 및 관리
* **audio_encoder.py**: 오디오 인코딩 및 벡터화
* **codebook_analysis.py**: 오디오 코드북 통계 분석
* **speaker_identification.py**: 화자 식별 알고리즘
* **main.py**: 통합 및 실행 프레임워크

## 🔊 오디오 이벤트 유형

시스템은 다음과 같은 다양한 준언어적 이벤트를 식별할 수 있습니다:

* 웃음
* 한숨
* 울음
* 기침
* 기타 비언어적 음성 표현

## 🚀 향후 개발 계획

* 🧠 더 많은 오디오 인코더 모델과의 통합
* 😢 확장된 준언어적 이벤트 인식
* 🎵 감정 톤 분류
* ⚡ 실시간 처리를 위한 성능 최적화

## 🤝 기여하기

기여는 언제나 환영합니다! Pull Request를 제출해 주세요.

## 📄 라이선스

이 프로젝트는 GNU General Public License v3.0에 따라 라이선스가 부여됩니다.

## 🙏 감사의 글

* [SNAC](https://github.com/hubertsiuzdak/snac) - Scalable Neural Audio Codec
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) - 머신 러닝 도구
* [Llama](https://ai.meta.com/llama/) - 텍스트 처리를 위한 언어 모델 