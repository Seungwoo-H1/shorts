#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
수정된 크롤러 테스트 스크립트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_crawler():
    """수정된 크롤러를 테스트합니다."""
    print("🚀 수정된 크롤러 테스트 시작")
    print("=" * 50)
    
    try:
        from news_crawler import NateNewsCrawler
        
        crawler = NateNewsCrawler()
        
        # 경제 뉴스만 테스트 (빠른 테스트를 위해)
        print("📰 경제 뉴스 크롤링 테스트...")
        economy_news = crawler.get_news_list('economy')
        
        print(f"✅ 경제 뉴스 {len(economy_news)}개 수집")
        
        if economy_news:
            print("\n📋 수집된 뉴스:")
            for i, news in enumerate(economy_news[:3], 1):  # 처음 3개만 출력
                print(f"\n{i}. {news['title']}")
                print(f"   언론사: {news['press']}")
                print(f"   링크: {news['link']}")
                print(f"   순위: {news['rank']}")
            
            # 첫 번째 뉴스의 상세 내용 가져오기
            if economy_news:
                print(f"\n🔍 첫 번째 뉴스 상세 내용 가져오기...")
                detailed_news = crawler.get_news_content(economy_news[0])
                
                if detailed_news:
                    print(f"✅ 상세 내용 수집 성공")
                    print(f"   제목: {detailed_news['title']}")
                    print(f"   내용 길이: {len(detailed_news.get('content', ''))}자")
                    print(f"   요약: {detailed_news.get('summary', 'N/A')}")
                    print(f"   이미지: {detailed_news.get('image_url', 'N/A')}")
                else:
                    print("❌ 상세 내용 수집 실패")
        
        print("\n✅ 크롤러 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crawler()
