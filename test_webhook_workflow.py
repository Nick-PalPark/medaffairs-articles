#!/usr/bin/env python3
"""
Test script for the webhook article processing workflow.
Run this to validate the workflow logic without triggering GitHub Actions.
"""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

def process_article_workflow(article_data, articles_file_path):
    """
    Simulate the exact workflow logic from process-article.yml
    """
    try:
        # Validate required fields
        required_fields = ['title', 'url']
        for field in required_fields:
            if not article_data.get(field):
                print(f"❌ Missing required field: {field}")
                return False
        
        # Load existing articles
        articles_file = Path(articles_file_path)
        if articles_file.exists():
            try:
                with open(articles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    articles = data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error loading existing articles: {e}")
                articles = []
        else:
            articles = []
        
        # Check if article already exists (by URL)
        existing_urls = {article.get('url') for article in articles}
        if article_data['url'] in existing_urls:
            print(f"❌ Article already exists: {article_data['url']}")
            return False
        
        # Create new article with required structure
        new_article = {
            'title': article_data.get('title', ''),
            'snappy_title': article_data.get('snappy_title', ''),
            'url': article_data.get('url', ''),
            'author': article_data.get('author', 'Unknown'),
            'date': article_data.get('date', datetime.now(timezone.utc).isoformat()),
            'category': article_data.get('category', 'general'),
            'cover_image': article_data.get('cover_image', ''),
            'processed_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Add new article to the beginning of the array (most recent first)
        articles.insert(0, new_article)
        
        # Save updated articles
        try:
            # Ensure parent directory exists
            articles_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            print(f"✅ Successfully added new article: {new_article['title']}")
            print(f"📊 Total articles: {len(articles)}")
            return True
        except IOError as e:
            print(f"❌ Error saving articles: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_tests():
    """Run comprehensive tests of the workflow"""
    print("🧪 Testing Webhook Article Processing Workflow")
    print("=" * 50)
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        articles_file = Path(temp_dir) / "_data" / "articles.json"
        
        test_cases = [
            {
                "name": "Complete article with all fields",
                "data": {
                    "title": "Revolutionary AI Medical Diagnosis Tool",
                    "snappy_title": "AI Diagnoses Disease in Seconds!",
                    "url": "https://example.com/ai-medical-tool",
                    "author": "Dr. Jane Smith",
                    "date": "2024-01-15T10:30:00Z",
                    "category": "technology",
                    "cover_image": "https://example.com/images/ai-tool.jpg"
                },
                "should_succeed": True
            },
            {
                "name": "Minimal article (only required fields)",
                "data": {
                    "title": "New Cancer Treatment Shows Promise",
                    "url": "https://example.com/cancer-treatment"
                },
                "should_succeed": True
            },
            {
                "name": "Article missing title",
                "data": {
                    "url": "https://example.com/no-title",
                    "author": "Test Author"
                },
                "should_succeed": False
            },
            {
                "name": "Article missing URL",
                "data": {
                    "title": "Article Without URL",
                    "author": "Test Author"
                },
                "should_succeed": False
            },
            {
                "name": "Duplicate URL",
                "data": {
                    "title": "Duplicate Article",
                    "url": "https://example.com/ai-medical-tool",  # Same as first test
                    "author": "Different Author"
                },
                "should_succeed": False
            }
        ]
        
        passed = 0
        total = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}: {test_case['name']}")
            print("-" * 40)
            
            success = process_article_workflow(test_case['data'], str(articles_file))
            
            if success == test_case['should_succeed']:
                print(f"✅ Test passed")
                passed += 1
            else:
                expected = "succeed" if test_case['should_succeed'] else "fail"
                actual = "succeeded" if success else "failed"
                print(f"❌ Test failed: Expected to {expected}, but {actual}")
        
        # Final verification
        print(f"\n📋 Final Verification")
        print("-" * 40)
        
        if articles_file.exists():
            with open(articles_file, 'r') as f:
                final_articles = json.load(f)
            
            print(f"📄 Final article count: {len(final_articles)}")
            print(f"🔗 Articles in order:")
            for i, article in enumerate(final_articles):
                print(f"  {i+1}. {article['title']} ({article['url']})")
            
            # Verify structure
            all_valid = True
            required_fields = ['title', 'snappy_title', 'url', 'author', 'date', 'category', 'cover_image', 'processed_at']
            
            for article in final_articles:
                for field in required_fields:
                    if field not in article:
                        print(f"❌ Missing field '{field}' in article: {article.get('title', 'Unknown')}")
                        all_valid = False
            
            if all_valid:
                print("✅ All articles have required fields")
                passed += 1
                total += 1
        
        print(f"\n🎯 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The workflow is ready for use.")
            return True
        else:
            print("❌ Some tests failed. Please review the workflow logic.")
            return False

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)