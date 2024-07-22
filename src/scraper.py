import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

BASE_URL = 'https://help.tecnomat.it/hc/it/categories/18305457266577-Tutte-le-domande'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def parse_category_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('h2.h3 a')
    return [urljoin(BASE_URL, link['href']) for link in links]

def parse_question_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('div.media-body a')
    return [urljoin(BASE_URL, link['href']) for link in links]


def parse_answer_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    question = soup.select_one('article h1').get_text(strip=True) if soup.select_one('h1') else None
    answer = soup.select_one('[itemprop="articleBody"]').get_text(strip=True) if soup.select_one('[itemprop="articleBody"]') else None
    return question, answer

def scrape():
    html = fetch_page(BASE_URL)
    if not html:
        return

    question_links = parse_category_page(html)
    
    data = []

    for question_link in question_links:
        question_html = fetch_page(question_link)
        if not question_html:
            continue

        answer_links = parse_question_page(question_html)
        
        for answer_link in answer_links:
            answer_html = fetch_page(answer_link)
            if not answer_html:
                continue
            
            question, answer = parse_answer_page(answer_html)
            if question and answer:
                data.append({
                    'question': question,
                    'answer': answer
                })

    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['question', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    scrape()
