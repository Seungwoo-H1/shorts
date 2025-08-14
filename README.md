# 네이트 뉴스 어그로 분석 및 요약 시스템

네이트 뉴스에서 경제, 스포츠, 연예 분야의 최신 뉴스를 수집하고, LLM을 활용해 가장 어그로가 높은 뉴스를 선별하여 1분짜리 요약을 생성하는 시스템입니다.

## 기능

- 네이트 뉴스 크롤링 (경제, 스포츠, 연예)
- LLM 기반 어그로 점수 평가
- 1분짜리 요약 생성
- 최고 어그로 뉴스 선별

## 설치 및 실행

1. 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일에 OpenAI API 키 입력
```

3. 실행:
```bash
python main.py
```

## 프로젝트 구조

- `main.py`: 메인 실행 파일
- `news_crawler.py`: 네이트 뉴스 크롤링 모듈
- `agro_analyzer.py`: LLM 기반 어그로 분석 모듈
- `news_summarizer.py`: 뉴스 요약 생성 모듈
- `config.py`: 설정 파일
- `test_system.py`: 시스템 테스트 스크립트
- `requirements.txt`: 필요한 Python 패키지 목록

## 사용법

### 1. 기본 실행
```bash
python main.py
```

### 2. 대화형 모드
```bash
python main.py --interactive
```

### 3. 시스템 테스트
```bash
python test_system.py
```

### 4. 데모 실행 (무료 버전)
```bash
python demo.py
```

## 환경 설정

### 1. 무료 LLM 사용

#### Ollama 사용 (로컬 실행)
1. [Ollama 설치](https://ollama.ai/download)
2. 모델 다운로드: `ollama pull llama2`
3. `.env` 파일에 설정:
```
LLM_TYPE=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

#### Hugging Face 사용
1. `.env` 파일에 설정:
```
LLM_TYPE=huggingface
HF_MODEL=microsoft/DialoGPT-medium
```

### 2. 규칙 기반 분석 (기본값)
API 키나 모델 설치 없이도 작동합니다:
```
LLM_TYPE=rule_based
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 원하는 설정을 추가하세요.

