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
