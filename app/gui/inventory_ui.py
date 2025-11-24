# app/gui/inventory_ui.py
import customtkinter as ctk
from tkinter import messagebox
from app.inventory import add_product, get_all_products, delete_product, update_product_stock

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=(20, 8))
        ctk.CTkLabel(header, text="Inventory", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=12)

        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=(0,20))

        # left: form
        form = ctk.CTkFrame(main, width=320, corner_radius=8)
        form.pack(side="left", padx=(0,12), pady=8, fill="y")

        ctk.CTkLabel(form, text="Product Name").pack(anchor="w", padx=12, pady=(12,4))
        self.name_entry = ctk.CTkEntry(form, placeholder_text="e.g. Wireless Mouse")
        self.name_entry.pack(padx=12, fill="x")

        ctk.CTkLabel(form, text="Category").pack(anchor="w", padx=12, pady=(10,4))
        self.category_entry = ctk.CTkEntry(form, placeholder_text="e.g. Electronics")
        self.category_entry.pack(padx=12, fill="x")

        ctk.CTkLabel(form, text="Price").pack(anchor="w", padx=12, pady=(10,4))
        self.price_entry = ctk.CTkEntry(form, placeholder_text="e.g. 499.99")
        self.price_entry.pack(padx=12, fill="x")

        ctk.CTkLabel(form, text="Stock").pack(anchor="w", padx=12, pady=(10,4))
        self.stock_entry = ctk.CTkEntry(form, placeholder_text="e.g. 50")
        self.stock_entry.pack(padx=12, fill="x")

        ctk.CTkButton(form, text="Add Product", command=self._add_product).pack(padx=12, pady=12, fill="x")
        ctk.CTkButton(form, text="Delete Selected", fg_color="#b00020", command=self._delete_selected).pack(padx=12, pady=(0,8), fill="x")
        ctk.CTkButton(form, text="Update Stock", command=self._open_update_stock).pack(padx=12, pady=(0,8), fill="x")

        # right: product list
        list_frame = ctk.CTkFrame(main, corner_radius=8)
        list_frame.pack(side="right", expand=True, fill="both")

        ctk.CTkLabel(list_frame, text="Products", anchor="w", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12,6))
        self.products_text = ctk.CTkTextbox(list_frame, width=600, height=380, state="disabled")
        self.products_text.pack(padx=12, pady=(0,12), fill="both", expand=True)

        # internal state
        self._refresh_products()

    def _refresh_products(self):
        products = get_all_products()
        self.products_text.configure(state="normal")
        self.products_text.delete("0.0", "end")
        for p in products:
            line = f"{p[0]} | {p[1]} | {p[2]} | ₹{p[3]} | Stock: {p[4]}\n"
            self.products_text.insert("end", line)
        self.products_text.configure(state="disabled")

    def _add_product(self):
        try:
            name = self.name_entry.get().strip()
            cat = self.category_entry.get().strip()
            price = float(self.price_entry.get().strip())
            stock = int(self.stock_entry.get().strip())
        except Exception:
            messagebox.showerror("Invalid", "Please fill all fields correctly.")
            return
        add_product(name, cat, price, stock)
        messagebox.showinfo("Added", f"Product '{name}' added.")
        self.name_entry.delete(0, "end"); self.category_entry.delete(0, "end")
        self.price_entry.delete(0, "end"); self.stock_entry.delete(0, "end")
        self._refresh_products()

    def _delete_selected(self):
        # get first number (id) from the first selected line in the textbox
        sel = self.products_text.get("sel.first", "sel.last") if self.products_text.tag_ranges("sel") else ""
        if not sel:
            messagebox.showwarning("Select", "Select a product line in the list to delete.")
            return
        try:
            pid = int(sel.split("|")[0].strip())
        except Exception:
            messagebox.showerror("Error", "Could not parse product id.")
            return
        delete_product(pid)
        messagebox.showinfo("Deleted", "Product deleted.")
        self._refresh_products()

    def _open_update_stock(self):
        sel = self.products_text.get("sel.first", "sel.last") if self.products_text.tag_ranges("sel") else ""
        if not sel:
            messagebox.showwarning("Select", "Select a product line in the list to update.")
            return
        try:
            pid = int(sel.split("|")[0].strip())
            old_stock = int(sel.split("Stock:")[1].strip())
        except Exception:
            messagebox.showerror("Error", "Could not parse selection.")
            return

        top = ctk.CTkToplevel()
        top.title("Update Stock")
        top.geometry("320x140")
        ctk.CTkLabel(top, text="New stock value").pack(pady=(12,6))
        entry = ctk.CTkEntry(top)
        entry.insert(0, str(old_stock))
        entry.pack(pady=6)
        def save():
            try:
                ns = int(entry.get().strip())
            except:
                messagebox.showerror("Error", "Enter a valid integer.")
                return
            update_product_stock(pid, ns)
            messagebox.showinfo("Saved", "Stock updated.")
            top.destroy()
            self._refresh_products()
        ctk.CTkButton(top, text="Save", command=save).pack(pady=8)
