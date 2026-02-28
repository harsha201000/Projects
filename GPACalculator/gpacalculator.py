# gpacalculator.py
# A simple GUI GPA calculator with icon buttons.
# Place optional icon files in an "icons" subfolder (add.png, remove.png, calculate.png, save.png, load.png).
# Requires Pillow (optional) for better image support: pip install pillow


import json
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

try:
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

GRADE_POINTS = {
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0
}
GRADE_OPTIONS = list(GRADE_POINTS.keys())
DEFAULT_CREDIT_OPTIONS = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]


def resource_path(rel_path):
    # For bundling; otherwise returns path relative to script
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


def load_icon(path, size=(24, 24), fallback_text=None, bg="#ddd"):
    path = resource_path(path)
    if PIL_AVAILABLE and os.path.exists(path):
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            pass
    # Fallback: draw a simple icon with text or colored box
    if PIL_AVAILABLE:
        img = Image.new("RGBA", size, bg)
        draw = ImageDraw.Draw(img)
        if fallback_text:
            try:
                # try to use a default font
                f = ImageFont.load_default()
                w, h = draw.textsize(fallback_text, font=f)
                draw.text(((size[0]-w)/2, (size[1]-h)/2), fallback_text, fill="black", font=f)
            except Exception:
                pass
        return ImageTk.PhotoImage(img)
    else:
        # tkinter native PhotoImage fallback (small colored square)
        img = tk.PhotoImage(width=size[0], height=size[1])
        # fill with bg color
        img.put(("{}".format(bg),), to=(0, 0, size[0], size[1]))
        return img


class CourseRow:
    def __init__(self, parent, app, row_index):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        self.course_var = tk.StringVar()
        self.credit_var = tk.DoubleVar(value=3.0)
        self.grade_var = tk.StringVar(value="A")

        self.entry_course = ttk.Entry(self.frame, textvariable=self.course_var, width=30)
        self.spin_credit = ttk.Spinbox(
            self.frame, from_=0.0, to=10.0, increment=0.5, textvariable=self.credit_var, width=6
        )
        self.combo_grade = ttk.Combobox(
            self.frame, values=GRADE_OPTIONS, textvariable=self.grade_var, state="readonly", width=6
        )
        self.btn_remove = ttk.Button(self.frame, image=app.icon_remove, command=self.remove)

        self.entry_course.grid(row=0, column=0, padx=(0, 6), sticky="w")
        self.spin_credit.grid(row=0, column=1, padx=(0, 6))
        self.combo_grade.grid(row=0, column=2, padx=(0, 6))
        self.btn_remove.grid(row=0, column=3)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def remove(self):
        self.app.remove_row(self)

    def get_data(self):
        name = self.course_var.get().strip()
        try:
            credits = float(self.credit_var.get())
        except Exception:
            credits = 0.0
        grade = self.grade_var.get()
        return {"name": name, "credits": credits, "grade": grade}

    def destroy(self):
        self.frame.destroy()


class GPACalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPA Calculator")
        self.minsize(600, 400)
        self.style = ttk.Style(self)
        
        # Use platform default theme
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Load icons (optional)
        self.icon_add = load_icon("icons/add.png", (20, 20), fallback_text="+", bg="#aaf")
        self.icon_remove = load_icon("icons/remove.png", (18, 18), fallback_text="-", bg="#faa")
        self.icon_calc = load_icon("icons/calculate.png", (20, 20), fallback_text="=", bg="#afa")
        self.icon_save = load_icon("icons/save.png", (20, 20), fallback_text="S", bg="#ffd")
        self.icon_load = load_icon("icons/load.png", (20, 20), fallback_text="L", bg="#ddf")

        self.rows = []
        self.build_ui()
        # Start with 4 rows
        for _ in range(4):
            self.add_row()

    def build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=12, pady=8)

        lbl_title = ttk.Label(top, text="GPA Calculator", font=("Segoe UI", 14, "bold"))
        lbl_title.pack(side="left")

        btn_frame = ttk.Frame(top)
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, image=self.icon_add, text=" Add", compound="left", command=self.add_row).pack(side="left", padx=4)
        ttk.Button(btn_frame, image=self.icon_calc, text=" Calculate", compound="left", command=self.calculate_gpa).pack(side="left", padx=4)
        ttk.Button(btn_frame, image=self.icon_save, text=" Save", compound="left", command=self.save_courses).pack(side="left", padx=4)
        ttk.Button(btn_frame, image=self.icon_load, text=" Load", compound="left", command=self.load_courses).pack(side="left", padx=4)

        # Headers
        hdr = ttk.Frame(self)
        hdr.pack(fill="x", padx=12)
        ttk.Label(hdr, text="Course", width=40).grid(row=0, column=0, sticky="w")
        ttk.Label(hdr, text="Credits", width=8).grid(row=0, column=1)
        ttk.Label(hdr, text="Grade", width=8).grid(row=0, column=2)
        # container for rows
        self.rows_container = ttk.Frame(self)
        self.rows_container.pack(fill="both", expand=True, padx=12, pady=8)

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=12, pady=(0, 12))
        self.lbl_result = ttk.Label(bottom, text="GPA: 0.00 (0.00 credits)", font=("Segoe UI", 11, "bold"))
        self.lbl_result.pack(side="left")

        # Shortcut: Enter to calculate
        self.bind("<Return>", lambda e: self.calculate_gpa())

    def add_row(self, at_end=True):
        row = CourseRow(self.rows_container, self, len(self.rows))
        self.rows.append(row)
        self.refresh_rows()

    def remove_row(self, row_obj):
        if row_obj in self.rows:
            if len(self.rows) == 1:
                messagebox.showinfo("Notice", "At least one course must remain.")
                return
            row_obj.destroy()
            self.rows.remove(row_obj)
            self.refresh_rows()

    def refresh_rows(self):
        for i, row in enumerate(self.rows):
            row.grid(row=i, column=0, pady=4, sticky="w")
        # update window
        self.update_idletasks()

    def calculate_gpa(self):
        total_points = 0.0
        total_credits = 0.0
        details = []
        for row in self.rows:
            data = row.get_data()
            credits = data["credits"]
            grade = data["grade"]
            if credits <= 0.0:
                continue
            gp = GRADE_POINTS.get(grade, None)
            if gp is None:
                continue
            total_points += gp * credits
            total_credits += credits
            details.append((data["name"], credits, grade, gp))
        if total_credits == 0:
            gpa = 0.0
        else:
            gpa = total_points / total_credits
        self.lbl_result.config(text=f"GPA: {gpa:.3f} ({total_credits:.2f} credits)")
        # optional: show breakdown dialog
        detail_lines = []
        for name, credits, grade, gp in details:
            name_display = name if name else "(unnamed)"
            detail_lines.append(f"{name_display}: {credits} cr x {grade} ({gp})")
        if detail_lines:
            # show a short summary in a tooltip-like message box
            messagebox.showinfo("Calculation Summary", f"GPA: {gpa:.3f}\nCredits: {total_credits:.2f}\n\n" + "\n".join(detail_lines[:20]))

    def save_courses(self):
        data = [row.get_data() for row in self.rows]
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Saved {len(data)} courses to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def load_courses(self):
        path = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # validate and populate
            for row in self.rows:
                row.destroy()
            self.rows.clear()
            for item in data:
                row = CourseRow(self.rows_container, self, len(self.rows))
                row.course_var.set(item.get("name", ""))
                try:
                    row.credit_var.set(float(item.get("credits", 0.0)))
                except Exception:
                    row.credit_var.set(0.0)
                grade = item.get("grade", "A")
                if grade not in GRADE_OPTIONS:
                    grade = "A"
                row.grade_var.set(grade)
                self.rows.append(row)
            if not self.rows:
                self.add_row()
            self.refresh_rows()
            messagebox.showinfo("Loaded", f"Loaded {len(self.rows)} courses from:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file:\n{e}")


if __name__ == "__main__":
    app = GPACalculatorApp()
    app.mainloop()