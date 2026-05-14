#!/usr/bin/env python3
"""Run no-credential, source-shaped demo tasks for generated local Airflow DAGs."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RAW_PAYLOADS: dict[str, list[dict[str, Any]]] = {
    "raw_kaggle_stock_news": [
        {
            "source_row_id": "kaggle-000001",
            "symbol": "AAPL",
            "published_at": "2024-01-02T13:30:00Z",
            "title": "Apple shares rise after analyst upgrade",
            "article_body": "Analysts cited stronger services revenue and resilient device demand.",
            "url": "https://example.invalid/kaggle/aapl-upgrade",
            "publisher": "demo-wire",
            "dataset_snapshot": "massive-stock-news-analysis-db-for-nlpbacktests:demo",
            "sentiment_label": "positive"
        },
        {
            "source_row_id": "kaggle-000002",
            "symbol": "MSFT",
            "published_at": "2024-01-02T14:05:00Z",
            "title": "Microsoft cloud demand remains firm",
            "article_body": "Enterprise cloud demand remained stable across major customer segments.",
            "url": "https://example.invalid/kaggle/msft-cloud",
            "publisher": "demo-wire",
            "dataset_snapshot": "massive-stock-news-analysis-db-for-nlpbacktests:demo",
            "sentiment_label": "neutral"
        }
    ],
    "raw_finnhub_company_news": [
        {
            "category": "company",
            "datetime": 1704204000,
            "headline": "Apple supplier outlook improves",
            "id": 100001,
            "image": "https://example.invalid/images/aapl.jpg",
            "related": "AAPL",
            "source": "Demo News",
            "summary": "Supplier commentary pointed to improving demand.",
            "url": "https://example.invalid/finnhub/aapl-supplier"
        },
        {
            "category": "company",
            "datetime": 1704207600,
            "headline": "Nvidia unveils expanded data center platform",
            "id": 100002,
            "image": "https://example.invalid/images/nvda.jpg",
            "related": "NVDA",
            "source": "Demo News",
            "summary": "The announcement focused on accelerated computing workloads.",
            "url": "https://example.invalid/finnhub/nvda-platform"
        }
    ],
    "raw_alpha_vantage_news_sentiment": [
        {
            "title": "Microsoft AI products gain enterprise traction",
            "url": "https://example.invalid/alpha-vantage/msft-ai",
            "time_published": "20240102T143000",
            "authors": ["Demo Analyst"],
            "summary": "Adoption of AI-assisted productivity tools continued among enterprise customers.",
            "banner_image": "https://example.invalid/images/msft-ai.jpg",
            "source": "Demo Source",
            "category_within_source": "Technology",
            "source_domain": "example.invalid",
            "topics": [{"topic": "technology", "relevance_score": "0.86"}],
            "overall_sentiment_score": 0.21,
            "overall_sentiment_label": "Somewhat-Bullish",
            "ticker_sentiment": [
                {
                    "ticker": "MSFT",
                    "relevance_score": "0.94",
                    "ticker_sentiment_score": "0.31",
                    "ticker_sentiment_label": "Somewhat-Bullish"
                }
            ]
        }
    ],
    "raw_alpha_vantage_daily_bars": [
        {
            "symbol": "AAPL",
            "last_refreshed": "2024-01-02",
            "time_zone": "US/Eastern",
            "date": "2024-01-02",
            "1. open": "187.15",
            "2. high": "188.44",
            "3. low": "183.89",
            "4. close": "185.64",
            "5. volume": "82488700"
        },
        {
            "symbol": "MSFT",
            "last_refreshed": "2024-01-02",
            "time_zone": "US/Eastern",
            "date": "2024-01-02",
            "1. open": "373.86",
            "2. high": "375.90",
            "3. low": "366.77",
            "4. close": "370.87",
            "5. volume": "25258600"
        }
    ],
    "raw_tiingo_daily_bars": [
        {
            "ticker": "AAPL",
            "date": "2024-01-02T00:00:00.000Z",
            "open": 187.15,
            "high": 188.44,
            "low": 183.89,
            "close": 185.64,
            "volume": 82488700,
            "adjOpen": 186.91,
            "adjHigh": 188.20,
            "adjLow": 183.65,
            "adjClose": 185.40,
            "adjVolume": 82488700,
            "divCash": 0.0,
            "splitFactor": 1.0
        },
        {
            "ticker": "NVDA",
            "date": "2024-01-02T00:00:00.000Z",
            "open": 492.44,
            "high": 492.95,
            "low": 475.95,
            "close": 481.68,
            "volume": 41125400,
            "adjOpen": 492.44,
            "adjHigh": 492.95,
            "adjLow": 475.95,
            "adjClose": 481.68,
            "adjVolume": 41125400,
            "divCash": 0.0,
            "splitFactor": 1.0
        }
    ],
    "raw_finnhub_company_profile": [
        {
            "country": "US",
            "currency": "USD",
            "exchange": "NASDAQ NMS - GLOBAL MARKET",
            "finnhubIndustry": "Technology",
            "ipo": "1980-12-12",
            "logo": "https://example.invalid/logos/aapl.png",
            "marketCapitalization": 2900000.0,
            "name": "Apple Inc",
            "phone": "14089961010",
            "shareOutstanding": 15500.0,
            "ticker": "AAPL",
            "weburl": "https://www.apple.com/"
        },
        {
            "country": "US",
            "currency": "USD",
            "exchange": "NASDAQ NMS - GLOBAL MARKET",
            "finnhubIndustry": "Technology",
            "ipo": "1986-03-13",
            "logo": "https://example.invalid/logos/msft.png",
            "marketCapitalization": 2750000.0,
            "name": "Microsoft Corp",
            "phone": "14258828080",
            "shareOutstanding": 7430.0,
            "ticker": "MSFT",
            "weburl": "https://www.microsoft.com/"
        }
    ],
    "raw_tiingo_symbol_metadata": [
        {
            "ticker": "AAPL",
            "name": "Apple Inc",
            "exchangeCode": "NASDAQ",
            "startDate": "1980-12-12",
            "endDate": None,
            "description": "Consumer technology company."
        },
        {
            "ticker": "NVDA",
            "name": "NVIDIA Corp",
            "exchangeCode": "NASDAQ",
            "startDate": "1999-01-22",
            "endDate": None,
            "description": "Accelerated computing and semiconductor company."
        }
    ],
    "raw_alpha_vantage_company_overview": [
        {
            "Symbol": "AAPL",
            "AssetType": "Common Stock",
            "Name": "Apple Inc",
            "Description": "Apple designs, manufactures, and markets smartphones, personal computers, and services.",
            "Exchange": "NASDAQ",
            "Currency": "USD",
            "Country": "USA",
            "Sector": "TECHNOLOGY",
            "Industry": "CONSUMER ELECTRONICS",
            "MarketCapitalization": "2900000000000",
            "PERatio": "29.4",
            "DividendYield": "0.0052",
            "EPS": "6.13"
        }
    ]
}


DERIVED_PAYLOADS: dict[str, list[dict[str, Any]]] = {
    "clean_news_candidate": [
        {
            "news_id": "demo-news-aapl-20240102",
            "symbol": "AAPL",
            "published_at": "2024-01-02T13:30:00Z",
            "headline": "Apple shares rise after analyst upgrade",
            "body": "Analysts cited stronger services revenue and resilient device demand.",
            "source_name": "kaggle_stock_news",
            "source_url": "https://example.invalid/kaggle/aapl-upgrade",
            "sentiment_score": 0.35,
            "sentiment_label": "positive",
            "as_of_time": "2024-01-02T13:30:00Z"
        },
        {
            "news_id": "demo-news-msft-20240102",
            "symbol": "MSFT",
            "published_at": "2024-01-02T14:30:00Z",
            "headline": "Microsoft AI products gain enterprise traction",
            "body": "Adoption of AI-assisted productivity tools continued among enterprise customers.",
            "source_name": "alpha_vantage",
            "source_url": "https://example.invalid/alpha-vantage/msft-ai",
            "sentiment_score": 0.21,
            "sentiment_label": "Somewhat-Bullish",
            "as_of_time": "2024-01-02T14:30:00Z"
        }
    ],
    "clean_room_news": [],
    "clean_price_bars_candidate": [
        {
            "symbol": "AAPL",
            "bar_date": "2024-01-02",
            "open": 187.15,
            "high": 188.44,
            "low": 183.89,
            "close": 185.64,
            "volume": 82488700,
            "adjusted_close": 185.40,
            "currency": "USD",
            "source_priority": ["alpha_vantage", "tiingo"],
            "as_of_time": "2024-01-03T00:30:00Z"
        },
        {
            "symbol": "MSFT",
            "bar_date": "2024-01-02",
            "open": 373.86,
            "high": 375.90,
            "low": 366.77,
            "close": 370.87,
            "volume": 25258600,
            "adjusted_close": 370.87,
            "currency": "USD",
            "source_priority": ["alpha_vantage"],
            "as_of_time": "2024-01-03T00:30:00Z"
        }
    ],
    "clean_room_price_bars": [],
    "clean_company_reference_candidate": [
        {
            "symbol": "AAPL",
            "company_name": "Apple Inc",
            "exchange": "NASDAQ",
            "currency": "USD",
            "country": "US",
            "sector": "Technology",
            "industry": "Technology",
            "ipo_date": "1980-12-12",
            "provider_ids": {"finnhub": "AAPL", "tiingo": "AAPL"}
        },
        {
            "symbol": "NVDA",
            "company_name": "NVIDIA Corp",
            "exchange": "NASDAQ",
            "currency": "USD",
            "country": "US",
            "sector": "Technology",
            "industry": "Semiconductors",
            "ipo_date": "1999-01-22",
            "provider_ids": {"tiingo": "NVDA"}
        }
    ],
    "clean_room_company_reference": [],
    "clean_fundamentals_candidate": [
        {
            "symbol": "AAPL",
            "as_of_date": "2024-01-02",
            "market_capitalization": 2900000000000,
            "pe_ratio": 29.4,
            "dividend_yield": 0.0052,
            "eps": 6.13,
            "source_name": "alpha_vantage"
        }
    ],
    "training_market_feature_panel_candidate": [
        {
            "symbol": "AAPL",
            "as_of_date": "2024-01-02",
            "close": 185.64,
            "volume": 82488700,
            "news_sentiment_1d": 0.35,
            "news_count_1d": 1,
            "market_capitalization": 2900000000000,
            "sector": "Technology",
            "label_return_5d": None,
            "label_available_at": "2024-01-09T21:00:00Z"
        }
    ],
    "trusted_training_market_feature_panel": []
}


QUALITY_PAYLOADS: dict[str, list[dict[str, Any]]] = {
    "clean_news_quality_scorecard": [
        {
            "quality_profile": "clean_news_v1",
            "overall_score": 0.91,
            "promotion_decision": "trusted_training_ready",
            "hard_gates": {"schema_valid": True, "no_future_timestamps": True},
            "soft_scores": {"completeness_quality": 0.93, "entity_linking_quality": 0.89},
            "blocking_failures": [],
            "warnings": []
        }
    ],
    "clean_price_bars_quality_scorecard": [
        {
            "quality_profile": "clean_price_bars_v1",
            "overall_score": 0.94,
            "promotion_decision": "trusted_training_ready",
            "hard_gates": {"schema_valid": True, "high_low_bounds_valid": True},
            "soft_scores": {"session_coverage_quality": 0.95, "provider_agreement_quality": 0.92},
            "blocking_failures": [],
            "warnings": []
        }
    ],
    "clean_company_reference_quality_scorecard": [
        {
            "quality_profile": "company_reference_v1",
            "overall_score": 0.90,
            "promotion_decision": "trusted_training_ready",
            "hard_gates": {"schema_valid": True, "symbol_present": True},
            "soft_scores": {"identifier_completeness_quality": 0.91, "provider_consistency_quality": 0.88},
            "blocking_failures": [],
            "warnings": []
        }
    ],
    "training_market_feature_panel_quality_scorecard": [
        {
            "quality_profile": "market_feature_panel_v1",
            "overall_score": 0.94,
            "promotion_decision": "trusted_training",
            "hard_gates": {"schema_valid": True, "no_label_leakage": True},
            "soft_scores": {"feature_completeness_quality": 0.93, "cross_source_join_quality": 0.94},
            "blocking_failures": [],
            "warnings": []
        }
    ]
}


def load_task_spec() -> dict[str, Any]:
    raw = os.environ.get("FRIENDLY_GIGGLE_TASK_SPEC")
    if not raw:
        return {}
    return json.loads(raw)


def records_for_asset(asset_name: str) -> list[dict[str, Any]]:
    if asset_name in RAW_PAYLOADS:
        return RAW_PAYLOADS[asset_name]
    if asset_name in QUALITY_PAYLOADS:
        return QUALITY_PAYLOADS[asset_name]
    if asset_name in DERIVED_PAYLOADS:
        records = DERIVED_PAYLOADS[asset_name]
        if records:
            return records
        candidate = asset_name.replace("clean_room_", "clean_") + "_candidate"
        if candidate in DERIVED_PAYLOADS:
            return DERIVED_PAYLOADS[candidate]
        if asset_name == "trusted_training_market_feature_panel":
            return DERIVED_PAYLOADS["training_market_feature_panel_candidate"]
    return [{"asset": asset_name, "demo_note": "No source-shaped sample registered."}]


def schema_name_for(asset_name: str) -> str:
    return f"{asset_name}_v1"


def write_outputs(output_dir: Path, task_name: str, task_spec: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    for asset_name in task_spec.get("outputs", []):
        records = records_for_asset(asset_name)
        manifest = {
            "asset_name": asset_name,
            "asset_version": f"demo-{now}",
            "output_uri": f"file://{output_dir / (asset_name + '.json')}",
            "input_assets": task_spec.get("inputs", []),
            "record_count": len(records),
            "code_version": "local-demo",
            "created_at": now,
            "producer_task": task_name,
            "schema_name": schema_name_for(asset_name),
            "demo_mode": True
        }
        payload = {
            "asset": asset_name,
            "schema_name": schema_name_for(asset_name),
            "producer_task": task_name,
            "created_at": now,
            "records": records
        }
        (output_dir / f"{asset_name}.manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / f"{asset_name}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    task_spec = load_task_spec()
    output_dir = Path(os.environ.get("FRIENDLY_GIGGLE_OUTPUT_DIR", "/tmp/friendly-giggle-demo"))
    write_outputs(output_dir, args.task, task_spec)

    print(
        json.dumps(
            {
                "task": args.task,
                "kind": task_spec.get("kind", "unknown"),
                "inputs": task_spec.get("inputs", []),
                "outputs": task_spec.get("outputs", []),
                "output_dir": str(output_dir),
                "demo_mode": True
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
