import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RoHI Calculator - 회전근개 치유 예측",
    page_icon="🩺",
    layout="centered",
)

# ── Password Authentication ──
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap');
    </style>
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:50vh">
        <div style="background:white;padding:40px 36px;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.08);
                    max-width:400px;width:100%;text-align:center">
            <div style="font-size:56px;margin-bottom:16px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.1))">🔐</div>
            <div style="font-size:26px;font-weight:800;color:#1a1a2e;font-family:'Noto Sans KR',sans-serif">RoHI Calculator</div>
            <div style="font-size:13px;color:#999;margin-top:6px;margin-bottom:24px">회전근개 치유 예측 시스템</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password = st.text_input("pw", type="password", label_visibility="collapsed", placeholder="🔑 비밀번호 입력")
        if st.button("로그인", use_container_width=True, type="primary"):
            correct_password = st.secrets.get("password", "rohi2024")
            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
    return False

if not check_password():
    st.stop()

# ══════════════════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp { font-family: 'Noto Sans KR', 'Inter', sans-serif; background: linear-gradient(180deg, #f0f4f8 0%, #fafbfc 100%); }

    .header-badge {
        display:inline-block; background:linear-gradient(135deg,#1a1a2e,#16213e);
        color:#fff; padding:6px 18px; border-radius:24px; font-size:11px;
        font-weight:700; letter-spacing:2px; text-transform:uppercase;
        box-shadow:0 4px 14px rgba(26,26,46,0.2);
    }
    .header-title { font-size:32px; font-weight:800; color:#1a1a2e; margin:12px 0 0; text-align:center; }
    .header-sub { font-size:13px; color:#8899aa; margin-top:6px; text-align:center; line-height:1.6; }

    .factor-num {
        display:inline-flex; align-items:center; justify-content:center;
        width:26px; height:26px; border-radius:50%;
        font-size:12px; font-weight:800; color:#fff; margin-right:8px;
    }
    .factor-title { font-size:15px; font-weight:700; color:#1a1a2e; }
    .factor-meta { font-size:11px; color:#aab; margin-top:2px; }

    .result-container {
        background:linear-gradient(135deg,#fff,#f8fafc); border-radius:24px;
        padding:32px 24px; text-align:center; border:2px solid #e8ecf0;
        box-shadow:0 8px 32px rgba(0,0,0,0.04);
    }
    .score-ring {
        width:160px; height:160px; border-radius:50%; margin:0 auto 16px;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        box-shadow:0 8px 24px rgba(0,0,0,0.08);
    }
    .score-num { font-size:44px; font-weight:800; line-height:1; }
    .score-max { font-size:14px; font-weight:500; opacity:0.6; }
    .risk-badge { display:inline-block; padding:6px 20px; border-radius:24px; font-size:15px; font-weight:700; margin:8px 0; }
    .risk-desc { font-size:13px; color:#666; margin-top:4px; }

    .metric-card-v2 {
        background:#fff; border-radius:16px; padding:20px 16px; text-align:center;
        border:1px solid #e8ecf0; box-shadow:0 2px 8px rgba(0,0,0,0.03);
    }
    .metric-icon { font-size:28px; margin-bottom:6px; }
    .metric-val { font-size:32px; font-weight:800; }
    .metric-lbl { font-size:11px; color:#999; margin-bottom:4px; font-weight:500; }

    .bar-row { display:flex; align-items:center; gap:10px; margin-bottom:6px; }
    .bar-label { width:110px; font-size:11px; color:#777; text-align:right; font-weight:500; }
    .bar-track { flex:1; height:10px; background:#f0f2f5; border-radius:5px; overflow:hidden; }
    .bar-fill { height:100%; border-radius:5px; transition:width 0.5s ease; }
    .bar-val { width:32px; font-size:12px; font-weight:700; }

    .algo-container {
        background:#fff; border-radius:20px; padding:24px;
        border:1px solid #e8ecf0; box-shadow:0 2px 8px rgba(0,0,0,0.03);
    }
    .algo-title { font-size:18px; font-weight:800; color:#1a1a2e; text-align:center; margin-bottom:2px; }
    .algo-sub { font-size:11px; color:#aab; text-align:center; margin-bottom:18px; }

    .info-card { border-radius:14px; padding:16px 18px; font-size:12px; line-height:1.8; margin-top:10px; }

    .goutallier-table { width:100%; border-collapse:collapse; font-size:12px; margin-top:8px; }
    .goutallier-table th { background:#f0f4f8; padding:8px 10px; text-align:left; font-weight:600; color:#555; border-bottom:2px solid #ddd; }
    .goutallier-table td { padding:7px 10px; border-bottom:1px solid #f0f0f0; color:#555; }
    .goutallier-table tr:hover { background:#fafbfc; }

    .disclaimer {
        background:linear-gradient(135deg,#FFFDF0,#FFF9E6); border:1px solid #F0E0A0;
        border-radius:14px; padding:16px 18px; font-size:11px; color:#8B7A2B; line-height:1.8;
    }
    .ref-link { color:#3B82F6; text-decoration:none; font-weight:500; }
    .ref-link:hover { text-decoration:underline; }

    #MainMenu {visibility:hidden;} footer {visibility:hidden;} .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

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
    if s<=4: return "저위험","#27AE60","#E8F8F0","✅","치유 실패 가능성이 낮습니다."
    if s<=6: return "중등도 위험","#F39C12","#FEF5E7","⚠️","치유 실패 가능성이 중등도입니다."
    if s<=9: return "고위험","#E74C3C","#FDEDEC","🔴","치유 실패 가능성이 높습니다."
    return "초고위험","#8E1600","#F9E0DB","🚨","치유 실패 가능성이 매우 높습니다."

def fh(idx,kr,en,desc,meta):
    c=COLORS[idx]
    st.markdown(f'<div style="margin-bottom:6px"><span class="factor-num" style="background:{c}">{idx+1}</span>'
        f'<span class="factor-title">{kr}</span><span style="font-size:12px;color:#aab;font-weight:500"> ({en})</span>'
        f'<div style="margin-left:34px"><span class="factor-meta">{desc} · {meta}</span></div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown('<div style="text-align:center;margin-top:8px"><span class="header-badge">Rotator Cuff Healing Index</span></div>',unsafe_allow_html=True)
st.markdown('<p class="header-title">회전근개 치유 예측 계산기</p>',unsafe_allow_html=True)
st.markdown('<p class="header-sub">Kwon et al. (2019) AJSM · 6가지 독립적 예후인자 · 15점 만점<br>치료 알고리즘: Jackson, Bedi & Denard (2022) Arthroscopy</p>',unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════
fh(0,"파열 퇴축","Tear Retraction","파열된 건의 내측 퇴축 거리","OR 4.56 · 최대 4점")
retraction=st.radio("r",["< 1 cm (0점)","1 ~ < 2 cm (1점)","2 ~ < 3 cm (2점)","≥ 3 cm (4점)"],horizontal=True,label_visibility="collapsed")
rs={"< 1 cm (0점)":0,"1 ~ < 2 cm (1점)":1,"2 ~ < 3 cm (2점)":2,"≥ 3 cm (4점)":4}[retraction]
st.markdown("---")

fh(1,"극하근 지방 침윤","Infraspinatus FI","Goutallier 분류 기준","OR 2.91 · 최대 3점")
fatty=st.radio("f",["Grade 0~1 (0점)","Grade ≥ 2 (3점)"],horizontal=True,label_visibility="collapsed")
fs=0 if "0~1" in fatty else 3

with st.expander("ℹ️ Goutallier 분류 기준 상세"):
    st.markdown("""
    <div style="padding:4px 0">
        <p style="font-size:14px;font-weight:700;color:#1a1a2e;margin-bottom:8px">
            📖 Goutallier Classification
        </p>
        <p style="font-size:12px;color:#777;margin-bottom:12px;line-height:1.6">
            Goutallier et al. (1994)이 제안한 회전근개 근육의 지방 변성 등급 분류입니다.<br>
            수술 전 MRI 또는 CT에서 평가하며, RoHI에서는 <strong style="color:#E67E22">극하근(Infraspinatus) Grade ≥ 2</strong>를 기준으로 3점을 부여합니다.
        </p>
        <table class="goutallier-table">
            <thead>
                <tr><th style="width:80px">Grade</th><th>설명</th><th style="width:90px;text-align:center">RoHI</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong style="color:#27AE60">Grade 0</strong></td>
                    <td>정상 근육 — 지방 침윤 없음 (Normal muscle)</td>
                    <td style="text-align:center;color:#27AE60;font-weight:700">0점</td>
                </tr>
                <tr>
                    <td><strong style="color:#2ECC71">Grade 1</strong></td>
                    <td>약간의 지방 줄무늬 (Some fatty streaks)</td>
                    <td style="text-align:center;color:#27AE60;font-weight:700">0점</td>
                </tr>
                <tr style="background:#FFF5EB">
                    <td><strong style="color:#E67E22">Grade 2</strong></td>
                    <td>근육 > 지방이나 의미있는 지방 침윤 (Fat &lt; Muscle)</td>
                    <td style="text-align:center;color:#E67E22;font-weight:700">3점 ⚠️</td>
                </tr>
                <tr style="background:#FFF0E6">
                    <td><strong style="color:#D35400">Grade 3</strong></td>
                    <td>근육과 지방 비율 동일 (Fat = Muscle)</td>
                    <td style="text-align:center;color:#E67E22;font-weight:700">3점 ⚠️</td>
                </tr>
                <tr style="background:#FDEBE6">
                    <td><strong style="color:#C0392B">Grade 4</strong></td>
                    <td>지방이 근육보다 많음 (Fat &gt; Muscle)</td>
                    <td style="text-align:center;color:#E67E22;font-weight:700">3점 ⚠️</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top:14px;padding:12px 14px;background:linear-gradient(135deg,#F0F4F8,#E8EDF2);border-radius:12px;font-size:11px;color:#555;line-height:1.8">
            <strong style="color:#333">📌 임상적 의의:</strong><br>
            • Grade ≥ 2 중등도 이상 지방 침윤 시 재파열률 유의하게 증가 (59% vs 25%, Khair et al.)<br>
            • 극하근의 지방 변성은 근육·건 질(quality)을 반영하는 핵심 지표<br>
            • 지방 변성은 수술 후에도 호전되지 않으므로 수술 전 평가가 중요 (Gladstone et al.)<br>
            • Massive tear에서 극하근 지방 침윤은 가장 중요한 독립적 예후인자 (OR 11.25, Chung et al.)
        </div>
    </div>
    """,unsafe_allow_html=True)
st.markdown("---")

fh(2,"나이","Age","수술 시점 연령","OR 2.71 · 최대 2점")
age=st.radio("a",["< 70세 (0점)","≥ 70세 (2점)"],horizontal=True,label_visibility="collapsed")
a_s=0 if "< 70" in age else 2
st.markdown("---")

fh(3,"전후방 파열 크기","AP Tear Size","Footprint 외측 가장자리 기준 측정","OR 1.94 · 최대 2점")
ap=st.radio("ap",["≤ 2.5 cm (0점)","> 2.5 cm (2점)"],horizontal=True,label_visibility="collapsed")
ap_s=0 if "≤ 2.5" in ap else 2
st.markdown("---")

fh(4,"골밀도","BMD","DEXA T-score 기준","OR 1.95 · 최대 2점")
bmd=st.radio("bmd",["T-score > −2.5 (0점)","T-score ≤ −2.5 (2점)"],horizontal=True,label_visibility="collapsed")
b_s=0 if ">" in bmd else 2
st.markdown("---")

fh(5,"노동 활동 수준","Work Activity","직업적 신체 활동 강도","OR 2.18 · 최대 2점")
work=st.radio("w",["낮음 ~ 중간 (0점)","높음 / 중노동 (2점)"],horizontal=True,label_visibility="collapsed")
w_s=0 if "낮음" in work else 2

with st.expander("ℹ️ 활동 수준 분류 기준 상세"):
    st.markdown("""
    <div style="padding:4px 0">
        <p style="font-size:14px;font-weight:700;color:#1a1a2e;margin-bottom:8px">
            📖 노동 및 스포츠 활동 수준 분류
        </p>
        <p style="font-size:12px;color:#777;margin-bottom:14px;line-height:1.6">
            Kwon et al. (2019)에서 정의한 활동 수준 분류입니다.<br>
            RoHI에서는 <strong style="color:#34495E">노동 활동 수준이 '높음'</strong>인 경우에만 2점을 부여합니다.
        </p>

        <p style="font-size:13px;font-weight:700;color:#34495E;margin-bottom:6px">🔨 노동 활동 수준 (Work Activity)</p>
        <table class="goutallier-table">
            <thead>
                <tr><th style="width:80px">수준</th><th>정의</th><th style="width:70px;text-align:center">RoHI</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong style="color:#27AE60">낮음</strong></td>
                    <td>좌식 업무 (Sedentary work) — 사무직, 경영직 등</td>
                    <td style="text-align:center;color:#27AE60;font-weight:700">0점</td>
                </tr>
                <tr>
                    <td><strong style="color:#2ECC71">중간</strong></td>
                    <td>경도 육체 노동 (Manual labor with less activity) — 가벼운 수작업, 서비스직 등</td>
                    <td style="text-align:center;color:#27AE60;font-weight:700">0점</td>
                </tr>
                <tr style="background:#F2F3F4">
                    <td><strong style="color:#E74C3C">높음</strong></td>
                    <td>중노동 (Heavy manual labor) — 건설, 농업, 운반 등 반복적 중량물 취급</td>
                    <td style="text-align:center;color:#E74C3C;font-weight:700">2점 ⚠️</td>
                </tr>
            </tbody>
        </table>

        <p style="font-size:13px;font-weight:700;color:#34495E;margin:18px 0 6px">🏃 스포츠 활동 수준 (Sports Activity) — 참고용</p>
        <table class="goutallier-table">
            <thead>
                <tr><th style="width:80px">수준</th><th>정의</th><th>예시</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong style="color:#27AE60">낮음</strong></td>
                    <td>스포츠 활동에 거의 참여하지 않음</td>
                    <td style="color:#888">—</td>
                </tr>
                <tr>
                    <td><strong style="color:#F39C12">중간</strong></td>
                    <td>정적 스포츠 참여</td>
                    <td style="color:#888">달리기, 자전거, 골프, 요가</td>
                </tr>
                <tr>
                    <td><strong style="color:#E74C3C">높음</strong></td>
                    <td>접촉 스포츠 또는 무술 참여</td>
                    <td style="color:#888">농구, 축구, 테니스, 배구, 무술</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top:14px;padding:12px 14px;background:linear-gradient(135deg,#F0F4F8,#E8EDF2);border-radius:12px;font-size:11px;color:#555;line-height:1.8">
            <strong style="color:#333">📌 임상적 의의:</strong><br>
            • 반복적 중량물 취급과 어색한 작업 자세는 지속적 어깨 통증의 위험인자 (Miranda et al.)<br>
            • 어깨 질환과 팔 거상(arm-hand elevation) 간 중등도 연관성 (OR 1.9, van der Molen et al.)<br>
            • 중노동 종사자는 양측성 회전근개 파열 위험이 높음 (Abate et al.)<br>
            • 노동 강도가 높은 환자는 수술 실패 후 예후가 더 불량 (Namdari et al.)<br>
            • RoHI에서는 스포츠 활동이 아닌 <strong>노동 활동 수준만</strong> 점수에 반영됩니다
        </div>
    </div>
    """,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# CALCULATE
# ══════════════════════════════════════════════════════════
total=rs+fs+a_s+ap_s+b_s+w_s
fail=get_fail(total)
heal=100-fail
nm,clr,bg,emo,dsc=get_risk(total)
smap=[("파열 퇴축",rs,4),("극하근 지방 침윤",fs,3),("나이",a_s,2),("전후방 파열 크기",ap_s,2),("골밀도",b_s,2),("노동 활동 수준",w_s,2)]

# ══════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)
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
st.markdown("<br>",unsafe_allow_html=True)

c1,c2=st.columns(2)
with c1:
    st.markdown(f'<div class="metric-card-v2"><div class="metric-icon">📉</div><div class="metric-lbl">예상 치유 실패율</div><div class="metric-val" style="color:#E74C3C">{fail:.1f}%</div></div>',unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card-v2"><div class="metric-icon">📈</div><div class="metric-lbl">예상 치유 성공률</div><div class="metric-val" style="color:#27AE60">{heal:.1f}%</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
active=[(n,v,mx) for n,v,mx in smap if v>0]
if active:
    st.markdown("##### 📊 점수 구성")
    for n,v,mx in active:
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
        st.success(f"**✅ 봉합 수술 (Standard Repair) 권고**\n\nRoHI **{total}점 (< 7)**으로 일반 봉합 수술로 충분한 치유율을 기대할 수 있습니다.\n\n- 예상 치유 성공률: **{heal:.1f}%**\n- 단일열 또는 이열 봉합 적용 가능")
    else:
        st.warning(f"**🔧 이식물 보강 수술 권고 (Graft Augmentation)**\n\nRoHI **{total}점 (≥ 7)**으로 일반 봉합 시 치유 실패 위험이 높습니다.\n6점에서 치유율 66%이던 것이 7점에서 38%로 급격히 하락하므로,\n**무세포 동종 진피 이식물(Acellular Dermal Allograft)** 등을 이용한 보강 수술이 권고됩니다.")
        st.markdown("""
        <div class="info-card" style="background:#f8f9fa;border:1px solid #e0e0e0;color:#555">
            <strong style="color:#333">📚 이식물 보강 효과 (문헌 근거):</strong><br>
            • 대형 파열: 일반 수술 40% → 보강 시 85% 치유율 (Barber et al.)<br>
            • 봉합-건 접합부 생역학적 강도 62% 증가 (Omae et al.)<br>
            • 동종 진피 이식물 치유율 82% vs 이종 이식물 68% vs 일반 수술 49% (Bailey et al.)<br>
            • Bioinductive bovine collagen implant 치유율 83.5% (Bushnell et al.)<br>
            • Porcine dermal patch 보강 시 97.6% vs 일반 수술 59.5% (Avanzi et al.)
        </div>
        """,unsafe_allow_html=True)
else:
    if a_s==0:
        st.info("**< 70세: 관절 보존 수술 고려**\n\n젊은 환자에서 수복 불가능한 파열의 경우, 견갑하근 상태 및 파열 특성에 따라 치료를 선택합니다.")
        ca,cb=st.columns(2)
        with ca:
            st.markdown('<div class="info-card" style="background:#F5EEF8;border:1px solid #D7BDE2"><div style="font-size:14px;font-weight:700;color:#6C3483;margin-bottom:8px">💜 견갑하근 보존/수복 가능</div><div style="font-size:12px;color:#555;line-height:1.8">• 상관절낭 재건 (SCR)<br>• vs 건 이전술 (Tendon Transfer)</div></div>',unsafe_allow_html=True)
        with cb:
            st.markdown('<div class="info-card" style="background:#FDEDEC;border:1px solid #F5B7B1"><div style="font-size:14px;font-weight:700;color:#922B21;margin-bottom:8px">❤️‍🩹 견갑하근 손상</div><div style="font-size:12px;color:#555;line-height:1.8">• 역행성 견관절 치환술 (RSA)<br>• vs 건 이전술 (Tendon Transfer)</div></div>',unsafe_allow_html=True)
        st.caption("※ 외회전 완전 소실 시 (극하근 + 소원근 침범) → 하승모근 건 이전술 고려")
        st.caption("※ Hamada grade 3 이상 → 관절 보존 수술 성공률 저하 (SCR 치유율 < 50%, Denard et al.)")
    else:
        st.error("**≥ 70세: 부분 봉합 (Partial Repair)**\n\n고령 환자에서 수복 불가능한 파열의 경우,\n관절염 변화가 경미하다면 (Hamada grade 1-2)\n**부분 봉합 ± 이식물 보강**을 고려할 수 있습니다.\n\n단, 부분 봉합의 결과는 시간이 지남에 따라 악화될 수 있습니다 (Shon et al.).")

# ══════════════════════════════════════════════════════════
# DETAIL TABLE
# ══════════════════════════════════════════════════════════
with st.expander("📋 점수별 상세 데이터 (연구 코호트 기준)"):
    rows=[d for d in RISK_DATA if d["sens"] is not None]
    df=pd.DataFrame(rows); df.columns=["점수 (≥)","민감도 (%)","특이도 (%)","양성예측도 (%)"]
    def hl(row):
        if row["점수 (≥)"]==total: return [f"background-color:{clr}22;font-weight:bold"]*len(row)
        return [""]*len(row)
    st.dataframe(df.style.apply(hl,axis=1).format(precision=1),use_container_width=True,hide_index=True)
    st.caption("* 민감도/특이도는 해당 점수를 임계점으로 설정했을 때의 값입니다.")

# ══════════════════════════════════════════════════════════
# DISCLAIMER & REFERENCES
# ══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ 주의사항</strong><br>
    본 계산기는 Kwon et al. (2019) AJSM의 RoHI 점수 체계와
    Jackson, Bedi & Denard (2022) Arthroscopy의 치료 알고리즘을 기반으로 합니다.
    연구 코호트(603명)에서의 후향적 검증 결과이며, 다른 코호트에서의 외적 타당도는 아직 검증되지 않았습니다.
    개별 환자의 치료 결정은 반드시 담당 의사의 종합적 판단에 따라야 합니다.
    이 도구는 치료를 거부하는 근거로 사용되어서는 안 됩니다.
</div>
""",unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:24px;padding:16px;font-size:12px;color:#999;line-height:2">
    <strong style="color:#666">References</strong><br>
    <a class="ref-link" href="https://journals.sagepub.com/doi/10.1177/0363546518810763" target="_blank">
        Kwon et al. <em>Am J Sports Med.</em> 2019;47(1):173-180
    </a><br>
    <a class="ref-link" href="https://www.arthroscopyjournal.org/article/S0749-8063(21)00963-4/fulltext" target="_blank">
        Jackson et al. <em>Arthroscopy.</em> 2022;38(7):2342-2347
    </a>
</div>
""",unsafe_allow_html=True)
