#!/usr/bin/env python3
"""
Transform raw articles.json (array format) to the structured format expected by the website.
The website expects: { "last_updated": timestamp, "heroes": [...], "columns": { "news": [...], "tech": [...], "opinion": [...] } }
"""

import argparse
import json
import time
from pathlib import Path


def get_display_title(article):
    """Get the best title to display following priority: manual_title -> generated_title -> title"""
    if article.get('manual_title') and article['manual_title'].strip():
        return article['manual_title']
    if article.get('generated_title') and article['generated_title'].strip():
        return article['generated_title']
    return article.get('title', 'Untitled')


def categorize_article(article):
    """Categorize article based on title/source keywords"""
    title = get_display_title(article).lower()
    source = (article.get('source') or '').lower()
    
    # Simple keyword-based categorization
    tech_keywords = ['ai', 'artificial intelligence', 'tech', 'digital', 'software', 'app', 'platform', 'innovation']
    opinion_keywords = ['opinion', 'analysis', 'editorial', 'commentary', 'perspective', 'viewpoint']
    
    if any(keyword in title or keyword in source for keyword in tech_keywords):
        return 'tech'
    elif any(keyword in title or keyword in source for keyword in opinion_keywords):
        return 'opinion'
    else:
        return 'news'  # default to industry news


def transform_articles(articles_data):
    """Transform raw articles array to structured site format"""
    if not articles_data:
        return {
            "last_updated": int(time.time() * 1000),
            "heroes": [],
            "columns": {"news": [], "tech": [], "opinion": []}
        }
    
    # Convert articles to site format
    site_articles = []
    for article in articles_data:
        site_article = {
            "title": get_display_title(article),
            "url": article.get('url'),
            "source": article.get('source'),
            "published": article.get('published')
        }
        # Add image if available (for potential heroes)
        if article.get('image'):
            site_article['image'] = article['image']
        site_articles.append(site_article)
    
    # Sort by published date (most recent first)
    site_articles.sort(key=lambda x: x.get('published') or '', reverse=True)
    
    # Select top 3 as heroes (preferably with images)
    heroes = []
    remaining_articles = []
    
    for article in site_articles:
        if len(heroes) < 3 and article.get('image'):
            heroes.append(article)
        else:
            remaining_articles.append(article)
    
    # If we don't have 3 heroes with images, fill from remaining
    while len(heroes) < 3 and remaining_articles:
        heroes.append(remaining_articles.pop(0))
    
    # Categorize remaining articles
    columns = {"news": [], "tech": [], "opinion": []}
    for article in remaining_articles:
        category = categorize_article(article)
        columns[category].append(article)
    
    # Add any articles that weren't selected as heroes
    for article in site_articles:
        if article not in heroes:
            category = categorize_article(article)
            if article not in columns[category]:
                columns[category].append(article)
    
    # Limit each column to reasonable number
    for category in columns:
        columns[category] = columns[category][:10]
    
    return {
        "last_updated": int(time.time() * 1000),
        "heroes": heroes,
        "columns": columns
    }


def main():
    parser = argparse.ArgumentParser(description='Transform articles.json to site format')
    parser.add_argument('--input', default='articles.json', help='Input articles.json file')
    parser.add_argument('--output', default='data/articles.json', help='Output file for site')
    
    args = parser.parse_args()
    
    # Load input articles
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file {args.input} not found")
        return 1
    
    try:
        articles_data = json.loads(input_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Error reading {args.input}: {e}")
        return 1
    
    # Transform to site format
    site_data = transform_articles(articles_data)
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    try:
        output_path.write_text(json.dumps(site_data, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"Successfully transformed {len(articles_data)} articles to {args.output}")
        print(f"Heroes: {len(site_data['heroes'])}, News: {len(site_data['columns']['news'])}, Tech: {len(site_data['columns']['tech'])}, Opinion: {len(site_data['columns']['opinion'])}")
    except Exception as e:
        print(f"Error writing {args.output}: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())