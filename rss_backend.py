from flask import Flask, jsonify
import feedparser

app = Flask(__name__)

rss_feeds = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/"
]

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150x100?text=Image+Not+Available"

@app.route("/api/news")
def get_news():
    all_items = []
    seen_links = set()
    seen_images = set()

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if entry.link in seen_links:
                continue
            seen_links.add(entry.link)

            image_url = PLACEHOLDER_IMAGE
            if 'media_content' in entry:
                image_url = entry.media_content[0]['url']
            elif 'media_thumbnail' in entry:
                image_url = entry.media_thumbnail[0]['url']

            # Avoid duplicate images
            if image_url in seen_images:
                image_url = PLACEHOLDER_IMAGE
            else:
                seen_images.add(image_url)

            item = {
                "title": entry.title,
                "link": entry.link,
                "pubDate": entry.published if 'published' in entry else '',
                "image": image_url
            }
            all_items.append(item)

    # Sort latest first
    all_items.sort(key=lambda x: x['pubDate'], reverse=True)
    return jsonify(all_items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)