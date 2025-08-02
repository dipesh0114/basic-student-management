import tkinter as tk
from tkinter import messagebox
import mysql.connector

# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",  # Change this
    database="student_db"
)
cursor = conn.cursor()

# GUI App
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x500")

# Form labels and fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Age").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Grade").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="ID (for Update/Delete/Search)").grid(row=3, column=0, padx=10, pady=5)

name_entry = tk.Entry(root)
age_entry = tk.Entry(root)
grade_entry = tk.Entry(root)
id_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
age_entry.grid(row=1, column=1)
grade_entry.grid(row=2, column=1)
id_entry.grid(row=3, column=1)

# Functions
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()
    if name and age and grade:
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
        conn.commit()
        messagebox.showinfo("Success", "Student added.")
    else:
        messagebox.showerror("Error", "Fill all fields!")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    result = "\n".join([f"ID: {r[0]}, Name: {r[1]}, Age: {r[2]}, Grade: {r[3]}" for r in rows])
    messagebox.showinfo("All Students", result or "No records found.")

def search_student():
    sid = id_entry.get()
    if sid:
        cursor.execute("SELECT * FROM students WHERE id=%s", (sid,))
        row = cursor.fetchone()
        if row:
            messagebox.showinfo("Student Found", f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
        else:
            messagebox.showwarning("Not Found", "Student ID not found.")
    else:
        messagebox.showerror("Error", "Enter Student ID.")

def update_student():
    sid = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()
    if sid and name and age and grade:
        cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s", (name, age, grade, sid))
        conn.commit()
        messagebox.showinfo("Updated", "Student record updated.")
    else:
        messagebox.showerror("Error", "Fill all fields including ID.")

def delete_student():
    sid = id_entry.get()
    if sid:
        cursor.execute("DELETE FROM students WHERE id=%s", (sid,))
        conn.commit()
        messagebox.showinfo("Deleted", "Student deleted.")
    else:
        messagebox.showerror("Error", "Enter Student ID.")

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=5, column=0, pady=10)
tk.Button(root, text="View All", command=view_students).grid(row=5, column=1)
tk.Button(root, text="Search", command=search_student).grid(row=6, column=0)
tk.Button(root, text="Update", command=update_student).grid(row=6, column=1)
tk.Button(root, text="Delete", command=delete_student).grid(row=7, column=0, columnspan=2)

# Run the app
root.mainloop()

# Close DB connection on exit
cursor.close()
conn.close()
