"""워드프레스에 초고를 '검토 대기' 글로 넣는다. REST API + 응용 프로그램 비밀번호."""
import os
import requests
from .config import CORNERS

SIGNATURE = {"최극형": "최극형 기자", "훈세김": "훈세김 기자", "린해박": "린해박 기자",
             "남새진": "남새진 기자", "다섯째 기자": "다섯째 기자"}


def render_post(corner_no: str, drafts: list[dict], lint_results: list[list[str]], seed: str, seed_url: str) -> tuple[str, str, str]:
    """초고 2편을 한 글에 담는다. 편집장이 한 편을 고르고 나머지를 지운다."""
    reporter = CORNERS[corner_no][2]
    parts = []
    for i, (d, probs) in enumerate(zip(drafts, lint_results), start=1):
        tag = "가" if i == 1 else "나"
        parts.append(f'<!-- wp:paragraph {{"className":"bg-draft-label"}} -->\n<p class="bg-draft-label"><strong>초고 {tag}</strong> · {d["title"]}'
                     + (f' · <span class="bg-red">검사: {", ".join(probs)}</span>' if probs else "") + "</p>\n<!-- /wp:paragraph -->")
        parts.append("<!-- wp:html -->\n" + d["body_html"] + "\n<!-- /wp:html -->")
        parts.append(f'<!-- wp:paragraph {{"className":"bg-byline"}} -->\n<p class="bg-byline">{SIGNATURE[reporter]} / 편집 박멀미</p>\n<!-- /wp:paragraph -->')
        parts.append(f'<!-- wp:paragraph {{"className":"bg-seed"}} -->\n<p class="bg-seed">이 글이 시작된 자리 — {d["seed_line"]} <a href="{seed_url}">출처</a></p>\n<!-- /wp:paragraph -->')
        if d.get("editor_note"):
            parts.append(f'<!-- wp:paragraph {{"className":"bg-note"}} -->\n<p class="bg-note">편집장 주석: {d["editor_note"]}</p>\n<!-- /wp:paragraph -->')
        if i == 1:
            parts.append("<!-- wp:separator -->\n<hr class=\"wp-block-separator\"/>\n<!-- /wp:separator -->")
    content = "\n\n".join(parts)
    title = drafts[0]["title"]
    excerpt = drafts[0]["excerpt"]
    return title, content, excerpt


def publish_pending(corner_no: str, title: str, content: str, excerpt: str, seed: str, seed_url: str) -> dict:
    base = os.environ["WP_URL"].rstrip("/")
    auth = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
    cat_id = CORNERS[corner_no][1]
    payload = {
        "title": title, "content": content, "excerpt": excerpt,
        "status": "pending", "categories": [cat_id],
        "meta": {"corner": corner_no, "seed": seed, "seed_url": seed_url},
    }
    r = requests.post(f"{base}/wp-json/wp/v2/posts", json=payload, auth=auth, timeout=60)
    r.raise_for_status()
    return r.json()
