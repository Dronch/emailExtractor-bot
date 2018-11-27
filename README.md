# emailExtractor-bot
Scrapy project for extracting emails from url

## Install
```bash
pip install scrapy
pip install -r requirements.txt
```

## Run
```bash
scrapy crawl extractor -a url=https://scrape.me -a depth=3 --set FEED_URI=scraped_data.csv --set FEED_FORMAT=csv
```


| Arg | Desc | Require | Example |
| :---: | :---: | :---: | :---: |
| `url` | Target website url | `True` | `url=https://scrape.me` |
| `depth` | Website crawling depth  | `False` | `depth=3` |

