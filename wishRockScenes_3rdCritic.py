from tkinter import Tk, Canvas, Button, Entry, Text
from PIL import Image, ImageTk
from pathlib import Path
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\yesju\OneDrive\바탕 화면\wishU")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# 씬 번호 및 텍스트 초기화
current_scene = 1
dream_text = ""
entry = None  # 텍스트 입력 박스 변수를 전역으로 선언

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    window.attributes('-fullscreen', fullscreen)
    load_scene()

def load_scene():
    global current_scene, dream_text, entry
    # 캔버스를 초기화
    canvas.delete("all")

    if current_scene <= 8:
        # 씬 1부터 8까지의 이미지 로드
        image_path = relative_to_assets(f"scene_{current_scene}.png")
        image = Image.open(image_path)

    elif current_scene == 9:
        # 씬 9: 이미지와 텍스트 입력 박스 로드
        image_path = relative_to_assets("scene_9.png")
        image = Image.open(image_path)

        # 텍스트 입력 박스 생성
        entry = Text(canvas, height=1.5, width=80, borderwidth=0, bg="#C4AAA6", font=("Arial", 16))
        entry.place(relx=0.5, rely=0.5, anchor="center")
        entry.bind("<Return>", lambda event: submit_dream())  # Enter 키로 제출

    elif current_scene >= 10 and current_scene <= 16:
        # 씬 10부터 16까지의 이미지 로드
        image_path = relative_to_assets(f"scene_{current_scene}.png")
        image = Image.open(image_path)

    elif current_scene == 17:
        # 씬 17: 새로 입력할 텍스트 박스 로드
        image_path = relative_to_assets("scene_17.png")
        image = Image.open(image_path)

        # 텍스트 입력 박스 생성
        entry = Text(canvas, height=2, width=50, borderwidth=0, bg="#A8C4A6", font=("Arial", 16))
        entry.place(relx=0.5, rely=0.5, anchor="center")
        entry.bind("<Return>", lambda event: play_dream(entry.get()))  # Enter 키로 제출

    # 이미지 크기 조정
    image_resized = image.resize((window.winfo_width(), window.winfo_height()), Image.ANTIALIAS)
    image_tk = ImageTk.PhotoImage(image_resized)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")

    # 이미지 참조 유지
    canvas.image = image_tk

def submit_dream():
    global current_scene, entry
    dream = entry.get("1.0", "end-1c")  # 텍스트박스의 내용을 가져옴
    if dream:  # 꿈이 입력된 경우에만 씬 전환
        entry.destroy()  # 입력 박스 제거
        current_scene += 1  # 씬 전환
        load_scene()
    else:
        # 입력이 없는 경우, 경고 메시지 표시 (옵션)
        print("꿈을 입력해 주세요.")  # 로그로 메시지 표시, 필요시 메시지 박스로 변경 가능

def play_dream(dream):
    # ElevenLabs API를 사용하여 입력된 텍스트를 음성으로 출력
    client = ElevenLabs(api_key="YOUR_API_KEY")  # API 키 설정
    play(client.generate_audio(dream))  # 새로 입력된 문장을 음성으로 출력
    # 씬 전환 (원하는 경우 씬 전환을 추가할 수 있음)
    current_scene += 1  # 씬 전환
    load_scene()

# 기본 창 설정
window = Tk()
fullscreen = False
window.geometry("1280x720")

# 캔버스 생성
canvas = Canvas(window, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# 초기 씬 로드
load_scene()  # 처음 로드할 때 이미지를 로드하도록 수정

# 전체화면 버튼
fullscreen_button = Button(window, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.pack()

# 클릭 이벤트 바인딩
canvas.bind("<Button-1>", lambda event: next_scene())  # 왼쪽 클릭 시 다음 씬으로

def next_scene():
    global current_scene
    if current_scene < 18:  # 최대 씬 수 체크
        current_scene += 1
        load_scene()

# 초기 씬을 scene_1.png로 설정
load_scene()  # 처음 로드할 때 씬 1을 로드

# 메인 루프 실행
window.mainloop()