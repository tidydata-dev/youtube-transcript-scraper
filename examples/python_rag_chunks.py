"""Chunks for RAG: one chunk per chapter (or per ~2 minutes when a video has no chapters). pip install apify-client"""
import json, os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("tidydata/youtube-transcript-scraper").call(run_input={
    "sources": ["@lexfridman"], "maxVideosPerSource": 3, "includeChapters": True, "includeSegments": True,
})
chunks = []
for v in client.dataset(run["defaultDatasetId"]).iterate_items():
    if v.get("status") != "ok":
        continue
    if v.get("chapters"):
        for ch in v["chapters"]:
            chunks.append({"text": ch["text"], "title": f'{v["title"]} — {ch["title"]}',
                           "url": f'{v["url"]}&t={ch["start"]}s'})
    else:
        window, start = [], 0
        for s in v["segments"]:
            if s["start"] - start > 120 and window:
                chunks.append({"text": " ".join(window), "title": v["title"], "url": f'{v["url"]}&t={int(start)}s'})
                window, start = [], s["start"]
            window.append(s["text"])
        if window:
            chunks.append({"text": " ".join(window), "title": v["title"], "url": f'{v["url"]}&t={int(start)}s'})
json.dump(chunks, open("chunks.json", "w"), ensure_ascii=False, indent=1)
print(len(chunks), "chunks ready for your embeddings / vector database")
