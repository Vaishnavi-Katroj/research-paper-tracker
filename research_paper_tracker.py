import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE_NAME = "papers.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Authors", "Domain", "Status"])


def add_paper():
    title = title_entry.get()
    authors = author_entry.get()
    domain = domain_entry.get()
    status = status_var.get()

    if title == "" or authors == "" or domain == "":
        messagebox.showwarning("Input Error", "All fields are required")
        return

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([title, authors, domain, status])

    load_papers()
    clear_fields()


def load_papers():
    for row in tree.get_children():
        tree.delete(row)

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)


def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    domain_entry.delete(0, tk.END)
    status_var.set("Reading")


def delete_paper():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a paper to delete")
        return

    values = tree.item(selected[0], "values")

    rows = []
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            if row != list(values):
                writer.writerow(row)

    load_papers()


# GUI
root = tk.Tk()
root.title("Research Paper Tracker")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Title").grid(row=0, column=0)
tk.Label(frame, text="Authors").grid(row=1, column=0)
tk.Label(frame, text="Domain").grid(row=2, column=0)
tk.Label(frame, text="Status").grid(row=3, column=0)

title_entry = tk.Entry(frame, width=40)
author_entry = tk.Entry(frame, width=40)
domain_entry = tk.Entry(frame, width=40)

title_entry.grid(row=0, column=1)
author_entry.grid(row=1, column=1)
domain_entry.grid(row=2, column=1)

status_var = tk.StringVar()
status_menu = ttk.Combobox(
    frame,
    textvariable=status_var,
    values=["Reading", "Completed", "Implemented"],
    state="readonly",
)
status_menu.grid(row=3, column=1)
status_var.set("Reading")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Paper", command=add_paper).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Selected", command=delete_paper).grid(row=0, column=1, padx=5)

columns = ("Title", "Authors", "Domain", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True, pady=10)

load_papers()
root.mainloop()
