# app/gui/reports_ui.py
import customtkinter as ctk
from datetime import date, timedelta
import calendar
import matplotlib
matplotlib.use("Agg")  # stable backend for embedding
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.sales import get_all_sales

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DARK_BG = "#1a1a1a"
AX_BG = "#1a1a1a"
SPINE_COLOR = "#333333"
LINE_COLOR = "#66c2ff"
BAR_COLOR = "#4db8e6"
GRID_COLOR = "#2b2b2b"


class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # HEADER
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(
            header,
            text="Sales Reports",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=12, pady=12)

        # BODY
        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=20, pady=10)

        left = ctk.CTkFrame(body, width=250)
        left.pack(side="left", fill="y", padx=(0, 12), pady=12)

        ctk.CTkLabel(
            left, text="Select Report",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 6))

        ctk.CTkButton(left, text="Today's Sales", command=self._today).pack(pady=8)
        ctk.CTkButton(left, text="Weekly Report", command=self._week).pack(pady=8)
        ctk.CTkButton(left, text="Monthly Report", command=self._month).pack(pady=8)

        # Right chart area
        self.chart_panel = ctk.CTkFrame(body)
        self.chart_panel.pack(side="right", fill="both", expand=True, pady=12)
        self.chart_panel.configure(fg_color=DARK_BG)

        # Default placeholder
        self.placeholder = ctk.CTkLabel(
            self.chart_panel,
            text="Select a report from the left panel",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.placeholder.pack(expand=True)

        # Track charts
        self.active_canvas = None
        self.active_fig = None

        # Global matplotlib styling (dark, subtle grid)
        self._apply_style()

    def _apply_style(self):
        plt.rcParams.update({
            "figure.facecolor": DARK_BG,
            "axes.facecolor": AX_BG,
            "savefig.facecolor": DARK_BG,
            "axes.edgecolor": SPINE_COLOR,
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.labelcolor": "white",
            "text.color": "white",
            "grid.color": GRID_COLOR,
            "grid.linewidth": 0.6,
            "grid.linestyle": "-",
            "axes.titlecolor": "white",
            "axes.titlesize": 14
        })

    def _clear(self):
        # remove existing canvas/figure cleanly
        if self.active_canvas:
            try:
                self.active_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.active_canvas = None
        if self.active_fig:
            try:
                plt.close(self.active_fig)
            except Exception:
                pass
            self.active_fig = None
        self.placeholder.pack_forget()
        # force update to ensure the panel background is fully painted
        self.chart_panel.update_idletasks()

    def _today(self):
        self._clear()
        sales = get_all_sales()
        today = date.today().strftime("%Y-%m-%d")
        total = sum(s[3] for s in sales if s[4] == today)

        label = ctk.CTkLabel(
            self.chart_panel,
            text=f"Today's Sales\n\n₹ {total}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#8be9fd"
        )
        label.pack(expand=True)

    def _week(self):
        self._clear()
        sales = get_all_sales()
        today = date.today()

        days = []
        amounts = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            days.append(calendar.day_name[d.weekday()][:3])
            total = sum(s[3] for s in sales if s[4] == d.strftime("%Y-%m-%d"))
            amounts.append(total)

        # create figure with matching dark facecolor
        fig = plt.Figure(figsize=(8, 4), facecolor=DARK_BG, dpi=100)
        ax = fig.add_subplot(111)
        ax.set_facecolor(AX_BG)

        ax.plot(days, amounts, marker="o", linewidth=2, color=LINE_COLOR)
        ax.fill_between(days, amounts, color=LINE_COLOR, alpha=0.10)
        ax.grid(True, color=GRID_COLOR, linestyle="-", linewidth=0.6)

        ax.set_title("Weekly Sales", color="white", fontsize=14)
        ax.set_xlabel("Day", color="white")
        ax.set_ylabel("Amount (₹)", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color(SPINE_COLOR)

        fig.tight_layout()

        # embed: draw off-screen then configure widget bg before showing
        self.active_fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.chart_panel)
        canvas.draw()  # render into the FigureCanvas backend (Agg) first

        widget = canvas.get_tk_widget()
        # ensure widget background matches dark theme before packing
        try:
            widget.configure(bg=DARK_BG, highlightthickness=0, bd=0)
        except Exception:
            pass
        # pack after draw and after bg set
        widget.pack(fill="both", expand=True)
        self.active_canvas = canvas

    def _month(self):
        self._clear()
        sales = get_all_sales()
        today = date.today()

        days = []
        amounts = []
        for i in range(29, -1, -1):
            d = today - timedelta(days=i)
            days.append(calendar.day_name[d.weekday()][:3])
            total = sum(s[3] for s in sales if s[4] == d.strftime("%Y-%m-%d"))
            amounts.append(total)

        fig = plt.Figure(figsize=(10, 4), facecolor=DARK_BG, dpi=100)
        ax = fig.add_subplot(111)
        ax.set_facecolor(AX_BG)

        bars = ax.bar(range(len(days)), amounts, color=BAR_COLOR, edgecolor="#2b2b2b", linewidth=0.4)
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels([days[i] if i % 3 == 0 else "" for i in range(len(days))], color="white")
        ax.grid(True, axis="y", color=GRID_COLOR, linestyle="-", linewidth=0.6)

        ax.set_title("Monthly Sales (Last 30 Days)", color="white", fontsize=14)
        ax.set_xlabel("Day", color="white")
        ax.set_ylabel("Amount (₹)", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color(SPINE_COLOR)

        fig.tight_layout()

        self.active_fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.chart_panel)
        canvas.draw()
        widget = canvas.get_tk_widget()
        try:
            widget.configure(bg=DARK_BG, highlightthickness=0, bd=0)
        except Exception:
            pass
        widget.pack(fill="both", expand=True)
        self.active_canvas = canvas
