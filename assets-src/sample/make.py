# -*- coding: utf-8 -*-
"""「살아있는 회사 소개서」 예시용 이미지 에셋 만들기.

HTML로 디자인한 뒤 헤드리스 Chrome으로 찍어 docs/assets/sample/ 에 저장한다.
문구는 원고 v2(2026-10-11)에서 가져왔다. 책 속 회사는 모두 가상 사례.
실행: python make.py   (Chrome, Pillow 필요, 인터넷 연결: 웹폰트)
"""
import os, subprocess, sys, tempfile, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'assets', 'sample'))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
TMP = tempfile.mkdtemp(prefix='sbassets_')
os.makedirs(OUT, exist_ok=True)

INK, GREEN, GOLD, PAPER, SUB = '#16201c', '#2f6b57', '#f0c35a', '#fffdf8', '#4a5752'

BASE = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&display=swap">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{font-family:Pretendard,'Malgun Gothic',sans-serif;word-break:keep-all;color:#16201c;-webkit-font-smoothing:antialiased}
.serif{font-family:'Noto Serif KR',serif}
.g{color:#2f6b57}.y{color:#f0c35a}
.ecg{display:block}
.page{background:#fffdf8;box-shadow:0 18px 40px rgba(0,0,0,.18),0 2px 6px rgba(0,0,0,.08);position:relative;overflow:hidden}
.tag{display:inline-block;background:#2f6b57;color:#fff;font-weight:800;border-radius:999px;padding:4px 12px;font-size:13px;letter-spacing:.5px}
mark{background:linear-gradient(transparent 55%%,#f6dc8f 55%%);color:inherit}
table{border-collapse:collapse;width:100%%}
%(css)s
</style></head><body>%(body)s<script>%(js)s</script></body></html>'''

ECG = '''<svg class="ecg" viewBox="0 0 400 110" width="%s" height="%s"><path d="M0 62 H170" stroke="rgba(255,255,255,.35)" stroke-width="3" stroke-dasharray="7 7" fill="none"/>
<path d="M170 62 H200 L214 30 L230 100 L248 6 L264 84 L276 62 H400" stroke="#f0c35a" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="400" cy="62" r="7" fill="#f0c35a"/></svg>'''


def shot(name, w, h, body, css='', js='', scale=2, fmt='jpg', q=86):
    html = BASE % dict(w=w, h=h, css=css, body=body, js=js)
    src = os.path.join(TMP, name + '.html')
    png = os.path.join(TMP, name + '.png')
    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=%s' % scale, '--window-size=%d,%d' % (w, h),
                    '--virtual-time-budget=8000', '--allow-file-access-from-files',
                    '--screenshot=' + png, 'file:///' + src.replace('\\', '/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    im = Image.open(png)
    if fmt == 'png':
        return im
    dst = os.path.join(OUT, name + '.' + fmt)
    im.convert('RGB').save(dst, quality=q, optimize=True, progressive=True)
    print('%-22s %4dx%-4d %4dKB' % (name + '.' + fmt, im.width, im.height, os.path.getsize(dst) // 1024))
    return dst


def url(name):
    return 'file:///' + os.path.join(OUT, name).replace('\\', '/')


# ---------- 1. 표지 ----------
COVER_CSS = '''
.cv{width:600px;height:860px;background:radial-gradient(120% 80% at 80% 0%,#2c4a3f 0%,#1d2b26 55%,#131d19 100%);color:#fff;padding:64px 56px;position:relative;overflow:hidden}
.cv .top{font-size:17px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,.7)}
.cv .ecgw{margin:84px -56px 26px 0}
.cv h1{font-size:76px;line-height:1.16;font-weight:900;letter-spacing:-2px}
.cv h2{font-size:25px;font-weight:600;color:#f0c35a;margin-top:26px;letter-spacing:-.3px}
.cv .one{position:absolute;left:56px;right:56px;bottom:118px;font-size:19px;line-height:1.65;color:rgba(255,255,255,.82)}
.cv .bot{position:absolute;left:56px;right:56px;bottom:56px;display:flex;justify-content:space-between;font-size:15px;font-weight:700;color:rgba(255,255,255,.6);letter-spacing:1px;border-top:1px solid rgba(255,255,255,.18);padding-top:18px}
.cv .ring{position:absolute;right:-140px;top:-140px;width:420px;height:420px;border-radius:50%;border:1px solid rgba(240,195,90,.18)}
.cv .ring2{position:absolute;right:-80px;top:-80px;width:300px;height:300px;border-radius:50%;border:1px solid rgba(240,195,90,.12)}
'''
COVER = '''<div class="cv"><div class="ring"></div><div class="ring2"></div>
<div class="top">작가 × 개발자 실전서</div>
<div class="ecgw">%s</div>
<h1 class="serif">살아있는<br>회사 소개서</h1>
<h2>고객을 팬으로 만드는 한 줄의 서사</h2>
<div class="one">장점만 나열하던 소개서를<br>고객이 끝까지 읽는 이야기로</div>
<div class="bot"><span>5부 13장 · 부록 7</span><span>빈칸 워크시트 13종</span></div></div>''' % (ECG % (544, 150))
shot('cover', 600, 860, COVER, COVER_CSS, fmt='jpg', q=90)

# ---------- 2. 첫 화면 배경 (위쪽에 실물, 아래는 글자 자리) ----------
HERO_CSS = '''
.h{width:860px;height:1000px;background:radial-gradient(90% 60% at 60% 22%,#33584a 0%,#1d2b26 52%,#111a16 100%);position:relative;overflow:hidden}
.bk{position:absolute;left:400px;top:70px;width:300px;height:430px;transform:perspective(1400px) rotateY(-24deg) rotateZ(2deg);box-shadow:-30px 40px 60px rgba(0,0,0,.55);border-radius:3px 8px 8px 3px;overflow:hidden}
.bk img{width:100%;height:100%;display:block}
.bk:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(255,255,255,.08) 6%,transparent 14%)}
.tab{position:absolute;left:120px;top:150px;width:300px;height:400px;background:#0c0f0e;border-radius:26px;padding:14px;box-shadow:0 40px 70px rgba(0,0,0,.6);transform:rotate(-7deg)}
.tab .sc{background:#fffdf8;width:100%;height:100%;border-radius:14px;padding:22px 20px;overflow:hidden}
.sc .tag{font-size:10px;padding:3px 9px}
.sc h5{font-size:17px;font-weight:900;margin:10px 0 12px}
.sc .r{border-top:1px solid #e3ddd0;padding:9px 0;font-size:11px;color:#4a5752;line-height:1.5}
.sc .r b{display:block;color:#16201c;font-size:11.5px;margin-bottom:3px}
.sc .ln{height:9px;border-bottom:1.5px solid #c9c2b2;margin-top:6px}
.sc .fill{font-family:'Noto Serif KR',serif;color:#2f6b57;font-size:12px;font-weight:700}
.note{position:absolute;background:#f0c35a;color:#16201c;font-weight:800;font-size:17px;padding:14px 16px;box-shadow:0 12px 24px rgba(0,0,0,.35);width:150px;line-height:1.35}
.fade{position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(180deg,rgba(17,26,22,0) 0%,rgba(17,26,22,.92) 45%,#111a16 100%)}
.glow{position:absolute;left:330px;top:30px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(240,195,90,.16),transparent 65%)}
'''
HERO = '''<div class="h"><div class="glow"></div>
<div class="tab"><div class="sc"><span class="tag">부록 A-1</span><h5>SB7 정리표</h5>
<div class="r"><b>① 주인공이 원하는 것</b><span class="fill">고객이 알아서 연락하는 홈페이지</span><div class="ln"></div></div>
<div class="r"><b>② 빌런</b><span class="fill">장점 나열</span><div class="ln"></div></div>
<div class="r"><b>③ 공감 한 문장</b><div class="ln"></div><div class="ln"></div></div>
<div class="r"><b>④ 계획 3단계</b><div class="ln"></div><div class="ln"></div></div>
<div class="r"><b>⑦ 성공 장면</b><div class="ln"></div></div></div></div>
<div class="bk"><img src="%s"></div>
<div class="note" style="left:640px;top:440px;transform:rotate(6deg)">우리 → 고객<br><small style="font-weight:600">주어 바꾸기</small></div>
<div class="note" style="left:60px;top:520px;transform:rotate(-5deg);background:#fffdf8">5초 테스트<br><small style="font-weight:600">답할 수 있나요?</small></div>
<div class="fade"></div></div>''' % url('cover.jpg')
shot('hero', 860, 1000, HERO, HERO_CSS, q=84)

# ---------- 3. 대표 이미지 슬라이드 (1200x675) ----------
SL_CSS = '''
.s{width:1200px;height:675px;position:relative;overflow:hidden;display:flex;align-items:center}
.d{background:radial-gradient(80% 90% at 75% 20%,#2c4a3f,#1d2b26 60%,#121b17);color:#fff}
.l{background:#fffdf8}
.k{font-size:20px;font-weight:800;letter-spacing:3px;color:#f0c35a;margin-bottom:22px}
.l .k{color:#2f6b57}
.H{font-size:64px;font-weight:900;line-height:1.22;letter-spacing:-2px}
.P{font-size:25px;line-height:1.6;margin-top:24px;color:rgba(255,255,255,.82)}
.l .P{color:#4a5752}
.foot{position:absolute;left:80px;right:80px;bottom:40px;font-size:15px;color:rgba(255,255,255,.5);display:flex;justify-content:space-between}
.l .foot{color:#8a8f88}
'''
s1 = '''<div class="s d" style="padding:0 80px"><div style="flex:1"><div class="k">작가 × 개발자 실전서</div>
<div class="H">우리 홈페이지,<br>5초 안에 <span class="y">답할 수</span><br>있나요?</div>
<div class="P">이 회사가 나에게 뭘 해 주는지.<br>장점만 나열한 소개서는 이 질문에 답하지 못합니다.</div></div>
<img src="%s" style="width:330px;box-shadow:-24px 30px 60px rgba(0,0,0,.55);transform:rotate(3deg);margin-left:40px">
<div class="foot"><span>살아있는 회사 소개서</span><span>전자책 + 빈칸 워크시트</span></div></div>''' % url('cover.jpg')
shot('slide1', 1200, 675, s1, SL_CSS, scale=1, q=88)

s2 = '''<div class="s l" style="padding:0 80px;flex-direction:column;align-items:stretch;justify-content:center">
<div class="k">같은 회사, 다른 첫 문장</div>
<div style="display:grid;grid-template-columns:1fr 70px 1fr;align-items:center;gap:10px">
<div style="background:#ece8df;border-radius:22px;padding:36px 34px"><div class="tag" style="background:#8a8f88">전</div>
<p style="font-size:27px;line-height:1.6;margin-top:16px;color:#4a5752">㈜정밀기계는 1995년 설립 이래 30년간 자동차 엔진 부품을 가공해 왔습니다.</p></div>
<div style="font-size:48px;color:#2f6b57;text-align:center;font-weight:900">→</div>
<div style="background:#1d2b26;border-radius:22px;padding:36px 34px;color:#fff"><div class="tag" style="background:#f0c35a;color:#16201c">후</div>
<p style="font-size:27px;line-height:1.6;margin-top:16px;font-weight:700">30년 동안 쌓은 가공 기록이 <span class="y">귀사의 다음 양산을 덜 불안하게</span> 만듭니다.</p></div></div>
<div style="font-size:22px;color:#4a5752;margin-top:34px;text-align:center">공식 4. 과거 → 미래 &nbsp;·&nbsp; 연혁은 남기고 의미를 더합니다</div>
<div class="foot"><span>책 Chapter 2 · 예시 회사는 가상 사례</span><span>살아있는 회사 소개서</span></div></div>'''
shot('slide2', 1200, 675, s2, SL_CSS, scale=1, q=88)

PARTS_TOC = [('제1부', '진단', '왜 아무도 읽지 않는가', '1~2'), ('제2부', '재료', '이유와 기원 서사', '3~4'),
             ('제3부', '설계', '고객을 영웅으로 만드는 SB7', '5~9'), ('제4부', '변신', '전후 비교와 숫자·문장', '10~11'),
             ('제5부', '확장', '여러 채널, 90일 실행', '12~13')]
s3 = '''<div class="s d" style="padding:0 80px"><div style="width:380px"><div class="k">5부 13장 + 부록 7</div>
<div class="H" style="font-size:54px">진단부터<br>90일 실행까지</div><div class="P" style="font-size:22px">읽는 순서대로 내 소개서가<br>한 장씩 고쳐집니다.</div></div>
<div style="flex:1;display:grid;gap:12px;margin-left:50px">%s
<div style="border:1.5px dashed rgba(240,195,90,.6);border-radius:16px;padding:16px 22px;font-size:20px;color:#f0c35a;font-weight:700">부록 A~G · 빈칸 워크시트 13종 · 점검표 3종 · 90일 캘린더</div></div>
<div class="foot"><span>살아있는 회사 소개서</span><span>목차</span></div></div>''' % ''.join(
    '<div style="display:flex;align-items:center;gap:18px;background:rgba(255,255,255,.07);border-radius:16px;padding:15px 22px">'
    '<b style="color:#f0c35a;font-size:17px;width:56px">%s</b><b style="font-size:25px;width:66px">%s</b>'
    '<span style="font-size:20px;flex:1;color:rgba(255,255,255,.85)">%s</span><span style="font-size:16px;color:rgba(255,255,255,.5)">Chapter %s</span></div>' % p
    for p in PARTS_TOC)
shot('slide3', 1200, 675, s3, SL_CSS, scale=1, q=88)

PARTS = [('A', '전자책 PDF', '5부 13장 + 부록 7개'), ('B', '빈칸 워크시트 13종', '편집 가능한 파일'),
         ('C', '점검표 3종', '자가진단·런칭·분기'), ('D', '금지어·주의어표', '표시광고 위험 표현'),
         ('E', '90일 실행 캘린더', '13주 할 일 표'), ('F', '스토리 빌더 작업 파일', '이 페이지를 만든 파일'),
         ('G', '1:1 첨삭 1회', '첫 화면 문장')]
s4 = '''<div class="s l" style="padding:0 70px;flex-direction:column;align-items:stretch;justify-content:center">
<div class="k" style="text-align:center">받는 것, 한눈에</div><div class="H" style="font-size:52px;text-align:center;margin-bottom:40px">읽고, 채우고, 점검하고, 고칩니다</div>
<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:12px">%s</div>
<div class="foot"><span>구성은 리워드마다 다릅니다 · 리워드 요약표 참고</span><span>살아있는 회사 소개서</span></div></div>''' % ''.join(
    '<div style="background:%s;color:%s;border-radius:18px;padding:22px 14px;text-align:center;min-height:300px;display:flex;flex-direction:column;align-items:center">'
    '<div style="width:64px;height:64px;border-radius:16px;margin:10px auto 22px;line-height:64px!important;background:%s;color:%s;font-size:28px;font-weight:900;line-height:52px">%s</div>'
    '<div style="font-size:22px;font-weight:900;line-height:1.35">%s</div><div style="font-size:16px;margin-top:8px;opacity:.75;line-height:1.45">%s</div></div>'
    % ((('#1d2b26', '#fff', '#f0c35a', '#16201c') if c in 'FG' else ('#eef2ef', '#16201c', '#2f6b57', '#fff')) + (c, n, d))
    for c, n, d in PARTS)
shot('slide4', 1200, 675, s4, SL_CSS, scale=1, q=88)

# ---------- 4. 저자 일러스트 (사진으로 바꿔 쓰기 전 임시) ----------
AV_CSS = '''.a{width:400px;height:300px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.a .c{width:170px;height:170px;border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative}'''
PEN = '<svg width="86" height="86" viewBox="0 0 24 24" fill="none" stroke="#16201c" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>'
CODE = '<svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="#f0c35a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/><path d="m14.5 4-5 16"/></svg>'
shot('author1', 400, 300, '<div class="a" style="background:#f2ede2"><div class="c" style="background:#f0c35a">%s</div>'
     '<div style="position:absolute;left:36px;bottom:30px;right:36px;height:2px;background:repeating-linear-gradient(90deg,#c9c2b2 0 10px,transparent 10px 18px)"></div></div>' % PEN, AV_CSS, q=88)
shot('author2', 400, 300, '<div class="a" style="background:#1d2b26"><div class="c" style="background:#2f6b57">%s</div>'
     '</div>' % CODE, AV_CSS, q=88)

# ---------- 5. 목차·내지 (책 펼침 일부) ----------
TP_CSS = '''.w{width:352px;height:360px;background:#e9e4d8;display:flex;align-items:center;justify-content:center}
.p{width:280px;height:330px;padding:30px 26px;font-size:10.5px;line-height:1.75;color:#33403a}
.p .ch{font-size:11px;font-weight:800;color:#2f6b57;letter-spacing:2px}
.p h3{font-size:22px;line-height:1.3;margin:10px 0 6px}
.p .sb{font-size:10.5px;color:#8a8f88;margin-bottom:14px}
.p .em{font-weight:800;color:#16201c;font-size:12.5px;margin:6px 0}
.p .bx{background:#eef2ef;border-radius:8px;padding:10px 12px;margin-top:10px}
.p .pn{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-size:9px;color:#aaa}
.p td,.p th{border-bottom:1px solid #e3ddd0;padding:5px 4px;font-size:9px;vertical-align:top;text-align:left;line-height:1.5}
.p th{background:#2f6b57;color:#fff;font-weight:700}
.p td:first-child{white-space:nowrap}'''
shot('toc1', 352, 360, '''<div class="w"><div class="page p"><div class="ch">CHAPTER 1</div><h3 class="serif">회사 소개서의 부고장</h3>
<div class="sb">당신의 회사 소개서는 지금 이 순간에도 죽어가고 있습니다</div>
<p>과장이라고요?</p><p>고객은 그걸 몇 초 만에 판단합니다. 단 하나의 질문으로요.</p>
<p class="em">"이거, 나랑 상관있나?"</p><p>첫 화면에서 그 답이 보이지 않으면 고객은 조용히 창을 닫습니다.</p>
<div class="bx"><b class="g">[5초 테스트]</b> 타이머를 5초로 맞추고 시작!</div></div></div>''', TP_CSS, q=88)
shot('toc2', 352, 360, '''<div class="w"><div class="page p"><div class="ch">CHAPTER 2</div><h3 class="serif" style="font-size:17px">단 한 글자:<br>'우리'를 '당신'으로</h3>
<table style="margin-top:12px"><tr><th>공식</th><th>바꾸기 전</th><th>바꾼 후</th></tr>
<tr><td><b>자랑 → 혜택</b></td><td>20년 경력의 세무사가 운영하는 사무소입니다.</td><td>사장님이 남들이 겪은 실수를 되풀이하지 않게 챙깁니다.</td></tr>
<tr><td><b>기능 → 변화</b></td><td>출장 세차 서비스를 제공합니다.</td><td>퇴근길에는 반짝이는 차를 타고 가시면 됩니다.</td></tr>
<tr><td><b>스펙 → 감정</b></td><td>유기농 인증 원료를 씁니다.</td><td>간식 뒷면을 들여다보던 부모의 마음으로 고릅니다.</td></tr>
</table>
</div></div>''', TP_CSS, q=88)

# ---------- 6. 번호 특징 이미지 (716x300) ----------
FT_CSS = '''.f{width:716px;height:300px;background:#f2f5f3;padding:30px;display:flex;gap:16px;align-items:stretch}
.cc{flex:1;background:#fff;border-radius:16px;padding:20px 18px;box-shadow:0 6px 16px rgba(0,0,0,.06);display:flex;flex-direction:column}
.cc .ic{width:46px;height:46px;border-radius:12px;background:#eef2ef;display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:12px}
.cc b{font-size:17px}.cc span{font-size:13px;color:#4a5752;line-height:1.5;margin-top:6px}
.cc .dead{margin-top:auto;font-size:12px;color:#8a8f88;text-decoration:line-through}
.cc .live{font-size:12.5px;color:#2f6b57;font-weight:800;margin-top:4px}'''
COS = [('🍪', '네이처팜', '아이 간식 식품 회사', '유기농 인증 원료를 씁니다', '부모의 마음으로 고릅니다'),
       ('⚙️', '㈜정밀기계', '자동차 엔진 부품 공장', '30년간 가공해 왔습니다', '다음 양산을 덜 불안하게'),
       ('🧾', '정진 세무회계', '20년 된 세무사무소', '정확하고 신속한 처리', '실수를 되풀이하지 않게'),
       ('🚗', '모아 프리미엄 세차', '한 번에 한 대 손세차', '출장 세차 서비스 제공', '퇴근길엔 반짝이는 차')]
shot('ft1', 716, 300, '<div class="f">%s</div>' % ''.join(
    '<div class="cc"><div class="ic">%s</div><b>%s</b><span>%s</span><div class="dead">%s</div><div class="live">→ %s</div></div>' % c for c in COS), FT_CSS, q=88)
shot('ft2', 716, 300, '''<div class="f" style="background:#1d2b26;align-items:center;gap:30px;padding:30px 40px">
<div style="width:190px;height:190px;border-radius:50%;border:10px solid rgba(255,255,255,.12);border-top-color:#f0c35a;border-right-color:#f0c35a;display:flex;align-items:center;justify-content:center;flex:none;transform:rotate(-20deg)">
<div style="transform:rotate(20deg);text-align:center;color:#fff"><div style="font-size:52px;font-weight:900;line-height:1">10:00</div><div style="font-size:14px;opacity:.7;margin-top:6px">미션 타이머</div></div></div>
<div style="color:#fff;flex:1"><span class="tag" style="background:#f0c35a;color:#16201c">즉시 실행 미션</span>
<div style="font-size:26px;font-weight:900;margin:14px 0 10px;line-height:1.35">우리 소개서 첫 세 문장의<br>주어를 세어 보세요</div>
<div style="font-size:15px;line-height:1.7;color:rgba(255,255,255,.75)">'우리'로 시작한 문장 ___개<br>고객으로 시작한 문장 ___개</div></div></div>''', FT_CSS, q=88)
shot('ft3', 716, 300, '''<div class="f" style="flex-direction:column;gap:12px;padding:30px 40px">
<div style="font-size:15px;font-weight:800;color:#2f6b57;letter-spacing:1px">원고 숫자 점검표</div>
<div style="display:grid;grid-template-columns:1fr auto;gap:10px 18px;align-items:center;background:#fff;border-radius:16px;padding:20px 24px;font-size:16px">
<span>출처와 기준일을 확인한 숫자</span><b style="background:#2f6b57;color:#fff;border-radius:999px;padding:5px 14px;font-size:14px">✓ 싣기</b>
<span>원문을 찾지 못한 통계</span><b style="background:#c94b3a;color:#fff;border-radius:999px;padding:5px 14px;font-size:14px">✕ 빼기</b>
<span>책 속 예시 회사의 숫자</span><b style="background:#8a8f88;color:#fff;border-radius:999px;padding:5px 14px;font-size:14px">가상 사례 표시</b></div>
<div style="font-size:13.5px;color:#4a5752">숫자 하나에도 출처를 붙이는 방법은 Chapter 11과 부록 C에 있습니다.</div></div>''', FT_CSS, q=88)

# ---------- 7. 미리보기 (716x420, 본문 펼침) ----------
PV_CSS = '''.v{width:716px;height:420px;background:#e9e4d8;display:flex;align-items:center;justify-content:center;gap:0}
.v .page{width:310px;height:380px;padding:30px 26px;font-size:12px;line-height:1.75;color:#33403a}
.v .page+.page{box-shadow:0 18px 40px rgba(0,0,0,.18),inset 14px 0 18px -14px rgba(0,0,0,.25)}
.v h4{font-size:19px;margin:8px 0 12px;line-height:1.35}
.v .ch{font-size:11px;font-weight:800;color:#2f6b57;letter-spacing:2px}
.v .q{display:flex;gap:10px;align-items:flex-start;margin:9px 0;font-size:13px;font-weight:700;color:#16201c}
.v .q i{flex:none;width:22px;height:22px;border-radius:6px;border:2px solid #2f6b57}
.v td,.v th{border:1px solid #e3ddd0;padding:6px 7px;font-size:10.5px;text-align:left;vertical-align:top;line-height:1.5}
.v th{background:#eef2ef}
.v .ln{display:block;height:15px;border-bottom:1.5px solid #c9c2b2}'''
shot('pv1', 716, 420, '''<div class="v"><div class="page"><div class="ch">CHAPTER 1 · 5초 테스트</div><h4 class="serif">5초 안에 다음 세 질문에<br>답할 수 있나요?</h4>
<div class="q"><i></i>이 회사는 나에게 뭘 해 주는가?</div><div class="q"><i></i>내 일이 어떻게 좋아지는가?</div><div class="q"><i></i>지금 당장 뭘 하면 되는가?</div>
<p style="margin-top:14px">답하지 못했다면, 축하합니다(역설적이지만). 방금 당신은 아픈 곳을 정확히 찾아냈습니다.</p></div>
<div class="page" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:#1d2b26;color:#fff">
<div style="width:170px;height:170px;border-radius:50%;border:9px solid #f0c35a;display:flex;align-items:center;justify-content:center;font-size:72px;font-weight:900">5</div>
<div style="margin-top:20px;font-size:15px;opacity:.8">타이머를 5초로 맞추고, 시작!</div></div></div>''', PV_CSS, q=88)
shot('pv2', 716, 420, '''<div class="v"><div class="page"><div class="ch">CHAPTER 2 · 주어 바꾸기</div><h4 class="serif">'20년 경력'은 회사에겐 자랑,<br>고객에겐 아직 아무 의미가 없습니다</h4>
<p>고객이 궁금한 건 하나입니다.</p><p style="font-weight:800;color:#16201c;font-size:13.5px;margin:6px 0">"그 20년이 나에게 뭘 해 주는데?"</p>
<p>경력을 고객이 받는 혜택으로 번역하세요. 같은 사실이 전혀 다르게 읽힙니다.</p></div>
<div class="page"><div class="ch">공식 1 · 자랑 → 혜택</div>
<div style="background:#f2efe8;border-radius:10px;padding:14px;margin-top:14px;color:#8a8f88;text-decoration:line-through">저희는 20년 경력의 세무사가 운영하는 사무소입니다.</div>
<div style="text-align:center;color:#2f6b57;font-size:20px;font-weight:900;margin:6px 0">↓</div>
<div style="background:#1d2b26;color:#fff;border-radius:10px;padding:14px;font-weight:700;font-size:13px">20년 동안 쌓인 신고 경험으로, 사장님이 <span class="y">남들이 겪은 실수를 되풀이하지 않게</span> 챙깁니다.</div>
<p style="font-size:10.5px;color:#8a8f88;margin-top:12px">정진 세무회계 · 책 속 가상 사례</p></div></div>''', PV_CSS, q=88)
shot('pv3', 716, 420, '''<div class="v"><div class="page" style="width:620px;height:380px"><div class="ch">부록 A-1 · 빈칸 워크시트</div><h4 class="serif" style="margin-bottom:10px">SB7 정리표: 우리 회사 설계도 한 장</h4>
<table><tr><th style="width:150px">단계</th><th>채울 질문</th><th style="width:170px">답</th></tr>
<tr><td><b>① 주인공</b></td><td>우리 고객은 누구이고, 원하는 단 한 가지는 무엇입니까?</td><td><span class="ln"></span></td></tr>
<tr><td><b>② 난관</b></td><td>외적·내적·철학적 문제, 빌런은 무엇입니까?</td><td><span class="ln"></span></td></tr>
<tr><td><b>③ 가이드</b></td><td>공감과 권위는 무엇입니까?</td><td><span class="ln"></span></td></tr>
<tr><td><b>④ 계획</b></td><td>이용 과정 3단계와 약속은 무엇입니까?</td><td><span class="ln"></span></td></tr>
<tr><td><b>⑤ 행동 촉구</b></td><td>직접 CTA와 전환 CTA는 무엇입니까?</td><td><span class="ln"></span></td></tr>
<tr><td><b>⑥ 실패 · ⑦ 성공</b></td><td>하지 않으면 잃는 것, 했을 때의 장면은?</td><td><span class="ln"></span></td></tr></table></div></div>''', PV_CSS, q=88)

# ---------- 8. 구성품 이미지 (664x220) ----------
PT_CSS = '''.b{width:664px;height:220px;background:#f2f5f3;border-radius:0;display:flex;align-items:center;justify-content:center;gap:16px;overflow:hidden;position:relative}
.mini{background:#fffdf8;box-shadow:0 10px 22px rgba(0,0,0,.14);border-radius:4px;padding:12px;font-size:9px;color:#4a5752;line-height:1.5}
.mini b{display:block;font-size:11px;color:#16201c;margin-bottom:4px}
.mini .ln{height:7px;border-bottom:1px solid #d6cfbf;margin-top:4px}'''
def sheet(t, w=120, h=160, rot=0, extra=''):
    return '<div class="mini" style="width:%dpx;height:%dpx;transform:rotate(%sdeg)"><b>%s</b>%s%s</div>' % (w, h, rot, t, extra, '<div class="ln"></div>' * 8)
shot('pA', 664, 220, '<div class="b" style="background:#1d2b26"><img src="%s" style="height:180px;box-shadow:0 14px 30px rgba(0,0,0,.5);transform:rotate(-3deg)">'
     '<div style="color:#fff;margin-left:20px"><div style="font-size:30px;font-weight:900">PDF 1권</div><div style="font-size:15px;opacity:.75;margin-top:6px;line-height:1.6">5부 13장 + 부록 A~G<br>태블릿·PC·휴대폰에서 읽기</div></div></div>' % url('cover.jpg'), PT_CSS, q=88)
shot('pB', 664, 220, '<div class="b">%s</div>' % ''.join(sheet(t, rot=r) for t, r in
     [('A-1 SB7 정리표', -6), ('A-2 기원 서사 5막', -2), ('A-3 홈페이지 6섹션', 2), ('A-5 주어 바꾸기', 5), ('+ 9종', 8)]), PT_CSS, q=88)
shot('pC', 664, 220, '<div class="b">%s</div>' % ''.join(
     '<div class="mini" style="width:170px;height:170px"><b>%s</b>%s</div>' % (t, ''.join('<div style="font-size:9.5px;margin-top:5px">□ %s</div>' % i for i in it)) for t, it in
     [('B-1 자가진단표 (40점)', ['첫 문장이 고객의 문제로 시작', "'고객'이 '우리'보다 많다", '5초 안에 무엇을 해 주는지', '분명한 빌런이 있다']),
      ('B-2 공개 전 점검', ['금지어·주의어 걸러 내기', '숫자마다 출처·기준일', '버튼 문구 하나로']),
      ('B-3 분기 점검', ['문의 수·예약 수 기록', '헤드라인 A/B 2주씩', '사례·숫자 새로 고치기'])]), PT_CSS, q=88)
shot('pD', 664, 220, '''<div class="b" style="padding:0 34px"><table style="background:#fff;border-radius:12px;overflow:hidden;font-size:13px">
<tr style="background:#2f6b57;color:#fff"><th style="padding:9px 14px;text-align:left">피할 말</th><th style="padding:9px 14px;text-align:left">대신 쓸 방향</th></tr>
<tr><td style="padding:9px 14px;border-bottom:1px solid #eee;color:#c94b3a;text-decoration:line-through">혁신적, 획기적</td><td style="padding:9px 14px;border-bottom:1px solid #eee">무엇이 어떻게 달라졌는지 전후 비교로</td></tr>
<tr><td style="padding:9px 14px;border-bottom:1px solid #eee;color:#c94b3a;text-decoration:line-through">최고, 넘버원</td><td style="padding:9px 14px;border-bottom:1px solid #eee">증거와 기준일을 보여 주기</td></tr>
<tr><td style="padding:9px 14px;color:#c94b3a;text-decoration:line-through">맞춤형, 최적화</td><td style="padding:9px 14px">어떻게 맞추는지로</td></tr></table></div>''', PT_CSS, q=88)
WEEKS = ['진단', '뼈대', '초안', '다듬기', '웹', '웹', '채널', '채널', '공개', '기록', '의견', '고치기', '돌아보기']
shot('pE', 664, 220, '<div class="b" style="padding:0 26px;flex-direction:column;align-items:stretch;gap:10px"><div style="font-size:14px;font-weight:800;color:#2f6b57">90일 실행 캘린더 · 하루 30분~1시간</div>'
     '<div style="display:grid;grid-template-columns:repeat(13,1fr);gap:5px">%s</div></div>' % ''.join(
         '<div style="background:%s;color:%s;border-radius:8px;height:110px;padding:8px 4px;text-align:center;font-size:11px;font-weight:700;line-height:1.3">'
         '<div style="font-size:15px;font-weight:900;margin-bottom:6px">%d주</div>%s</div>' % ((('#2f6b57', '#fff') if i < 4 else ('#fff', '#16201c')) + (i + 1, w))
         for i, w in enumerate(WEEKS)), PT_CSS, q=88)
shot('pF', 664, 220, '''<div class="b" style="background:#1d2b26"><div style="width:520px;height:170px;background:#fff;border-radius:10px;overflow:hidden;display:flex;box-shadow:0 14px 30px rgba(0,0,0,.4)">
<div style="width:170px;background:#f2f5f3;padding:12px;font-size:10px;line-height:1.9;color:#4a5752"><b style="color:#16201c">블록</b><br>01 첫 화면<br>02 문제 체크리스트<br>03 빌런 비교<br>04 받는 것<br>05 저자 소개<br>…</div>
<div style="flex:1;background:#1d2b26;margin:10px;border-radius:6px;color:#fff;padding:16px;font-size:16px;font-weight:900;line-height:1.35">우리 홈페이지,<br>5초 안에 답할 수 있나요?<div style="font-size:10px;font-weight:600;color:#f0c35a;margin-top:10px">점검 90점 · 막힘 0</div></div></div></div>''', PT_CSS, q=88)
shot('pG', 664, 220, '''<div class="b"><div class="mini" style="width:420px;height:170px;font-size:13px;padding:18px 20px;line-height:1.7">
<b style="font-size:12px;color:#2f6b57">첫 화면 첨삭</b><span style="text-decoration:line-through;color:#8a8f88">저희 회사는 1998년에 설립되어 고객 만족을 위해…</span>
<div style="color:#c94b3a;font-weight:800;margin-top:4px">→ 고객의 고민으로 시작해 보세요. 예: "견적 비교에 지치셨죠?"</div>
<div style="font-size:11px;color:#4a5752;margin-top:6px">✎ 주어 '저희' 3회 → 고객 2회로 / 버튼 문구는 하나로</div></div></div>''', PT_CSS, q=88)

# ---------- 9. GIF: 워크시트에 바꾼 문장을 적는 장면 (860x480) ----------
GIF_CSS = '''.g0{width:860px;height:480px;background:#e9e4d8;display:flex;align-items:center;justify-content:center}
.ws{width:760px;height:420px;background:#fffdf8;border-radius:10px;box-shadow:0 14px 30px rgba(0,0,0,.15);padding:30px 36px}
.ws h4{font-size:22px;margin:8px 0 18px}
.row{display:grid;grid-template-columns:120px 1fr;gap:14px;padding:12px 0;border-top:1px solid #e3ddd0;align-items:start}
.row b{font-size:15px;color:#2f6b57;padding-top:2px}
.row .v{font-size:18px;line-height:1.55;min-height:28px}
.ops span{display:inline-block;border:1.5px solid #c9c2b2;border-radius:999px;padding:4px 12px;font-size:14px;margin:0 6px 6px 0;color:#4a5752}
.ops span.on{background:#2f6b57;border-color:#2f6b57;color:#fff;font-weight:800}
.hand{font-family:'Noto Serif KR',serif;font-weight:700;color:#16201c}
.cur{display:inline-block;width:2px;height:22px;background:#2f6b57;vertical-align:-4px;margin-left:2px}
.stamp{position:absolute;right:70px;bottom:46px;border:4px solid #c94b3a;color:#c94b3a;font-weight:900;font-size:22px;padding:8px 16px;border-radius:10px;transform:rotate(-8deg);background:rgba(255,253,248,.9)}'''
BEFORE = '㈜정밀기계는 1995년 설립 이래 30년간 자동차 엔진 부품을 가공해 왔습니다.'
AFTER = '30년 동안 쌓은 가공 기록이 귀사의 다음 양산을 덜 불안하게 만듭니다.'
OPS = ['자랑 → 혜택', '기능 → 변화', '스펙 → 감정', '과거 → 미래']
def gframe(op, n, stamp, cur=True):
    o = ''.join('<span class="%s">%s</span>' % ('on' if i == op else '', t) for i, t in enumerate(OPS))
    return '''<div class="g0" style="position:relative"><div class="ws"><span class="tag">부록 A-5 · 주어 바꾸기 연습</span><h4 class="serif">첫 문장, 고객이 주인공이 되게</h4>
<div class="row"><b>지금 문장</b><div class="v" style="color:#4a5752">%s</div></div>
<div class="row"><b>공식 고르기</b><div class="v ops">%s</div></div>
<div class="row"><b>바꾼 문장</b><div class="v hand">%s%s</div></div></div>%s</div>''' % (
        BEFORE, o, AFTER[:n], '<span class="cur"></span>' if cur else '', '<div class="stamp">주어: 우리 → 고객 ✓</div>' if stamp else '')
seq = [(-1, 0, False, 900)] + [(i, 0, False, 260) for i in range(4)] + [(3, 0, False, 500)]
steps = list(range(3, len(AFTER) + 1, 3))
if steps[-1] != len(AFTER):
    steps.append(len(AFTER))
seq += [(3, n, False, 90) for n in steps] + [(3, len(AFTER), True, 2600)]
frames, durs = [], []
for k, (op, n, st, d) in enumerate(seq):
    im = shot('gif_%02d' % k, 860, 480, gframe(op, n, st, cur=not st), GIF_CSS, scale=1, fmt='png')
    frames.append(im.convert('RGB'))
    durs.append(d)
pal = frames[-1].quantize(colors=128, method=Image.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
gp = os.path.join(OUT, 'worksheet.gif')
q[0].save(gp, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
print('%-22s %4dx%-4d %4dKB  frames=%d' % ('worksheet.gif', 860, 480, os.path.getsize(gp) // 1024, len(q)))

shutil.rmtree(TMP, ignore_errors=True)
