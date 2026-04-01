from __future__ import annotations

from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from xml.etree import ElementTree as ET

from app.providers.base import NewsProvider
from app.schemas.news import NewsItem


class RssNewsProvider(NewsProvider):
    def __init__(self, feeds: tuple[str, ...]) -> None:
        self.feeds = feeds

    def list_items(self) -> list[NewsItem]:
        items: list[NewsItem] = []
        for feed in self.feeds:
            try:
                root = self._load_xml(feed)
            except Exception:
                continue
            items.extend(self._parse_feed(root, feed))
        unique = {item.id: item for item in items}
        return sorted(unique.values(), key=lambda item: item.publishedAt, reverse=True)

    def _load_xml(self, location: str) -> ET.Element:
        parsed = urlparse(location)
        if parsed.scheme in {"http", "https"}:
            with urlopen(location, timeout=10) as response:
                return ET.fromstring(response.read())
        return ET.parse(Path(location)).getroot()

    def _parse_feed(self, root: ET.Element, feed: str) -> list[NewsItem]:
        channel_items = root.findall(".//item")
        entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        parsed_items: list[NewsItem] = []
        if channel_items:
            for item in channel_items:
                parsed = self._parse_rss_item(item, feed)
                if parsed:
                    parsed_items.append(parsed)
        elif entries:
            for entry in entries:
                parsed = self._parse_atom_entry(entry, feed)
                if parsed:
                    parsed_items.append(parsed)
        return parsed_items

    def _parse_rss_item(self, item: ET.Element, feed: str) -> NewsItem | None:
        title = self._text(item, "title")
        link = self._text(item, "link")
        description = self._text(item, "description")
        pub_date = self._text(item, "pubDate")
        if not title or not link or not pub_date:
            return None
        published_at = parsedate_to_datetime(pub_date).date()
        return NewsItem(
            id=self._build_id(feed, link),
            publishedAt=published_at,
            source=urlparse(feed).netloc or Path(feed).name,
            title=title,
            summary=description or title,
            impact="Imported from RSS feed; requires editorial enrichment for business impact.",
            topics=self._infer_topics(title=title, summary=description or ""),
            region="EU",
            url=link,
        )

    def _parse_atom_entry(self, entry: ET.Element, feed: str) -> NewsItem | None:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        title = entry.findtext("atom:title", default="", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        summary = entry.findtext("atom:summary", default="", namespaces=ns) or entry.findtext(
            "atom:content", default="", namespaces=ns
        )
        published_raw = entry.findtext("atom:updated", default="", namespaces=ns) or entry.findtext(
            "atom:published", default="", namespaces=ns
        )
        link = link_el.get("href", "") if link_el is not None else ""
        if not title or not link or not published_raw:
            return None
        published_at = parsedate_to_datetime(published_raw).date() if "," in published_raw else published_raw[:10]
        if isinstance(published_at, str):
            year, month, day = [int(part) for part in published_at.split("-")]
            from datetime import date

            published_at = date(year, month, day)
        return NewsItem(
            id=self._build_id(feed, link),
            publishedAt=published_at,
            source=urlparse(feed).netloc or Path(feed).name,
            title=title,
            summary=summary or title,
            impact="Imported from RSS feed; requires editorial enrichment for business impact.",
            topics=self._infer_topics(title=title, summary=summary or ""),
            region="EU",
            url=link,
        )

    def _infer_topics(self, title: str, summary: str) -> list[str]:
        haystack = f"{title} {summary}".lower()
        topics = []
        for keyword, topic in (
            ("cbam", "CBAM"),
            ("digital product passport", "DPP"),
            ("product passport", "DPP"),
            ("battery", "Battery Passport"),
            ("ecodesign", "ESPR"),
            ("espr", "ESPR"),
        ):
            if keyword in haystack and topic not in topics:
                topics.append(topic)
        return topics or ["Trade"]

    def _build_id(self, feed: str, link: str) -> str:
        raw = f"{feed}:{link}"
        return raw.replace("https://", "").replace("http://", "").replace("/", "-")[:120]

    def _text(self, item: ET.Element, tag: str) -> str:
        value = item.findtext(tag, default="")
        return value.strip()
