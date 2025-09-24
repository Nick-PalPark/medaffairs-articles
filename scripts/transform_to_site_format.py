#!/usr/bin/env python3
"""
Transform raw articles.json to structured website format.

Converts the simple article array format to the structured format expected by
the medaffairs.tech website with heroes and categorized columns.
"""

import argparse
import json
import time
import re
from pathlib import Path
from datetime import datetime

def categorize_article(article):
    """Categorize article based on title and source keywords"""
    title = (article.get('title') or '').lower()
    source = (article.get('source') or '').lower()
    
    # Tech/AI keywords
    tech_keywords = ['ai', 'artificial intelligence', 'machine learning', 'digital', 'software', 'app', 'technology', 'tech', 'data', 'algorithm', 'automation']
    
    # Opinion keywords  
    opinion_keywords = ['opinion', 'editorial', 'commentary', 'analysis', 'perspective', 'viewpoint', 'insight']
    
    # Check for tech category
    if any(keyword in title or keyword in source for keyword in tech_keywords):
        return 'tech'
    
    # Check for opinion category
    if any(keyword in title or keyword in source for keyword in opinion_keywords):
        return 'opinion'
    
    # Default to news
    return 'news'

def convert_published_date(published_str):
    """Convert published date string to timestamp"""
    if not published_str:
        return int(time.time() * 1000)
    
    try:
        # Parse various date formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(published_str, fmt)
                return int(dt.timestamp() * 1000)
            except ValueError:
                continue
                
        # If all formats fail, return current time
        return int(time.time() * 1000)
        
    except Exception:
        return int(time.time() * 1000)

def create_hero_article(article):
    """Create hero article format"""
    return {
        'manual_title': article.get('manual_title'),
        'generated_title': None,  # Could be enhanced with AI generation
        'original_title': article.get('title'),
        'url': article.get('url'),
        'image': None,  # Could be enhanced with image extraction
        'source': article.get('source'),
        'published_at': convert_published_date(article.get('published'))
    }

def create_column_article(article):
    """Create column article format"""
    return {
        'manual_title': article.get('manual_title'),
        'generated_title': None,
        'original_title': article.get('title'),
        'url': article.get('url'),
        'source': article.get('source'),
        'published_at': convert_published_date(article.get('published'))
    }

def main():
    parser = argparse.ArgumentParser(description='Transform raw articles to website format')
    parser.add_argument('--input', default='articles.json', help='Input articles JSON file')
    parser.add_argument('--output', default='data/articles.json', help='Output site format JSON file')
    parser.add_argument('--heroes-count', type=int, default=3, help='Number of hero articles')
    
    args = parser.parse_args()
    
    # Load raw articles
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file {args.input} not found")
        return False
    
    with open(input_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if not articles:
        print("No articles to process")
        return False
    
    # Filter articles with URLs (valid articles)
    valid_articles = [a for a in articles if a.get('url')]
    
    if not valid_articles:
        print("No valid articles with URLs found")
        return False
    
    # Sort by published date (newest first)
    valid_articles.sort(
        key=lambda x: convert_published_date(x.get('published')), 
        reverse=True
    )
    
    # Select heroes (top articles)
    heroes = []
    remaining_articles = valid_articles[:]
    
    for i in range(min(args.heroes_count, len(valid_articles))):
        article = valid_articles[i]
        heroes.append(create_hero_article(article))
        remaining_articles.remove(article)
    
    # Categorize remaining articles
    columns = {
        'news': [],
        'tech': [],
        'opinion': []
    }
    
    for article in remaining_articles:
        category = categorize_article(article)
        columns[category].append(create_column_article(article))
    
    # Create final structure
    result = {
        'last_updated': int(time.time() * 1000),
        'heroes': heroes,
        'columns': columns
    }
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Transformed {len(valid_articles)} articles:")
    print(f"  Heroes: {len(heroes)}")
    print(f"  News: {len(columns['news'])}")
    print(f"  Tech: {len(columns['tech'])}")
    print(f"  Opinion: {len(columns['opinion'])}")
    print(f"  Output: {args.output}")
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)