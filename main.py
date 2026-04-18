import tkinter as tk
from tkinter import ttk
import pyautogui as pg
import pyperclip
import threading
import time
import configparser
import os
import keyboard

# ================= BASIC SETUP =================
CONFIG_FILE = "config.ini"
pg.FAILSAFE = True   # mouse to top-left = force stop


class AWBScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AWB Scanner Tool")
        self.geometry("780x450")
        self.resizable(False, False)

        # ---------- state ----------
        self.running = False
        self.paused = False

        # ---------- config ----------
        self.cfg = configparser.ConfigParser()
        self.load_config()

        # ---------- hotkey handler storage ----------
        self.hotkey_handlers = []

        # ---------- tkinter vars ----------
        self.pos_mode = tk.IntVar(value=1)
        self.key_mode = tk.IntVar(value=2)

        # ---------- style ----------
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))

        # ---------- UI ----------
        self.build_ui()
        self.load_to_ui()

        # ---------- bindings ----------
        self.bind("=", self.capture_position)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # ---------- global hotkeys ----------
        self.register_hotkeys()

    # ================= CONFIG =================
    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.cfg["POSITION"] = dict(x1=0, y1=0, x2=0, y2=0)
            self.cfg["DELAY"] = dict(click=0.5, key=0.3)
            self.cfg["HOTKEY"] = dict(
                emergency_stop="F12",
                pause_resume="F11",
                stop="F10"
            )
            self.save_config()
        else:
            self.cfg.read(CONFIG_FILE)

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            self.cfg.write(f)

    # ================= HOTKEY =================
    def register_hotkeys(self):
        # remove old hotkeys safely
        for h in self.hotkey_handlers:
            try:
                keyboard.remove_hotkey(h)
            except Exception:
                pass
        self.hotkey_handlers
        self.hotkey_handlers.clear()

        try:
            h1 = keyboard.add_hotkey(
                self.cfg["HOTKEY"]["emergency_stop"],
                self.emergency_stop
            )
            h2 = keyboard.add_hotkey(
                self.cfg["HOTKEY"]["pause_resume"],
                self.toggle_pause
            )
            h3 = keyboard.add_hotkey(
                self.cfg["HOTKEY"]["stop"],
                self.stop_scan
            )
            self.hotkey_handlers.extend([h1, h2, h3])
        except Exception as e:
            print("Hotkey register error:", e)

    # ================= UI =================
    def build_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        # ----- LEFT -----
        awb_frame = ttk.LabelFrame(self, text="AWB List")
        awb_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        awb_frame.columnconfigure(0, weight=1)
        awb_frame.rowconfigure(0, weight=1)

        # Vertical scrollbar
        v_scroll = tk.Scrollbar(
            awb_frame,
            orient="vertical",
            width=14
        )
        v_scroll.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar (ยังไม่ grid)
        self.h_scroll = tk.Scrollbar(
            awb_frame,
            orient="horizontal",
            width=14
        )

        self.awb_text = tk.Text(
            awb_frame,
            font=("Consolas", 10),
            wrap="none",                     # ⭐ สำคัญ
            yscrollcommand=v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )
        self.awb_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        v_scroll.config(command=self.awb_text.yview)
        self.h_scroll.config(command=self.awb_text.xview)


        # ----- RIGHT -----
        control = ttk.Frame(self)
        control.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Position
        pos = ttk.LabelFrame(control, text="Position (Press =)")
        pos.grid(row=0, column=0, sticky="ew", pady=5)

        ttk.Radiobutton(pos, text="Input", variable=self.pos_mode, value=1)\
            .grid(row=0, column=0, sticky="w")
        self.pos1 = ttk.Label(pos, text="0 , 0")
        self.pos1.grid(row=0, column=1, sticky="e")

        ttk.Radiobutton(pos, text="Submit", variable=self.pos_mode, value=2)\
            .grid(row=1, column=0, sticky="w")
        self.pos2 = ttk.Label(pos, text="0 , 0")
        self.pos2.grid(row=1, column=1, sticky="e")

        # Delay
        delay = ttk.LabelFrame(control, text="Delay")
        delay.grid(row=1, column=0, sticky="ew", pady=5)

        ttk.Label(delay, text="Click").grid(row=0, column=0, sticky="w")
        self.delay_click = ttk.Entry(delay, width=6, justify="right")
        self.delay_click.grid(row=0, column=1)

        ttk.Label(delay, text="Type").grid(row=1, column=0, sticky="w")
        self.delay_key = ttk.Entry(delay, width=6, justify="right")
        self.delay_key.grid(row=1, column=1)

        # Input mode
        key = ttk.LabelFrame(control, text="Input Mode")
        key.grid(row=2, column=0, sticky="ew", pady=5)

        ttk.Radiobutton(key, text="Type", variable=self.key_mode, value=1)\
            .grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(key, text="Paste (Ctrl+V)", variable=self.key_mode, value=2)\
            .grid(row=1, column=0, sticky="w")

        # Actions
        act = ttk.LabelFrame(control, text="Actions")
        act.grid(row=3, column=0, sticky="ew", pady=5)

        ttk.Button(act, text="▶ Auto Scan", command=self.start_auto)\
            .grid(row=0, column=0, sticky="ew", pady=2)
        ttk.Button(act, text="⏸ Pause / Resume", command=self.toggle_pause)\
            .grid(row=1, column=0, sticky="ew", pady=2)
        ttk.Button(act, text="⏹ Stop", command=self.stop_scan)\
            .grid(row=2, column=0, sticky="ew", pady=2)
        ttk.Button(act, text="💾 Save Config", command=self.save_current)\
            .grid(row=3, column=0, sticky="ew", pady=2)

        # Status bar
        status = ttk.Frame(self)
        status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

        self.awb_label = ttk.Label(status, text="AWB: -")
        self.awb_label.grid(row=0, column=0, sticky="w")

        self.count_label = ttk.Label(status, text="Remaining: 0")
        self.count_label.grid(row=0, column=1, sticky="e")

    # ================= POSITION =================
    def capture_position(self, event=None):
        x, y = pg.position()
        if self.pos_mode.get() == 1:
            self.cfg["POSITION"]["x1"] = str(x)
            self.cfg["POSITION"]["y1"] = str(y)
            self.pos1.config(text=f"{x} , {y}")
        else:
            self.cfg["POSITION"]["x2"] = str(x)
            self.cfg["POSITION"]["y2"] = str(y)
            self.pos2.config(text=f"{x} , {y}")
        self.save_config()

    # ================= LOGIC =================
    def pull_awb(self):
        lines = self.awb_text.get("1.0", tk.END).strip().split("\n")
        if not lines or lines[0] == "":
            return None

        awb = lines.pop(0)

        self.awb_text.delete("1.0", tk.END)
        self.awb_text.insert(tk.END, "\n".join(lines))

        pyperclip.copy(awb)

        self.after(0, lambda: (
            self.awb_label.config(text=f"AWB: {awb}"),
            self.count_label.config(text=f"Remaining: {len(lines)}")
        ))

        if self.key_mode.get() == 1:
            pg.write(awb, interval=float(self.delay_key.get()))
        else:
            pg.hotkey("ctrl", "v")

        return awb

    def scan_once(self):
        x1 = int(self.cfg["POSITION"]["x1"])
        y1 = int(self.cfg["POSITION"]["y1"])
        x2 = int(self.cfg["POSITION"]["x2"])
        y2 = int(self.cfg["POSITION"]["y2"])

        pg.click(x1, y1)
        time.sleep(0.2)
        if self.pull_awb():
            pg.click(x2, y2)

    # ================= AUTO =================
    def start_auto(self):
        if self.running:
            return
        self.running = True
        self.paused = False
        threading.Thread(target=self.auto_loop, daemon=True).start()

    def auto_loop(self):
        delay = float(self.delay_click.get())
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue

            if not self.awb_text.get("1.0", tk.END).strip():
                break

            self.scan_once()
            time.sleep(delay)

        self.running = False
        self.paused = False

    def toggle_pause(self):
        if self.running:
            self.paused = not self.paused

    def stop_scan(self):
        self.running = False
        self.paused = False

    def emergency_stop(self):
        self.running = False
        self.paused = False
        self.after(0, lambda:
            self.awb_label.config(text="AWB: ⛔ EMERGENCY STOP")
        )

    # ================= UTIL =================
    def save_current(self):
        self.cfg["DELAY"]["click"] = self.delay_click.get()
        self.cfg["DELAY"]["key"] = self.delay_key.get()
        self.save_config()
        self.register_hotkeys()

    def load_to_ui(self):
        self.delay_click.insert(0, self.cfg["DELAY"]["click"])
        self.delay_key.insert(0, self.cfg["DELAY"]["key"])
        self.pos1.config(text=f'{self.cfg["POSITION"]["x1"]} , {self.cfg["POSITION"]["y1"]}')
        self.pos2.config(text=f'{self.cfg["POSITION"]["x2"]} , {self.cfg["POSITION"]["y2"]}')

    def on_close(self):
        for h in self.hotkey_handlers:
            try:
                keyboard.remove_hotkey(h)
            except Exception:
                pass
        self.hotkey_handlers.clear()
        self.destroy()


if __name__ == "__main__":
    AWBScannerApp().mainloop()
