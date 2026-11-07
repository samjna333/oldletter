"""강령·기자·코너 설계서에서 시스템 프롬프트와 사용자 프롬프트를 조립한다."""
import re
from pathlib import Path
from .config import ROOT, CORNERS_DIR, CORNERS, EMPHASIS_CLASSES


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def reporter_section(name: str) -> str:
    """기자.md 에서 해당 기자의 설정 블록만 뽑는다."""
    text = _read(ROOT / "기자.md")
    key = "다섯째 기자" if name.startswith("다섯째") else name
    m = re.search(rf"^## {re.escape(key)}.*?(?=^## |\Z)", text, re.S | re.M)
    return m.group(0).strip() if m else ""


def instruction_block(corner_md: str) -> str:
    """코너 설계서의 '## 기자 지시문' 아래 코드 블록을 뽑는다."""
    m = re.search(r"## 기자 지시문.*?```(.*?)```", corner_md, re.S)
    return m.group(1).strip() if m else ""


def build_system(corner_no: str) -> str:
    fname, _, reporter, _ = CORNERS[corner_no]
    corner_md = _read(CORNERS_DIR / fname)
    emphasis = "\n".join(f"- `{k}`: {v}" for k, v in EMPHASIS_CLASSES.items())
    return "\n\n".join([
        "너는 창작 매체 '부고란'(사라지는 것들의 소식)의 기자다. 아래 강령, 기자 설정, 코너 설계서를 따른다.",
        "# 편집 강령\n" + _read(ROOT / "강령.md"),
        "# 기자 설정\n" + reporter_section(reporter),
        "# 코너 설계서\n" + corner_md,
        "# 출력 규칙\n"
        "- 초고를 정확히 2편 쓴다. 코너 설계서가 요구한 차이(사인·받는 이·꺾이는 방향 등)를 둘 사이에 둔다.\n"
        "- body_html 은 워드프레스 본문용 HTML 이다. 양식 코너는 형식 틀 그대로 <div class=\"bg-form ...\"> 안에 쓴다. 산문은 <p> 단위.\n"
        "- 강조 장치는 다음 클래스만 쓴다. 형광펜(bg-mark)은 한 편에 한 번.\n" + emphasis + "\n"
        "- body_html 에 서명, 씨앗 줄, 편집장 주석을 넣지 않는다. 그것은 별도 필드다.\n"
        "- excerpt 는 홈 카드에 보일 두 줄. 본문 첫 문장들에서 가져온다. 60자 이내.\n"
        "- seed_line 은 '이 글이 시작된 자리' 한 줄. 씨앗을 자기 말로. 출처 문장을 옮기지 않는다.\n"
        "- editor_note 는 편집장 주석 초안 한 줄. 필요 없으면 빈 문자열.\n"
        "- self_check 에는 강령의 금지 표현·금지 소재를 스스로 점검한 결과를 짧게 적는다.",
    ])


def build_user(corner_no: str, seed: str, seed_url: str, editor_request: str = "", extra: dict | None = None) -> str:
    fname = CORNERS[corner_no][0]
    corner_md = _read(CORNERS_DIR / fname)
    block = instruction_block(corner_md)
    values = {"seed": seed, "seed_url": seed_url, "editor_request": editor_request or "(없음)"}
    if extra:
        values.update(extra)
    for k, v in values.items():
        block = block.replace("{" + k + "}", str(v))
    return block
