import tkinter as tk
import requests
from datetime import datetime

LAT = 37.5966
LON = 127.0634
RAIN_THRESHOLD = 40

API_URL = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&hourly=precipitation_probability"
    f"&current=temperature_2m"
    f"&timezone=Asia%2FSeoul"
)


def check_weather():
    status_label.config(text="날씨 불러오는 중...")
    root.update_idletasks()

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 응답 확인용
        print(data)

        hourly_times = data["hourly"]["time"]
        rain_probs = data["hourly"]["precipitation_probability"]

        now_str = datetime.now().strftime("%Y-%m-%dT%H:00")

        if now_str in hourly_times:
            idx = hourly_times.index(now_str)
        else:
            idx = 0

        rain_prob = rain_probs[idx]

        current_temp = None
        if "current" in data and "temperature_2m" in data["current"]:
            current_temp = data["current"]["temperature_2m"]

        if rain_prob >= RAIN_THRESHOLD:
            msg = f"강수확률 {rain_prob}%\n우산 챙겨!"
        else:
            msg = f"강수확률 {rain_prob}%\n우산 없어도 될 듯"

        if current_temp is not None:
            msg += f"\n기온 {current_temp}°C"

        status_label.config(text=msg)

    except Exception as e:
        status_label.config(text=f"오류 발생:\n{e}")
        print("오류:", e)


root = tk.Tk()
root.title("외대앞역 우산체크")
root.geometry("420x300")
root.resizable(False, False)

title_label = tk.Label(root, text="외대앞역 우산체크", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

status_label = tk.Label(root, text="대기 중...", font=("Arial", 16), justify="center")
status_label.pack(pady=30)

check_button = tk.Button(root, text="날씨 확인", font=("Arial", 14), command=check_weather)
check_button.pack(pady=20)

root.mainloop()