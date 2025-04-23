import ctypes
import json
import os
import tkinter as tk
from ctypes import windll

import pydash
import pyqrcode
import threading
from io import BytesIO

import threading
import tkinter as tk
import os
from ctypes import windll


def generate_qr_and_show(content):
    # 生成二维码
    qr = pyqrcode.create(content)
    buffer = BytesIO()
    qr.png(buffer, scale=8, module_color=(0, 0, 0, 255), background=(255, 255, 255, 255))
    png_data = buffer.getvalue()

    class WindowThread(threading.Thread):
        def __init__(self):
            super().__init__()
            self._stop_event = threading.Event()
            self.daemon = True  # 主线程退出时自动结束
            self.window = None

        def stop(self):
            """请求线程停止"""
            # print("调用关闭")
            self._stop_event.set()

        def should_stop(self):
            """检查是否应该停止"""
            return self._stop_event.is_set()

        def run(self):
            try:

                # Windows DPI感知设置
                if os.name == 'nt':
                    windll.shcore.SetProcessDpiAwareness(1)

                # 创建主窗口
                window = tk.Tk()
                window.title("登录")
                window.resizable(False, False)

                # DPI缩放计算
                dpi_scale = window.winfo_fpixels('1i') / 96

                # 窗口尺寸设置
                base_size = 200
                min_width = int(base_size * 1.1 * dpi_scale)
                min_height = int(base_size * 1.4 * dpi_scale)
                window.minsize(min_width, min_height)

                # 主界面布局
                main_frame = tk.Frame(window)
                main_frame.pack(padx=int(10 * dpi_scale), pady=int(12 * dpi_scale))

                # 显示二维码
                img = tk.PhotoImage(data=png_data)
                label = tk.Label(main_frame, image=img)
                label.image = img
                label.pack()

                # 文字标签
                font_size = int(8 * dpi_scale)
                text_label = tk.Label(
                    main_frame,
                    text="使用微信扫一扫登录",
                    font=('Microsoft YaHei', font_size)
                )
                text_label.pack(pady=(int(10 * dpi_scale), 0))

                # 窗口居中
                width = max(min_width, window.winfo_reqwidth())
                height = max(min_height, window.winfo_reqheight())
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
                window.geometry(f"{width}x{height}+{x}+{y}")
                def on_closed_set():
                    if self.should_stop():
                        window.quit()
                        # window.destroy()
                    else:
                        window.after(100, on_closed_set)

                def window_close():
                    window.quit()

                # 拦截窗口关闭事件
                window.protocol("WM_DELETE_WINDOW", window_close)
                window.after(100, on_closed_set)

                window.mainloop()

            finally:
                self.cleanup()

        def cleanup(self):
            """清理资源"""
            pass
            # print("Cleaning up resources")

    # 启动 tkinter 在单独的线程中
    tkinter_thread = WindowThread()
    tkinter_thread.start()

    return tkinter_thread, tkinter_thread.stop


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
