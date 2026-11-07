"""발행 전 자동 검사. 강령의 금지 표현·개인정보 패턴·분량."""
import re

BANNED = [
    (r"되새기게", "교훈형 마무리"),
    (r"우리 모두에게", "교훈형 마무리"),
    (r"생각해 보게 된다", "교훈형 마무리"),
    (r"것이다[.。」\"']?\s*$", "문장 끝 '것이다'"),
    (r"것이다\.", "문장 끝 '것이다'"),
    (r"일 것이다", "문장 끝 '것이다'"),
    (r"에 다름 아니", "번역투"),
    (r"에 있어서", "번역투"),
    (r"겹친다|겹쳤다|겹치는", "번역투 '겹치다'"),
    (r"슬펐다|아름다웠다|쓸쓸했다|외로웠다|행복했다", "감정 명명"),
    (r"(^|[^가-힣])우리(는|가|의|를|에게)", "주어 '우리'"),
    (r"소중함|평범한 하루", "금지 마무리(비역사)"),
]
PERSONAL = [
    (r"0\d{1,2}-\d{3,4}-\d{4}", "전화번호"),
    (r"\d{2,3}[가-힣]\d{4}", "차량번호"),
    (r"\d{6}-\d{7}", "주민번호"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "이메일"),
]
LIMITS = {  # 코너 번호: (최소, 최대) 글자 수, 태그 제외
    "01": (0, 400), "02": (400, 800), "03": (0, 200), "04": (0, 600), "05": (800, 1200),
    "06": (0, 300), "07": (0, 150), "09": (150, 300), "10": (0, 200), "11": (0, 300),
    "12": (0, 200), "13": (0, 400), "14": (0, 300), "15": (0, 300), "16": (0, 600),
    "17": (0, 300), "18": (0, 200), "21": (0, 600), "22": (500, 700), "23": (600, 900), "24": (0, 300),
}


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("&nbsp;", " ")


def lint(corner_no: str, body_html: str) -> list[str]:
    text = strip_tags(body_html)
    problems = []
    for pat, label in BANNED:
        if re.search(pat, text, re.M):
            problems.append(f"금지 표현: {label}")
    for pat, label in PERSONAL:
        if re.search(pat, text):
            problems.append(f"개인정보 의심: {label}")
    if body_html.count("bg-mark") > 1:
        problems.append("형광펜이 두 번 이상")
    if "어쩌면" in text and text.count("어쩌면") > 1:
        problems.append("'어쩌면' 반복")
    lo, hi = LIMITS.get(corner_no, (0, 10**6))
    n = len(re.sub(r"\s", "", text))
    if n < lo or n > hi:
        problems.append(f"분량 {n}자 (허용 {lo}~{hi})")
    return problems
