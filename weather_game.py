import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# 외대앞역 근처 좌표
LAT = 37.5966
LON = 127.0634

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&hourly=precipitation_probability"
    "&current=temperature_2m"
    "&timezone=Asia%2FSeoul"
)

RAIN_THRESHOLD = 40


class WeatherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("외대앞역 우산체크")
        self.root.geometry("520x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#111111")

        self.title_label = tk.Label(
            root,
            text="외대앞역 우산체크",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#111111"
        )
        self.title_label.pack(pady=(20, 10))

        self.desc_label = tk.Label(
            root,
            text="버튼을 눌러 지금 날씨를 확인해라",
            font=("Arial", 12),
            fg="#cccccc",
            bg="#111111"
        )
        self.desc_label.pack(pady=(0, 20))

        self.status_frame = tk.Frame(root, bg="#1e1e1e", bd=0, highlightthickness=0)
        self.status_frame.pack(padx=20, pady=10, fill="both", expand=False)

        self.status_label = tk.Label(
            self.status_frame,
            text="대기 중...",
            font=("Arial", 18, "bold"),
            fg="#00ff99",
            bg="#1e1e1e",
            wraplength=440,
            justify="center",
            height=5
        )
        self.status_label.pack(padx=20, pady=20)

        self.check_button = tk.Button(
            root,
            text="날씨 확인",
            font=("Arial", 16, "bold"),
            width=14,
            height=2,
            bg="#2d6cdf",
            fg="white",
            activebackground="#1f4ea8",
            activeforeground="white",
            command=self.check_weather
        )
        self.check_button.pack(pady=15)

        self.footer_label = tk.Label(
            root,
            text="기준: 강수확률 40% 이상이면 우산 권장",
            font=("Arial", 10),
            fg="#999999",
            bg="#111111"
        )
        self.footer_label.pack(pady=(10, 0))

    def check_weather(self):
        self.status_label.config(text="날씨 불러오는 중...")
        self.root.update()

        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            hourly_times = data["hourly"]["time"]
            rain_probs = data["hourly"]["precipitation_probability"]

            now_str = datetime.now().strftime("%Y-%m-%dT%H:00")
            closest_index = self.find_closest_time_index(hourly_times, now_str)
            rain_prob = rain_probs[closest_index]

            current_temp = None
            if "current" in data and "temperature_2m" in data["current"]:
                current_temp = data["current"]["temperature_2m"]

            if rain_prob >= RAIN_THRESHOLD:
                result_text = (
                    f"현재 강수확률 {rain_prob}%\n"
                    f"우산 챙겨!"
                )
                color = "#ffcc00"
            else:
                result_text = (
                    f"현재 강수확률 {rain_prob}%\n"
                    f"우산 없어도 됨 ㅎㅎ"
                )
                color = "#00ff99"

            if current_temp is not None:
                result_text += f"\n현재 기온 {current_temp}°C"

            self.status_label.config(text=result_text, fg=color)

        except requests.exceptions.RequestException as e:
            self.status_label.config(
                text="네트워크 오류 생김 ㅠㅠ.\n인터넷 연결 확인해주세용....",
                fg="#ff6666"
            )
            messagebox.showerror("오류", f"오류남:\n{e}")
        except (KeyError, ValueError, IndexError) as e:
            self.status_label.config(
                text="오류남2\n 좀 이따가 다시 켜봐.",
                fg="#ff6666"
            )
            messagebox.showerror("오류", f"데이터 잘못 나옴:\n{e}")

    @staticmethod
    def find_closest_time_index(time_list, target_time):
        if target_time in time_list:
            return time_list.index(target_time)
        return 0


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()