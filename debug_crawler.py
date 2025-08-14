#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이트 뉴스 크롤링 디버깅 스크립트
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_nate_news():
    """네이트 뉴스 사이트 구조를 디버깅합니다."""
    
    # 테스트할 URL들
    test_urls = [
        "https://news.nate.com/rank/interest?sc=eco",
        "https://news.nate.com/rank/interest?sc=spo", 
        "https://news.nate.com/rank/interest?sc=ent",
        "https://news.nate.com/rank/interest",  # 전체 랭킹
        "https://news.nate.com"  # 메인 페이지
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'='*60}")
        print(f"🔍 테스트 {i}: {url}")
        print(f"{'='*60}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            print(f"✅ 응답 상태: {response.status_code}")
            print(f"📄 응답 길이: {len(response.content)} bytes")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 페이지 제목 확인
            title = soup.find('title')
            if title:
                print(f"📰 페이지 제목: {title.get_text()}")
            
            # 가능한 뉴스 요소들 찾기
            print("\n🔍 뉴스 요소 검색:")
            
            # 다양한 클래스명으로 뉴스 요소 찾기
            possible_selectors = [
                'div.mduSubject',
                'div.newsSubject', 
                'div.subject',
                'div.news_item',
                'div.article',
                'a[href*="/view/"]',
                'a[href*="/article/"]',
                'div[class*="news"]',
                'div[class*="article"]',
                'div[class*="subject"]'
            ]
            
            for selector in possible_selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"✅ {selector}: {len(elements)}개 발견")
                    if len(elements) <= 3:  # 처음 3개만 출력
                        for j, elem in enumerate(elements[:3]):
                            text = elem.get_text(strip=True)[:100]
                            print(f"   {j+1}. {text}...")
                else:
                    print(f"❌ {selector}: 없음")
            
            # 링크들 확인
            print(f"\n🔗 링크 분석:")
            links = soup.find_all('a', href=True)
            news_links = [link for link in links if '/view/' in link['href'] or '/article/' in link['href']]
            print(f"뉴스 링크: {len(news_links)}개")
            
            if news_links:
                for j, link in enumerate(news_links[:3]):
                    href = link.get('href')
                    text = link.get_text(strip=True)[:50]
                    print(f"   {j+1}. {text} -> {href}")
            
            # HTML 구조 일부 출력
            print(f"\n📋 HTML 구조 (처음 1000자):")
            print(response.text[:1000])
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print(f"\n{'='*60}")

if __name__ == "__main__":
    debug_nate_news()
