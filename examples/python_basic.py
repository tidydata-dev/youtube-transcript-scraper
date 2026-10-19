"""Transcripts of a channel's newest videos saved as .txt files. pip install apify-client"""
import os, re
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("tidydata/youtube-transcript-scraper").call(run_input={
    "sources": ["@veritasium"],
    "maxVideosPerSource": 10,
    "textFormat": "paragraphs",
})
os.makedirs("transcripts", exist_ok=True)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    if item.get("status") != "ok":
        print("skipped", item.get("videoId"), item.get("status"))
        continue
    name = re.sub(r"[^\w\- ]+", "", item["title"])[:80]
    with open(f"transcripts/{name}.txt", "w", encoding="utf-8") as f:
        f.write(item["transcript"])
    print("saved", name)
