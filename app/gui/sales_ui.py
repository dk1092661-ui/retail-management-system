# app/gui/sales_ui.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from app.inventory import get_all_products, update_product_stock
from app.sales import record_sale

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SalesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=(20, 8))
        ctk.CTkLabel(header, text="Sales", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=12)

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=20, pady=(0,20))

        # product dropdown
        products = get_all_products()
        if not products:
            ctk.CTkLabel(body, text="No products available. Add items in Inventory.", font=ctk.CTkFont(size=12)).pack(pady=12)
            return

        entries = {f"{p[1]} — ₹{p[3]} — Stock:{p[4]}": p for p in products}
        choices = list(entries.keys())

        ctk.CTkLabel(body, text="Select Product").pack(anchor="w", padx=12, pady=(12,4))
        self.product_var = ctk.StringVar(value=choices[0])
        dropdown = ctk.CTkOptionMenu(body, values=choices, variable=self.product_var, width=480)
        dropdown.pack(padx=12, pady=(0,12))

        qty_frame = ctk.CTkFrame(body)
        qty_frame.pack(padx=12, pady=8, fill="x")
        ctk.CTkLabel(qty_frame, text="Quantity").pack(side="left", padx=(6,8))
        self.qty_entry = ctk.CTkEntry(qty_frame, width=120)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left")

        ctk.CTkButton(body, text="Submit Sale", width=200, command=lambda: self._submit(entries)).pack(pady=14)

    def _submit(self, entries):
        sel = self.product_var.get()
        if not sel:
            messagebox.showwarning("Select", "Select a product.")
            return
        product = entries.get(sel)
        pid, _, _, price, stock = product
        try:
            qty = int(self.qty_entry.get().strip())
        except:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return
        if qty <= 0:
            messagebox.showerror("Error", "Quantity must be >= 1.")
            return
        if qty > stock:
            messagebox.showerror("Error", "Not enough stock.")
            return
        total = price * qty
        today = date.today().strftime("%Y-%m-%d")
        record_sale(pid, qty, total, today)
        update_product_stock(pid, stock - qty)
        messagebox.showinfo("Sale", f"Sale recorded — Total: ₹{total}")
        # Optionally refresh page: recreate frame contents by destroying and reinitializing
        self.destroy()
        SalesFrame(self.master).pack(fill="both", expand=True)
