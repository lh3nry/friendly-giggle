# Source-Shaped Demo Schemas

The local demo now emits source-shaped records instead of one generic placeholder shape. The contracts live in `specs/source_schemas.yaml`, and generated copies are written to `runtime/manifests/generated/source_schemas.json`.

## Raw Source Shapes

- `raw_kaggle_stock_news_v1`: Kaggle dataset snapshot rows with source row ID, ticker, publication time, title, body, URL, publisher, dataset snapshot, and optional sentiment label.
- `raw_finnhub_company_news_v1`: Finnhub company-news style items with category, epoch `datetime`, headline, provider ID, related ticker, source, summary, and URL.
- `raw_alpha_vantage_news_sentiment_v1`: Alpha Vantage `NEWS_SENTIMENT` feed items with title, URL, `time_published`, source, topics, overall sentiment, and nested ticker sentiment.
- `raw_alpha_vantage_daily_bars_v1`: Alpha Vantage daily time-series rows preserving numbered fields such as `1. open`, `2. high`, `3. low`, `4. close`, and `5. volume`.
- `raw_tiingo_daily_bars_v1`: Tiingo daily price rows with raw and adjusted OHLCV fields, `divCash`, and `splitFactor`.
- `raw_finnhub_company_profile_v1`: Finnhub company profile records for ticker, exchange, industry, market cap, shares outstanding, and web URL.
- `raw_tiingo_symbol_metadata_v1`: Tiingo symbol metadata for ticker, name, exchange code, date range, and description.
- `raw_alpha_vantage_company_overview_v1`: Alpha Vantage company overview fields for fundamentals and sector/industry joins.

## Canonical Shapes

- `clean_news_candidate_v1`: normalized article records with `news_id`, `symbol`, `published_at`, headline/body, source, sentiment, and `as_of_time`.
- `clean_price_bars_candidate_v1`: normalized daily OHLCV bars with adjusted close, currency, source priority, and `as_of_time`.
- `clean_company_reference_candidate_v1`: normalized reference rows with company identity, exchange, currency, country, sector, industry, IPO date, and provider IDs.
- `training_market_feature_panel_candidate_v1`: point-in-time feature rows with price, news aggregate, fundamentals/reference fields, and label availability time.

These shapes are intentionally small. They are high-fidelity enough to start writing ingestion and normalization code, while avoiding a full provider-client implementation in the local demo.
