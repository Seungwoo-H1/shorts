#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이트 뉴스 어그로 분석 시스템 데모 스크립트
무료 버전으로 테스트해볼 수 있습니다.
"""

import sys
import os
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_rule_based_analysis():
    """규칙 기반 분석 데모를 실행합니다."""
    print("🚀 규칙 기반 분석 데모 시작")
    print("=" * 50)
    
    try:
        from config import Config
        from agro_analyzer import AgroAnalyzer
        from news_summarizer import NewsSummarizer
        
        # 설정을 규칙 기반으로 변경
        Config.LLM_TYPE = 'rule_based'
        
        # 샘플 뉴스 데이터
        sample_news = [
            {
                'title': '삼성전자, AI 반도체 시장 진출 선언',
                'content': '삼성전자가 AI 반도체 시장에 본격 진출한다고 발표했습니다. 이는 반도체 업계에 큰 변화를 가져올 것으로 예상됩니다.',
                'category': 'economy',
                'press': '경제일보',
                'link': 'https://example.com/news1'
            },
            {
                'title': '손흥민, 프리미어리그 득점왕 등극',
                'content': '손흥민이 프리미어리그에서 득점왕에 등극했습니다. 아시아 선수 최초의 기록입니다.',
                'category': 'sports',
                'press': '스포츠뉴스',
                'link': 'https://example.com/news2'
            },
            {
                'title': 'BTS 지민, 솔로 앨범 발매 예정',
                'content': 'BTS 지민이 솔로 앨범을 발매할 예정입니다. 팬들의 기대가 높아지고 있습니다.',
                'category': 'entertainment',
                'press': '연예뉴스',
                'link': 'https://example.com/news3'
            }
        ]
        
        print("📰 샘플 뉴스 데이터:")
        for i, news in enumerate(sample_news, 1):
            print(f"{i}. {news['title']} ({news['category']})")
        print()
        
        # 어그로 분석
        print("🔍 어그로 분석 시작...")
        analyzer = AgroAnalyzer()
        
        analyzed_news = []
        for news in sample_news:
            analyzed_item = analyzer.analyze_news_agro(news)
            analyzed_news.append(analyzed_item)
            print(f"제목: {analyzed_item['title']}")
            print(f"어그로 점수: {analyzed_item['agro_score']}점")
            print(f"분석 이유: {analyzed_item['agro_reasoning']}")
            print("-" * 40)
        
        # 상위 어그로 뉴스 선별
        top_news = sorted(analyzed_news, key=lambda x: x.get('agro_score', 0), reverse=True)
        print(f"\n🏆 TOP 어그로 뉴스: {top_news[0]['title']}")
        
        # 요약 생성
        print("\n📝 요약 생성 시작...")
        summarizer = NewsSummarizer()
        
        for i, news in enumerate(top_news[:2], 1):
            print(f"\n{i}위 뉴스 요약:")
            summarized_item = summarizer.create_short_summary(news)
            print(f"제목: {summarized_item['title']}")
            print(f"요약: {summarized_item['short_summary']}")
            print(f"핵심 포인트: {summarized_item['key_points']}")
            print(f"예상 시간: {summarized_item['estimated_duration']}초")
            print("-" * 40)
        
        print("\n✅ 규칙 기반 분석 데모 완료!")
        
    except Exception as e:
        print(f"❌ 데모 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

def demo_ollama_setup():
    """Ollama 설정 가이드를 보여줍니다."""
    print("🦙 Ollama 설정 가이드")
    print("=" * 50)
    print("1. Ollama 설치:")
    print("   - https://ollama.ai/download 에서 다운로드")
    print("   - 설치 후 터미널에서 'ollama serve' 실행")
    print()
    print("2. 모델 다운로드:")
    print("   ollama pull llama2")
    print("   ollama pull mistral")
    print()
    print("3. 환경 변수 설정 (.env 파일):")
    print("   LLM_TYPE=ollama")
    print("   OLLAMA_MODEL=llama2")
    print("   OLLAMA_BASE_URL=http://localhost:11434")
    print()
    print("4. 테스트:")
    print("   python test_system.py")

def main():
    """메인 데모 함수"""
    print("🎯 네이트 뉴스 어그로 분석 시스템 데모")
    print("=" * 60)
    print("1. 규칙 기반 분석 데모 (무료)")
    print("2. Ollama 설정 가이드")
    print("3. 종료")
    
    while True:
        try:
            choice = input("\n선택하세요 (1-3): ").strip()
            
            if choice == '1':
                demo_rule_based_analysis()
                break
            elif choice == '2':
                demo_ollama_setup()
                break
            elif choice == '3':
                print("데모를 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 1-3 중에서 선택해주세요.")
                
        except KeyboardInterrupt:
            print("\n\n데모를 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
