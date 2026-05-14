group "default" {
  targets = ["ingest_kaggle_stock_news", "ingest_finnhub_company_news", "ingest_alpha_vantage_news_sentiment", "normalize_news", "validate_clean_news", "promote_clean_news", "ingest_alpha_vantage_daily_bars", "ingest_tiingo_daily_bars", "normalize_price_bars", "validate_price_bars", "promote_price_bars", "ingest_finnhub_company_profile", "ingest_tiingo_symbol_metadata", "normalize_company_reference", "validate_company_reference", "promote_company_reference", "ingest_alpha_vantage_company_overview", "normalize_fundamentals", "build_market_feature_panel", "validate_market_feature_panel", "promote_market_feature_panel"]
}

target "ingest_kaggle_stock_news" {
  context = "./runtime/stubs"
  tags = ["market/ingest-kaggle-stock-news:${GIT_SHA}"]
}

target "ingest_finnhub_company_news" {
  context = "./runtime/stubs"
  tags = ["market/ingest-finnhub-company-news:${GIT_SHA}"]
}

target "ingest_alpha_vantage_news_sentiment" {
  context = "./runtime/stubs"
  tags = ["market/ingest-alpha-vantage-news-sentiment:${GIT_SHA}"]
}

target "normalize_news" {
  context = "./runtime/stubs"
  tags = ["market/normalize-news:${GIT_SHA}"]
}

target "validate_clean_news" {
  context = "./runtime/stubs"
  tags = ["market/validate-clean-news:${GIT_SHA}"]
}

target "promote_clean_news" {
  context = "./runtime/stubs"
  tags = ["market/promote-clean-news:${GIT_SHA}"]
}

target "ingest_alpha_vantage_daily_bars" {
  context = "./runtime/stubs"
  tags = ["market/ingest-alpha-vantage-daily-bars:${GIT_SHA}"]
}

target "ingest_tiingo_daily_bars" {
  context = "./runtime/stubs"
  tags = ["market/ingest-tiingo-daily-bars:${GIT_SHA}"]
}

target "normalize_price_bars" {
  context = "./runtime/stubs"
  tags = ["market/normalize-price-bars:${GIT_SHA}"]
}

target "validate_price_bars" {
  context = "./runtime/stubs"
  tags = ["market/validate-price-bars:${GIT_SHA}"]
}

target "promote_price_bars" {
  context = "./runtime/stubs"
  tags = ["market/promote-price-bars:${GIT_SHA}"]
}

target "ingest_finnhub_company_profile" {
  context = "./runtime/stubs"
  tags = ["market/ingest-finnhub-company-profile:${GIT_SHA}"]
}

target "ingest_tiingo_symbol_metadata" {
  context = "./runtime/stubs"
  tags = ["market/ingest-tiingo-symbol-metadata:${GIT_SHA}"]
}

target "normalize_company_reference" {
  context = "./runtime/stubs"
  tags = ["market/normalize-company-reference:${GIT_SHA}"]
}

target "validate_company_reference" {
  context = "./runtime/stubs"
  tags = ["market/validate-company-reference:${GIT_SHA}"]
}

target "promote_company_reference" {
  context = "./runtime/stubs"
  tags = ["market/promote-company-reference:${GIT_SHA}"]
}

target "ingest_alpha_vantage_company_overview" {
  context = "./runtime/stubs"
  tags = ["market/ingest-alpha-vantage-company-overview:${GIT_SHA}"]
}

target "normalize_fundamentals" {
  context = "./runtime/stubs"
  tags = ["market/normalize-fundamentals:${GIT_SHA}"]
}

target "build_market_feature_panel" {
  context = "./runtime/stubs"
  tags = ["market/build-market-feature-panel:${GIT_SHA}"]
}

target "validate_market_feature_panel" {
  context = "./runtime/stubs"
  tags = ["market/validate-market-feature-panel:${GIT_SHA}"]
}

target "promote_market_feature_panel" {
  context = "./runtime/stubs"
  tags = ["market/promote-market-feature-panel:${GIT_SHA}"]
}
