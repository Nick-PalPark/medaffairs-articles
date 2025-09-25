#!/usr/bin/env python3
"""
Test script for validating Zapier Table API connection and configuration.
Use this to verify your setup before running the main workflow.
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_config():
    """Test if config is properly set up"""
    print("🔧 Testing configuration...")
    
    try:
        import config
        print("✓ config.py found")
    except ImportError:
        print("✗ config.py not found. Copy config_template.py to config.py first.")
        return False

    # Check required settings
    required_settings = ['ZAPIER_TABLE_ID', 'ZAPIER_API_KEY', 'ZAPIER_API_BASE']
    missing = []
    
    for setting in required_settings:
        if not hasattr(config, setting):
            missing.append(setting)
        elif getattr(config, setting) == "your_zapier_api_key_here":
            missing.append(f"{setting} (still has template value)")
    
    if missing:
        print(f"✗ Missing or incomplete settings: {', '.join(missing)}")
        return False
    
    print(f"✓ Table ID: {config.ZAPIER_TABLE_ID}")
    print(f"✓ API Base: {config.ZAPIER_API_BASE}")
    print(f"✓ API Key: {'*' * (len(config.ZAPIER_API_KEY) - 4) + config.ZAPIER_API_KEY[-4:] if len(config.ZAPIER_API_KEY) > 4 else '***'}")
    
    if hasattr(config, 'REQUIRED_TAGS') and config.REQUIRED_TAGS:
        print(f"✓ Tag filtering enabled: {config.REQUIRED_TAGS}")
    else:
        print("ℹ Tag filtering disabled (will fetch all articles)")
    
    return True

def test_api_connection():
    """Test API connection to Zapier Tables"""
    print("\n🌐 Testing API connection...")
    
    import config
    
    # Set up session
    session = requests.Session()
    if config.ZAPIER_API_KEY and config.ZAPIER_API_KEY != "your_zapier_api_key_here":
        session.headers.update({
            'Authorization': f'Bearer {config.ZAPIER_API_KEY}',
            'Content-Type': 'application/json'
        })
    
    # Test endpoints
    endpoints = [
        f"{config.ZAPIER_API_BASE}/{config.ZAPIER_TABLE_ID}/records",
        f"{config.ZAPIER_API_BASE}/{config.ZAPIER_TABLE_ID}/rows",
        f"https://tables.zapier.com/api/v1/tables/{config.ZAPIER_TABLE_ID}/records",
        f"https://api.zapier.com/v1/tables/{config.ZAPIER_TABLE_ID}/records"
    ]
    
    params = {'limit': 1}  # Just fetch 1 record for testing
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"  Testing endpoint {i}/{len(endpoints)}: {endpoint}")
        try:
            response = session.get(endpoint, params=params, timeout=10)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"    ✓ Success! Response type: {type(data)}")
                    
                    # Try to extract articles
                    articles = []
                    if isinstance(data, list):
                        articles = data
                    elif 'records' in data:
                        articles = data['records']
                    elif 'data' in data:
                        articles = data['data']
                    elif 'rows' in data:
                        articles = data['rows']
                    
                    print(f"    ✓ Found {len(articles)} articles")
                    
                    if articles:
                        first_article = articles[0]
                        print(f"    ✓ Sample article keys: {list(first_article.keys())}")
                        
                        # Check for common fields
                        common_fields = ['id', 'title', 'url', 'content', 'tags', 'created_at', 'published']
                        found_fields = [field for field in common_fields if field in first_article]
                        if found_fields:
                            print(f"    ✓ Common fields found: {found_fields}")
                        
                        # Check tag filtering compatibility
                        if 'tags' in first_article:
                            tags = first_article['tags']
                            print(f"    ✓ Tags field format: {type(tags)} - {tags}")
                        else:
                            print("    ⚠ No 'tags' field found - tag filtering may not work")
                    
                    return True, endpoint, data
                    
                except json.JSONDecodeError:
                    print(f"    ✗ Invalid JSON response")
                    
            elif response.status_code == 401:
                print(f"    ✗ Authentication failed - check your API key")
            elif response.status_code == 403:
                print(f"    ✗ Access forbidden - check permissions")
            elif response.status_code == 404:
                print(f"    ✗ Table not found - check table ID")
            else:
                print(f"    ✗ Unexpected status code")
                
        except requests.exceptions.Timeout:
            print(f"    ✗ Request timeout")
        except requests.exceptions.ConnectionError as e:
            print(f"    ✗ Connection error: {e}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print("  ✗ All endpoints failed")
    return False, None, None

def test_article_processing():
    """Test article processing pipeline"""
    print("\n📄 Testing article processing...")
    
    # Sample article data to test processing
    sample_article = {
        'id': 'test-article-1',
        'title': 'Test Medical Article',
        'url': 'https://example.com/test-article',
        'content': '<p>This is a <strong>test</strong> article with <em>HTML</em> content.</p>',
        'source': 'Test Medical Journal',
        'author': 'Dr. Test',
        'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tags': ['medical', 'test']
    }
    
    try:
        from capture_articles import ArticleProcessor
        processor = ArticleProcessor()
        
        # Test filename generation
        filename = processor.generate_filename(sample_article['title'], sample_article['published'])
        print(f"✓ Generated filename: {filename}")
        
        # Test HTML cleaning
        clean_content = processor.clean_html_content(sample_article['content'])
        print(f"✓ Cleaned content: {clean_content[:50]}...")
        
        print("✓ Article processing works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Article processing failed: {e}")
        return False

def test_github_secrets():
    """Check if GitHub secrets would be properly configured"""
    print("\n🔐 Checking GitHub environment compatibility...")
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print("✓ Running in GitHub Actions environment")
        
        # Check if secrets would be available
        table_id = os.getenv('ZAPIER_TABLE_ID')
        api_key = os.getenv('ZAPIER_API_KEY')
        
        if table_id and api_key:
            print("✓ Zapier secrets are available")
            print(f"  Table ID: {table_id}")
            print(f"  API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '***'}")
        else:
            print("⚠ Zapier secrets not found - ensure they are configured in repository settings")
        
        medaffairs_pat = os.getenv('MEDAFFAIRS_TECH_PAT')
        if medaffairs_pat:
            print("✓ MedAffairs PAT is available")
        else:
            print("⚠ MEDAFFAIRS_TECH_PAT secret not found - website updates may not work")
            
    else:
        print("ℹ Not running in GitHub Actions - secrets check skipped")
        print("  Make sure to configure these secrets in GitHub repository settings:")
        print("  - ZAPIER_TABLE_ID")
        print("  - ZAPIER_API_KEY") 
        print("  - MEDAFFAIRS_TECH_PAT (optional)")

def main():
    """Run all tests"""
    print("🧪 Zapier Table Connection Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Configuration
    if test_config():
        tests_passed += 1
    
    # Test 2: API Connection
    success, endpoint, data = test_api_connection()
    if success:
        tests_passed += 1
    
    # Test 3: Article Processing
    if test_article_processing():
        tests_passed += 1
    
    # Test 4: GitHub Environment
    test_github_secrets()
    tests_passed += 1  # This test is informational only
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your setup should work correctly.")
    elif tests_passed >= 2:
        print("⚠ Some tests failed, but basic functionality should work.")
        print("  Check the failed tests above and refer to SETUP_ZAPIER_ACCESS.md")
    else:
        print("❌ Multiple tests failed. Please review your configuration.")
        print("  See SETUP_ZAPIER_ACCESS.md for setup instructions.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)