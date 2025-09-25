#!/usr/bin/env python3
"""
Validation script to help repository owner verify their Zapier setup is correct.
Run this to check if all requirements are met for Zapier data collection.
"""

import os
import sys
import requests
import json
import subprocess
import tempfile

def check_github_secrets():
    """Check if running in GitHub Actions with proper secrets"""
    print("🔐 Checking GitHub Actions environment...")
    
    if not os.getenv('GITHUB_ACTIONS'):
        print("❌ Not running in GitHub Actions environment")
        print("   This script should be run as part of a GitHub Actions workflow")
        return False
    
    table_id = os.getenv('ZAPIER_TABLE_ID')
    api_key = os.getenv('ZAPIER_API_KEY')
    
    if not table_id:
        print("❌ ZAPIER_TABLE_ID secret not configured")
        return False
    
    if not api_key or api_key == "your_zapier_api_key_here":
        print("❌ ZAPIER_API_KEY secret not configured or still has template value")
        return False
    
    print("✅ GitHub secrets properly configured")
    print(f"   Table ID: {table_id}")
    print(f"   API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '***'}")
    
    return True

def validate_config_generation():
    """Test that config.py is generated correctly"""
    print("\n🔧 Validating config.py generation...")
    
    if not os.path.exists('config.py'):
        print("❌ config.py not found - workflow should generate this file")
        return False
    
    try:
        import config
        
        # Check required attributes
        required_attrs = ['ZAPIER_TABLE_ID', 'ZAPIER_API_KEY', 'ZAPIER_API_BASE']
        for attr in required_attrs:
            if not hasattr(config, attr):
                print(f"❌ config.py missing required attribute: {attr}")
                return False
        
        # Check for template values
        if config.ZAPIER_TABLE_ID == '$ZAPIER_TABLE_ID':
            print("❌ config.py still contains template value for ZAPIER_TABLE_ID")
            print("   This indicates the GitHub workflow variable substitution failed")
            return False
        
        if config.ZAPIER_API_KEY == '$ZAPIER_API_KEY':
            print("❌ config.py still contains template value for ZAPIER_API_KEY")
            print("   This indicates the GitHub workflow variable substitution failed")
            return False
        
        print("✅ config.py generated correctly")
        print(f"   Table ID: {config.ZAPIER_TABLE_ID}")
        print(f"   API Base: {config.ZAPIER_API_BASE}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import config.py: {e}")
        return False

def test_zapier_api_connection():
    """Test actual connection to Zapier API"""
    print("\n🌐 Testing Zapier API connection...")
    
    try:
        import config
    except ImportError:
        print("❌ Cannot import config - skipping API test")
        return False
    
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {config.ZAPIER_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Test the primary endpoint
    endpoint = f"https://tables.zapier.com/api/v1/tables/{config.ZAPIER_TABLE_ID}/records"
    
    try:
        response = session.get(endpoint, params={'limit': 1}, timeout=30)
        
        print(f"   Endpoint: {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Zapier API connection successful!")
            try:
                data = response.json()
                if isinstance(data, dict) and ('records' in data or 'data' in data):
                    record_count = len(data.get('records', data.get('data', [])))
                    print(f"   Found {record_count} records in response")
                elif isinstance(data, list):
                    print(f"   Found {len(data)} records in response")
                else:
                    print("   Response format not recognized - may need endpoint adjustment")
            except json.JSONDecodeError:
                print("   Response is not valid JSON")
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed - check API key")
            print("   Make sure your ZAPIER_API_KEY secret is valid")
            
        elif response.status_code == 403:
            print("❌ Access forbidden - check API key permissions")
            print("   Your API key may not have access to this table")
            
        elif response.status_code == 404:
            print("❌ Table not found - check table ID")
            print("   Make sure your ZAPIER_TABLE_ID is correct")
            
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
        
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_full_workflow():
    """Test the complete article capture workflow"""
    print("\n📄 Testing complete workflow...")
    
    try:
        # Run the capture script
        result = subprocess.run([sys.executable, 'capture_articles.py'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Article capture completed successfully")
            
            # Check if articles were saved
            if "articles saved" in result.stdout:
                saved_count = 0
                for line in result.stdout.split('\n'):
                    if "articles saved" in line:
                        # Extract number
                        words = line.split()
                        for i, word in enumerate(words):
                            if word.isdigit():
                                saved_count = int(word)
                                break
                
                if saved_count > 0:
                    print(f"   Successfully saved {saved_count} new articles")
                else:
                    print("   No new articles to save (may be expected)")
            
            return True
        else:
            print("❌ Article capture failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Article capture timed out")
        return False
    except Exception as e:
        print(f"❌ Error running workflow: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🧪 Zapier Setup Validation")
    print("=" * 50)
    
    checks = [
        ("GitHub Secrets", check_github_secrets),
        ("Config Generation", validate_config_generation),
        ("API Connection", test_zapier_api_connection),
        ("Full Workflow", test_full_workflow),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Zapier data collection should work correctly.")
        print("\nNext steps:")
        print("1. The workflow will now collect real articles from your Zapier table")
        print("2. Check the Actions tab for successful runs")
        print("3. Monitor the website for updated content")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        if passed == 0:
            print("\nCommon issues:")
            print("• Make sure ZAPIER_TABLE_ID and ZAPIER_API_KEY secrets are configured")
            print("• Verify your Zapier API key has the correct permissions")
            print("• Check that the table ID matches your Zapier table")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)