#!/bin/sh
# Run the Actor synchronously and get the transcripts as JSON in one call.
curl -s -X POST \
  "https://api.apify.com/v2/acts/tidydata~youtube-transcript-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sources": ["https://youtu.be/iCvmsMzlF7o"], "includeSrt": true}'
