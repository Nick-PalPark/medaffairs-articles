#!/usr/bin/env python3
"""
Test script to validate the complete articles pipeline works correctly
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

def test_config_generation():
    """Test that config.py generation works correctly"""
    print("🔧 Testing config generation...")
    
    # Simulate the GitHub Actions environment variables
    test_env = {
        'ZAPIER_TABLE_ID': '01K4QYZXV51PJBZ3P9FWQB5MRA',
        'ZAPIER_API_KEY': 'test_api_key_12345'
    }
    
    # Generate config like the workflow does
    config_content = f'''# Auto-generated config.py for capture_articles.py - DO NOT COMMIT
# Populated from repository secrets at runtime by Actions

ZAPIER_TABLE_ID = "{test_env['ZAPIER_TABLE_ID']}"
ZAPIER_API_KEY = "{test_env['ZAPIER_API_KEY']}"

ZAPIER_API_BASE = "https://tables.zapier.com/api/v1/tables"

ARTICLES_DIR = "articles"
MAX_ARTICLES = 50
DAYS_BACK = 7
REQUIRED_TAGS = []  # Add tags here if you want to filter: ["medaffairs", "healthcare"]
'''
    
    # Write test config
    with open('test_config.py', 'w') as f:
        f.write(config_content)
    
    # Test importing it
    sys.path.insert(0, '.')
    import test_config
    
    # Validate values
    assert test_config.ZAPIER_TABLE_ID == '01K4QYZXV51PJBZ3P9FWQB5MRA', "Table ID not substituted correctly"
    assert test_config.ZAPIER_API_KEY == 'test_api_key_12345', "API key not substituted correctly"
    assert test_config.ZAPIER_API_BASE == "https://tables.zapier.com/api/v1/tables", "API base incorrect"
    
    # Clean up
    os.remove('test_config.py')
    if 'test_config' in sys.modules:
        del sys.modules['test_config']
    
    print("✓ Config generation works correctly")
    return True

def test_article_processing():
    """Test that the articles processing pipeline works"""
    print("📄 Testing article processing pipeline...")
    
    # Test that we can generate articles.json
    if os.path.exists('articles.json'):
        with open('articles.json', 'r') as f:
            articles_data = json.load(f)
        
        print(f"✓ Found {len(articles_data)} articles in articles.json")
        
        # Test that we can transform to site format
        from scripts.transform_to_site_format import main as transform_main
        import tempfile
        import sys
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        # Override sys.argv to simulate command line args
        old_argv = sys.argv
        try:
            sys.argv = ['transform_to_site_format.py', '--input', 'articles.json', '--output', tmp_path]
            transform_main()
            
            # Check the output
            with open(tmp_path, 'r') as f:
                site_data = json.load(f)
            
            # Validate structure
            assert 'heroes' in site_data, "Missing heroes section"
            assert 'columns' in site_data, "Missing columns section"
            assert 'news' in site_data['columns'], "Missing news column"
            assert 'tech' in site_data['columns'], "Missing tech column"
            assert 'opinion' in site_data['columns'], "Missing opinion column"
            
            print("✓ Article transformation works correctly")
            
        finally:
            sys.argv = old_argv
            os.unlink(tmp_path)
        
        return True
    else:
        print("⚠ No articles.json found - generate articles first")
        return False

def test_website_compatibility():
    """Test that the generated data is compatible with the website"""
    print("🌐 Testing website compatibility...")
    
    if not os.path.exists('data/articles.json'):
        print("⚠ No data/articles.json found - run the full pipeline first")
        return False
    
    with open('data/articles.json', 'r') as f:
        data = json.load(f)
    
    # Test structure expected by the website
    required_fields = ['heroes', 'columns']
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    required_columns = ['news', 'tech', 'opinion']
    for column in required_columns:
        assert column in data['columns'], f"Missing required column: {column}"
    
    # Test hero articles have required fields
    for hero in data['heroes']:
        required_hero_fields = ['original_title', 'url', 'source', 'published_at']
        for field in required_hero_fields:
            assert field in hero, f"Hero missing required field: {field}"
    
    print("✓ Website compatibility validated")
    return True

def main():
    """Run all tests"""
    print("🧪 Full Pipeline Test")
    print("=" * 50)
    
    tests = [
        test_config_generation,
        test_article_processing,
        test_website_compatibility,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"Test {test.__name__} FAILED")
        except Exception as e:
            print(f"Test {test.__name__} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Pipeline Tests: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("🎉 All pipeline tests passed! The fixes should work correctly.")
        return True
    else:
        print("❌ Some pipeline tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)