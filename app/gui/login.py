# app/gui/login.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from app.auth import verify_user
from app.gui.dashboard_ui import open_dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def run_login():
    root = ctk.CTk()
    root.title("Retail System — Login")
    root.geometry("480x360")
    root.resizable(False, False)

    # center window (optional)
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = int((screen_w - 480) / 2)
    y = int((screen_h - 360) / 4)
    root.geometry(f"+{x}+{y}")

    # header frame with subtle gradient-like color using label backgrounds
    header = ctk.CTkFrame(root, corner_radius=12, fg_color="#06283D")
    header.pack(padx=20, pady=(20,10), fill="x")

    title = ctk.CTkLabel(header, text="Retail Management", font=ctk.CTkFont(size=20, weight="bold"))
    subtitle = ctk.CTkLabel(header, text="Sign in to your account", font=ctk.CTkFont(size=12))
    title.pack(pady=(12,0))
    subtitle.pack(pady=(0,12))

    # form frame
    frame = ctk.CTkFrame(root, corner_radius=12)
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Username", anchor="w").pack(padx=20, pady=(12,4), fill="x")
    username = ctk.CTkEntry(frame, placeholder_text="username")
    username.pack(padx=20, fill="x")

    ctk.CTkLabel(frame, text="Password", anchor="w").pack(padx=20, pady=(12,4), fill="x")
    password = ctk.CTkEntry(frame, show="*", placeholder_text="password")
    password.pack(padx=20, fill="x")

    # animated feedback label
    feedback = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=11))
    feedback.pack(pady=(8,0))

    def attempt_login():
        user = username.get().strip()
        pwd = password.get().strip()
        ok, role = verify_user(user, pwd)
        if ok:
            feedback.configure(text="Login successful ✓", text_color="#7FFFD4")
            root.after(300, lambda: (root.destroy(), open_dashboard(role)))
        else:
            feedback.configure(text="Invalid username or password", text_color="#FF6B6B")

    # animated login button
    login_btn = ctk.CTkButton(frame, text="Login", command=attempt_login, width=200, corner_radius=10)
    login_btn.pack(pady=16)

    # small hint + animated pulse on focus
    hint = ctk.CTkLabel(root, text="Demo admin — username: admin, password: Admin@123", font=ctk.CTkFont(size=10))
    hint.pack(pady=(2,12))

    root.mainloop()


if __name__ == "__main__":
    run_login()
