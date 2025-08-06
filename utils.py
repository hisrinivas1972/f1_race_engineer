import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def format_strategy_context(inputs: dict) -> str:
    return f"""
**Track:** {inputs['track']}
**Driver:** {inputs['driver']}
**Grid Position:** {inputs['grid']}
**Air Temp:** {inputs['air_temp']} °C
**Track Temp:** {inputs['track_temp']} °C
**Weather:** {inputs['weather']}
**Pit Loss:** {inputs['pit_loss']} s
**Degradation:** {inputs['degradation']}
**Tyre Sets:** Soft = {inputs['soft']}, Medium = {inputs['medium']}, Hard = {inputs['hard']}
**Safety Car Probability:** {inputs['safety_car']}%
**Overtaking Difficulty:** {inputs['overtake_difficulty']}
""".strip()

def simulate_lap_times(tyre_choice: str, degradation: str, laps: int) -> pd.DataFrame:
    base_times = {"Soft": 95, "Medium": 98, "Hard": 100}
    degradation_factors = {"Low": 0.1, "Medium": 0.3, "High": 0.5}

    base = base_times.get(tyre_choice, 100)
    degr = degradation_factors.get(degradation, 0.3)

    lap_times = [base + degr * lap for lap in range(laps)]
    df = pd.DataFrame({"Lap": list(range(1, laps+1)), "LapTime": lap_times})
    return df

def plot_stints(driver: str, degradation: str):
    fig, ax = plt.subplots(figsize=(6, 2))
    stints = [5, 7, 3]
    colors = ['red', 'yellow', 'blue']

    start = 0
    for stint, color in zip(stints, colors):
        ax.broken_barh([(start, stint)], (0, 5), facecolors=color)
        start += stint

    ax.set_ylim(0, 5)
    ax.set_xlim(0, sum(stints))
    ax.set_xlabel("Laps")
    ax.set_yticks([])
    ax.set_title(f"{driver}'s Stint Visualization (Degradation: {degradation})")
    return fig

def simulate_undercut(degradation: str) -> str:
    delta_map = {"Low": 1.5, "Medium": 2.5, "High": 3.5}
    delta = delta_map.get(degradation, 2.5)
    return f"Expected undercut delta: ~{delta:.1f} seconds. Use pit stops strategically!"
