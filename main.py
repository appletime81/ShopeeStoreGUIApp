import time
import threading
import customtkinter as ctk

from PIL import ImageTk
from read_google_sheet import get_secret_key


class TextInput(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")
        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.grid(row=0, column=0, padx=84, pady=65)
        self.focus_force()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.password = None
        self.title("Python專業代寫")
        self.geometry(f"{400}x{200}")
        self.toplevel_window = None
        self.label_for_order_no_input = ctk.CTkLabel(self, text="請輸入您的訂單編號:", width=200)
        self.text_order_no_input = TextInput(self, width=200)
        self.submit_button = ctk.CTkButton(
            self, text="提交", command=self.submit_button_func, width=200
        )
        self.show_top_level_window_button = ctk.CTkButton(
            self,
            text="顯示密碼彈窗",
            command=self.show_top_level_window_button_func,
            width=200,
        )
        self.label_for_order_no_input.pack(pady=7)
        self.text_order_no_input.pack(pady=7)
        self.submit_button.pack(pady=7)
        self.show_top_level_window_button.pack(pady=7)

    def submit_button_func(self):
        self.password = self.text_order_no_input.get()
        thread = threading.Thread(target=self.retrieve_password)
        thread.start()
        self.text_order_no_input.delete(0, "end")
        self.text_order_no_input.insert(0, "請稍等...密碼獲得中")

    def retrieve_password(self):
        password = get_secret_key(self.password)
        self.update_password_label(password)

    def update_password_label(self, password):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.text_order_no_input.delete(0, "end")
            self.toplevel_window = ToplevelWindow(self)
        if password:
            self.toplevel_window.label.configure(text=f"你的解壓縮密碼: {password}")
        else:
            self.toplevel_window.label.configure(text="沒有找到你的訂單編號")

    def show_top_level_window_button_func(self):
        if self.toplevel_window:
            self.toplevel_window.focus()  # if window exists focus it


app = App()
# iconpath = ImageTk.PhotoImage(file="logo002.ico")
app.iconbitmap("logo003.ico")
app.mainloop()
