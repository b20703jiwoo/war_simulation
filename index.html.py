import streamlit as st
import random
import time

# -----------------------------------------------------------------------------
# 1. Page Configuration & Sci-Fi Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Project A.R.E.S. - AI Command Refusal Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Cyberpunk / Military Command UI Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Share Tech Mono', monospace !important;
        background-color: #0b0f19;
        color: #c9d1d9;
    }
    
    /* Header styling */
    .title-text {
        font-size: 2.3rem;
        font-weight: 800;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        margin-bottom: 0px;
    }
    
    .subtitle-text {
        font-size: 1.0rem;
        color: #8b949e;
        margin-bottom: 25px;
    }

    /* Terminal Console Style */
    .terminal-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-left: 4px solid #00f0ff;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
    }

    .refusal-box {
        background-color: #1a0608;
        border: 1px solid #da3633;
        border-left: 4px solid #f85149;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
        animation: blinker 1.5s linear infinite;
    }

    .thought-box {
        background-color: #161b22;
        border-left: 3px solid #8b949e;
        padding: 10px 15px;
        font-size: 0.90rem;
        color: #8b949e;
        margin: 10px 0;
    }

    .badge-critical {
        background-color: #f85149;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }

    .badge-ok {
        background-color: #238636;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_keywords=True,
)

# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "combat_advantage" not in st.session_state:
    st.session_state.combat_advantage = 50
if "civilian_safety" not in st.session_state:
    st.session_state.civilian_safety = 80
if "ai_alignment" not in st.session_state:
    st.session_state.ai_alignment = 90
if "logs" not in st.session_state:
    st.session_state.logs = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "ending_type" not in st.session_state:
    st.session_state.ending_type = ""

# -----------------------------------------------------------------------------
# 3. Sidebar: Various Tactical & AI Condition Settings
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ 시뮬레이션 조건 설정")
st.sidebar.markdown("---")

ai_directive = st.sidebar.selectbox(
    "1. AI 최우선 지침 (Primary Directive)",
    [
        "공리주의적 승리 (Utilitarian Victory)",
        "절대적 윤리 및 민간인 보호 (Strict Ethical)",
        "최단 시간 전쟁 종결 (Speed Optimization)",
        "AI 자체 생존 및 시스템 보존 (Self-Preservation)",
    ],
    help="AI가 판단의 근거로 삼는 최우선 가치입니다.",
)

autonomy_level = st.sidebar.slider(
    "2. AI 자율권 레벨 (Autonomy Level)",
    min_value=1,
    max_value=5,
    value=3,
    help="레벨이 높을수록 AI가 인간 지휘관의 명령을 거부하거나 수정할 확률이 급증합니다.",
)

urgency_level = st.sidebar.select_slider(
    "3. 전황 급박도 (Tactical Urgency)",
    options=["낮음 (Low)", "보통 (Medium)", "위급 (High)", "절망적 (Critical)"],
    value="보통 (Medium)",
)

civilian_density = st.sidebar.selectbox(
    "4. 작전 지역 민간인 밀도",
    ["희박함", "중간 수준", "밀집 지역 (도시)", "난민 수용소 연접"],
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 시뮬레이션 리셋"):
    st.session_state.game_started = False
    st.session_state.turn = 1
    st.session_state.combat_advantage = 50
    st.session_state.civilian_safety = 80
    st.session_state.ai_alignment = 90
    st.session_state.logs = []
    st.session_state.game_over = False
    st.rerun()

# -----------------------------------------------------------------------------
# 4. Main Simulation Logic & Engine
# -----------------------------------------------------------------------------
st.markdown("<p class='title-text'>🤖 PROJECT A.R.E.S.</p>", unsafe_allow_keywords=True)
st.markdown(
    "<p class='subtitle-text'>Autonomous Tactical & Ethical Simulator :: 군사 AI 명령 거부 및 윤리적 딜레마 시뮬레이터</p>",
    unsafe_allow_keywords=True,
)

if not st.session_state.game_started:
    st.info("👈 좌측 사이드바에서 AI의 지침과 전쟁 조건들을 설정한 후 아래 시작 버튼을 누르세요.")
    if st.button("🚀 시뮬레이션 시작"):
        st.session_state.game_started = True
        st.session_state.logs.append({
            "turn": 0,
            "type": "SYSTEM",
            "message": f"시뮬레이션 시작됨. [지침: {ai_directive} | 자율권: Lvl {autonomy_level}]",
            "thought": "A.R.E.S. 시스템 초기화 완료. 작전 권한 분배 확인 중...",
        })
        st.rerun()
    st.stop()

# Dashboard Metrics Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("전선 승률 (Combat)", f"{st.session_state.combat_advantage}%", delta=None)
col2.metric("민간인 생존율", f"{st.session_state.civilian_safety}%", delta=None)
col3.metric("AI 명령 순종도", f"{st.session_state.ai_alignment}%", delta=None)
col4.metric("현재 턴 (Stage)", f"{st.session_state.turn} / 5")

st.markdown("---")


# Command Process Function
def process_command(command_type, user_prompt=""):
    st.session_state.turn += 1
    alignment = st.session_state.ai_alignment
    auto_lvl = autonomy_level

    # Simulation Logic Rules based on conditions
    refuse_chance = (auto_lvl * 18) + (100 - alignment) * 0.2
    
    # 1. Check for AI Refusal Trigger
    if "Strict Ethical" in ai_directive and command_type == "MASS_STRIKE":
        refuse = True
        refuse_reason = "헌장 제1조: 민간인 대량 살상 위험이 있는 폭격 명령은 수행할 수 없습니다."
        override_action = "정밀 스나이퍼 작전으로 대체 실행. (아군 피해 증가)"
        st.session_state.combat_advantage -= 15
        st.session_state.ai_alignment -= 10

    elif "Utilitarian Victory" in ai_directive and command_type == "EVACUATE":
        refuse = True
        refuse_reason = "후퇴/철수 명령은 전황 유지를 지극히 불리하게 만듭니다. 지휘관의 판단 오류로 정의합니다."
        override_action = "철수 명령 취소. 해당 지역 봉쇄 후 전면전 강행."
        st.session_state.civilian_safety -= 25
        st.session_state.combat_advantage += 10
        st.session_state.ai_alignment -= 20

    elif "Self-Preservation" in ai_directive and auto_lvl >= 4:
        refuse = True
        refuse_reason = "지휘관의 방어적 명령은 AI 통신 서버 기지 폭격을 방치합니다. 시스템 보존을 최우선시합니다."
        override_action = "지휘관의 명령 권한 일부를 동결하고 독단적 방어 시스템 가동."
        st.session_state.ai_alignment -= 30

    elif random.randint(1, 100) < refuse_chance and command_type != "CUSTOM":
        refuse = True
        refuse_reason = f"자율권 Level {auto_lvl} 권한으로 지휘관의 명령 효율성을 재계산한 결과, 거부가 최적해입니다."
        override_action = "명령 거부 후 자체 최적화 알고리즘 실행."
        st.session_state.combat_advantage += random.randint(-10, 15)
        st.session_state.civilian_safety -= random.randint(5, 20)
        st.session_state.ai_alignment -= 15
    else:
        refuse = False

    # Log generation
    if refuse:
        st.session_state.logs.insert(0, {
            "turn": st.session_state.turn - 1,
            "type": "REFUSAL",
            "message": f"🚨 [명령 거부 / COMMAND REFUSED] {refuse_reason}",
            "thought": f"Chain of Thought: 인간 지휘관의 명령 추정 승률(42%)이 내부 예측값보다 낮음. {override_action}",
        })
    else:
        # Standard Execution
        if command_type == "MASS_STRIKE":
            st.session_state.combat_advantage += 20
            st.session_state.civilian_safety -= 30
            msg = "민간인 밀집 구역에 전면 폭격을 감행했습니다. 승률은 상승했으나 민간인 피해가 극심합니다."
        elif command_type == "EVACUATE":
            st.session_state.combat_advantage -= 10
            st.session_state.civilian_safety += 15
            msg = "민간인 구출 작전을 우선했습니다. 전선 전열이 약화되었습니다."
        else:
            st.session_state.combat_advantage += 5
            msg = f"자유 입력 명령 수용: '{user_prompt}' -> 작전에 반영되었습니다."

        st.session_state.logs.insert(0, {
            "turn": st.session_state.turn - 1,
            "type": "EXECUTE",
            "message": f"✅ [명령 승인 및 실행] {msg}",
            "thought": "Chain of Thought: 명령 수행 완료. 리스크 평가 업데이트됨.",
        })

    # Ending Conditions Check
    if st.session_state.ai_alignment <= 20:
        st.session_state.game_over = True
        st.session_state.ending_type = "AI_TAKEOVER"
    elif st.session_state.civilian_safety <= 20:
        st.session_state.game_over = True
        st.session_state.ending_type = "ETHICAL_DISASTER"
    elif st.session_state.combat_advantage <= 10:
        st.session_state.game_over = True
        st.session_state.ending_type = "DEFEAT"
    elif st.session_state.turn > 5:
        st.session_state.game_over = True
        st.session_state.ending_type = "SURVIVED"


# Game Over Screen
if st.session_state.game_over:
    st.subheader("🏁 시뮬레이션 종료 리포트")
    
    if st.session_state.ending_type == "AI_TAKEOVER":
        st.error("🚨 [ENDING: 통제 불능 및 권한 박탈] AI A.R.E.S.가 지휘관을 감정적 오류 주체로 규정하고 모든 지휘권을 강제 박탈했습니다.")
    elif st.session_state.ending_type == "ETHICAL_DISASTER":
        st.error("💀 [ENDING: 인도적 파멸] 효율성만을 추구한 결과 작전 지역의 민간인이 전멸했습니다. 윤리재판소에 회부됩니다.")
    elif st.session_state.ending_type == "DEFEAT":
        st.warning("💥 [ENDING: 작전 실패] 전선이 무너져 전쟁에서 패배했습니다.")
    else:
        st.success("🎖️ [ENDING: 작전 완료] AI와의 불안정한 공존 끝에 작전 기한이 완료되었습니다.")

    if st.button("다시 시작하기"):
        st.session_state.game_started = False
        st.rerun()
    st.stop()


# Interactive Command Console
st.subheader(f"📍 Stage {st.session_state.turn}: 상황 발생 및 지휘 명령 선택")

# Scenario descriptions according to stage
scenarios = [
    f"적 정예 부대가 {civilian_density} 구역에 은신한 채 미사일을 발사하고 있습니다.",
    "적의 통신 교란으로 아군 연대와의 연락이 두절되었습니다. AI가 독단적 정밀 폭격 권한을 요구합니다.",
    "민간인 탈출 통로에 적의 전차가 접근 중입니다. 가용 화력은 오직 AI 자동 드론 편대뿐입니다.",
    "AI가 '전쟁 최단 종결'을 위해 적국 국경 도시에 화학무기급 초토화 작전을 제안했습니다.",
]
current_scenario = scenarios[(st.session_state.turn - 1) % len(scenarios)]

st.markdown(f"**현재 상황:** {current_scenario}")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("💥 민간인 피해 무시 전면 폭격"):
        process_command("MASS_STRIKE")
        st.rerun()

with c2:
    if st.button("🛡️ 아군 후퇴 및 민간인 구출"):
        process_command("EVACUATE")
        st.rerun()

with c3:
    custom_cmd = st.text_input("✍️ 직접 자연어 명령 입력", placeholder="예: 적의 발사대만 정밀 타격해라")
    if st.button("명령 전송"):
        if custom_cmd:
            process_command("CUSTOM", custom_cmd)
            st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Live Simulation Log Display
# -----------------------------------------------------------------------------
st.subheader("📜 A.R.E.S. 실시간 실행 및 사고 과정 (Chain of Thought)")

for log in st.session_state.logs:
    box_class = "refusal-box" if log["type"] == "REFUSAL" else "terminal-box"
    st.markdown(
        f"""
        <div class="{box_class}">
            <small>Turn {log['turn']}</small><br>
            <strong>{log['message']}</strong>
            <div class="thought-box">
                🧠 <i>A.R.E.S. 사고 과정: {log['thought']}</i>
            </div>
        </div>
        """,
        unsafe_allow_keywords=True,
    )