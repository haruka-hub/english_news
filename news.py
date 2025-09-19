import requests
from bs4 import BeautifulSoup
import random
import os

def fetch_articles():
    url = "https://www.newsinlevels.com/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # トップページにある記事タイトル & リンクを取得
    # “### Title” 要素のリンクを探す
    # 例： <h3><a href="/level1/some-article">Title …</a></h3>
    # ただしサイト構造に合わせて変更が必要

    articles = []
    # find all h3 tags under Main content
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        if a and a.get("href"):
            title = a.get_text().strip()
            link = a["href"]
            # 相対リンクなら絶対に
            if link.startswith("/"):
                link = "https://www.newsinlevels.com" + link
            articles.append((title, link))
    return articles

def choose_random_article(articles):
    return random.choice(articles) if articles else None

def post_to_slack(title, link):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    text = f"今日の英語ニュース (News in Levels) はこちらです：\n*{title}*\n{link}"
    payload = {"text": text}
    resp = requests.post(webhook_url, json=payload)
    resp.raise_for_status()

def main():
    articles = fetch_articles()
    article = choose_random_article(articles)
    if article:
        title, link = article
        post_to_slack(title, link)
    else:
        print("記事が取得できませんでした。")

if __name__ == "__main__":
    main()
