import tkinter as tk
from tkinter import ttk, messagebox as msg
from titlebar import TitleTk

style_settings = {
    "background": "black",
    "foreground": "grey",
    "button_bg": "#222",
    "button_fg": "white",
    "button_active_bg": "#333",
    "button_active_fg": "white",
    "button_press_bg": "#555",
    "button_press_fg": "white",
    "font": ("JetBrains Mono", 17),
    "select_bg": "#555"
}


theme_settings = {
    "TButton": {
        "configure": {
            "background": style_settings["button_bg"],
            "foreground": style_settings["button_fg"],
            "font": style_settings["font"],
            "anchor": "center",
            "focuscolor": "clear",
            "borderwidth": 0,
        },
        "map": {
            "background": [
                ("pressed", style_settings["button_press_bg"]),
                ("active", style_settings["button_active_bg"])
            ],
            "foreground": [
                ("pressed", style_settings["button_press_fg"]),
                ("active", style_settings["button_active_fg"])
            ]
        }
    },
    "BiggerFont.TButton": {
        "configure": {
            "font": (None, style_settings["font"][1] + 7)
        }
    },
    "Minus.BiggerFont.TButton": {
        "configure": {
            "font": (None, style_settings["font"][1] + 12)
        }
    },
    "TEntry": {
        "configure": {
            "fieldbackground": style_settings["button_bg"],
            "foreground": style_settings["button_fg"],
            "selectbackground": style_settings["select_bg"],
            "insertcolor": style_settings["button_fg"],
            "borderwidth": 0
        }
    }
}


# layout
# =============
# (   )   %  /
# 7   8   9  ×
# 4   5   6  -
# 1   2   3  +
# +/- 0   .  =

class Calculator(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bg=style_settings["button_bg"])

        self.make_gui()

        # varibles
        self.trantable = str.maketrans({"^": "**", "×": "*"})
        self.valid_inputs = set("1234567890-+/×xX*^.%()")
        self.entry = self.nametowidget("entry")

        # configure and change the style
        self.style = ttk.Style(self)
        self.style.theme_create("dark.vista", settings=theme_settings)
        self.style.theme_use("dark.vista")

        # binding shortcuts
        self.master.bind("<BackSpace>", self.backspace)
        self.master.bind("<Return>", lambda e: self.calc())
        self.entry.bind("<BackSpace>", self.backspace)
        self.entry.bind("<Return>", lambda e: self.calc())
        self.entry.bind("<FocusOut>", lambda e: self.entry.icursor("end"))

    def make_gui(self):

        # self.button_grid_opts = {}
        # self.button_opts = {}
        entry_validate_cmd = self.register(self.validate)
        self.layout = [
            [
                [
                    ttk.Entry(
                        self, name="entry",
                        justify="right",
                        font=style_settings["font"],
                        validate="key",
                        validatecommand=(entry_validate_cmd, "%S")
                    ),
                    {"columnspan": 4, "padx": 7, "ipady": 10}
                ]
            ],
            [
                [ttk.Button(self, text="^")],
                [ttk.Button(self, text="n²", command=lambda: self.add("^2"))],
                [ttk.Button(self, text="c", command=lambda: self.entry.delete(0, "end"))],
                [ttk.Button(self, text="<--", command=self.backspace)]
            ],
            [
                [ttk.Button(self, text="(")],
                [ttk.Button(self, text=")")],
                [ttk.Button(self, text="%")],
                [ttk.Button(self, text="/")]
            ],
            [
                [ttk.Button(self, text="7")],
                [ttk.Button(self, text="8")],
                [ttk.Button(self, text="9")],
                [ttk.Button(self, text="×", style="BiggerFont.TButton")]
            ],
            [
                [ttk.Button(self, text="4")],
                [ttk.Button(self, text="5")],
                [ttk.Button(self, text="6")],
                [ttk.Button(self, text="-", style="Minus.BiggerFont.TButton")]
            ],
            [
                [ttk.Button(self, text="1")],
                [ttk.Button(self, text="2")],
                [ttk.Button(self, text="3")],
                [ttk.Button(self, text="+", style="BiggerFont.TButton")]
            ],
            [
                [ttk.Button(self, text="+/-", command=lambda: self.calc(neget=True))],
                [ttk.Button(self, text="0")],
                [ttk.Button(self, text="·", command=lambda: self.add("."))],
                [ttk.Button(self, text="=", command=self.calc, style="BiggerFont.TButton")]
            ]
        ]

        for row, widgets_info in enumerate(self.layout):
            for col, widget_info in enumerate(widgets_info):
                widget = widget_info[0]
                grid_opts = {"row": row, "column": col, "sticky": "nswe"}
                if len(widget_info) == 2:
                    grid_opts.update(widget_info[1])

                if isinstance(widget, ttk.Button) and not widget.cget("command"):
                    widget.config(
                        command=lambda text=widget.cget("text"): self.add(text)
                    )
                widget.grid(grid_opts)

        for i in range(self.grid_size()[0]):
            self.columnconfigure(i, weight=1)
        for j in range(1, self.grid_size()[1]):
            self.rowconfigure(j, weight=1)

    def add(self, string):
        self.entry.insert("end", string)

    def backspace(self, event=None):
        pos = self.entry.index("insert")
        self.entry.delete(pos - 1)
        return "break"

    def calc(self, neget=False):
        string = self.entry.get().translate(self.trantable).lstrip("0")
        try:
            res = eval(string)
            self.entry.delete(0, "end")
            self.entry.insert(0, -res if neget else res)
        except:
            msg.showerror(title="Error", message="Value Error")

    def validate(self, string):
        return all(c in self.valid_inputs for c in string)


if __name__ == "__main__":
    root = TitleTk()
    root.title("Calculator")
    root.geometry("400x400+100+200")
    window = Calculator(root)
    window.pack(fill="both", expand=True)
    root.mainloop()
