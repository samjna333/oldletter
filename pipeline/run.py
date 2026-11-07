"""실행기.
  python -m pipeline.run --corner 01 --seed "..." --url "..."        한 건
  python -m pipeline.run --inbox seeds/inbox.json                      대기함 전부
  --dry-run : API 호출·발행 없이 프롬프트만 drafts/ 에 저장
  --no-publish : 초고는 만들되 워드프레스에 넣지 않음 (drafts/ 에 저장)
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from .config import DRAFTS_DIR, CORNERS
from .prompts import build_system, build_user
from .lint import lint


def process(item: dict, dry_run: bool, no_publish: bool) -> dict:
    corner = item["corner"]
    seed, url = item["seed"], item.get("url", "")
    req = item.get("editor_request", "")
    extra = item.get("extra")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = DRAFTS_DIR / f"{stamp}-{corner}.json"
    DRAFTS_DIR.mkdir(exist_ok=True)

    if dry_run:
        out.write_text(json.dumps({"system": build_system(corner), "user": build_user(corner, seed, url, req, extra)},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        return {"corner": corner, "dry_run": str(out)}

    from .write import write_drafts
    from .publish import render_post, publish_pending
    data = write_drafts(corner, seed, url, req, extra)
    results = [lint(corner, d["body_html"]) for d in data["drafts"]]
    data["lint"] = results
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = {"corner": corner, "titles": [d["title"] for d in data["drafts"]], "lint": results,
               "usage": data["_usage"], "saved": str(out)}
    if no_publish:
        return summary
    title, content, excerpt = render_post(corner, data["drafts"], results, seed, url)
    post = publish_pending(corner, title, content, excerpt, seed, url)
    summary["post_id"] = post.get("id")
    summary["edit_link"] = f'{post.get("link", "")}'
    return summary


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--corner", choices=sorted(CORNERS))
    p.add_argument("--seed")
    p.add_argument("--url", default="")
    p.add_argument("--request", default="", help="편집장 재작성 지시")
    p.add_argument("--inbox", help="씨앗 대기함 JSON (목록)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-publish", action="store_true")
    a = p.parse_args(argv)

    items = []
    if a.inbox:
        items = json.loads(Path(a.inbox).read_text(encoding="utf-8"))
    elif a.corner and a.seed:
        items = [{"corner": a.corner, "seed": a.seed, "url": a.url, "editor_request": a.request}]
    else:
        p.error("--corner 와 --seed, 또는 --inbox 가 필요합니다")

    ok = True
    for item in items:
        try:
            print(json.dumps(process(item, a.dry_run, a.no_publish), ensure_ascii=False))
        except Exception as e:  # 한 건 실패해도 다음 건 진행
            ok = False
            print(json.dumps({"corner": item.get("corner"), "error": str(e)}, ensure_ascii=False), file=sys.stderr)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
