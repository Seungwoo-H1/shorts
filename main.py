#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이트 뉴스 어그로 분석 및 요약 시스템 메인 실행 파일
"""

import logging
import json
from datetime import datetime
from typing import Dict, List
from config import Config
from utils.news_crawler import NateNewsCrawler
from utils.agro_analyzer import AgroAnalyzer
from utils.news_summarizer import NewsSummarizer

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nate_news_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NateNewsAnalysisSystem:
    def __init__(self):
        self.crawler = NateNewsCrawler()
        self.analyzer = AgroAnalyzer()
        self.summarizer = NewsSummarizer()
        
    def run_full_analysis(self) -> Dict:
        """전체 분석 프로세스를 실행합니다."""
        logger.info("=== 네이트 뉴스 어그로 분석 시스템 시작 ===")
        
        try:
            # 1단계: 뉴스 크롤링
            logger.info("1단계: 네이트 뉴스 크롤링 시작...")
            all_news = self.crawler.crawl_all_categories()
            
            if not all_news:
                logger.error("뉴스 크롤링에 실패했습니다.")
                return {}
            
            total_news = sum(len(news_list) for news_list in all_news.values())
            logger.info(f"총 {total_news}개의 뉴스를 수집했습니다.")
            
            # 2단계: 어그로 분석
            logger.info("2단계: 어그로 분석 시작...")
            top_agro_news = self.analyzer.get_top_agro_news(all_news, top_n=3)
            
            if not top_agro_news:
                logger.error("어그로 분석에 실패했습니다.")
                return {}
            
            logger.info(f"상위 {len(top_agro_news)}개의 어그로 뉴스를 선별했습니다.")
            
            # 3단계: 요약 생성
            logger.info("3단계: 숏츠 요약 생성 시작...")
            summarized_news = self.summarizer.create_summaries_for_top_news(top_agro_news)
            
            if not summarized_news:
                logger.error("요약 생성에 실패했습니다.")
                return {}
            
            logger.info(f"총 {len(summarized_news)}개의 요약을 생성했습니다.")
            
            # 결과 정리
            result = {
                'analysis_timestamp': Config.get_current_time(),
                'total_news_crawled': total_news,
                'top_agro_news': summarized_news,
                'categories_analyzed': list(all_news.keys())
            }
            
            # 결과 저장
            self._save_results(result)
            
            logger.info("=== 분석 완료 ===")
            return result
            
        except Exception as e:
            logger.error(f"전체 분석 중 오류 발생: {e}")
            return {}
    
    def _save_results(self, results: Dict):
        """분석 결과를 파일로 저장합니다."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nate_news_analysis_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"결과가 {filename}에 저장되었습니다.")
            
        except Exception as e:
            logger.error(f"결과 저장 중 오류 발생: {e}")
    
    def display_results(self, results: Dict):
        """분석 결과를 콘솔에 출력합니다."""
        if not results:
            print("분석 결과가 없습니다.")
            return
        
        print("\n" + "="*80)
        print("🔥 네이트 뉴스 어그로 분석 결과 🔥")
        print("="*80)
        
        print(f"📅 분석 시간: {results.get('analysis_timestamp', 'N/A')}")
        print(f"📊 총 수집 뉴스: {results.get('total_news_crawled', 0)}개")
        print(f"🏆 선별된 뉴스: {len(results.get('top_agro_news', []))}개")
        
        print("\n" + "🏆 TOP 어그로 뉴스 요약 🏆")
        print("-"*80)
        
        for i, news in enumerate(results.get('top_agro_news', []), 1):
            print(f"\n🥇 {i}위 (어그로 점수: {news.get('agro_score', 0)}점)")
            print(f"📰 제목: {news.get('title', 'N/A')}")
            print(f"📺 언론사: {news.get('press', 'N/A')}")
            print(f"🏷️ 카테고리: {Config.CATEGORIES.get(news.get('category', ''), 'N/A')}")
            print(f"📝 요약: {news.get('short_summary', 'N/A')}")
            print(f"⏱️ 예상 시청 시간: {news.get('estimated_duration', 60)}초")
            
            if news.get('key_points'):
                print("💡 핵심 포인트:")
                for point in news['key_points']:
                    print(f"   • {point}")
            
            print("-"*80)
    
    def run_interactive_mode(self):
        """대화형 모드로 실행합니다."""
        print("=== 네이트 뉴스 어그로 분석 시스템 ===")
        print("1. 전체 분석 실행")
        print("2. 뉴스 크롤링만 실행")
        print("3. 기존 데이터로 어그로 분석")
        print("4. 종료")
        
        while True:
            try:
                choice = input("\n선택하세요 (1-4): ").strip()
                
                if choice == '1':
                    print("\n전체 분석을 시작합니다...")
                    results = self.run_full_analysis()
                    self.display_results(results)
                    
                elif choice == '2':
                    print("\n뉴스 크롤링을 시작합니다...")
                    all_news = self.crawler.crawl_all_categories()
                    if all_news:
                        total = sum(len(news_list) for news_list in all_news.values())
                        print(f"총 {total}개의 뉴스를 수집했습니다.")
                    
                elif choice == '3':
                    print("\n기존 데이터로 어그로 분석을 실행합니다...")
                    # 여기에 기존 데이터 로드 로직 추가 가능
                    print("기능 준비 중...")
                    
                elif choice == '4':
                    print("시스템을 종료합니다.")
                    break
                    
                else:
                    print("잘못된 선택입니다. 1-4 중에서 선택해주세요.")
                    
            except KeyboardInterrupt:
                print("\n\n시스템을 종료합니다.")
                break
            except Exception as e:
                print(f"오류 발생: {e}")

def main():
    """메인 실행 함수"""
    try:
        system = NateNewsAnalysisSystem()
        
        # 명령행 인수 확인
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            system.run_interactive_mode()
        else:
            # 기본 실행: 전체 분석
            results = system.run_full_analysis()
            system.display_results(results)
            
    except Exception as e:
        logger.error(f"메인 실행 중 오류 발생: {e}")
        print(f"시스템 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
