# app/gui/dashboard_ui.py
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Header / title
        header = ctk.CTkFrame(self, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 12))
        ctk.CTkLabel(header, text="Overview", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=12, pady=12)

        # Stats area (3 cards)
        cards = ctk.CTkFrame(self)
        cards.pack(fill="x", padx=20, pady=(0, 12))

        card1 = ctk.CTkFrame(cards, width=220, height=110, corner_radius=8)
        card1.pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(card1, text="Total Products", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=12, pady=(10, 0))
        self.total_products_label = ctk.CTkLabel(card1, text="—", font=ctk.CTkFont(size=22, weight="bold"))
        self.total_products_label.pack(anchor="w", padx=12, pady=(6, 10))

        card2 = ctk.CTkFrame(cards, width=220, height=110, corner_radius=8)
        card2.pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(card2, text="Today's Sales", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=12, pady=(10, 0))
        self.todays_sales_label = ctk.CTkLabel(card2, text="—", font=ctk.CTkFont(size=22, weight="bold"))
        self.todays_sales_label.pack(anchor="w", padx=12, pady=(6, 10))

        card3 = ctk.CTkFrame(cards, width=220, height=110, corner_radius=8)
        card3.pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(card3, text="Low Stock Items", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=12, pady=(10, 0))
        self.low_stock_label = ctk.CTkLabel(card3, text="—", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FFA500")
        self.low_stock_label.pack(anchor="w", padx=12, pady=(6, 10))

        # Recent activity placeholder
        section = ctk.CTkFrame(self, corner_radius=8)
        section.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        ctk.CTkLabel(section, text="Recent Activity", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12, 6))
        self.activity_box = ctk.CTkTextbox(section, width=760, height=260, corner_radius=8)
        self.activity_box.pack(padx=12, pady=(0, 12), fill="both", expand=True)
        self.activity_box.configure(state="disabled")

        # when frame is created, optionally populate placeholders
        self._populate_placeholders()

    def _populate_placeholders(self):
        # Lightweight placeholder values — real values will be updated by external code if desired
        self.total_products_label.configure(text="0")
        self.todays_sales_label.configure(text="₹0")
        self.low_stock_label.configure(text="0")
        self.activity_box.configure(state="normal")
        self.activity_box.delete("0.0", "end")
        self.activity_box.insert("end", "Open Inventory or Sales to see activity here...\n")
        self.activity_box.configure(state="disabled")
