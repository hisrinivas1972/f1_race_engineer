import streamlit as st
from chat import setup_gemini, ask_strategy
from utils import format_strategy_context

st.set_page_config(page_title="Mach - F1 Race Engineer", layout="wide")

st.sidebar.title("🔐 API Configuration")
google_api_key = st.sidebar.text_input("Google API Key", type="password")
eleven_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
voice_id = st.sidebar.text_input("ElevenLabs Voice ID")

st.title("🏎️ Mach - F1 Race Engineer")
st.markdown("Chat with your AI race strategist to explore optimal race strategies.")

# Strategy Inputs
st.header("📋 Race Setup")

col1, col2 = st.columns(2)
with col1:
    track = st.selectbox("Track", ["Silverstone", "Monza", "Spa", "Suzuka"])
    driver = st.selectbox("Driver", ["VER", "HAM", "LEC", "NOR"])
    grid = st.number_input("Grid Position", 1, 20, 1)
    air_temp = st.number_input("Air Temp (°C)", 10, 50, 25)
    track_temp = st.number_input("Track Temp (°C)", 10, 60, 35)

with col2:
    weather = st.selectbox("Weather", ["Dry", "Wet", "Mixed"])
    pit_loss = st.number_input("Pit Loss (s)", 15, 40, 22)
    degradation = st.selectbox("Degradation", ["Low", "Medium", "High"])
    safety_car = st.slider("Safety Car Probability (%)", 0, 100, 20)
    overtake_difficulty = st.slider("Overtaking Difficulty (1-10)", 1, 10, 5)

st.header("🛞 Tyre Allocation")
soft = st.number_input("Soft Sets", 0, 5, 2)
medium = st.number_input("Medium Sets", 0, 5, 3)
hard = st.number_input("Hard Sets", 0, 5, 2)

# Strategy Chat
if google_api_key:
    model = setup_gemini(google_api_key)
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
        "overtake_difficulty": overtake_difficulty
    }

    prompt = format_strategy_context(user_inputs)
    st.header("💬 Mach - Strategy Chat")

    if st.button("Ask for Strategy"):
        with st.spinner("Thinking..."):
            response = ask_strategy(model, prompt)
            st.success("Strategy Received")
            st.markdown(response)

        # Optional: Speak response
        if eleven_api_key and voice_id:
            from elevenlabs import set_api_key, generate, play
            set_api_key(eleven_api_key)
            audio = generate(text=response, voice=voice_id)
            play(audio)
else:
    st.warning("Please enter your Google API key in the sidebar.")
