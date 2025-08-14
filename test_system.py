#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이트 뉴스 어그로 분석 시스템 테스트 스크립트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """모든 모듈이 정상적으로 import되는지 테스트합니다."""
    print("=== 모듈 Import 테스트 ===")
    
    try:
        from config import Config
        print("✅ config.py - 성공")
    except Exception as e:
        print(f"❌ config.py - 실패: {e}")
        return False
    
    try:
        from news_crawler import NateNewsCrawler
        print("✅ news_crawler.py - 성공")
    except Exception as e:
        print(f"❌ news_crawler.py - 실패: {e}")
        return False
    
    try:
        from agro_analyzer import AgroAnalyzer
        print("✅ agro_analyzer.py - 성공")
    except Exception as e:
        print(f"❌ agro_analyzer.py - 실패: {e}")
        return False
    
    try:
        from news_summarizer import NewsSummarizer
        print("✅ news_summarizer.py - 성공")
    except Exception as e:
        print(f"❌ news_summarizer.py - 실패: {e}")
        return False
    
    try:
        from main import NateNewsAnalysisSystem
        print("✅ main.py - 성공")
    except Exception as e:
        print(f"❌ main.py - 실패: {e}")
        return False
    
    return True

def test_config():
    """설정 파일이 정상적으로 작동하는지 테스트합니다."""
    print("\n=== 설정 파일 테스트 ===")
    
    try:
        from config import Config
        
        print(f"카테고리 수: {len(Config.CATEGORIES)}")
        print(f"카테고리: {list(Config.CATEGORIES.keys())}")
        print(f"LLM 타입: {Config.LLM_TYPE}")
        print(f"최대 뉴스 수: {Config.MAX_NEWS_PER_CATEGORY}")
        
        if Config.LLM_TYPE == 'ollama':
            print(f"Ollama 모델: {Config.OLLAMA_MODEL}")
            print(f"Ollama URL: {Config.OLLAMA_BASE_URL}")
        elif Config.LLM_TYPE == 'huggingface':
            print(f"HF 모델: {Config.HF_MODEL}")
        
        print("✅ 설정 파일 테스트 - 성공")
        return True
        
    except Exception as e:
        print(f"❌ 설정 파일 테스트 - 실패: {e}")
        return False

def test_crawler():
    """크롤러가 정상적으로 초기화되는지 테스트합니다."""
    print("\n=== 크롤러 테스트 ===")
    
    try:
        from news_crawler import NateNewsCrawler
        
        crawler = NateNewsCrawler()
        print(f"크롤러 세션 헤더: {crawler.session.headers.get('User-Agent', 'N/A')[:50]}...")
        
        print("✅ 크롤러 테스트 - 성공")
        return True
        
    except Exception as e:
        print(f"❌ 크롤러 테스트 - 실패: {e}")
        return False

def test_analyzer():
    """어그로 분석기가 정상적으로 초기화되는지 테스트합니다."""
    print("\n=== 어그로 분석기 테스트 ===")
    
    try:
        from agro_analyzer import AgroAnalyzer
        
        analyzer = AgroAnalyzer()
        print(f"LLM 타입: {analyzer.llm_type}")
        print(f"최대 토큰: {analyzer.max_tokens}")
        
        if analyzer.llm_type == 'ollama':
            print(f"Ollama 모델: {analyzer.ollama_model}")
            print(f"Ollama URL: {analyzer.ollama_url}")
        
        print("✅ 어그로 분석기 테스트 - 성공")
        return True
        
    except Exception as e:
        print(f"❌ 어그로 분석기 테스트 - 실패: {e}")
        return False

def test_summarizer():
    """요약기가 정상적으로 초기화되는지 테스트합니다."""
    print("\n=== 요약기 테스트 ===")
    
    try:
        from news_summarizer import NewsSummarizer
        
        summarizer = NewsSummarizer()
        print(f"LLM 타입: {summarizer.llm_type}")
        print(f"온도: {summarizer.temperature}")
        
        if summarizer.llm_type == 'ollama':
            print(f"Ollama 모델: {summarizer.ollama_model}")
            print(f"Ollama URL: {summarizer.ollama_url}")
        
        print("✅ 요약기 테스트 - 성공")
        return True
        
    except Exception as e:
        print(f"❌ 요약기 테스트 - 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 네이트 뉴스 어그로 분석 시스템 테스트 시작")
    print("=" * 60)
    
    # LLM 설정 확인
    from config import Config
    print(f"\n🔧 LLM 설정: {Config.LLM_TYPE}")
    if Config.LLM_TYPE == 'ollama':
        print(f"Ollama 모델: {Config.OLLAMA_MODEL}")
        print(f"Ollama URL: {Config.OLLAMA_BASE_URL}")
        print("⚠️  Ollama가 로컬에서 실행 중인지 확인하세요.")
    elif Config.LLM_TYPE == 'huggingface':
        print(f"Hugging Face 모델: {Config.HF_MODEL}")
    else:
        print("규칙 기반 분석 모드를 사용합니다.")
    print()
    
    # 각 테스트 실행
    tests = [
        test_imports,
        test_config,
        test_crawler,
        test_analyzer,
        test_summarizer
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 통과했습니다! 시스템이 정상적으로 작동합니다.")
        print("\n📋 다음 단계:")
        print("1. python demo.py로 데모를 실행해보세요")
        print("2. python main.py로 시스템을 실행하세요")
        print("3. python main.py --interactive로 대화형 모드를 실행하세요")
    else:
        print("❌ 일부 테스트가 실패했습니다. 오류를 확인하고 수정해주세요.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
