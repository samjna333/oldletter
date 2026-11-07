"""기자 호출: Claude API 로 초고 2편을 구조화된 JSON 으로 받는다."""
import json
import anthropic
from .config import MODEL
from .prompts import build_system, build_user

DRAFT_SCHEMA = {
    "type": "object",
    "properties": {
        "drafts": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body_html": {"type": "string"},
                    "excerpt": {"type": "string"},
                    "seed_line": {"type": "string"},
                    "editor_note": {"type": "string"},
                },
                "required": ["title", "body_html", "excerpt", "seed_line", "editor_note"],
                "additionalProperties": False,
            },
        },
        "self_check": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["drafts", "self_check"],
    "additionalProperties": False,
}


class WriteError(RuntimeError):
    pass


def write_drafts(corner_no: str, seed: str, seed_url: str, editor_request: str = "",
                 extra: dict | None = None, client: anthropic.Anthropic | None = None) -> dict:
    client = client or anthropic.Anthropic()
    system = build_system(corner_no)
    user = build_user(corner_no, seed, seed_url, editor_request, extra)
    try:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "high", "format": {"type": "json_schema", "schema": DRAFT_SCHEMA}},
            # 강령·기자·코너 설계서는 호출마다 같으므로 시스템 프롬프트 끝에 캐시 경계
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.RateLimitError as e:
        raise WriteError(f"속도 제한. {e.response.headers.get('retry-after', '60')}초 뒤 재시도") from e
    except anthropic.APIStatusError as e:
        raise WriteError(f"API 오류 {e.status_code}: {e.message}") from e
    except anthropic.APIConnectionError as e:
        raise WriteError("네트워크 오류") from e

    if response.stop_reason == "refusal":
        detail = response.stop_details.category if response.stop_details else "?"
        raise WriteError(f"모델이 거절함 (분류: {detail}). 씨앗을 바꾸거나 편집장 확인")
    if response.stop_reason == "max_tokens":
        raise WriteError("출력이 잘림. max_tokens 를 올리거나 분량을 줄일 것")

    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    data["_usage"] = {
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "cache_read": getattr(response.usage, "cache_read_input_tokens", 0),
        "model": response.model,
    }
    return data
