import streamlit as st

st.set_page_config(
    page_title="RoHI Calculator - 회전근개 치유 예측",
    page_icon="🩺",
    layout="centered",
)

# ── Password Authentication ──
def check_password():
    """비밀번호 확인 후 True/False 반환"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div style="text-align:center;margin-top:60px;margin-bottom:20px">
        <div style="font-size:48px;margin-bottom:12px">🔒</div>
        <div style="font-size:22px;font-weight:800;color:#1a1a2e">RoHI Calculator</div>
        <div style="font-size:13px;color:#999;margin-top:4px">접속하려면 비밀번호를 입력하세요</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("비밀번호", type="password", label_visibility="collapsed", placeholder="비밀번호 입력")
        login_btn = st.button("로그인", use_container_width=True, type="primary")

        if login_btn:
            # ⚠️ 아래 비밀번호를 원하는 값으로 변경하세요
            # Streamlit Cloud 배포 시 st.secrets["password"]를 사용하는 것을 권장합니다
            correct_password = st.secrets.get("password", "rohi2024")

            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")

    return False


if not check_password():
    st.stop()

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap');
    .stApp { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; font-size: 28px; font-weight: 800; color: #1a1a2e; margin-bottom: 0; }
    .sub-title { text-align: center; font-size: 13px; color: #888; margin-top: 4px; margin-bottom: 24px; }
    .badge { display: inline-block; background: #1a1a2e; color: #fff; padding: 4px 14px;
             border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .score-big { font-size: 48px; font-weight: 800; text-align: center; margin: 0; }
    .score-label { font-size: 14px; color: #888; text-align: center; }
    .metric-card { background: #fff; border-radius: 12px; padding: 16px; text-align: center;
                   box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    .metric-value { font-size: 28px; font-weight: 800; }
    .metric-label { font-size: 12px; color: #999; margin-bottom: 4px; }
    .ref-box { background: #f8f9fa; border-radius: 8px; padding: 12px 14px; font-size: 12px;
               color: #666; line-height: 1.7; margin-top: 10px; }
    .algo-header { font-size: 15px; font-weight: 800; color: #1a1a2e; text-align: center; margin-bottom: 4px; }
    .algo-sub { font-size: 11px; color: #999; text-align: center; margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

# ── Risk Data from Kwon et al. (2019) Table 4 ──
RISK_DATA = [
    {"score": 0, "sens": None, "spec": None, "ppv": None},
    {"score": 1, "sens": 100, "spec": 9.4, "ppv": 26.0},
    {"score": 2, "sens": 99.3, "spec": 39.3, "ppv": 34.1},
    {"score": 3, "sens": 95.9, "spec": 47.4, "ppv": 36.1},
    {"score": 4, "sens": 91.0, "spec": 65.1, "ppv": 45.2},
    {"score": 5, "sens": 84.1, "spec": 78.4, "ppv": 55.2},
    {"score": 6, "sens": 74.5, "spec": 85.4, "ppv": 61.7},
    {"score": 7, "sens": 62.1, "spec": 93.6, "ppv": 73.8},
    {"score": 8, "sens": 56.6, "spec": 94.1, "ppv": 75.2},
    {"score": 9, "sens": 44.1, "spec": 95.6, "ppv": 76.2},
    {"score": 10, "sens": 34.5, "spec": 98.3, "ppv": 86.2},
    {"score": 11, "sens": 29.0, "spec": 98.9, "ppv": 89.4},
    {"score": 12, "sens": 12.4, "spec": 99.6, "ppv": 90.0},
    {"score": 13, "sens": 11.0, "spec": 99.6, "ppv": 88.9},
    {"score": 15, "sens": 4.1, "spec": 100, "ppv": 100},
]


def get_cumulative_fail_rate(score):
    if score <= 0:
        return 0.0
    for d in RISK_DATA:
        if d["score"] == score and d["ppv"] is not None:
            return d["ppv"]
    if score >= 15:
        return 100.0
    lower = [d for d in RISK_DATA if d["score"] < score and d["ppv"] is not None]
    upper = [d for d in RISK_DATA if d["score"] > score and d["ppv"] is not None]
    if lower and upper:
        l, u = lower[-1], upper[0]
        ratio = (score - l["score"]) / (u["score"] - l["score"])
        return l["ppv"] + ratio * (u["ppv"] - l["ppv"])
    return lower[-1]["ppv"] if lower else 0.0


def get_risk_level(score):
    if score <= 4:
        return "저위험", "#27AE60", "✅", "치유 실패 가능성이 낮습니다."
    elif score <= 6:
        return "중등도 위험", "#F39C12", "⚠️", "치유 실패 가능성이 중등도입니다."
    elif score <= 9:
        return "고위험", "#E74C3C", "🔴", "치유 실패 가능성이 높습니다."
    else:
        return "초고위험", "#8E1600", "🚨", "치유 실패 가능성이 매우 높습니다."


# ── Header ──
st.markdown('<div style="text-align:center"><span class="badge">Rotator Cuff Healing Index</span></div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">회전근개 치유 예측 계산기</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Kwon et al. (2019) AJSM 기반 · 6가지 독립적 예후인자 · 15점 만점<br>치료 알고리즘: Jackson, Bedi & Denard (2022) Arthroscopy</p>', unsafe_allow_html=True)

st.divider()

# ── Factor Inputs ──
st.subheader("📋 예후인자 입력")

# 1. Tear Retraction
st.markdown("**① 파열 퇴축 (Tear Retraction)** — 파열된 건의 내측 퇴축 거리 · OR: 4.56")
retraction = st.radio(
    "파열 퇴축",
    options=["< 1 cm (0점)", "1 ~ < 2 cm (1점)", "2 ~ < 3 cm (2점)", "≥ 3 cm (4점)"],
    horizontal=True,
    label_visibility="collapsed",
)
retraction_score = {"< 1 cm (0점)": 0, "1 ~ < 2 cm (1점)": 1, "2 ~ < 3 cm (2점)": 2, "≥ 3 cm (4점)": 4}[retraction]

# 2. Fatty Infiltration
st.markdown("**② 극하근 지방 침윤 (Infraspinatus FI)** — Goutallier 분류 기준 · OR: 2.91")
fatty = st.radio(
    "극하근 지방 침윤",
    options=["Grade 0~1 (0점)", "Grade ≥ 2 (3점)"],
    horizontal=True,
    label_visibility="collapsed",
)
fatty_score = 0 if "0~1" in fatty else 3

# 3. Age
st.markdown("**③ 나이 (Age)** — 수술 시점 연령 · OR: 2.71")
age = st.radio(
    "나이",
    options=["< 70세 (0점)", "≥ 70세 (2점)"],
    horizontal=True,
    label_visibility="collapsed",
)
age_score = 0 if "< 70" in age else 2

# 4. AP Tear Size
st.markdown("**④ 전후방 파열 크기 (AP Tear Size)** — Footprint 외측 가장자리 기준 · OR: 1.94")
ap_size = st.radio(
    "전후방 파열 크기",
    options=["≤ 2.5 cm (0점)", "> 2.5 cm (2점)"],
    horizontal=True,
    label_visibility="collapsed",
)
ap_score = 0 if "≤ 2.5" in ap_size else 2

# 5. BMD
st.markdown("**⑤ 골밀도 (Bone Mineral Density)** — DEXA T-score 기준 · OR: 1.95")
bmd = st.radio(
    "골밀도",
    options=["T-score > -2.5 (0점)", "T-score ≤ -2.5 (2점)"],
    horizontal=True,
    label_visibility="collapsed",
)
bmd_score = 0 if "> -2.5" in bmd else 2

# 6. Work Activity
st.markdown("**⑥ 노동 활동 수준 (Work Activity)** — 직업적 신체 활동 강도 · OR: 2.18")
work = st.radio(
    "노동 활동 수준",
    options=["낮음 ~ 중간 (0점)", "높음 / 중노동 (2점)"],
    horizontal=True,
    label_visibility="collapsed",
)
work_score = 0 if "낮음" in work else 2

# ── Calculate ──
total_score = retraction_score + fatty_score + age_score + ap_score + bmd_score + work_score
fail_rate = get_cumulative_fail_rate(total_score)
heal_rate = 100 - fail_rate
level_name, level_color, level_emoji, level_desc = get_risk_level(total_score)

# ── Results ──
st.divider()
st.subheader("📊 결과")

# Score display
st.markdown(f'<p class="score-label">총점</p>', unsafe_allow_html=True)
st.markdown(f'<p class="score-big" style="color:{level_color}">{total_score} / 15</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; font-size:18px; font-weight:700; color:{level_color}">{level_emoji} {level_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; font-size:13px; color:#666">{level_desc}</p>', unsafe_allow_html=True)

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">예상 치유 실패율</div>
        <div class="metric-value" style="color:#E74C3C">{fail_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">예상 치유 성공률</div>
        <div class="metric-value" style="color:#27AE60">{heal_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Score breakdown
st.markdown("")
scores = {
    "파열 퇴축": retraction_score,
    "극하근 지방 침윤": fatty_score,
    "나이": age_score,
    "전후방 파열 크기": ap_score,
    "골밀도": bmd_score,
    "노동 활동 수준": work_score,
}
breakdown_items = {k: v for k, v in scores.items() if v > 0}
if breakdown_items:
    st.markdown("**점수 구성:**")
    for name, val in breakdown_items.items():
        pct = val / 15
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">'
            f'<span style="width:120px;font-size:12px;color:#666;text-align:right">{name}</span>'
            f'<div style="flex:1;height:12px;background:#f0f0f0;border-radius:6px;overflow:hidden">'
            f'<div style="width:{pct*100:.0f}%;height:100%;background:{level_color};border-radius:6px"></div>'
            f'</div>'
            f'<span style="width:30px;font-size:12px;font-weight:700;color:{level_color}">+{val}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Treatment Algorithm ──
st.divider()
st.markdown('<p class="algo-header">🩺 치료 권고 알고리즘</p>', unsafe_allow_html=True)
st.markdown('<p class="algo-sub">Jackson, Bedi & Denard (2022) Arthroscopy 기반 · Hamada grade 1-2 대상</p>', unsafe_allow_html=True)

reparability = st.radio(
    "**파열의 수복 가능성 (Reparability)**",
    options=["수복 가능 (Repairable)", "수복 불가 (Irreparable)"],
    horizontal=True,
)

if "수복 가능" in reparability:
    if total_score < 7:
        st.success(f"""
        **✅ 봉합 수술 (Standard Repair) 권고**
        
        RoHI **{total_score}점 (< 7)**으로 일반 봉합 수술로 충분한 치유율을 기대할 수 있습니다.
        
        - 예상 치유 성공률: **{heal_rate:.1f}%**
        - 단일열 또는 이열 봉합 적용 가능
        """)
    else:
        st.warning(f"""
        **🔧 이식물 보강 수술 권고 (Graft Augmentation)**
        
        RoHI **{total_score}점 (≥ 7)**으로 일반 봉합 시 치유 실패 위험이 높습니다.
        6점에서 치유율 66%이던 것이 7점에서 38%로 급격히 하락하므로,
        **무세포 동종 진피 이식물(Acellular Dermal Allograft)** 등을 이용한 보강 수술이 권고됩니다.
        """)
        st.markdown("""
        <div class="ref-box">
            <strong>이식물 보강 효과 (문헌 근거):</strong><br>
            • 대형 파열: 일반 수술 40% → 보강 시 85% 치유율 (Barber et al.)<br>
            • 봉합-건 접합부 생역학적 강도 62% 증가 (Omae et al.)<br>
            • 동종 진피 이식물 치유율 82% vs 이종 이식물 68% vs 일반 수술 49% (Bailey et al.)<br>
            • Bioinductive bovine collagen implant 치유율 83.5% (Bushnell et al.)<br>
            • Porcine dermal patch 보강 시 97.6% vs 일반 수술 59.5% (Avanzi et al.)
        </div>
        """, unsafe_allow_html=True)

else:  # Irreparable
    if age_score == 0:  # < 70세
        st.info("""
        **< 70세: 관절 보존 수술 고려**
        
        젊은 환자에서 수복 불가능한 파열의 경우, 견갑하근 상태 및 파열 특성에 따라 치료를 선택합니다.
        """)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div style="background:#F5EEF8;border-radius:10px;padding:14px;border:1px solid #D7BDE2;height:100%">
                <div style="font-size:13px;font-weight:700;color:#6C3483;margin-bottom:6px">견갑하근 보존/수복 가능</div>
                <div style="font-size:12px;color:#555;line-height:1.7">
                    • 상관절낭 재건 (SCR)<br>
                    • vs 건 이전술 (Tendon Transfer)
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div style="background:#FDEDEC;border-radius:10px;padding:14px;border:1px solid #F5B7B1;height:100%">
                <div style="font-size:13px;font-weight:700;color:#922B21;margin-bottom:6px">견갑하근 손상</div>
                <div style="font-size:12px;color:#555;line-height:1.7">
                    • 역행성 견관절 치환술 (RSA)<br>
                    • vs 건 이전술 (Tendon Transfer)
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.caption("""
        ※ 외회전 완전 소실 시 (극하근 + 소원근 침범) → 하승모근 건 이전술 고려  
        ※ Hamada grade 3 이상 → 관절 보존 수술 성공률 저하 (SCR 치유율 < 50%, Denard et al.)
        """)
    else:  # ≥ 70세
        st.error("""
        **≥ 70세: 부분 봉합 (Partial Repair)**
        
        고령 환자에서 수복 불가능한 파열의 경우,
        관절염 변화가 경미하다면 (Hamada grade 1-2)
        **부분 봉합 ± 이식물 보강**을 고려할 수 있습니다.
        
        단, 부분 봉합의 결과는 시간이 지남에 따라 악화될 수 있습니다 (Shon et al.).
        """)

# ── Detail Table ──
with st.expander("📊 점수별 상세 데이터 (연구 코호트 기준)"):
    import pandas as pd
    rows = [d for d in RISK_DATA if d["sens"] is not None]
    df = pd.DataFrame(rows)
    df.columns = ["점수 (≥)", "민감도 (%)", "특이도 (%)", "양성예측도 (%)"]
    
    def highlight_row(row):
        if row["점수 (≥)"] == total_score:
            return [f"background-color: {level_color}22; font-weight: bold"] * len(row)
        return [""] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_row, axis=1).format(precision=1),
        use_container_width=True,
        hide_index=True,
    )
    st.caption("* 민감도/특이도는 해당 점수를 임계점으로 설정했을 때의 값입니다.")

# ── Disclaimer ──
st.divider()
st.markdown("""
<div style="background:#FFF9E6;border:1px solid #F5DFA0;border-radius:10px;padding:14px 16px;font-size:11px;color:#8B7A2B;line-height:1.7">
    <strong>⚠️ 주의사항</strong><br>
    본 계산기는 Kwon et al. (2019) AJSM의 RoHI 점수 체계와
    Jackson, Bedi & Denard (2022) Arthroscopy의 치료 알고리즘을 기반으로 합니다.
    연구 코호트(603명)에서의 후향적 검증 결과이며, 다른 코호트에서의 외적 타당도는 아직 검증되지 않았습니다.
    개별 환자의 치료 결정은 반드시 담당 의사의 종합적 판단에 따라야 합니다.
    이 도구는 치료를 거부하는 근거로 사용되어서는 안 됩니다.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:20px;font-size:11px;color:#999;line-height:1.8">
    <strong>References:</strong><br>
    <a href="https://journals.sagepub.com/doi/10.1177/0363546518810763" target="_blank" style="color:#3498DB">
        Kwon et al. Am J Sports Med. 2019;47(1):173-180
    </a><br>
    <a href="https://www.arthroscopyjournal.org/article/S0749-8063(21)00963-4/fulltext" target="_blank" style="color:#3498DB">
        Jackson et al. Arthroscopy. 2022;38(7):2342-2347
    </a>
</div>
""", unsafe_allow_html=True)
