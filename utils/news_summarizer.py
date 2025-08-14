import requests
import json
from typing import List, Dict
from config.config import Config
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsSummarizer:
    def __init__(self):
        self.llm_type = Config.LLM_TYPE
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Ollama 설정
        self.ollama_url = Config.OLLAMA_BASE_URL
        self.ollama_model = Config.OLLAMA_MODEL
        
        # Hugging Face 설정
        self.hf_model = Config.HF_MODEL
    
    def create_short_summary(self, news_item: Dict) -> Dict:
        """뉴스를 1분짜리 숏츠 형식으로 요약합니다."""
        try:
            # 요약을 위한 프롬프트 구성
            prompt = self._create_summary_prompt(news_item)
            
            # LLM 타입에 따라 다른 방식으로 요청
            if self.llm_type == 'ollama':
                summary_text = self._call_ollama(prompt)
            elif self.llm_type == 'huggingface':
                summary_text = self._call_huggingface(prompt)
            else:
                # 기본값: 간단한 규칙 기반 요약
                summary_text = self._rule_based_summary(news_item)
            
            # 응답 파싱
            summary_info = self._parse_summary_response(summary_text)
            
            # 결과 업데이트
            news_item.update({
                'short_summary': summary_info['summary'],
                'key_points': summary_info['key_points'],
                'estimated_duration': summary_info['estimated_duration'],
                'summary_created_at': Config.get_current_time()
            })
            
            logger.info(f"Short summary created for '{news_item['title']}': {summary_info['estimated_duration']}초")
            return news_item
            
        except Exception as e:
            logger.error(f"Error creating summary for '{news_item.get('title', 'Unknown')}': {e}")
            # 에러 발생 시 기본 요약 생성
            news_item.update({
                'short_summary': f"'{news_item.get('title', '뉴스')}'에 대한 요약을 생성할 수 없습니다.",
                'key_points': ["요약 생성 실패"],
                'estimated_duration': 30,
                'summary_created_at': Config.get_current_time()
            })
            return news_item
    
    def _create_summary_prompt(self, news_item: Dict) -> str:
        """요약 생성을 위한 프롬프트를 생성합니다."""
        category_name = Config.CATEGORIES.get(news_item['category'], news_item['category'])
        
        prompt = f"""
다음 뉴스를 유튜브 숏츠(1분 이내)용으로 요약해주세요:

카테고리: {category_name}
제목: {news_item['title']}
언론사: {news_item['press']}
내용: {news_item.get('content', '')[:800]}...

요구사항:
1. 핵심 내용을 1분 이내로 읽을 수 있는 분량으로 요약
2. 시청자의 관심을 끌 수 있는 흥미로운 표현 사용
3. 핵심 포인트 3-5개 포함
4. 한국어로 자연스럽게 작성

다음 형식으로 응답해주세요:
[요약 내용 - 1분 이내로 읽을 수 있는 분량]

핵심 포인트:
- [포인트 1]
- [포인트 2]
- [포인트 3]

예상 읽기 시간: [X]초
"""
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """Ollama API를 호출합니다."""
        try:
            url = f"{self.ollama_url}/api/generate"
            data = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '요약을 생성할 수 없습니다.')
            
        except Exception as e:
            logger.warning(f"Ollama API 호출 실패: {e}")
            return f"Ollama API 오류: {str(e)}"
    
    def _call_huggingface(self, prompt: str) -> str:
        """Hugging Face 모델을 호출합니다."""
        try:
            # 간단한 구현: 실제로는 transformers 라이브러리를 사용해야 함
            return "Hugging Face 모델 요약 결과: 이 뉴스는 중요한 내용을 담고 있어 많은 관심을 받을 것으로 예상됩니다."
            
        except Exception as e:
            logger.warning(f"Hugging Face 모델 호출 실패: {e}")
            return f"Hugging Face 모델 오류: {str(e)}"
    
    def _rule_based_summary(self, news_item: Dict) -> str:
        """규칙 기반으로 간단한 요약을 생성합니다."""
        try:
            title = news_item.get('title', '')
            content = news_item.get('content', '')
            category = news_item.get('category', '')
            
            # 제목을 기반으로 간단한 요약 생성
            summary = f"'{title}'에 대한 주요 내용입니다. "
            
            # 내용에서 첫 번째 문장을 추출하여 요약에 추가
            if content and len(content) > 50:
                first_sentence = content.split('.')[0] + '.'
                summary += first_sentence
            else:
                summary += "자세한 내용은 원문을 참고하세요."
            
            # 핵심 포인트 생성
            key_points = [
                f"카테고리: {Config.CATEGORIES.get(category, category)}",
                f"제목: {title}",
                "핵심 내용 요약"
            ]
            
            # 예상 시간 계산 (단어 수 기반)
            word_count = len(summary.split())
            estimated_duration = min(60, max(30, word_count * 2))  # 단어당 약 2초
            
            return f"{summary}\n\n핵심 포인트:\n- {key_points[0]}\n- {key_points[1]}\n- {key_points[2]}\n\n예상 읽기 시간: {estimated_duration}초"
            
        except Exception as e:
            logger.warning(f"규칙 기반 요약 생성 실패: {e}")
            return f"'{news_item.get('title', '뉴스')}'에 대한 요약을 생성할 수 없습니다.\n\n핵심 포인트:\n- 요약 생성 실패\n\n예상 읽기 시간: 30초"
    
    def _parse_summary_response(self, response_text: str) -> Dict:
        """LLM 응답에서 요약 정보를 파싱합니다."""
        try:
            # 요약 내용과 핵심 포인트 분리
            lines = response_text.split('\n')
            summary = ""
            key_points = []
            estimated_duration = 60  # 기본값 1분
            
            current_section = "summary"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "핵심 포인트:" in line or "핵심포인트:" in line:
                    current_section = "key_points"
                    continue
                elif "예상 읽기 시간:" in line or "예상시간:" in line:
                    # 시간 추출
                    import re
                    time_match = re.search(r'(\d+)', line)
                    if time_match:
                        estimated_duration = int(time_match.group(1))
                    current_section = "time"
                    continue
                
                if current_section == "summary":
                    if line.startswith('-') or line.startswith('•'):
                        continue
                    summary += line + " "
                elif current_section == "key_points":
                    if line.startswith('-') or line.startswith('•'):
                        point = line.lstrip('-• ').strip()
                        if point:
                            key_points.append(point)
            
            # 요약 정리
            summary = summary.strip()
            if not summary:
                summary = "요약 내용을 생성할 수 없습니다."
            
            # 핵심 포인트가 없으면 기본값 설정
            if not key_points:
                key_points = ["핵심 내용 요약"]
            
            return {
                'summary': summary,
                'key_points': key_points,
                'estimated_duration': estimated_duration
            }
            
        except Exception as e:
            logger.warning(f"Error parsing summary response: {e}")
            return {
                'summary': "요약 내용을 파싱할 수 없습니다.",
                'key_points': ["파싱 오류"],
                'estimated_duration': 60
            }
    
    def create_summaries_for_top_news(self, top_news: List[Dict]) -> List[Dict]:
        """상위 어그로 뉴스들에 대해 요약을 생성합니다."""
        summarized_news = []
        
        for news_item in top_news:
            summarized_item = self.create_short_summary(news_item)
            summarized_news.append(summarized_item)
            
            # API 호출 간격 조절
            import time
            time.sleep(1)
        
        return summarized_news
    
    def format_for_shorts(self, news_item: Dict) -> str:
        """숏츠 형식으로 포맷팅합니다."""
        category_name = Config.CATEGORIES.get(news_item['category'], news_item['category'])
        
        shorts_format = f"""
🔥 {category_name.upper()} 뉴스 요약 🔥

📰 {news_item['title']}
📺 {news_item['press']}

📝 요약:
{news_item.get('short_summary', '요약 없음')}

💡 핵심 포인트:
"""
        
        for point in news_item.get('key_points', []):
            shorts_format += f"• {point}\n"
        
        shorts_format += f"\n⏱️ 예상 시청 시간: {news_item.get('estimated_duration', 60)}초"
        shorts_format += f"\n🔥 어그로 점수: {news_item.get('agro_score', 0)}점"
        
        return shorts_format

if __name__ == "__main__":
    # 테스트 실행
    summarizer = NewsSummarizer()
    
    # 샘플 뉴스 데이터로 테스트
    sample_news = {
        'title': '테스트 뉴스 제목',
        'content': '테스트 뉴스 내용입니다. 이것은 요약 생성을 위한 샘플 데이터입니다.',
        'category': 'economy',
        'press': '테스트 언론사',
        'agro_score': 85
    }
    
    result = summarizer.create_short_summary(sample_news)
    print("=== 숏츠 형식 요약 ===")
    print(summarizer.format_for_shorts(result))
