import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    # LLM 설정 (무료 대안)
    LLM_TYPE = os.getenv('LLM_TYPE', 'ollama')  # 'ollama' 또는 'huggingface'
    
    # Ollama 설정
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')  # 또는 'mistral', 'codellama' 등
    
    # Hugging Face 설정
    HF_MODEL = os.getenv('HF_MODEL', 'microsoft/DialoGPT-medium')
    
    # 공통 LLM 설정
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    
    # 네이트 뉴스 설정
    NATE_NEWS_BASE_URL = os.getenv('NATE_NEWS_BASE_URL', 'https://news.nate.com')
    MAX_NEWS_PER_CATEGORY = int(os.getenv('MAX_NEWS_PER_CATEGORY', 10))
    
    # 뉴스 카테고리
    CATEGORIES = {
        'economy': '경제',
        'sports': '스포츠', 
        'entertainment': '연예'
    }
    
    # 카테고리별 URL 패턴
    CATEGORY_URLS = {
        'economy': 'https://news.nate.com/rank/interest?sc=eco',
        'sports': 'https://news.nate.com/rank/interest?sc=spo',
        'entertainment': 'https://news.nate.com/rank/interest?sc=ent'
    }
    
    # 요약 설정
    SUMMARY_TARGET_LENGTH = 60  # 1분 (초 단위)
    SUMMARY_MAX_WORDS = 150     # 대략적인 단어 수
    
    @staticmethod
    def get_current_time():
        """현재 시간을 ISO 형식으로 반환합니다."""
        from datetime import datetime
        return datetime.now().isoformat()

