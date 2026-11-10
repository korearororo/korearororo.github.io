"""Public portfolio with one concrete view of each kind of work."""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve()
REPO = HERE.parents[1]
OUT = REPO / "assets" / "portfolio" / "han-jinwoo-portfolio-v5-20261110.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", "C:/Windows/Fonts/malgunbd.ttf"))
pdfmetrics.registerFont(TTFont("Batang", "C:/Windows/Fonts/HANBatang.ttf"))

W, H = 595.28, 841.89
PAPER = HexColor("#f8f6f1")
INK = HexColor("#242923")
MUTED = HexColor("#5c625c")
GOLD = HexColor("#896f49")
RULE = HexColor("#d8d3c8")
WHITE = HexColor("#fffefa")

c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
c.setTitle("한진우 | 개발 포트폴리오")
c.setAuthor("한진우")
c.setSubject("팀 프로젝트, 개인 앱, 실무에서 맡은 개발 경험")


def text(x, y, s, size=10, bold=False, color=INK, font=None):
    c.setFillColor(color)
    c.setFont(font or ("MalgunBold" if bold else "Malgun"), size)
    c.drawString(x, y, s)


def lines(s, width, size, font="Malgun"):
    out, current = [], ""
    for word in s.split():
        candidate = word if not current else current + " " + word
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
            continue
        if current:
            out.append(current)
            current = ""
        if pdfmetrics.stringWidth(word, font, size) <= width:
            current = word
            continue
        for char in word:
            if current and pdfmetrics.stringWidth(current + char, font, size) > width:
                out.append(current)
                current = char
            else:
                current += char
    if current:
        out.append(current)
    return out


def para(x, y, s, width, size=10, leading=18, color=INK, bold=False):
    font = "MalgunBold" if bold else "Malgun"
    for line in lines(s, width, size, font):
        text(x, y, line, size, bold, color)
        y -= leading
    return y


def bar(y, x1=44, x2=W-44, color=RULE):
    c.setLineWidth(.65)
    c.setStrokeColor(color)
    c.line(x1, y, x2, y)


def rect(x, y, w, h, fill=WHITE, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    c.rect(x, y, w, h, fill=1, stroke=bool(stroke))


def link(x, y, w, h, url):
    c.linkURL(url, (x, y, x+w, y+h), relative=0)


def page(no, kind, project):
    rect(0, 0, W, H, PAPER)
    text(44, H-39, "한진우", 11, True)
    text(113, H-39, "개발 포트폴리오", 9, color=MUTED)
    text(W-135, H-39, "2026.11.10", 8, color=MUTED)
    bar(H-54)
    text(44, 37, "korearororo.github.io", 8.5, color=GOLD)
    link(44, 29, 145, 18, "https://korearororo.github.io/")
    text(W-167, 37, f"{kind}  /  {no:02d} · 03", 8, color=MUTED)
    bar(57)
    text(44, H-94, project, 9, True, GOLD)


def label(x, y, value):
    text(x, y, value, 8.5, True, GOLD)


def text_link(x, y, label_text, url):
    text(x, y, label_text + "  ↗", 9.5, True, GOLD)
    link(x, y-8, 400, 23, url)


# 01 / team work.
page(1, "팀 프로젝트", "OPENMATH  ·  3인 팀 / 2026.03–06")
text(44, H-144, "문제 생성에 쓸", 25, font="Batang")
text(44, H-182, "참고 문항 검색", 25, font="Batang")
para(44, H-216,
     "OpenMath는 수학 문제를 만드는 팀 프로젝트입니다. 저는 새 문제를 만들기 전 참고 문항을 학년과 단원에 맞게 찾는 기능, 정답 비교, 문항 선택 화면을 맡았습니다.",
     W-88, 10.7, 20)

bar(550)
label(44, 525, "공개 자료로 실행한 검색")
rect(44, 330, W-88, 170, HexColor("#efede7"))
text(61, 476, "요청", 9, color=MUTED)
text(130, 476, "중3 · 이차방정식 · 단답형 · 쉬움", 11, True)
bar(461, 61, W-61)
text(61, 430, "문항 01", 9, color=MUTED)
text(161, 424, "x² − 5x + 6 = 0", 19, font="Batang")
bar(406, 61, W-61)
text(61, 373, "문항 02", 9, color=MUTED)
text(161, 367, "x² − 4x + 4 = 0", 19, font="Batang")
para(44, 309, "팀 검색 코드와 공개 예시 문항 7개로 실행했습니다. 전체 검색 품질을 평가한 결과는 아닙니다.", W-88, 8.5, 16, MUTED)

bar(264)
label(44, 240, "제가 맡은 일")
para(44, 215,
     "형식이 다른 문항 파일을 공통 형식으로 읽고 학교급·학년·단원·유형·난이도로 후보를 좁혔습니다. 남은 문항은 텍스트 점수와 ID로 정렬했습니다. 수식의 기호 표기 차이를 처리하는 정답 비교와 기준 문항 선택 화면도 수정했습니다.",
     W-88, 9.7, 18)
para(44, 135, "검색·정답 검증·문항 선택 화면의 변경은 팀 코드에 병합됐습니다.", W-88, 8.5, 16, MUTED)
text_link(44, 89, "실행 결과와 코드 보기", "https://korearororo.github.io/projects/openmath.html#comparison")
c.showPage()


# 02 / personal work: actual interface is allowed to carry the page.
page(2, "개인 앱", "POKECHI  ·  초기 독립 앱 2026.09.24–29 / 이후 보강")
text(44, H-144, "타이핑으로 자라는", 25, font="Batang")
text(44, H-182, "Windows 앱", 25, font="Batang")
para(44, H-216,
     "타이핑 횟수에 따라 포켓몬이 부화·성장하고 기록이 도감에 남는 Windows 앱을 만들었습니다. VS Code 확장의 아이디어와 자산을 활용했고, 앱을 다시 열어도 성장 기록이 이어집니다.",
     W-88, 10.7, 20)

poster = ImageReader(str(REPO / "assets" / "pokechi-demo-poster.jpg"))
rect(44, 325, W-88, 231, HexColor("#242923"))
c.drawImage(poster, 44, 325, W-88, 231, preserveAspectRatio=True, anchor="c", mask="auto")
text(44, 305, "실제 앱 실행 화면 · 44초 영상에서 입력, 부화, 도감, 재실행 복원을 볼 수 있습니다.", 8.5, color=MUTED)

bar(283)
label(44, 261, "독립 앱 이후")
para(44, 237,
     "저장 형식이 바뀌어도 진행이 남도록 백업과 변환을 넣었습니다. 이후 Google 로그인과 Supabase 동기화를 추가했습니다. 계정·모드별 기록을 분리하고 저장 내용이 충돌해도 진행 기록을 보존하도록 병합했습니다.",
     W-88, 9.8, 18)
para(44, 145,
     "영상은 로컬 기능만 보여줍니다. 서버 통신은 같은 PC의 독립 클라이언트에서 확인했고, 서로 다른 물리 PC에서의 설치·동기화는 아직 검증하지 않았습니다.",
     W-88, 8.5, 16, MUTED)
text_link(44, 85, "실제 실행 영상 보기", "https://korearororo.github.io/projects/pokechi.html#demo")
c.showPage()


# 03 / work: two workstreams, each with its own purpose and scope.
page(3, "실무", "유동산  ·  연구개발부문 매니저 / 2026.09–현재")
text(44, H-144, "공시 보고서와", 25, font="Batang")
text(44, H-182, "부동산 조사 도구", 25, font="Batang")
para(44, H-216,
     "유동산 연구개발부문에서 기업 공시 기반 AI 보고서의 검증 흐름을 보완하고, 부동산 조사 자료를 조회·정리하는 로컬 도구를 개발했습니다.",
     W-88, 10.7, 20)

bar(540)
text(44, 508, "공시 기반 AI 보고서", 17, True)
para(44, 475,
     "기존 시스템이 만든 보고서의 수치와 판단을 공시 원문과 대조했습니다. 이전 추이가 없는 자료에 ‘회복’이라고 쓰는 경우처럼 근거가 부족한 표현을 다시 검토하도록 기준을 정리했습니다. 문체를 고친 뒤에도 의미가 유지되는지 확인하는 흐름을 보완했습니다.",
     W-88, 9.9, 18)
para(44, 377,
     "같은 입력으로 교정 전후를 대조하고 모델·추론 설정별 누락과 처리 시간도 비교했습니다.",
     W-88, 9.3, 17, MUTED)

bar(323)
text(44, 290, "부동산 조사 도구", 17, True)
para(44, 257,
     "조사 대상 주변의 거래를 기간·반경·유형으로 찾는 기능을 구현·보완했습니다. 실거래가, 건축물대장, KB 정보를 읽어 면적 기준을 맞추고 비교표와 지도 보고서로 내보냅니다. 과거 개별 실거래와 현재 평균 호가는 구분해 표시했습니다.",
     W-88, 9.9, 18)

bar(151)
para(44, 132,
     "보고서 원문과 고객 정보 등 내부 자료는 제외했습니다.",
     W-88, 8.5, 16, MUTED)
text_link(44, 85, "맡은 작업 자세히 보기", "https://korearororo.github.io/projects/youdongsan.html#report")
c.showPage()
c.save()
print(OUT)
