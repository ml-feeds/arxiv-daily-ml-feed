# arxiv-daily-ml-feed
**arxiv-daily-ml-feed** uses Python 3.9 to serve an RSS feed with meta updates of ArXiv entries in machine learning and
artificial intelligence.
It doesn't include the individual new entries themselves. Rather, it includes daily meta updates.
As a disclaimer, it has no affiliation with ArXiv.

## Links
* [Project repo](https://github.com/ml-feeds/arxiv-daily-ml-feed)
* [**Unofficial RSS feed**](https://us-east1-ml-feeds.cloudfunctions.net/arxiv-daily-ml)

## Deployment
Serverless deployment to [Google Cloud Functions](https://console.cloud.google.com/functions/) is configured.
It requires the following files:
* requirements.txt
* main.py (having callable `serve(request: flask.Request) -> Tuple[bytes, int, Dict[str, str]]`)

Deployment version updates are not automated.
They can be performed manually by editing and saving the function configuration.

These deployment links require access:
* [Dashboard](https://console.cloud.google.com/functions/details/us-east1/arxiv-daily-ml?project=ml-feeds)
* [Logs](https://console.cloud.google.com/logs?service=cloudfunctions.googleapis.com&key1=arxiv-daily-ml&key2=us-east1&project=ml-feeds)
* [Repo](https://source.cloud.google.com/ml-feeds/github_ml-feeds_arxiv-daily-ml-feed)
