"""부고란 홈 페이지·푸터 콘텐츠 블록의 WPBakery 단축코드를 만든다.

사용: python3 design/build_home.py
결과: design/out/home.txt (홈 본문), footer.txt (푸터 콘텐츠 블록 ID 179780), home.css (추가 CSS에 합침)
홈 전용 CSS는 홈 첫 줄의 raw html 안에, 푸터 CSS는 푸터 블록 안에 들어간다.
그래서 이 부분을 바꿀 때는 추가 CSS를 다시 붙여 넣을 필요가 없다.
"""
import base64
import urllib.parse
from pathlib import Path

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

INK, INK2, RULE, RED, SOFT, PAPER = "#2B2924", "#6E6A60", "#E4DED0", "#D9532F", "#F4EFE4", "#FBF8F1"

_sid = [811000]


def sid():
    _sid[0] += 1
    return _sid[0]


def raw(html):
    """vc_raw_html 은 rawurlencode 후 base64 로 저장한다."""
    enc = base64.b64encode(urllib.parse.quote(html, safe="").encode()).decode()
    return f'[vc_raw_html uncode_shortcode_id="{sid()}"]{enc}[/vc_raw_html]'


def row(inner, top=2, bottom=2, cls="", h=2):
    el = f' el_class="{cls}"' if cls else ""
    return (f'[vc_row row_height_percent="0" override_padding="yes" h_padding="{h}" top_padding="{top}" bottom_padding="{bottom}" '
            f'overlay_alpha="100" gutter_size="4" column_width_percent="100" shift_y="0" z_index="0" style="inherited"{el} '
            f'uncode_shortcode_id="{sid()}"]{inner}[/vc_row]')


def col(inner, w="1/1", cls=""):
    el = f' el_class="{cls}"' if cls else ""
    return (f'[vc_column column_width_percent="100" gutter_size="3" overlay_alpha="100" shift_x="0" shift_y="0" shift_y_down="0" '
            f'z_index="0" medium_width="0" mobile_width="0" width="{w}"{el} uncode_shortcode_id="{sid()}"]{inner}[/vc_column]')


def text(html, cls=""):
    el = f' el_class="{cls}"' if cls else ""
    return f'[vc_column_text{el} uncode_shortcode_id="{sid()}"]{html}[/vc_column_text]'


def index(el_id, loop, items, extra=""):
    return (f'[uncode_index el_id="{el_id}" index_type="css_grid" loop="{loop}" {extra} '
            f'screen_lg_breakpoint="960" screen_md_breakpoint="570" screen_sm_breakpoint="480" '
            f'post_items="{items}" single_border="yes" uncode_shortcode_id="{sid()}"]')


# ---------- 홈 전용 스타일 + 발행일 띠 ----------
HOME_CSS = f"""
<style>
/* 발행일 띠 */
.bg-dateline{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 18px;padding:10px 0;border-top:1px solid {INK};border-bottom:1px solid {RULE};font-size:13px;letter-spacing:.04em;color:{INK2}}}
.bg-dateline b{{color:{RED};font-weight:400}}
/* 섹션 공통 머리 */
.bg-kicker{{display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-top:2px solid {INK};padding-top:12px;margin-bottom:18px}}
.bg-kicker h3{{margin:0!important;font-size:22px!important;font-weight:700!important;letter-spacing:-.01em}}
.bg-kicker span{{font-size:13px;color:{INK2}}}
.bg-kicker a{{font-size:13px;color:{RED}!important;white-space:nowrap}}
/* 면별로 읽기 띠 */
.bg-band{{background:{SOFT}!important}}
.bg-band .bg-sec .bg-kicker{{border-top-width:2px;margin-bottom:6px}}
.bg-band .bg-sec .bg-kicker h3{{font-size:18px!important}}
.bg-band .bg-sec .tmb{{border-bottom:1px solid {RULE}}}
.bg-band .bg-sec .tmb:last-child{{border-bottom:0}}
.bg-band .bg-sec .t-entry-title{{font-size:15px!important;line-height:1.5!important}}
.bg-band .bg-sec .t-entry-visual img{{border-radius:3px}}
@media (min-width:960px){{
  .bg-band .bg-sec + .bg-sec > .uncol{{border-left:1px solid {RULE};padding-left:28px}}
}}
/* 기자들 */
.bg-desk{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}}
.bg-desk a.bg-card{{display:flex;flex-direction:column;gap:8px;padding:18px 16px 16px;border:1px solid {RULE};border-radius:6px;background:#fff;color:{INK}!important;text-decoration:none;transition:border-color .2s,transform .2s}}
.bg-desk a.bg-card:hover{{border-color:{INK};transform:translateY(-2px)}}
.bg-card .bg-seal{{width:40px;height:40px;border:2px solid {RED};border-radius:50%;display:grid;place-items:center;color:{RED};font-weight:700;font-size:17px;transform:rotate(-6deg)}}
.bg-card b{{font-size:16px}}
.bg-card p{{margin:0!important;font-size:13.5px!important;line-height:1.6!important;color:{INK2}}}
.bg-card small{{font-size:12px;color:{RED};letter-spacing:.02em}}
@media (max-width:959px){{.bg-desk{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:480px){{.bg-desk{{grid-template-columns:1fr}}}}
/* 뉴스레터 띠 */
.bg-news{{background:{INK}!important}}
.bg-news, .bg-news p, .bg-news h3{{color:{PAPER}!important}}
.bg-news h3{{font-size:26px!important;font-weight:700!important;margin:0 0 8px!important}}
.bg-news p{{margin:0!important;font-size:15px!important;opacity:.8}}
.bg-news .bg-news__label{{font-size:12px;letter-spacing:.2em;color:{RED}!important;opacity:1}}
.bg-news .jetpack_subscription_widget .widgettitle,.bg-news #subscribe-text{{display:none}}
.bg-news #subscribe-email input,.bg-news input[type=email]{{background:transparent!important;border:1px solid rgba(251,248,241,.4)!important;color:{PAPER}!important;border-radius:4px}}
.bg-news input[type=email]::placeholder{{color:rgba(251,248,241,.55)}}
.bg-news form{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.bg-news form p{{margin:0!important}}
</style>
"""

DATELINE = (
    '<div class="bg-dateline"><span><b id="bg-issue">창간 준비호</b></span><span id="bg-date">2026년 11월 8일 일요일</span>'
    '<span>사라지는 것들의 소식</span></div>'
    '<script>(function(){var d=new Date();'
    'var s=d.toLocaleDateString("ko-KR",{timeZone:"Asia/Seoul",year:"numeric",month:"long",day:"numeric",weekday:"long"});'
    'document.getElementById("bg-date").textContent=s;'
    'var k=new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Seoul"}).format(d).split("-");'
    'var n=Math.round((Date.UTC(+k[0],+k[1]-1,+k[2])-Date.UTC(2026,10,7))/864e5);'
    'document.getElementById("bg-issue").textContent=n>0?"제"+n+"호":"창간 준비호";})();</script>'
)


def kicker(title, sub="", more=""):
    s = f"<span>{sub}</span>" if sub else ""
    m = f'<a href="{more}">더 보기 →</a>' if more else ""
    right = m or s
    return f'<div class="bg-kicker"><h3>{title}</h3>{right}</div>'


def section(title, cats, slug):
    idx = index(
        f"index-{slug}", f"size:3|order_by:date|post_type:post|categories:{cats}",
        "media|featured|onpost|original,category|nobg|relative|hide-icon,title",
        'grid_items="1" screen_lg_items="1" screen_md_items="1" screen_sm_items="1" gutter_size="1" '
        'single_text="lateral" single_image_size="4" css_grid_images_size="three-two" single_vertical_text="middle" '
        'single_padding="1" single_title_dimension="h6" single_title_weight="700"')
    return col(text(kicker(title, more=f"/category/{slug}/")) + idx, "1/3", "bg-sec")


REPORTERS = [
    ("최", "최극형", "choi-geukhyeong", "시립도서관 야간 열람실을 지키던 사서. 사람보다 사람이 남긴 물건을 먼저 본다.", "그날의 부고 · 산문시 · 인사란"),
    ("훈", "훈세김", "hun-segim", "은퇴한 해외 통신원. 냉소적이지만 다정하다.", "세 줄 뉴스 · 광고란 · 이달의 운세"),
    ("린", "린해박", "rin-haebak", "숫자를 다루던 일을 그만두고 숫자 뒤의 사람을 쓴다.", "숫자 하나의 에세이 · 일기예보"),
    ("남", "남새진", "nam-saejin", "정체를 밝히지 않는다. 사물의 목소리로만 말한다.", "사물의 편지 · 공고란 · 사물의 사설"),
    ("문", "문지기", "mun-jigi", "폐관한 극장의 영사기사. 현재형으로만 쓴다.", "낱말란 · 세시기 · 사진 없는 사진면"),
]


def desk():
    cards = "".join(
        f'<a class="bg-card" href="/tag/{slug}/"><span class="bg-seal">{ch}</span><b>{name}</b><p>{bio}</p><small>{beat}</small></a>'
        for ch, name, slug, bio, beat in REPORTERS)
    return kicker("부고란의 기자들", "초고는 기자 다섯이 쓰고, 편집장이 고릅니다") + f'<div class="bg-desk">{cards}</div>'


def build_home():
    parts = []
    # 1. 홈 전용 CSS + 발행일 띠
    parts.append(row(col(raw(DATELINE)), top=1, bottom=0))
    # 2. 메인 1편 (이미지 왼쪽)
    parts.append(row(col(index(
        "index-hero", "size:1|order_by:date|post_type:post",
        "media|featured|onpost|original,category|nobg|relative|hide-icon,title,text|excerpt|160,date",
        'grid_items="1" screen_lg_items="1" screen_md_items="1" screen_sm_items="1" gutter_size="3" '
        'single_text="lateral" css_grid_images_size="three-two" single_image_size="6" single_vertical_text="middle" '
        'single_padding="3" single_title_dimension="h2" single_title_weight="700"'))))
    # 3. 최신 소식 8편
    parts.append(row(col(text(kicker("최신 소식", "새로 도착한 부고와 소식")) + index(
        "index-latest", "size:8|order_by:date|post_type:post",
        "media|featured|onpost|original,category|nobg|relative|hide-icon,title,text|excerpt|60,date",
        'screen_lg_items="4" screen_md_items="2" screen_sm_items="1" gutter_size="3" offset="1" '
        'css_grid_images_size="three-two" single_padding="1" single_title_dimension="h5" single_title_weight="700"')), top=1))
    # 4. 면별로 읽기 (옅은 띠)
    parts.append(row(col(text(kicker("면별로 읽기", "신문의 면을 빌려 씁니다"))), top=4, bottom=0, cls="bg-band"))
    parts.append(row(section("1면", "15,16,17,18", "front") + section("세계면", "22", "world") + section("문화면", "28,29,30,31,32,33", "culture"),
                     top=1, bottom=1, cls="bg-band"))
    parts.append(row(section("생활면", "34,35,36", "life") + section("과학면", "25,26,27,24", "science") + section("사회·인사", "19,20,21,37", "society"),
                     top=1, bottom=4, cls="bg-band"))
    # 5. 기자들
    parts.append(row(col(raw(desk())), top=4, bottom=4))
    # 6. 뉴스레터 띠
    left = text('<p class="bg-news__label">NEWSLETTER</p><h3>부고란 뉴스레터</h3>'
                '<p>매주 일요일 저녁, 한 주 동안 사라진 것들의 소식을 메일함으로 보냅니다.</p>')
    right = text('[jetpack_subscription_form title="" subscribe_text="" subscribe_button="구독하기" '
                 'subscribe_placeholder="이메일 주소" show_subscribers_total="false" show_only_email_and_button="true"]')
    parts.append(row(col(left, "7/12") + col(right, "5/12"), top=4, bottom=4, cls="bg-news"))
    return "".join(parts)


# ---------- 푸터 (콘텐츠 블록) ----------
FOOTER_CSS = f"""
<style>
.bg-foot{{background:{PAPER}!important;border-top:1px solid {INK}}}
.bg-foot, .bg-foot p, .bg-foot a{{color:{INK}}}
.bg-foot .bg-foot__brand{{font-size:40px;font-weight:700;letter-spacing:.04em;line-height:1}}
.bg-foot .bg-foot__tag{{display:inline-block;margin-top:10px;font-size:13px;letter-spacing:.24em;color:{RED}}}
.bg-foot .bg-foot__lead{{margin-top:18px!important;font-size:14px!important;line-height:1.8!important;color:{INK2}!important;max-width:28em}}
.bg-foot h4{{font-size:12px!important;letter-spacing:.2em;color:{INK2}!important;font-weight:400!important;margin:0 0 14px!important}}
.bg-foot ul{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.bg-foot ul.bg-2col{{grid-template-columns:1fr 1fr;column-gap:16px}}
.bg-foot li a{{font-size:14px;text-decoration:none}}
.bg-foot li a:hover{{color:{RED}}}
.bg-foot-bottom{{background:{PAPER}!important}}
.bg-foot-bottom .bg-foot__line{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 24px;border-top:1px solid {RULE};padding-top:18px;font-size:12.5px;color:{INK2}}}
</style>
"""


def footer_html_brand():
    return ('<div class="bg-foot__brand">부고란</div><span class="bg-foot__tag">사라지는 것들의 소식</span>'
            '<p class="bg-foot__lead">새 소식을 전하지 않습니다. 신문이 싣지 않았거나 실었다가 잊어버린 작은 것들을, 부고와 예보와 인사 발령의 모양으로 다시 씁니다.</p>')


def links(title, items, two=False):
    cls = ' class="bg-2col"' if two else ""
    lis = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in items)
    return f"<h4>{title}</h4><ul{cls}>{lis}</ul>"


def build_footer():
    sections = [("1면", "/category/front/"), ("사회면", "/category/society/"), ("세계면", "/category/world/"),
                ("경제면", "/category/economy/"), ("과학면", "/category/science/"), ("문화면", "/category/culture/"),
                ("생활면", "/category/life/"), ("인사면", "/category/people/"), ("편집장", "/category/editor/")]
    about = [("부고란 소개", "/about/"), ("편집 강령", "/code/"), ("기자들", "/reporters/"), ("편집장의 편지", "/category/editor/")]
    desk_links = [(name, f"/tag/{slug}/") for _, name, slug, _, _ in REPORTERS]
    top = row(col(raw(footer_html_brand()), "5/12")
              + col(raw(links("면", sections, two=True)), "3/12")
              + col(raw(links("부고란", about)), "2/12")
              + col(raw(links("기자", desk_links)), "2/12"),
              top=5, bottom=3, cls="bg-foot")
    bottom = row(col(raw('<div class="bg-foot__line"><span>© 2026 부고란 · bnote.kr</span>'
                         '<span>씨앗은 실제로 있던 것이고, 글은 지어낸 것입니다. 초안 단계에 AI 도구를 씁니다.</span></div>')),
                 top=0, bottom=3, cls="bg-foot-bottom")
    return top + bottom


if __name__ == "__main__":
    css = (HOME_CSS + FOOTER_CSS).replace("<style>", "").replace("</style>", "")
    (OUT / "home.css").write_text(css.strip() + "\n", encoding="utf-8")
    footer = build_footer()
    # 홈은 테마 공통 푸터를 숨기므로 푸터 콘텐츠 블록(ID 179780)을 끝에서 불러온다.
    (OUT / "home.txt").write_text(build_home() + '[uncode_block id="179780"]', encoding="utf-8")
    (OUT / "footer.txt").write_text(footer, encoding="utf-8")
    for f in ("home.txt", "footer.txt"):
        print(f, len((OUT / f).read_text(encoding="utf-8")))
