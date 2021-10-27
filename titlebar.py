from tkinter import ttk
import tkinter as tk
from ctypes import windll
# stolen some codes from https://github.com/Terranova-Python/Tkinter-Menu-Bar/blob/main/main.py
# i thought i just need some buttons and label that all but noooo

titlebar_theme_settings = {
    "Title.TButton": {
        "configure": {
            "background": "#111",
            "foreground": "white",
            "focuscolor": "clear",
            "anchor": "center",
            "font": (None, 15),
            "borderwidth": 0
        },
        "map": {"background": [("active", "#555555"), ("pressed", "#666666")]}
    },
    "Min.Title.TButton": {
        "configure": {"font": (None, 10)}
    },
    "Max.Title.TButton": {
        "configure": {"font": (None, 10)}
    },
    "Close.Title.TButton": {
        "map": {"background": [("active", "#da2e25")]}
    },
    "Title.TLabel": {
        "configure": {
            "background": "#111",
            "foreground": "white",
            "font": (None, 10)
        }
    }
}


class SqrtButton(tk.Frame):
    def __init__(self, master, **kargs):
        super().__init__(master, width=kargs["side"], height=kargs["side"])
        del kargs["side"]
        self.pack_propagate(False)
        self.button = ttk.Button(self, **kargs)
        self.button.pack(fill="both", expand=True)


def config_map_style(settings):
    style = ttk.Style()
    for widget_cls, changes in settings.items():
        for func, options in changes.items():
            if func == "configure":
                style.configure(widget_cls, **options)
            elif func == "map":
                style.map(widget_cls, **options)
            else:
                raise ValueError("Can only change the 'map' and 'configure'")


def change_bg(background):
    style = ttk.Style()
    style.configure("Title.TButton", background=background)
    style.configure("Title.TLabel", background=background)


class TitleBar(tk.Frame):
    """Treat the TitleBar as a normal widget\n
    You can pack it to the top or using grid instead\n
    The TitleBar will change the theme of the app to 'alt'\n
    If you you want to use other theme or make your own don't forget to call:\n
    1.0 (option:1) 'titlebar.config_map_style(settings=titlebar.titlebar_theme_settings)'\n
    1.1 (option:2) add "Title.TButton, Min.Title.TButton, Max.Title.TButton, Close.Title.TButton, Title.TLabel" to your style\n
    2. 'change_bg(background="your titlebar background")' don't need if bg is default"""

    def __init__(self, master, title="tk", **kargs):
        self.fix_kargs(kargs)
        super().__init__(master, **kargs, bg=self.style_settings["bg"])

        self.style = ttk.Style(self)
        self.change_theme()
        self.maximized = False
        self.minimized = False

        self.title = ttk.Label(
            self, text=title,
            compound="left",
            style="Title.TLabel"
        )
        self.maximize = SqrtButton(
            self, text="☐",
            compound="center",
            side=30, style="Max.Title.TButton",
            command=self.maximize_window
        )
        self.minimize = SqrtButton(
            self, text="—",
            side=30, style="Min.Title.TButton",
            command=self.minimize_window
        )
        self.close = SqrtButton(
            self, text="×",
            side=30, style="Close.Title.TButton",
            command=self.master.quit
        )

        self.title.pack(side="left", padx=(5, 0))
        self.close.pack(side="right")
        self.maximize.pack(side="right")
        self.minimize.pack(side="right")

        # NOTE make sure to add param("<Motion>", func, add="+") if you want to bind the already binded action
        self.after(10, lambda: self.set_appwindow())
        self.title_bar_bind("<B1-Motion>", self.move_window)
        self.title_bar_bind("<B1-ButtonRelease>", self.release_window)
        self.title_bar_bind("<Double-Button-1>", self.maximize_window)
        self.master.bind("<FocusIn>", self.deminimize_window)
        self.master.bind("<Motion>", self.get_resize_info)
        self.master.bind("<B1-Motion>", self.resize_window)
        self.master.bind("<B1-ButtonRelease>", self.release_window)

    def title_bar_bind(self, key, func):
        self.bind(key, func)
        self.title.bind(key, func)

    def release_window(self, event=None):
        # keeping the last_movement will mess up the resize and move methods
        # it needs to be record again
        try:
            del self.last_movement
        except AttributeError:
            pass

    def fix_kargs(self, kargs):
        self.style_settings = {"bg": "#111", "fg": "white"}
        items_lst = [("bg", "background"), ("fg", "foreground")]

        for items in items_lst:
            for item in items:
                if item in kargs:
                    self.style_settings[items[0]] = kargs[item]
                    break

        if self.style_settings["fg"] == "white":
            self.restore_down_png = tk.PhotoImage(file="images/restore_down_white15.png")
        elif self.style_settings["fg"] == "black":
            self.restore_down_png = tk.PhotoImage(file="images/restore_down_dark15.png")
        else:
            raise ValueError('foreground can only be "white", "black"')

        try:
            del kargs["fg"]
        except KeyError:
            pass

    def get_resize_info(self, event=None):
        """Get the resize info and change the cursor style to indecate user that widget is resizable"""
        self.resize_left = event.x_root - self.master.winfo_x() < 5
        self.resize_right = event.x_root > self.master.winfo_x() + self.master.winfo_width() - 5

        self.resize_top = event.y_root - self.master.winfo_y() < 5
        self.resize_bottom = event.y_root > self.master.winfo_y() + self.master.winfo_height() - 5

        if self.resize_left or self.resize_right:
            self.master.config(cursor='sb_h_double_arrow')
        elif self.resize_top or self.resize_bottom:
            self.master.config(cursor='sb_v_double_arrow')
        else:
            self.master.config(cursor="arrow")

    def resize_window(self, event=None):
        # We need last_movement to calculate width and height to resize
        # resizing: "bottom" and "right" are the same. Calculate the different and add to geometry
        # resizing: "top" and "left" the same above, but we need to move(NOT RESIZE) widget along with cursor

        if hasattr(self, "last_movement"):
            if self.resize_bottom:
                self.master.geometry("{}x{}".format(
                    self.master.winfo_width(),
                    self.master.winfo_height() + event.y_root - self.last_movement[1]
                ))
            elif self.resize_top:
                self.master.geometry("{}x{}+{}+{}".format(
                    self.master.winfo_width(),
                    self.master.winfo_height() + self.last_movement[1] - event.y_root,
                    self.master.winfo_x(),
                    self.master.winfo_y() + event.y_root - self.last_movement[1]
                ))
            elif self.resize_left:
                self.master.geometry("{}x{}+{}+{}".format(
                    self.master.winfo_width() + self.last_movement[0] - event.x_root,
                    self.master.winfo_height(),
                    self.master.winfo_x() + event.x_root - self.last_movement[0],
                    self.master.winfo_y()
                ))
            elif self.resize_right:
                self.master.geometry("{}x{}".format(
                    self.master.winfo_width() + event.x_root - self.last_movement[0],
                    self.master.winfo_height()
                ))
        self.last_movement = (event.x_root, event.y_root)

    def move_window(self, event=None):
        # record the last_movement
        # (next movement) calculate the different and move the main-window
        if not (self.maximized or self.resize_top):
            if hasattr(self, "last_movement"):
                self.master.geometry("+{}+{}".format(
                    self.master.winfo_x() + event.x_root - self.last_movement[0],
                    self.master.winfo_y() + event.y_root - self.last_movement[1]
                ))
            self.last_movement = (event.x_root, event.y_root)

    def set_appwindow(self):
        """add icon on the taskbar"""
        # Some WindowsOS styles, required for task bar integration
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(self.master.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

        self.master.wm_withdraw()
        self.master.after(10, lambda: self.master.wm_deiconify())

    def config_button_map(self, button_map=None, close_map=None):
        if button_map is not None:
            self.style.map("TButton", **button_map)
        if close_map is not None:
            self.style.map("Close.TButton", **close_map)

    def change_theme(self):
        theme_settings = {
            "Title.TButton": {
                "configure": {
                    "background": self.style_settings["bg"],
                    "foreground": self.style_settings["fg"],
                    "focuscolor": "clear",
                    "anchor": "center",
                    "font": (None, 15),
                    "borderwidth": 0
                },
                "map": {"background": [("active", "#555555"), ("pressed", "#666666")]}
            },
            "Min.Title.TButton": {
                "configure": {"font": (None, 10)}
            },
            "Max.Title.TButton": {
                "configure": {"font": (None, 10)}
            },
            "Close.Title.TButton": {
                "map": {"background": [("active", "#da2e25")]}
            },
            "Title.TLabel": {
                "configure": {
                    "background": self.style_settings["bg"],
                    "foreground": self.style_settings["fg"],
                    "font": (None, 10)
                }
            }
        }

        self.style.theme_use("alt")
        config_map_style(settings=theme_settings)

    def maximize_window(self, event=None):
        if self.maximized:
            self.master.geometry(self.old_window_geomerty)
            self.maximize.button.config(text="☐", image='')
            self.maximized = False
        else:
            self.old_window_geomerty = self.master.geometry()
            self.maximized = True
            self.master.geometry("{}x{}+0+0".format(
                self.master.winfo_screenwidth(),
                self.master.winfo_screenheight()
            ))
            self.maximize.button.config(text="", image=self.restore_down_png)  # 🗇

    def minimize_window(self, event=None):
        if not self.minimized:
            self.master.attributes("-alpha", 0)
            self.minimized = True

    def deminimize_window(self, event=None):
        self.master.focus()
        if self.minimized:
            self.master.attributes("-alpha", 1)
            self.minimized = False


class CustomTitleBarTk(tk.Tk):
    def __init__(self, **kargs):
        super().__init__()
        self.overrideredirect(True)
        self.title_bar = TitleBar(self, **kargs)
        self.title_bar.pack(fill="x")

        self.window = tk.Frame(self)
        self.window.pack(fill="both", expand=True)


if __name__ == "__main__":
    # root = tk.Tk()
    # root.geometry("500x400+800+100")
    # root.overrideredirect(True)
    # root.attributes("-topmost", 1)
    # root.config(bg="#333")

    # title_bar = TitleBar(root, fg="white", title="Finally")
    # title_bar.pack(fill="x")

    # label = tk.Label(root, text="hello world".upper())
    # label.pack(ipadx=5, ipady=5)
    # root.mainloop()

    root = CustomTitleBarTk()
    root.geometry("400x400")
    label = tk.Label(root.window, text="hello world".upper())
    label.pack(ipadx=5, ipady=5)
    root.mainloop()
