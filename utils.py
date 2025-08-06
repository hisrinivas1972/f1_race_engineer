import pandas as pd
import matplotlib.pyplot as plt

def format_strategy_context(inputs: dict) -> str:
    return f"""
You are an F1 Race Strategist. Based on the following conditions, suggest the optimal race strategy.

Track: {inputs['track']}
Driver: {inputs['driver']}
Grid Position: {inputs['grid']}
Air Temp: {inputs['air_temp']}°C
Track Temp: {inputs['track_temp']}°C
Weather: {inputs['weather']}
Pit Loss: {inputs['pit_loss']}s
Tyre Degradation: {inputs['degradation']}
Tyre Allocation: Soft: {inputs['soft']} | Medium: {inputs['medium']} | Hard: {inputs['hard']}
Safety Car Probability: {inputs['safety_car']}%
Overtaking Difficulty: {inputs['overtake_difficulty']} (1-10)
"""

def simulate_lap_times(compound, degradation, laps=15):
    base_times = {'Soft': 85.0, 'Medium': 86.5, 'Hard': 88.0}
    degrade_factor = {'Low': 0.1, 'Medium': 0.25, 'High': 0.4}
    lap_times = []
    for lap in range(1, laps + 1):
        lap_time = base_times[compound] + degrade_factor[degradation] * lap
        lap_times.append(round(lap_time, 2))
    return pd.DataFrame({'Lap': list(range(1, laps + 1)), 'LapTime': lap_times})

def plot_stints(driver, degradation):
    fig, ax = plt.subplots(figsize=(8, 2))
    colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    ax.barh(driver, 15, color=colors[degradation])
    ax.set_xlabel("Laps")
    ax.set_title(f"Simulated Stint for {driver} ({degradation} degradation)")
    return fig

def simulate_undercut(degradation):
    gain_per_lap = {'Low': 0.2, 'Medium': 0.5, 'High': 0.8}
    laps_undercut = 3
    time_gain = gain_per_lap[degradation] * laps_undercut
    return f"Estimated undercut gain by pitting {laps_undercut} laps earlier: {time_gain:.2f} seconds"
