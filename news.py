# news.py
import requests
from bs4 import BeautifulSoup
import random
import os

# Slack Webhook URL（GitHub Secretsから取得）
slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]

# ニュースサイト（RSSの例：NHKニュース）
rss_url = "https://www3.nhk.or.jp/rss/news/cat0.xml"

# RSSから記事取得
res = requests.get(rss_url)
soup = BeautifulSoup(res.content, "xml")
items = soup.find_all("item")

# 記事をランダムで1つ選ぶ
article = random.choice(items)
title = article.title.text
link = article.link.text

# Slackに通知
payload = {
    "text": f"今日のニュースはこちら！\n*{title}*\n{link}"
}
requests.post(slack_webhook_url, json=payload)
