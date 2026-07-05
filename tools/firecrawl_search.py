"""
firecrawl_search.py — web discovery for the university finder workflow.

Runs one or more search queries through Firecrawl's /search endpoint and,
optionally, scrapes the top result URLs for clean markdown the agent can read.
Normalized results are written to .tmp/search_results.json.

(Copied from the guest_speakers WAT project — same proven discovery logic.)

Usage:
    # one or more queries as positional args
    python tools/firecrawl_search.py "BSc Computer Science UK entry requirements" "QS computer science ranking"

    # queries from a JSON file (a list of strings)
    python tools/firecrawl_search.py --queries-file .tmp/queries.json

    # control how many results per query, and how many to scrape for full text
    python tools/firecrawl_search.py "University of Manchester CS fees" --limit 8 --scrape-top 3

Output (.tmp/search_results.json):
    [
      {
        "query": "...",
        "results": [
          {"title": "...", "url": "...", "snippet": "...", "markdown": "..."|null},
          ...
        ]
      },
      ...
    ]

The FIRECRAWL_API_KEY must be set in .env (never hardcode it here).
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Resolve repo paths relative to this file so the tool works from any cwd.
REPO_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = REPO_ROOT / ".tmp"
OUTPUT_PATH = TMP_DIR / "search_results.json"

# Firecrawl returns "Website Not Supported" for these domains, so scraping them
# burns a credit and a scrape slot for nothing. We still keep them in the results
# (their URL + snippet are useful leads — e.g. Reddit/forum sentiment) — we just
# never pick them as scrape targets.
SOCIAL_DOMAINS = (
    "instagram.com",
    "facebook.com",
    "fb.com",
    "fb.watch",
    "threads.net",
    "tiktok.com",
    "x.com",
    "twitter.com",
)


def is_social_url(url):
    """True if the URL is on a social domain Firecrawl can't scrape."""
    u = (url or "").lower()
    return any(domain in u for domain in SOCIAL_DOMAINS)


def get_client():
    """Return a Firecrawl client, tolerating SDK version differences."""
    load_dotenv(REPO_ROOT / ".env")
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        sys.exit("ERROR: FIRECRAWL_API_KEY is not set in .env")

    try:
        # firecrawl-py v2+
        from firecrawl import Firecrawl  # type: ignore

        return Firecrawl(api_key=api_key)
    except Exception:
        pass

    try:
        # older firecrawl-py
        from firecrawl import FirecrawlApp  # type: ignore

        return FirecrawlApp(api_key=api_key)
    except Exception as exc:  # pragma: no cover - import/setup failure
        sys.exit(
            "ERROR: could not initialize the Firecrawl SDK "
            f"({exc}). Is firecrawl-py installed? Run: pip install -r requirements.txt"
        )


def _as_dict(obj):
    """Best-effort convert an SDK object (pydantic/dataclass) to a plain dict."""
    if isinstance(obj, dict):
        return obj
    for attr in ("model_dump", "dict"):
        fn = getattr(obj, attr, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
    if hasattr(obj, "__dict__"):
        return dict(vars(obj))
    return {}


def _extract_results(raw):
    """Pull a flat list of result dicts out of whatever shape search returned."""
    data = _as_dict(raw) if not isinstance(raw, (list, dict)) else raw

    if isinstance(data, dict):
        # Common containers across versions: data / web / results.
        for key in ("data", "web", "results"):
            if isinstance(data.get(key), list):
                return [_as_dict(item) for item in data[key]]
        # Some v2 responses nest the web list under data.
        inner = data.get("data")
        if isinstance(inner, dict):
            for key in ("web", "results"):
                if isinstance(inner.get(key), list):
                    return [_as_dict(item) for item in inner[key]]
        return []
    if isinstance(data, list):
        return [_as_dict(item) for item in data]
    return []


def _normalize_item(item):
    """Map a raw result dict to {title, url, snippet}."""
    return {
        "title": item.get("title") or item.get("name") or "",
        "url": item.get("url") or item.get("link") or "",
        "snippet": item.get("description") or item.get("snippet") or item.get("excerpt") or "",
        "markdown": None,
    }


def run_search(client, query, limit):
    try:
        raw = client.search(query=query, limit=limit)
    except TypeError:
        # Older signature: positional query.
        raw = client.search(query, limit=limit)
    except Exception as exc:
        print(f"  ! search failed for {query!r}: {exc}", file=sys.stderr)
        return []
    items = [_normalize_item(i) for i in _extract_results(raw)]
    return [i for i in items if i["url"]]


def scrape_markdown(client, url):
    """Return clean markdown for a URL, or None on failure."""
    for method in ("scrape", "scrape_url"):
        fn = getattr(client, method, None)
        if not callable(fn):
            continue
        try:
            try:
                doc = fn(url, formats=["markdown"])
            except TypeError:
                doc = fn(url)
        except Exception as exc:
            print(f"  ! scrape failed for {url}: {exc}", file=sys.stderr)
            return None
        d = _as_dict(doc)
        md = d.get("markdown")
        if md is None and isinstance(d.get("data"), dict):
            md = d["data"].get("markdown")
        return md
    return None


def load_queries(args):
    if args.queries_file:
        path = Path(args.queries_file)
        if not path.is_absolute():
            path = REPO_ROOT / path
        queries = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(queries, list):
            sys.exit("ERROR: --queries-file must contain a JSON list of strings")
        return [str(q) for q in queries]
    return list(args.queries)


def main():
    parser = argparse.ArgumentParser(description="Firecrawl web discovery for the university finder workflow.")
    parser.add_argument("queries", nargs="*", help="One or more search queries.")
    parser.add_argument("--queries-file", help="Path to a JSON file containing a list of queries.")
    parser.add_argument("--limit", type=int, default=6, help="Results per query (default 6).")
    parser.add_argument(
        "--scrape-top",
        type=int,
        default=0,
        help="Scrape full markdown for the top N results per query (default 0 = none).",
    )
    args = parser.parse_args()

    queries = load_queries(args)
    if not queries:
        parser.error("provide at least one query, or use --queries-file")

    client = get_client()
    TMP_DIR.mkdir(exist_ok=True)

    output = []
    for query in queries:
        print(f"Searching: {query}")
        results = run_search(client, query, args.limit)
        # Pick scrape targets from the top NON-social results only. Social URLs
        # (IG/FB/etc.) return "Website Not Supported", so scraping them wastes a
        # slot — skip them and scrape the next real prospectus/course page instead.
        scraped = 0
        for item in results:
            if scraped >= max(0, args.scrape_top):
                break
            if is_social_url(item["url"]):
                continue
            print(f"  scraping: {item['url']}")
            item["markdown"] = scrape_markdown(client, item["url"])
            scraped += 1
        output.append({"query": query, "results": results})
        print(f"  -> {len(results)} results")

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(len(o["results"]) for o in output)
    print(f"\nWrote {total} results across {len(output)} queries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
