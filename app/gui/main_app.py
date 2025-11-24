# app/gui/main_app.py

import customtkinter as ctk
from app.gui.inventory_ui import InventoryFrame
from app.gui.sales_ui import SalesFrame
from app.gui.reports_ui import ReportsFrame
from app.gui.dashboard_ui import DashboardFrame


class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Retail Management System")
        self.geometry("1100x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---------------------------
        # MAIN LAYOUT
        # ---------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # ---------------------------
        # SIDEBAR BUTTONS
        # ---------------------------
        ctk.CTkLabel(
            self.sidebar_frame,
            text="Menu",
            font=("Arial", 22, "bold"),
            text_color="#00b4d8"
        ).pack(pady=20)

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame,
            text="Dashboard",
            height=40,
            command=self.load_dashboard
        )
        self.btn_dashboard.pack(pady=10)

        self.btn_inventory = ctk.CTkButton(
            self.sidebar_frame,
            text="Inventory",
            height=40,
            command=self.load_inventory
        )
        self.btn_inventory.pack(pady=10)

        self.btn_sales = ctk.CTkButton(
            self.sidebar_frame,
            text="Sales",
            height=40,
            command=self.load_sales
        )
        self.btn_sales.pack(pady=10)

        self.btn_reports = ctk.CTkButton(
            self.sidebar_frame,
            text="Reports",
            height=40,
            command=self.load_reports
        )
        self.btn_reports.pack(pady=10)

        # ---------------------------
        # FRAMES INITIALIZATION
        # ---------------------------
        self.current_page = None
        self.load_dashboard()

    # ---------------------------------------
    # PAGE SWITCHER
    # ---------------------------------------
    def switch_page(self, new_page):
        if self.current_page is not None:
            self.current_page.pack_forget()

        self.current_page = new_page
        self.current_page.pack(fill="both", expand=True)

    # ---------------------------------------
    # LOAD PAGES
    # ---------------------------------------
    def load_dashboard(self):
        self.switch_page(DashboardFrame(self.content_frame))

    def load_inventory(self):
        self.switch_page(InventoryFrame(self.content_frame))

    def load_sales(self):
        self.switch_page(SalesFrame(self.content_frame))

    def load_reports(self):
        self.switch_page(ReportsFrame(self.content_frame))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
