import streamlit as st
from chat import setup_gemini, ask_strategy
from utils import format_strategy_context, simulate_lap_times, plot_stints, simulate_undercut

st.set_page_config(page_title="Mach - F1 Race Engineer", layout="wide")

st.sidebar.title("🔐 API Configuration")
google_api_key = st.sidebar.text_input("Google API Key", type="password")
eleven_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
voice_id = st.sidebar.text_input("ElevenLabs Voice ID")

st.title("🏎️ Mach - F1 Race Engineer")

# --- Race Setup Inputs ---
with st.expander("📋 Race Setup & Tyre Allocation", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        track = st.selectbox("Track", ["Silverstone", "Monza", "Spa", "Suzuka"])
        driver = st.selectbox("Driver", ["VER", "HAM", "LEC", "NOR"])
        grid = st.number_input("Grid Position", 1, 20, 10)
        air_temp = st.number_input("Air Temp (°C)", 10, 50, 25)
        track_temp = st.number_input("Track Temp (°C)", 10, 60, 35)
    with col2:
        weather = st.selectbox("Weather", ["Dry", "Wet", "Mixed"])
        pit_loss = st.number_input("Pit Loss (s)", 15, 40, 22)
        degradation = st.selectbox("Degradation", ["Low", "Medium", "High"])
        safety_car = st.slider("Safety Car Probability (%)", 0, 100, 20)
        overtake_difficulty = st.slider("Overtaking Difficulty (1-10)", 1, 10, 5)

    st.markdown("### 🛞 Tyre Allocation")
    col3, col4, col5 = st.columns(3)
    with col3:
        soft = st.number_input("Soft Sets", 0, 5, 2)
    with col4:
        medium = st.number_input("Medium Sets", 0, 5, 3)
    with col5:
        hard = st.number_input("Hard Sets", 0, 5, 2)

user_inputs = {
    "track": track,
    "driver": driver,
    "grid": grid,
    "air_temp": air_temp,
    "track_temp": track_temp,
    "weather": weather,
    "pit_loss": pit_loss,
    "degradation": degradation,
    "soft": soft,
    "medium": medium,
    "hard": hard,
    "safety_car": safety_car,
    "overtake_difficulty": overtake_difficulty,
}

strategy_context_text = format_strategy_context(user_inputs)

container_style = """
    border: 2px solid #ddd;
    padding: 15px;
    border-radius: 8px;
    background-color: #fafafa;
"""

# --- Top row: Strategy Context (30%) & Chat with Mach (70%) ---
col_strategy, col_chat = st.columns([3,7], gap="large")

with col_strategy:
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
    st.header("📋 Strategy Context")
    st.code(strategy_context_text, language="markdown")
    st.markdown("</div>", unsafe_allow_html=True)

with col_chat:
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
    st.header("💬 Chat with Mach")

    if google_api_key:
        model = setup_gemini(google_api_key)
        prompt = strategy_context_text

        if st.button("Ask for Strategy"):
            with st.spinner("Thinking..."):
                response = ask_strategy(model, prompt)
                st.success("Strategy Received")
                st.markdown(response)

                if eleven_api_key and voice_id:
                    from elevenlabs import set_api_key, generate, play
                    set_api_key(eleven_api_key)
                    audio = generate(text=response, voice=voice_id)
                    play(audio)
    else:
        st.warning("Please enter your Google API key in the sidebar.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Bottom row: Simulation Data (30%) below Strategy Context, right empty ---
col_sim, col_empty = st.columns([3,7], gap="large")

with col_sim:
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
    st.header("📊 Simulation Data")

    tyre_choice = st.selectbox("Tyre for Simulation", ["Soft", "Medium", "Hard"], key="sim_tyre")
    laps = st.slider("Number of Laps", 5, 30, 15, key="sim_laps")

    sim_df = simulate_lap_times(tyre_choice, degradation, laps)
    st.line_chart(sim_df.set_index("Lap")["LapTime"])

    st.pyplot(plot_stints(driver, degradation))

    undercut_result = simulate_undercut(degradation)
    st.markdown(f"### Undercut Simulation\n{undercut_result}")
    st.markdown("</div>", unsafe_allow_html=True)

with col_empty:
    st.write("")
