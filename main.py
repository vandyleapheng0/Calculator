import tkinter as tk
from tkinter import ttk, messagebox as msg


class Calculator(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title("Calculator")
        self.config(bg="#0a0a0a")
        self.attributes("-topmost", 3)
        self.minsize(width=400, height=400)
        self.iconbitmap("icons\\cal.ico")

        # styling the button
        self.style = ttk.Style(self)

        black = "#1f1f1f"
        font = ("JetBrains Mono", 20)
        btn_clicked_bg = "#525252"
        btn_clicked_fg = "grey"
        btn_hover_bg = "#333333"

        style_settings = {
            "TButton": {
                "configure": {
                    "background": black,
                    "foreground": "white",
                    "font": font,
                    "focuscolor": "clear",
                    "anchor": "center"
                },
                "map": {
                    "background": [('pressed', btn_clicked_bg), ("active", btn_hover_bg)],
                    "foreground": [('pressed', btn_clicked_fg), ("active", "white")]
                }
            }
        }
        self.style.theme_create("custom", settings=style_settings)
        self.style.theme_use("custom")

        self.entry = tk.Entry(
            self, validate="key", font=font, justify="right",
            bg=black, fg="white", bd=0, insertbackground="white",
            validatecommand=(self.register(self.validate), "%P")
        )
        self.entry.grid(row=0, column=0, columnspan=4, sticky="ewsn", ipady=10, padx=2, pady=(3, 2))

        buttons = [
            ['^', 'n²', 'c', '<--'],
            ['(', ')', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]

        for x in range(len(buttons[0])):
            self.columnconfigure(x, weight=1)
        for y in range(1, len(buttons) + 1):
            self.rowconfigure(y, weight=1)

        for row, buttons_ in enumerate(buttons, 1):
            for col, btn_text in enumerate(buttons_):
                command = self.get_func(btn_text)
                button_ = ttk.Button(self, text=btn_text, command=command)
                button_.grid(row=row, column=col, sticky="wesn", padx=2, pady=2)

        # Shortcuts
        self.bind("<BackSpace>", self.backspace)
        self.bind("<Return>", self.calculate)

    def validate(self, value):
        return all(x in "0123456789.-+x/*^%" for x in value)

    def get_func(self, btn_text):
        if btn_text == "<--":
            return lambda: self.backspace()
        elif btn_text == "c":
            return lambda: self.clear()
        elif btn_text == "n²":
            return lambda: self.add_to_entry("^2")
        elif btn_text == "+/-":
            return self.negat
        elif btn_text == "=":
            return lambda: self.calculate()
        else:
            return lambda s=btn_text: self.add_to_entry(s)

    def negat(self):
        self.calculate()
        if "-" not in self.entry.get():
            self.entry.insert(0, "-")
        else:
            self.entry.delete(0)

    def add_to_entry(self, string): self.entry.insert("end", string)

    def clear(self): self.entry.delete(0, "end")

    def backspace(self, event=None):
        content = self.entry.get()
        self.entry.delete(len(content) - 1)

    def calculate(self, event=None):
        content = self.entry.get().replace("^", "**").replace("x", "*").lstrip("0")
        try:
            result = eval(content)
            self.entry.delete(0, "end")
            self.entry.insert(0, result)
        except:
            msg.showerror("Error", "Value error")


app = Calculator()
app.mainloop()
