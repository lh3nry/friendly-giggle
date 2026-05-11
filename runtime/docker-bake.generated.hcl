group "default" {
  targets = ["ingest_news", "normalize_news", "validate_clean_news"]
}

target "ingest_news" {
  context = "./tasks/ingest_news"
  tags = ["market/ingest-news:${GIT_SHA}"]
}

target "normalize_news" {
  context = "./tasks/normalize_news"
  tags = ["market/normalize-news:${GIT_SHA}"]
}

target "validate_clean_news" {
  context = "./tasks/validate_clean_news"
  tags = ["market/validate-clean-news:${GIT_SHA}"]
}
