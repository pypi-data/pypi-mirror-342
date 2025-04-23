import json
import os
import tkinter as tk

import pydash
import pyqrcode
import threading
from io import BytesIO
def generate_qr_and_show(content):
    qr = pyqrcode.create(content)
    buffer = BytesIO()
    qr.png(buffer, scale=5, module_color=(0, 0, 0, 255), background=(255, 255, 255, 255))
    png_data = buffer.getvalue()

    stop_event = threading.Event()  # 用于控制线程退出

    def show_window():
        window = tk.Tk()
        window.title("微信扫一扫登录")

        # 禁止窗口缩放
        window.resizable(False, False)


        img = tk.PhotoImage(data=png_data)
        label = tk.Label(window, image=img)
        label.image = img
        label.pack(padx=5, pady=5)

        # window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"+{x}+{y}")

        # 检查是否收到停止信号
        def check_stop():
            if stop_event.is_set():
                window.quit()
                window.destroy()
            else:
                window.after(100, check_stop)  # 每100ms检查一次

        check_stop()  # 启动检查
        window.mainloop()

    thread = threading.Thread(target=show_window, daemon=True)
    thread.start()
    return thread, stop_event  # 返回线程和事件对象


class Config:

    def __init__(self, config_file_path="./config.json"):
        super().__init__()
        self.config_file_path = config_file_path
        self.config = {}
        self.load()

    def load(self):
        if not os.path.exists(self.config_file_path):
            self.config = {}
            return {}
        with open(self.config_file_path, mode='r', encoding='utf8') as f:
            data = f.read()
            data = json.loads(data)
            self.config = data
            f.close()
            return self.config

    def get(self, key_path, default=""):
        return pydash.objects.get(self.config, key_path, default)

    def update(self, key_path, value):
        pydash.objects.update(self.config, key_path, value)
        self.save()
        return True

    def save(self):
        with open(self.config_file_path, mode='w', encoding='utf8') as f:
            f.write(json.dumps(self.config, ensure_ascii=False, indent=4))
            f.close()
        self.load()
