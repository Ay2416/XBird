import feedparser

rss_url_hashtag = 'nitter hashtag rss url'
rss_url_user = 'nitter user rss url'

d = feedparser.parse(rss_url_user)

try:
    print(d['entries'][0])
except Exception:
    print("エラー")
    exit()

for entry in d.entries:
    url_split = entry.link.split("/")

    url_data = "/" + url_split[3] + "/" +  url_split[4] + "/" + url_split[5]

    url_split = url_data.split("#")
    url_data = url_split[0]

    print(url_data)