import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RoHI Calculator - 회전근개 치유 예측",
    page_icon="🩺",
    layout="wide",
)

# ── Password Authentication ──
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown("""
    <style>@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap');</style>
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:50vh">
        <div style="background:white;padding:40px 36px;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.08);max-width:400px;width:100%;text-align:center">
            <div style="font-size:56px;margin-bottom:16px">🔐</div>
            <div style="font-size:26px;font-weight:800;color:#1a1a2e;font-family:'Noto Sans KR',sans-serif">RoHI Calculator</div>
            <div style="font-size:13px;color:#999;margin-top:6px;margin-bottom:24px">회전근개 치유 예측 시스템</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password = st.text_input("pw", type="password", label_visibility="collapsed", placeholder="🔑 비밀번호 입력")
        if st.button("로그인", use_container_width=True, type="primary"):
            if password == st.secrets.get("password", "rohi2024"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
    return False

if not check_password():
    st.stop()

# ══════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════
TABLE_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp { font-family:'Noto Sans KR','Inter',sans-serif; }
    .header-badge { display:inline-block; background:linear-gradient(135deg,#1a1a2e,#16213e);
        color:#fff; padding:6px 18px; border-radius:24px; font-size:11px;
        font-weight:700; letter-spacing:2px; text-transform:uppercase; box-shadow:0 4px 14px rgba(26,26,46,0.2); }
    .header-title-en { font-size:38px; font-weight:800; color:#1a1a2e; margin:14px 0 2px; text-align:center; letter-spacing:-0.5px; }
    .header-title-kr { font-size:22px; font-weight:700; color:#555; margin:0 0 6px; text-align:center; }
    .header-sub { font-size:12px; color:#8899aa; margin-top:6px; text-align:center; line-height:1.6; }
    .factor-num { display:inline-flex; align-items:center; justify-content:center;
        width:24px; height:24px; border-radius:50%; font-size:11px; font-weight:800; color:#fff; margin-right:6px; }
    .factor-title { font-size:14px; font-weight:700; color:#1a1a2e; }
    .factor-meta { font-size:10px; color:#aab; }
    .result-container { background:linear-gradient(135deg,#fff,#f8fafc); border-radius:24px;
        padding:28px 20px; text-align:center; border:2px solid #e8ecf0; box-shadow:0 8px 32px rgba(0,0,0,0.04); }
    .score-ring { width:140px; height:140px; border-radius:50%; margin:0 auto 14px;
        display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 8px 24px rgba(0,0,0,0.08); }
    .score-num { font-size:40px; font-weight:800; line-height:1; }
    .score-max { font-size:13px; font-weight:500; opacity:0.6; }
    .risk-badge { display:inline-block; padding:5px 18px; border-radius:24px; font-size:14px; font-weight:700; margin:6px 0; }
    .risk-desc { font-size:12px; color:#666; margin-top:4px; }
    .metric-card-v2 { background:#fff; border-radius:14px; padding:16px 12px; text-align:center;
        border:1px solid #e8ecf0; box-shadow:0 2px 8px rgba(0,0,0,0.03); }
    .metric-icon { font-size:24px; margin-bottom:4px; }
    .metric-val { font-size:28px; font-weight:800; }
    .metric-lbl { font-size:10px; color:#999; margin-bottom:2px; font-weight:500; }
    .bar-row { display:flex; align-items:center; gap:8px; margin-bottom:5px; }
    .bar-label { width:100px; font-size:10px; color:#777; text-align:right; font-weight:500; }
    .bar-track { flex:1; height:8px; background:#f0f2f5; border-radius:4px; overflow:hidden; }
    .bar-fill { height:100%; border-radius:4px; }
    .bar-val { width:28px; font-size:11px; font-weight:700; }
    .algo-container { background:#fff; border-radius:18px; padding:20px;
        border:1px solid #e8ecf0; box-shadow:0 2px 8px rgba(0,0,0,0.03); }
    .algo-title { font-size:16px; font-weight:800; color:#1a1a2e; text-align:center; margin-bottom:2px; }
    .algo-sub { font-size:10px; color:#aab; text-align:center; margin-bottom:14px; }
    .info-card { border-radius:12px; padding:14px 16px; font-size:11px; line-height:1.8; margin-top:8px; }
    .disclaimer { background:linear-gradient(135deg,#FFFDF0,#FFF9E6); border:1px solid #F0E0A0;
        border-radius:12px; padding:14px 16px; font-size:10px; color:#8B7A2B; line-height:1.8; }
    .ref-link { color:#3B82F6; text-decoration:none; font-weight:500; }
    .ref-link:hover { text-decoration:underline; }
    .sidebar-section { margin-bottom:24px; }
    .sidebar-title { font-size:15px; font-weight:800; color:#1a1a2e; margin-bottom:10px; padding-bottom:6px; border-bottom:2px solid #e0e0e0; }
    .sb-table { width:100%; border-collapse:collapse; font-size:11px; }
    .sb-table th { background:#f0f4f8; padding:7px 8px; text-align:left; font-weight:600; color:#555; border-bottom:2px solid #ddd; }
    .sb-table td { padding:6px 8px; border-bottom:1px solid #f0f0f0; color:#555; }
    .sb-table tr:hover { background:#fafbfc; }
    .sb-note { margin-top:10px; padding:10px 12px; background:#f0f4f8; border-radius:10px; font-size:10px; color:#555; line-height:1.7; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} .stDeployButton {display:none;}
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#f8fafc,#fff); min-width:280px; max-width:600px; resize:horizontal; overflow:auto; }
    [data-testid="stSidebar"] > div { padding-top:16px; }
</style>
"""
st.markdown(TABLE_STYLE, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════
RISK_DATA = [
    {"score":0,"sens":None,"spec":None,"ppv":None},
    {"score":1,"sens":100,"spec":9.4,"ppv":26.0},
    {"score":2,"sens":99.3,"spec":39.3,"ppv":34.1},
    {"score":3,"sens":95.9,"spec":47.4,"ppv":36.1},
    {"score":4,"sens":91.0,"spec":65.1,"ppv":45.2},
    {"score":5,"sens":84.1,"spec":78.4,"ppv":55.2},
    {"score":6,"sens":74.5,"spec":85.4,"ppv":61.7},
    {"score":7,"sens":62.1,"spec":93.6,"ppv":73.8},
    {"score":8,"sens":56.6,"spec":94.1,"ppv":75.2},
    {"score":9,"sens":44.1,"spec":95.6,"ppv":76.2},
    {"score":10,"sens":34.5,"spec":98.3,"ppv":86.2},
    {"score":11,"sens":29.0,"spec":98.9,"ppv":89.4},
    {"score":12,"sens":12.4,"spec":99.6,"ppv":90.0},
    {"score":13,"sens":11.0,"spec":99.6,"ppv":88.9},
    {"score":15,"sens":4.1,"spec":100,"ppv":100},
]
COLORS = ["#E74C3C","#E67E22","#3498DB","#9B59B6","#1ABC9C","#34495E"]

def get_fail(s):
    if s<=0: return 0.0
    for d in RISK_DATA:
        if d["score"]==s and d["ppv"] is not None: return d["ppv"]
    if s>=15: return 100.0
    lo=[d for d in RISK_DATA if d["score"]<s and d["ppv"] is not None]
    hi=[d for d in RISK_DATA if d["score"]>s and d["ppv"] is not None]
    if lo and hi:
        l,u=lo[-1],hi[0]; return l["ppv"]+(s-l["score"])/(u["score"]-l["score"])*(u["ppv"]-l["ppv"])
    return lo[-1]["ppv"] if lo else 0.0

def get_risk(s):
    if s<=4: return "저위험","#27AE60","✅","치유 실패 가능성이 낮습니다."
    if s<=6: return "중등도 위험","#F39C12","⚠️","치유 실패 가능성이 중등도입니다."
    if s<=9: return "고위험","#E74C3C","🔴","치유 실패 가능성이 높습니다."
    return "초고위험","#8E1600","🚨","치유 실패 가능성이 매우 높습니다."

def fh(idx,kr,en,desc,meta):
    c=COLORS[idx]
    st.markdown(f'<div style="margin-bottom:4px"><span class="factor-num" style="background:{c}">{idx+1}</span>'
        f'<span class="factor-title">{kr}</span><span style="font-size:11px;color:#aab;font-weight:500"> ({en})</span>'
        f'<div style="margin-left:30px"><span class="factor-meta">{desc} · {meta}</span></div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SIDEBAR — Reference Info (Expandable)
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:16px">
        <div style="font-size:20px;font-weight:800;color:#1a1a2e">📚 참고 자료</div>
        <div style="font-size:10px;color:#aaa;margin-top:4px">항목을 눌러 펼쳐보세요</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 Goutallier 분류 기준", expanded=False):
        st.markdown("""<p style="font-size:11px;color:#777;margin-bottom:10px;line-height:1.6">
Goutallier et al. (1994) 회전근개 근육 지방 변성 등급<br>
RoHI: 극하근(Infraspinatus) <strong style="color:#E67E22">Grade ≥ 2 → 3점</strong></p>
<table class="sb-table">
<thead><tr><th>Grade</th><th>설명</th><th style="text-align:center">RoHI</th></tr></thead>
<tbody>
<tr><td><strong style="color:#27AE60">0</strong></td><td>정상 근육 (No fat)</td><td style="text-align:center;color:#27AE60;font-weight:700">0점</td></tr>
<tr><td><strong style="color:#2ECC71">1</strong></td><td>약간의 지방 줄무늬 (Some fatty streaks)</td><td style="text-align:center;color:#27AE60;font-weight:700">0점</td></tr>
<tr style="background:#FFF5EB"><td><strong style="color:#E67E22">2</strong></td><td>지방 &lt; 근육 (Fat &lt; Muscle)</td><td style="text-align:center;color:#E67E22;font-weight:700">3점⚠️</td></tr>
<tr style="background:#FFF0E6"><td><strong style="color:#D35400">3</strong></td><td>지방 = 근육 (Fat = Muscle)</td><td style="text-align:center;color:#E67E22;font-weight:700">3점⚠️</td></tr>
<tr style="background:#FDEBE6"><td><strong style="color:#C0392B">4</strong></td><td>지방 &gt; 근육 (Fat &gt; Muscle)</td><td style="text-align:center;color:#E67E22;font-weight:700">3점⚠️</td></tr>
</tbody></table>
<div class="sb-note"><strong>📌 임상적 의의:</strong><br>
• Grade ≥ 2 시 재파열률 유의 증가 (59% vs 25%, Khair et al.)<br>
• 극하근 지방 변성 = 근육·건 질(quality) 핵심 지표<br>
• 수술 후에도 호전 안 됨 → 수술 전 평가 중요 (Gladstone et al.)<br>
• Massive tear 최중요 독립적 예후인자 (OR 11.25, Chung et al.)</div>""", unsafe_allow_html=True)

    with st.expander("🔨 노동 활동 수준 분류", expanded=False):
        st.markdown("""<p style="font-size:11px;color:#777;margin-bottom:10px;line-height:1.6">
Kwon et al. (2019) 정의<br>
RoHI: <strong style="color:#34495E">노동 활동 '높음' → 2점</strong></p>
<table class="sb-table">
<thead><tr><th>수준</th><th>정의</th><th style="text-align:center">RoHI</th></tr></thead>
<tbody>
<tr><td><strong style="color:#27AE60">낮음</strong></td><td>좌식 업무 (Sedentary work)</td><td style="text-align:center;color:#27AE60;font-weight:700">0점</td></tr>
<tr><td><strong style="color:#2ECC71">중간</strong></td><td>경도 육체 노동 (Manual labor, less activity)</td><td style="text-align:center;color:#27AE60;font-weight:700">0점</td></tr>
<tr style="background:#F2F3F4"><td><strong style="color:#E74C3C">높음</strong></td><td>중노동 (Heavy manual labor)</td><td style="text-align:center;color:#E74C3C;font-weight:700">2점⚠️</td></tr>
</tbody></table>
<p style="font-size:12px;font-weight:700;color:#34495E;margin:16px 0 6px">🏃 스포츠 활동 수준 (참고용)</p>
<table class="sb-table">
<thead><tr><th>수준</th><th>정의</th><th>예시</th></tr></thead>
<tbody>
<tr><td><strong style="color:#27AE60">낮음</strong></td><td>거의 참여 안 함</td><td style="color:#888">—</td></tr>
<tr><td><strong style="color:#F39C12">중간</strong></td><td>정적 스포츠</td><td style="color:#888">달리기, 자전거, 골프, 요가</td></tr>
<tr><td><strong style="color:#E74C3C">높음</strong></td><td>접촉 스포츠 / 무술</td><td style="color:#888">농구, 축구, 테니스, 배구</td></tr>
</tbody></table>
<div class="sb-note"><strong>📌 임상적 의의:</strong><br>
• 반복적 중량물 취급 + 어색한 자세 → 어깨 통증 위험인자 (Miranda et al.)<br>
• 어깨 질환 ↔ 팔 거상 중등도 연관 (OR 1.9, van der Molen et al.)<br>
• 중노동 → 양측성 회전근개 파열 위험 증가 (Abate et al.)<br>
• 수술 실패 후 예후 불량 (Namdari et al.)<br>
• RoHI: <strong>노동 활동만</strong> 점수 반영 (스포츠 활동 미반영)</div>""", unsafe_allow_html=True)

    with st.expander("📋 점수별 상세 데이터", expanded=False):
        st.markdown('<p style="font-size:10px;color:#999;margin-bottom:8px">Kwon et al. (2019) 연구 코호트 (n=603)</p>', unsafe_allow_html=True)
        rows = [d for d in RISK_DATA if d["sens"] is not None]
        df = pd.DataFrame(rows)
        df.columns = ["점수(≥)", "민감도(%)", "특이도(%)", "PPV(%)"]
        st.dataframe(df.style.format(precision=1), use_container_width=True, hide_index=True, height=400)
        st.caption("* 해당 점수를 임계점으로 설정했을 때의 값")

    st.markdown("---")
    with st.expander("🔗 References", expanded=False):
        st.markdown("""<div style="font-size:11px;line-height:2.2;color:#555">
<strong>1.</strong> <a href="https://journals.sagepub.com/doi/10.1177/0363546518810763" target="_blank" style="color:#3B82F6;text-decoration:none">Kwon et al. <em>Am J Sports Med.</em> 2019;47(1):173-180</a><br>
<strong>2.</strong> <a href="https://www.arthroscopyjournal.org/article/S0749-8063(21)00963-4/fulltext" target="_blank" style="color:#3B82F6;text-decoration:none">Jackson et al. <em>Arthroscopy.</em> 2022;38(7):2342-2347</a>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN CONTENT — HEADER
# ══════════════════════════════════════════════════════════
st.markdown('<div style="text-align:center;margin-top:4px"><span class="header-badge">RoHI Score Calculator</span></div>',unsafe_allow_html=True)
st.markdown('<p class="header-title-en">Rotator Cuff Healing Index</p>',unsafe_allow_html=True)
st.markdown('<p class="header-title-kr">회전근개 치유 예측 계산기</p>',unsafe_allow_html=True)
st.markdown('<p class="header-sub">Kwon et al. (2019) AJSM · 6가지 독립적 예후인자 · 15점 만점 · 치료 알고리즘: Jackson, Bedi & Denard (2022) Arthroscopy</p>',unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN — INPUTS (2 columns for compactness)
# ══════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 1])

with left_col:
    fh(0,"파열 퇴축","Tear Retraction","내측 퇴축 거리","OR 4.56 · 최대 4점")
    retraction=st.radio("r",["< 1 cm (0점)","1~<2 cm (1점)","2~<3 cm (2점)","≥ 3 cm (4점)"],horizontal=True,label_visibility="collapsed",key="r1")
    rs={"< 1 cm (0점)":0,"1~<2 cm (1점)":1,"2~<3 cm (2점)":2,"≥ 3 cm (4점)":4}[retraction]
    st.markdown("---")

    fh(1,"극하근 지방 침윤","Infraspinatus FI","Goutallier 분류 ← 좌측 참고","OR 2.91 · 최대 3점")
    fatty=st.radio("f",["Grade 0~1 (0점)","Grade ≥ 2 (3점)"],horizontal=True,label_visibility="collapsed",key="f1")
    fs=0 if "0~1" in fatty else 3
    st.markdown("---")

    fh(2,"나이","Age","수술 시점 연령","OR 2.71 · 최대 2점")
    age=st.radio("a",["< 70세 (0점)","≥ 70세 (2점)"],horizontal=True,label_visibility="collapsed",key="a1")
    a_s=0 if "< 70" in age else 2

with right_col:
    fh(3,"전후방 파열 크기","AP Tear Size","Footprint 외측 가장자리","OR 1.94 · 최대 2점")
    ap=st.radio("ap",["≤ 2.5 cm (0점)","> 2.5 cm (2점)"],horizontal=True,label_visibility="collapsed",key="ap1")
    ap_s=0 if "≤ 2.5" in ap else 2
    st.markdown("---")

    fh(4,"골밀도","BMD","DEXA T-score","OR 1.95 · 최대 2점")
    bmd=st.radio("bmd",["T-score > −2.5 (0점)","T-score ≤ −2.5 (2점)"],horizontal=True,label_visibility="collapsed",key="b1")
    b_s=0 if ">" in bmd else 2
    st.markdown("---")

    fh(5,"노동 활동 수준","Work Activity","활동 강도 ← 좌측 참고","OR 2.18 · 최대 2점")
    work=st.radio("w",["낮음~중간 (0점)","높음/중노동 (2점)"],horizontal=True,label_visibility="collapsed",key="w1")
    w_s=0 if "낮음" in work else 2

# ══════════════════════════════════════════════════════════
# CALCULATE
# ══════════════════════════════════════════════════════════
total=rs+fs+a_s+ap_s+b_s+w_s
fail=get_fail(total)
heal=100-fail
nm,clr,emo,dsc=get_risk(total)
smap=[("파열 퇴축",rs),("극하근 지방 침윤",fs),("나이",a_s),("전후방 파열 크기",ap_s),("골밀도",b_s),("노동 활동 수준",w_s)]

# ══════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)

res_left, res_right = st.columns([1, 1.2])

with res_left:
    st.markdown(f"""
    <div class="result-container" style="border-color:{clr}33">
        <div class="score-ring" style="background:linear-gradient(135deg,{clr}15,{clr}08);border:4px solid {clr}">
            <div class="score-num" style="color:{clr}">{total}</div>
            <div class="score-max" style="color:{clr}">/ 15점</div>
        </div>
        <div class="risk-badge" style="background:{clr}18;color:{clr};border:1px solid {clr}33">{emo} {nm}</div>
        <div class="risk-desc">{dsc}</div>
    </div>
    """,unsafe_allow_html=True)

with res_right:
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(f'<div class="metric-card-v2"><div class="metric-icon">📉</div><div class="metric-lbl">예상 치유 실패율</div><div class="metric-val" style="color:#E74C3C">{fail:.1f}%</div></div>',unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="metric-card-v2"><div class="metric-icon">📈</div><div class="metric-lbl">예상 치유 성공률</div><div class="metric-val" style="color:#27AE60">{heal:.1f}%</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    active=[(n,v) for n,v in smap if v>0]
    if active:
        st.markdown("**📊 점수 구성**")
        for n,v in active:
            idx=[x[0] for x in smap].index(n)
            c=COLORS[idx]; pct=v/15*100
            st.markdown(f'<div class="bar-row"><span class="bar-label">{n}</span><div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{c}cc,{c})"></div></div><span class="bar-val" style="color:{c}">+{v}</span></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TREATMENT ALGORITHM
# ══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)
st.markdown('<div class="algo-container"><div class="algo-title">🩺 치료 권고 알고리즘</div><div class="algo-sub">Jackson, Bedi & Denard (2022) Arthroscopy 기반 · Hamada grade 1-2 대상</div></div>',unsafe_allow_html=True)

rep=st.radio("**파열의 수복 가능성 (Reparability)**",["수복 가능 (Repairable)","수복 불가 (Irreparable)"],horizontal=True)

if "수복 가능" in rep:
    if total<7:
        st.success(f"**✅ 봉합 수술 (Standard Repair) 권고**\n\nRoHI **{total}점 (< 7)** — 일반 봉합 수술로 충분한 치유율 기대\n\n- 예상 치유 성공률: **{heal:.1f}%**\n- 단일열 또는 이열 봉합 적용 가능")
    else:
        st.warning(f"**🔧 이식물 보강 수술 권고 (Graft Augmentation)**\n\nRoHI **{total}점 (≥ 7)** — 일반 봉합 시 치유 실패 위험 높음\n\n6점 치유율 66% → 7점 38%로 급격히 하락하므로 **무세포 동종 진피 이식물(Acellular Dermal Allograft)** 보강 권고")
        st.markdown("""
        <div class="info-card" style="background:#f8f9fa;border:1px solid #e0e0e0;color:#555">
            <strong style="color:#333">📚 이식물 보강 효과:</strong><br>
            • 대형 파열: 일반 40% → 보강 85% (Barber et al.)<br>
            • 생역학적 강도 62%↑ (Omae et al.)<br>
            • Allograft 82% vs Xenograft 68% vs Standard 49% (Bailey et al.)<br>
            • Bovine collagen 83.5% (Bushnell et al.) · Porcine patch 97.6% vs 59.5% (Avanzi et al.)
        </div>
        """,unsafe_allow_html=True)
else:
    if a_s==0:
        st.info("**< 70세: 관절 보존 수술 고려**\n\n견갑하근 상태 및 파열 특성에 따라 치료를 선택합니다.")
        ca,cb=st.columns(2)
        with ca:
            st.markdown('<div class="info-card" style="background:#F5EEF8;border:1px solid #D7BDE2"><div style="font-size:13px;font-weight:700;color:#6C3483;margin-bottom:6px">💜 견갑하근 보존/수복 가능</div><div style="font-size:11px;color:#555;line-height:1.8">• 상관절낭 재건 (SCR)<br>• vs 건 이전술 (Tendon Transfer)</div></div>',unsafe_allow_html=True)
        with cb:
            st.markdown('<div class="info-card" style="background:#FDEDEC;border:1px solid #F5B7B1"><div style="font-size:13px;font-weight:700;color:#922B21;margin-bottom:6px">❤️‍🩹 견갑하근 손상</div><div style="font-size:11px;color:#555;line-height:1.8">• 역행성 견관절 치환술 (RSA)<br>• vs 건 이전술 (Tendon Transfer)</div></div>',unsafe_allow_html=True)
        st.caption("※ 외회전 완전 소실(극하근+소원근) → 하승모근 건 이전술 · Hamada ≥3 → SCR 치유율 <50%")
    else:
        st.error("**≥ 70세: 부분 봉합 (Partial Repair)**\n\n관절염 경미 시 (Hamada 1-2) **부분 봉합 ± 이식물 보강** 고려\n\n단, 시간 경과에 따라 결과 악화 가능 (Shon et al.)")

# ══════════════════════════════════════════════════════════
# DISCLAIMER & REFERENCES
# ══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ 주의사항</strong><br>
    본 계산기는 Kwon et al. (2019) AJSM의 RoHI 점수 체계와
    Jackson, Bedi & Denard (2022) Arthroscopy의 치료 알고리즘을 기반으로 합니다.
    연구 코호트(603명) 후향적 검증 결과이며, 외적 타당도는 미검증 상태입니다.
    개별 환자의 치료 결정은 반드시 담당 의사의 종합적 판단에 따라야 합니다.
</div>
""",unsafe_allow_html=True)
