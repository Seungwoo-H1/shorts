import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from typing import List, Dict, Optional
from config import Config
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NateNewsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_news_list(self, category: str) -> List[Dict]:
        """특정 카테고리의 뉴스 목록을 가져옵니다."""
        try:
            url = Config.CATEGORY_URLS.get(category)
            if not url:
                logger.error(f"Unknown category: {category}")
                return []
            
            logger.info(f"Crawling {category} news from: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 네이트 뉴스 랭킹 페이지의 뉴스 항목들을 파싱
            # 실제 사이트 구조에 맞게 수정
            news_links = soup.find_all('a', href=lambda x: x and '/view/' in x)
            
            for i, link_element in enumerate(news_links[:Config.MAX_NEWS_PER_CATEGORY]):
                try:
                    # 제목과 링크 추출
                    title = link_element.get_text(strip=True)
                    link = link_element.get('href')
                    
                    # 링크 정규화
                    if link and not link.startswith('http'):
                        if link.startswith('//'):
                            link = 'https:' + link
                        else:
                            link = Config.NATE_NEWS_BASE_URL + link
                    
                    # 제목에서 언론사 정보 추출 (괄호 안의 내용)
                    import re
                    press_match = re.search(r'\(([^)]+)\)', title)
                    press = press_match.group(1) if press_match else "언론사 정보 없음"
                    
                    # 제목에서 언론사 정보 제거
                    clean_title = re.sub(r'\([^)]+\)', '', title).strip()
                    
                    # 제목이 너무 짧으면 건너뛰기
                    if len(clean_title) < 10:
                        continue
                    
                    news_item = {
                        'title': clean_title,
                        'link': link,
                        'press': press,
                        'category': category,
                        'rank': i + 1,
                        'crawled_at': datetime.now().isoformat()
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.warning(f"Error parsing news item {i}: {e}")
                    continue
            
            logger.info(f"Successfully crawled {len(news_items)} news items for {category}")
            return news_items
            
        except Exception as e:
            logger.error(f"Error crawling {category} news: {e}")
            return []
    
    def get_news_content(self, news_item: Dict) -> Optional[Dict]:
        """개별 뉴스의 상세 내용을 가져옵니다."""
        try:
            if not news_item.get('link'):
                return None
            
            logger.info(f"Fetching content for: {news_item['title']}")
            response = self.session.get(news_item['link'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 본문 내용 추출 (네이트 뉴스의 실제 구조에 맞게 수정)
            content = ""
            
            # 다양한 가능한 본문 요소들 시도
            possible_content_selectors = [
                'div.articleCont',
                'div.article_body', 
                'div.article_content',
                'div#articleCont',
                'div.article',
                'div.content',
                'div[class*="article"]',
                'div[class*="content"]'
            ]
            
            for selector in possible_content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content = content_element.get_text(strip=True)
                    break
            
            # 위 방법으로 안 되면 p 태그들에서 추출
            if not content:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            
            if not content:
                content = "본문을 추출할 수 없습니다."
            
            # 요약 정보 추출
            summary_element = soup.find('meta', attrs={'name': 'description'})
            summary = summary_element.get('content', '') if summary_element else ""
            
            # 이미지 URL 추출
            img_element = soup.find('img', class_='thumb')
            image_url = img_element.get('src', '') if img_element else ""
            
            news_item.update({
                'content': content,
                'summary': summary,
                'image_url': image_url
            })
            
            # 크롤링 간격 조절
            time.sleep(1)
            
            return news_item
            
        except Exception as e:
            logger.error(f"Error fetching content for {news_item.get('title', 'Unknown')}: {e}")
            return None
    
    def crawl_all_categories(self) -> Dict[str, List[Dict]]:
        """모든 카테고리의 뉴스를 크롤링합니다."""
        all_news = {}
        
        for category in Config.CATEGORIES.keys():
            logger.info(f"Starting to crawl {category} category...")
            news_list = self.get_news_list(category)
            
            # 각 뉴스의 상세 내용 가져오기
            detailed_news = []
            for news_item in news_list:
                detailed_item = self.get_news_content(news_item)
                if detailed_item:
                    detailed_news.append(detailed_item)
            
            all_news[category] = detailed_news
            logger.info(f"Completed crawling {category}: {len(detailed_news)} items")
            
            # 카테고리 간 크롤링 간격 조절
            time.sleep(2)
        
        return all_news

if __name__ == "__main__":
    # 테스트 실행
    crawler = NateNewsCrawler()
    news = crawler.crawl_all_categories()
    
    for category, items in news.items():
        print(f"\n=== {category.upper()} ===")
        for item in items[:3]:  # 상위 3개만 출력
            print(f"제목: {item['title']}")
            print(f"언론사: {item['press']}")
            print(f"내용 길이: {len(item.get('content', ''))}자")
            print("-" * 50)

