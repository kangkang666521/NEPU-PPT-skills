#!/usr/bin/env python3
"""Collect public web text and image candidates for a NEPU PPT workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import ipaddress
import json
import mimetypes
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; nepu-ppt-template-skill/1.0; "
    "+https://github.com/kangkang666521/NEPU-PPT-skills)"
)
DEFAULT_MAX_PAGE_BYTES = 10 * 1024 * 1024
DEFAULT_MAX_IMAGE_BYTES = 20 * 1024 * 1024

# HTML tags whose text content we collect
TEXT_TAGS = {"title", "h1", "h2", "h3", "p", "li", "a"}


def slugify(value: str, fallback: str = "page") -> str:
    value = urllib.parse.urlparse(value).netloc + urllib.parse.urlparse(value).path
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return value[:80] or fallback


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._captures: list[tuple[str, list[str]]] = []
        self.headings: list[dict[str, str]] = []
        self.paragraphs: list[str] = []
        self.images: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): v or "" for k, v in attrs}
        tag = tag.lower()
        if tag in TEXT_TAGS:
            self._captures.append((tag, []))
        if tag == "img":
            src = attrs_dict.get("src", "")
            if src and not src.startswith("data:"):
                self.images.append(
                    {
                        "src": src,
                        "alt": normalize_text(attrs_dict.get("alt", "")),
                        "title": normalize_text(attrs_dict.get("title", "")),
                    }
                )

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self._captures) - 1, -1, -1):
            capture_tag, buffer = self._captures[index]
            if capture_tag != tag:
                continue
            text = normalize_text("".join(buffer))
            if text:
                if tag == "title" and not self.title:
                    self.title = text
                elif tag in {"h1", "h2", "h3"}:
                    self.headings.append({"level": tag, "text": text})
                elif tag in {"p", "li"}:
                    self.paragraphs.append(text)
                elif tag == "a":
                    self.links.append({"text": text})
            del self._captures[index]
            break

    def handle_data(self, data: str) -> None:
        for _tag, buffer in self._captures:
            buffer.append(data)


def validate_public_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Only public http/https URLs are supported: {url}")
    hostname = (parsed.hostname or "").lower()
    if hostname == "localhost" or hostname.endswith(".localhost") or hostname.endswith(".local"):
        raise ValueError(f"Local/private hosts are not supported: {url}")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        address = None
    if address and (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_unspecified
    ):
        raise ValueError(f"Local/private IP addresses are not supported: {url}")
    return url


def fetch(
    url: str,
    user_agent: str,
    timeout: int = 30,
    max_bytes: int = DEFAULT_MAX_PAGE_BYTES,
) -> tuple[bytes, str]:
    validate_public_url(url)
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        validate_public_url(response.geturl())
        content_type = response.headers.get("Content-Type", "")
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > max_bytes:
            raise ValueError(
                f"Download exceeds limit ({int(content_length)} > {max_bytes} bytes): {url}"
            )
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"Download exceeds limit ({max_bytes} bytes): {url}")
        return body, content_type


def decode_html(body: bytes, content_type: str) -> str:
    charset_match = re.search(r"charset=([\w.-]+)", content_type, flags=re.I)
    encodings = [charset_match.group(1)] if charset_match else []
    encodings += ["utf-8", "gb18030", "latin-1"]
    for encoding in encodings:
        try:
            return body.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return body.decode("utf-8", errors="replace")


def choose_extension(url: str, content_type: str, default: str = ".bin") -> str:
    path_ext = Path(urllib.parse.urlparse(url).path).suffix
    if path_ext and len(path_ext) <= 8:
        return path_ext
    guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
    return guessed or default


def download_image(
    url: str,
    dest_dir: Path,
    user_agent: str,
    index: int,
    timeout: int,
    max_bytes: int,
) -> dict[str, str]:
    body, content_type = fetch(url, user_agent, timeout, max_bytes)
    if not content_type.lower().startswith("image/"):
        raise ValueError(f"URL did not return an image ({content_type or 'unknown type'}): {url}")
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or choose_extension(
        url, content_type, ".img"
    )
    filename = f"web-image-{index:02d}-{digest}{ext}"
    target = dest_dir / filename
    target.write_bytes(body)
    return {
        "url": url,
        "local_path": str(target),
        "content_type": content_type,
        "bytes": str(len(body)),
    }


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"sources": []}


def append_markdown(path: Path, record: dict) -> None:
    """Append a source record to the markdown log using efficient append I/O."""
    lines = [
        "",
        f"## {record.get('title') or record['url']}",
        "",
        f"- URL: {record['url']}",
        f"- Accessed: {record['accessed_at']}",
        f"- Saved page: `{record['saved_page']}`",
        f"- Usage decision: review before slide insertion",
        "",
        "### Headings",
        "",
    ]
    for heading in record.get("headings", [])[:12]:
        lines.append(f"- {heading['level']}: {heading['text']}")
    lines += ["", "### Text Snippets", ""]
    for paragraph in record.get("paragraphs", [])[:20]:
        lines.append(f"- {paragraph}")
    lines += ["", "### Image Candidates", ""]
    for image in record.get("images", [])[:20]:
        local = image.get("local_path", "")
        local_part = f" -> `{local}`" if local else ""
        alt = f" | alt: {image.get('alt')}" if image.get("alt") else ""
        lines.append(f"- {image['url']}{local_part}{alt}")
    # Use append mode to avoid reading the entire file on each write
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def format_error(exc: Exception) -> str:
    """Extract a concise error message from common HTTP/fetch exceptions."""
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}: {exc.reason}"
    return str(exc)


def collect_url(args: argparse.Namespace, workspace: Path, url: str, index: int) -> dict:
    web_dir = workspace / "assets" / "web"
    page_dir = web_dir / "pages"
    image_dir = web_dir / "images"
    page_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    body, content_type = fetch(url, args.user_agent, args.timeout, args.max_page_bytes)
    if content_type and not (
        content_type.lower().startswith("text/html")
        or content_type.lower().startswith("application/xhtml+xml")
        or content_type.lower().startswith("text/plain")
    ):
        raise ValueError(f"URL did not return an HTML/text page ({content_type}): {url}")
    text = decode_html(body, content_type)
    parser = PageParser()
    parser.feed(text)

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = slugify(url, f"source-{index:02d}")
    page_name = f"{timestamp}-{index:02d}-{slug}.html"
    page_path = page_dir / page_name
    page_path.write_text(text, encoding="utf-8", errors="replace")

    images = []
    seen_images: set[str] = set()
    for img in parser.images:
        absolute = urllib.parse.urljoin(url, img["src"])
        if absolute in seen_images:
            continue
        seen_images.add(absolute)
        item: dict[str, str] = {"url": absolute, "alt": img.get("alt", ""), "title": img.get("title", "")}
        if args.download_images and len(images) < args.max_images:
            try:
                item.update(
                    download_image(
                        absolute,
                        image_dir,
                        args.user_agent,
                        len(images) + 1,
                        args.timeout,
                        args.max_image_bytes,
                    )
                )
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                item["download_error"] = format_error(exc)
        images.append(item)
        if len(images) >= args.max_images and not args.list_all_images:
            break

    return {
        "url": url,
        "accessed_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "content_type": content_type,
        "title": parser.title,
        "saved_page": str(page_path),
        "headings": parser.headings[: args.max_text],
        "paragraphs": parser.paragraphs[: args.max_text],
        "images": images,
        "usage_note": "Review copyright, source authority, and deck use case before inserting into slides.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path, help="Task workspace created by create_workspace.py")
    parser.add_argument("urls", nargs="+", help="Public page URLs to collect")
    parser.add_argument("--download-images", action="store_true", help="Download image candidates")
    parser.add_argument("--list-all-images", action="store_true", help="Keep all image URLs in the manifest")
    parser.add_argument("--max-images", type=int, default=12)
    parser.add_argument("--max-text", type=int, default=80)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-page-bytes", type=int, default=DEFAULT_MAX_PAGE_BYTES)
    parser.add_argument("--max-image-bytes", type=int, default=DEFAULT_MAX_IMAGE_BYTES)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    args = parser.parse_args()
    for name in ("max_images", "max_text", "timeout", "max_page_bytes", "max_image_bytes"):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be at least 1")

    workspace = args.workspace.resolve()
    (workspace / "planning").mkdir(parents=True, exist_ok=True)
    (workspace / "assets" / "web").mkdir(parents=True, exist_ok=True)
    markdown_path = workspace / "planning" / "web-sources.md"
    manifest_path = workspace / "assets" / "web" / "sources.json"
    if not markdown_path.exists():
        markdown_path.write_text("# Web Sources\n\n", encoding="utf-8")

    manifest = load_manifest(manifest_path)
    success_count = 0
    fail_count = 0
    for index, url in enumerate(args.urls, start=1):
        try:
            record = collect_url(args, workspace, url, index)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            error_msg = format_error(exc)
            print(json.dumps({"url": url, "error": error_msg}, ensure_ascii=False), file=sys.stderr)
            manifest.setdefault("sources", []).append(
                {"url": url, "error": error_msg, "accessed_at": dt.datetime.now().astimezone().isoformat(timespec="seconds")}
            )
            fail_count += 1
            continue
        manifest.setdefault("sources", []).append(record)
        append_markdown(markdown_path, record)
        print(json.dumps({"url": url, "title": record.get("title"), "images": len(record["images"])}, ensure_ascii=False))
        success_count += 1

    manifest_tmp = manifest_path.with_suffix(".json.tmp")
    manifest_tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_tmp.replace(manifest_path)
    print(json.dumps({"success": success_count, "failed": fail_count, "total": len(args.urls)}, ensure_ascii=False), file=sys.stderr)
    return 1 if fail_count == len(args.urls) else 0


if __name__ == "__main__":
    raise SystemExit(main())
