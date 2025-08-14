import requests
import json
from typing import List, Dict
from config import Config
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgroAnalyzer:
    def __init__(self):
        self.llm_type = Config.LLM_TYPE
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Ollama 설정
        self.ollama_url = Config.OLLAMA_BASE_URL
        self.ollama_model = Config.OLLAMA_MODEL
        
        # Hugging Face 설정
        self.hf_model = Config.HF_MODEL
    
    def analyze_news_agro(self, news_item: Dict) -> Dict:
        """개별 뉴스의 어그로 점수를 분석합니다."""
        try:
            # 분석을 위한 프롬프트 구성
            prompt = self._create_agro_analysis_prompt(news_item)
            
            # LLM 타입에 따라 다른 방식으로 요청
            if self.llm_type == 'ollama':
                analysis_text = self._call_ollama(prompt)
            elif self.llm_type == 'huggingface':
                analysis_text = self._call_huggingface(prompt)
            else:
                # 기본값: 간단한 규칙 기반 분석
                analysis_text = self._rule_based_analysis(news_item)
            
            # 응답 파싱
            agro_score, reasoning = self._parse_agro_analysis(analysis_text)
            
            # 결과 업데이트
            news_item.update({
                'agro_score': agro_score,
                'agro_reasoning': reasoning,
                'analyzed_at': Config.get_current_time()
            })
            
            logger.info(f"Agro analysis completed for '{news_item['title']}': Score {agro_score}")
            return news_item
            
        except Exception as e:
            logger.error(f"Error analyzing agro for '{news_item.get('title', 'Unknown')}': {e}")
            # 에러 발생 시 기본값 설정
            news_item.update({
                'agro_score': 50,
                'agro_reasoning': f"분석 중 오류 발생: {str(e)}",
                'analyzed_at': Config.get_current_time()
            })
            return news_item
    
    def _create_agro_analysis_prompt(self, news_item: Dict) -> str:
        """어그로 분석을 위한 프롬프트를 생성합니다."""
        category_name = Config.CATEGORIES.get(news_item['category'], news_item['category'])
        
        prompt = f"""
다음 뉴스의 어그로(관심도, 충격도)를 분석해주세요:

카테고리: {category_name}
제목: {news_item['title']}
언론사: {news_item['press']}
내용: {news_item.get('content', '')[:500]}...

다음 형식으로 응답해주세요:
어그로 점수: [0-100점]
분석 이유: [구체적인 이유 설명]

어그로 점수 기준:
- 90-100: 매우 높은 어그로 (전국민적 관심, 충격적 내용)
- 80-89: 높은 어그로 (광범위한 관심, 중요한 소식)
- 70-79: 중상위 어그로 (상당한 관심, 주목할 만한 내용)
- 60-69: 중간 어그로 (일반적인 관심, 흥미로운 내용)
- 50-59: 보통 어그로 (평범한 관심, 일반적인 뉴스)
- 40-49: 낮은 어그로 (적은 관심, 일상적인 내용)
- 0-39: 매우 낮은 어그로 (거의 관심 없음, 사소한 내용)
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
            return result.get('response', '분석을 완료할 수 없습니다.')
            
        except Exception as e:
            logger.warning(f"Ollama API 호출 실패: {e}")
            return f"Ollama API 오류: {str(e)}"
    
    def _call_huggingface(self, prompt: str) -> str:
        """Hugging Face 모델을 호출합니다."""
        try:
            # 간단한 구현: 실제로는 transformers 라이브러리를 사용해야 함
            # 여기서는 기본 응답만 반환
            return "Hugging Face 모델 분석 결과: 중간 수준의 어그로를 보이는 뉴스입니다."
            
        except Exception as e:
            logger.warning(f"Hugging Face 모델 호출 실패: {e}")
            return f"Hugging Face 모델 오류: {str(e)}"
    
    def _rule_based_analysis(self, news_item: Dict) -> str:
        """규칙 기반으로 간단한 어그로 분석을 수행합니다."""
        try:
            title = news_item.get('title', '').lower()
            content = news_item.get('content', '').lower()
            category = news_item.get('category', '')
            
            # 키워드 기반 점수 계산
            score = 50  # 기본 점수
            
            # 제목에 포함된 키워드로 점수 조정
            high_impact_keywords = ['충격', '폭로', '사건', '사고', '논란', '파문', '폭발', '붕괴', '사망', '부상']
            medium_impact_keywords = ['발표', '공개', '계획', '정책', '결정', '변경', '발견', '연구', '성과']
            
            for keyword in high_impact_keywords:
                if keyword in title:
                    score += 20
                    break
            
            for keyword in medium_impact_keywords:
                if keyword in title:
                    score += 10
                    break
            
            # 카테고리별 기본 점수 조정
            if category == 'entertainment':
                score += 5  # 연예 뉴스는 기본적으로 관심도가 높음
            elif category == 'sports':
                score += 3  # 스포츠 뉴스도 관심도가 높음
            
            # 점수 범위 제한
            score = max(0, min(100, score))
            
            # 이유 생성
            if score >= 80:
                reasoning = "높은 충격도와 관심을 끄는 키워드가 포함된 뉴스입니다."
            elif score >= 60:
                reasoning = "상당한 관심을 끌 수 있는 내용을 담고 있습니다."
            else:
                reasoning = "일반적인 관심 수준의 뉴스입니다."
            
            return f"어그로 점수: {score}\n분석 이유: {reasoning}"
            
        except Exception as e:
            logger.warning(f"규칙 기반 분석 실패: {e}")
            return "어그로 점수: 50\n분석 이유: 규칙 기반 분석 중 오류 발생"
    
    def _parse_agro_analysis(self, analysis_text: str) -> tuple:
        """LLM 응답에서 어그로 점수와 이유를 파싱합니다."""
        try:
            # 점수 추출
            score_line = None
            for line in analysis_text.split('\n'):
                if '어그로 점수:' in line or '점수:' in line:
                    score_line = line
                    break
            
            if score_line:
                # 숫자 추출
                import re
                score_match = re.search(r'(\d+)', score_line)
                if score_match:
                    score = int(score_match.group(1))
                    score = max(0, min(100, score))  # 0-100 범위로 제한
                else:
                    score = 50
            else:
                score = 50
            
            # 이유 추출
            reasoning = ""
            if '분석 이유:' in analysis_text:
                reasoning = analysis_text.split('분석 이유:')[1].strip()
            elif '이유:' in analysis_text:
                reasoning = analysis_text.split('이유:')[1].strip()
            else:
                reasoning = analysis_text.strip()
            
            return score, reasoning
            
        except Exception as e:
            logger.warning(f"Error parsing agro analysis: {e}")
            return 50, "분석 결과 파싱 중 오류 발생"
    
    def analyze_category_news(self, category_news: List[Dict]) -> List[Dict]:
        """특정 카테고리의 모든 뉴스에 대해 어그로 분석을 수행합니다."""
        analyzed_news = []
        
        for news_item in category_news:
            analyzed_item = self.analyze_news_agro(news_item)
            analyzed_news.append(analyzed_item)
            
            # API 호출 간격 조절
            import time
            time.sleep(1)
        
        # 어그로 점수 기준으로 정렬
        analyzed_news.sort(key=lambda x: x.get('agro_score', 0), reverse=True)
        
        return analyzed_news
    
    def get_top_agro_news(self, all_news: Dict[str, List[Dict]], top_n: int = 3) -> List[Dict]:
        """모든 카테고리에서 가장 어그로가 높은 뉴스를 선별합니다."""
        all_analyzed_news = []
        
        # 모든 카테고리의 뉴스를 하나의 리스트로 합치기
        for category, news_list in all_news.items():
            analyzed_list = self.analyze_category_news(news_list)
            all_analyzed_news.extend(analyzed_list)
        
        # 전체 어그로 점수 기준으로 정렬
        all_analyzed_news.sort(key=lambda x: x.get('agro_score', 0), reverse=True)
        
        # 상위 N개 반환
        return all_analyzed_news[:top_n]

if __name__ == "__main__":
    # 테스트 실행
    analyzer = AgroAnalyzer()
    
    # 샘플 뉴스 데이터로 테스트
    sample_news = {
        'title': '테스트 뉴스 제목',
        'content': '테스트 뉴스 내용입니다. 이것은 어그로 분석을 위한 샘플 데이터입니다.',
        'category': 'economy',
        'press': '테스트 언론사'
    }
    
    result = analyzer.analyze_news_agro(sample_news)
    print(f"어그로 점수: {result['agro_score']}")
    print(f"분석 이유: {result['agro_reasoning']}")
