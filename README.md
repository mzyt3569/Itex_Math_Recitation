# Itex_Math_Recitation

## Installation

1. Conda 환경 생성 및 패키지 설치:
    ```sh
    conda create -n itex python=3.12
    pip install -r requirements.txt
    ```

2. Tesseract 설치:
    - **Windows**: [설치 링크](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치 후, PATH에 추가합니다.
    - **Linux**: 다음 명령어를 사용하여 설치합니다.
        ```sh
        apt-get install tesseract-ocr
        ```

## How to Use

1. 기본 사용법:
    ```sh
    python Inference.py -i /source_directory -o /output_directory -d /database_directory_for_rag --debug --full
    ```

2. 추가 옵션:
    - RAG 사용: `--rag` 옵션 추가(다만, RAG가 조금 불안정한 부분이 있습니다.)
    - 단계 확인: `--debug` 옵션 추가 (CSV 파일 생성, logs/steps.csv로 저장됩니다.)
    - 음성 생성: `--full` 옵션 추가 (MP3 파일 생성)

3. 웹 데모 실행:
    ```sh
    python web_launcher.py
    ```
    - 이 웹 데모는 RAG를 사용하지 않으며, 음성을 생성하지 않습니다.
    - RAG를 사용하려면, 16번째 줄의 `False`를 `True`로 바꾸시고, db의 경로도 기본 경로가 아니라면 추가로 지정해주세요.
    - Gradio를 사용하였습니다.
  
4. Usage Instructions

    각 함수에 쉽게 판별할 수 있는 주석이 첨부되어 있습니다.

## Other Information
- 각 스텝 별 output은 logs의 csv파일들을 참조해주세요.
- **OCR**: 이미지를 받아 JSON 구조 파일 생성
- **Parser**: 분수와 부등호 분리
- **Translator**: LaTeX 번역
- **Merger**: LaTeX 병합

