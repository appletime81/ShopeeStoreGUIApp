import time
import customtkinter as ctk
from read_google_sheet import get_secret_key


class TextInput(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("150x30")
        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.pack()
        self.focus_force()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python專業代寫")
        self.geometry(f"{400}x{200}")
        self.toplevel_window = None
        self.label_for_order_no_input = ctk.CTkLabel(self, text="請輸入您的訂單編號:", width=200)
        self.text_order_no_input = TextInput(self, width=200)
        self.submit_button = ctk.CTkButton(
            self, text="提交", command=self.submit_button_func, width=200
        )
        self.show_top_level_window_button = ctk.CTkButton(
            self, text="顯示密碼彈窗", command=self.show_top_level_window_button_func, width=200
        )
        self.label_for_order_no_input.pack(pady=7)
        self.text_order_no_input.pack(pady=7)
        self.submit_button.pack(pady=7)
        self.show_top_level_window_button.pack(pady=7)

    def submit_button_func(self):
        print(self.text_order_no_input.get())
        self.text_order_no_input.delete(0, "end")
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(
                self
            )  # create window if its None or destroyed

    def show_top_level_window_button_func(self):
        if self.toplevel_window:
            self.toplevel_window.focus()  # if window exists focus it


app = App()
app.mainloop()
