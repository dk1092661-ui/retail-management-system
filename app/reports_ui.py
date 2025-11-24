# app/gui/reports_ui.py

import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
import matplotlib.pyplot as plt

from app.sales import get_all_sales


def open_reports_window():
    win = tk.Toplevel()
    win.title("Reports & Charts")
    win.geometry("500x400")

    tk.Label(win, text="Sales Reports & Charts", font=("Arial", 18, "bold")).pack(pady=20)

    tk.Button(
        win,
        text="Show Today's Sales",
        width=25,
        font=("Arial", 12),
        command=show_today_sales
    ).pack(pady=10)

    tk.Button(
        win,
        text="Show Weekly Sales Chart",
        width=25,
        font=("Arial", 12),
        command=show_weekly_chart
    ).pack(pady=10)

    tk.Button(
        win,
        text="Show Monthly Sales Chart",
        width=25,
        font=("Arial", 12),
        command=show_monthly_chart
    ).pack(pady=10)

    win.mainloop()


# ------------- REPORT FUNCTIONS -----------------

def show_today_sales():
    today = date.today().strftime("%Y-%m-%d")
    sales = get_all_sales()

    total = sum(s[3] for s in sales if s[4] == today)

    messagebox.showinfo("Today's Sales", f"Total Sales Today: ₹{total}")


def show_weekly_chart():
    sales = get_all_sales()
    today = date.today()

    week_data = {}
    for i in range(7):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        week_data[d] = 0

    for s in sales:
        if s[4] in week_data:
            week_data[s[4]] += s[3]

    dates = list(week_data.keys())
    amounts = list(week_data.values())

    plt.plot(dates, amounts)
    plt.xlabel("Date")
    plt.ylabel("Sales Amount")
    plt.title("Weekly Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_monthly_chart():
    sales = get_all_sales()
    today = date.today()

    month_data = {}
    for i in range(30):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        month_data[d] = 0

    for s in sales:
        if s[4] in month_data:
            month_data[s[4]] += s[3]

    dates = list(month_data.keys())
    amounts = list(month_data.values())

    plt.plot(dates, amounts)
    plt.xlabel("Date")
    plt.ylabel("Sales Amount")
    plt.title("Monthly Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
