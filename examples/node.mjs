// npm i apify-client  ·  APIFY_TOKEN=... node examples/node.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('tidydata/youtube-transcript-scraper').call({
    sources: ['https://www.youtube.com/playlist?list=PLFs4vir_WsTwEd-nJgVJCZPNL3HALHHpF'],
    maxVideosPerSource: 10,
    includeVtt: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const v of items.filter((i) => i.status === 'ok')) {
    console.log(`${v.title} (${v.language}, ${v.wordCount} words)`);
}
