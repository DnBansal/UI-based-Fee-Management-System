# gui.py
# Full graphical version of your original console-based Fee Management System
# (Preserves the original main menu structure and submenus)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import admin, cls, fee, report

# Ensure DB exists at startup
try:
    admin.create_db_if_missing()
except Exception as e:
    messagebox.showerror('Database Error', f'Could not initialize DB: {e}')

class FeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fee Management System")
        self.geometry("900x600")
        self.configure(bg="#f8f8f8")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ================= MAIN MENU =================
    def show_main_menu(self):
        self.clear_screen()
        tk.Label(self, text="*** FEE MANAGEMENT PROJECT ***", 
                 font=("Helvetica", 20, "bold"), fg="#2a2a2a", bg="#f8f8f8").pack(pady=40)

        menu_frame = tk.Frame(self, bg="#f8f8f8")
        menu_frame.pack(pady=30)

        buttons = [
            ("1. Class Management", self.open_class_menu),
            ("2. Fee Management", self.open_fee_menu),
            ("3. Report", self.open_report_menu),
            ("4. Admin", self.open_admin_menu),
            ("5. Exit", self.quit)
        ]

        for text, cmd in buttons:
            ttk.Button(menu_frame, text=text, width=30, command=cmd).pack(pady=10)

    # ================= CLASS MENU =================
    def open_class_menu(self):
        self.clear_screen()
        tk.Label(self, text="*** CLASS MANAGEMENT ***", 
                 font=("Helvetica", 18, "bold"), bg="#f8f8f8").pack(pady=20)

        frame = tk.Frame(self, bg="#f8f8f8")
        frame.pack()

        self.cls_list = tk.Listbox(frame, width=70, height=15, font=("Consolas", 11))
        self.cls_list.pack(side="left", padx=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.cls_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.cls_list.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self, bg="#f8f8f8")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Add Class", command=self.add_class_dialog).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Refresh", command=self.load_classes).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side="left", padx=10)

        self.load_classes()

    def load_classes(self):
        self.cls_list.delete(0, "end")
        try:
            rows = cls.get_all_classes()
            if not rows:
                self.cls_list.insert("end", "No class records found.")
                return
            for r in rows:
                self.cls_list.insert("end", f"CID:{r[0]}  Class:{r[1]}{r[2]}  Teacher:{r[3]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classes: {e}")

    def add_class_dialog(self):
        cname = simpledialog.askstring("Class", "Enter class name (e.g., 10):", parent=self)
        if cname is None:
            return
        sec = simpledialog.askstring("Section", "Enter section (e.g., A):", parent=self)
        if sec is None:
            return
        tname = simpledialog.askstring("Teacher", "Enter teacher name:", parent=self)
        try:
            cls.add_class(cname.strip(), sec.strip().upper(), (tname or "").strip())
            messagebox.showinfo("Success", "Class added successfully!")
            self.load_classes()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add class: {e}")

    # ================= FEE MENU =================
    def open_fee_menu(self):
        self.clear_screen()
        tk.Label(self, text="*** FEE MANAGEMENT ***", 
                 font=("Helvetica", 18, "bold"), bg="#f8f8f8").pack(pady=20)

        frame = tk.Frame(self, bg="#f8f8f8")
        frame.pack()

        self.fee_list = tk.Listbox(frame, width=90, height=15, font=("Consolas", 11))
        self.fee_list.pack(side="left", padx=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.fee_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.fee_list.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self, bg="#f8f8f8")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Add Fee Entry", command=self.add_fee_dialog).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Refresh", command=self.load_fees).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side="left", padx=10)

        self.load_fees()

    def load_fees(self):
        self.fee_list.delete(0, "end")
        try:
            all_classes = cls.get_all_classes()
            for cdata in all_classes:
                fees = fee.get_fees_by_class(cdata[0])
                for fdata in fees:
                    self.fee_list.insert("end", f"FID:{fdata[0]} CID:{fdata[1]} STU:{fdata[2]} DATE:{fdata[3]} GT:{fdata[4]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load fees: {e}")

    def add_fee_dialog(self):
        cid = simpledialog.askinteger("Class ID", "Enter Class ID:", parent=self)
        stu = simpledialog.askinteger("Student Roll", "Enter student roll/id:", parent=self)
        date = simpledialog.askstring("Date", "Enter date (dd-mm-yyyy):", parent=self)
        gt = simpledialog.askinteger("Total", "Enter total fee amount:", parent=self)
        if not all([cid, stu, date, gt]):
            return
        try:
            fee.add_fee(cid, stu, date, 0, 0, 0, 0, 0, 0, 0, gt)
            messagebox.showinfo("Success", "Fee record added successfully!")
            self.load_fees()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add fee: {e}")

    # ================= REPORT MENU =================
    def open_report_menu(self):
        self.clear_screen()
        tk.Label(self, text="*** REPORT MENU ***", 
                 font=("Helvetica", 18, "bold"), bg="#f8f8f8").pack(pady=20)

        frame = tk.Frame(self, bg="#f8f8f8")
        frame.pack()

        self.report_list = tk.Listbox(frame, width=90, height=15, font=("Consolas", 11))
        self.report_list.pack(side="left", padx=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.report_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.report_list.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self, bg="#f8f8f8")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Show Fees by Date", command=self.report_on_date).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side="left", padx=10)

    def report_on_date(self):
        date = simpledialog.askstring("Date", "Enter date (dd-mm-yyyy):", parent=self)
        if not date:
            return
        try:
            data = report.fees_on_date(date)
            self.report_list.delete(0, "end")
            if not data:
                self.report_list.insert("end", "No fees found on this date.")
                return
            for r in data:
                self.report_list.insert("end", f"FID:{r[0]} CID:{r[1]} STU:{r[2]} DATE:{r[3]} GT:{r[4]}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load report: {e}")

    # ================= ADMIN MENU =================
    def open_admin_menu(self):
        self.clear_screen()
        tk.Label(self, text="*** ADMIN MENU ***", 
                 font=("Helvetica", 18, "bold"), bg="#f8f8f8").pack(pady=20)

        frame = tk.Frame(self, bg="#f8f8f8")
        frame.pack(pady=20)

        ttk.Button(frame, text="Recreate Database", command=self.recreate_db).pack(pady=10)
        ttk.Button(frame, text="Change Password", command=self.change_password).pack(pady=10)
        ttk.Button(frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def recreate_db(self):
        if messagebox.askyesno("Confirm", "This will delete and recreate the entire database. Continue?"):
            try:
                admin.drop_database()
                admin.create_db_if_missing()
                messagebox.showinfo("Done", "Database recreated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to recreate database: {e}")

    def change_password(self):
        old_pw = simpledialog.askstring("Old Password", "Enter current admin password:", show="*", parent=self)
        if not old_pw:
            return
        if not admin.verify_password(old_pw):
            messagebox.showerror("Error", "Incorrect password.")
            return
        new_pw = simpledialog.askstring("New Password", "Enter new password:", show="*", parent=self)
        if not new_pw:
            return
        try:
            admin.change_password(new_pw)
            messagebox.showinfo("Success", "Password changed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not change password: {e}")

# ================= RUN APP =================
if __name__ == "__main__":
    app = FeeApp()
    app.mainloop()
