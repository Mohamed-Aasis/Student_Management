import mysql.connector # type: ignore
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="root",  # Replace with your MySQL password
        database="student_db"
    )

def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to Add Student
def add_student():
    if name_var.get() == "" or age_var.get() == "" or dept_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, department) VALUES (%s, %s, %s)", 
                       (name_var.get(), age_var.get(), dept_var.get()))
        conn.commit()
        conn.close()
        clear_fields()
        display_students()
        messagebox.showinfo("Success", "Student added successfully")

# Function to Update Student
def update_student():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, age=%s, department=%s WHERE id=%s", 
                   (name_var.get(), age_var.get(), dept_var.get(), id_var.get()))
    conn.commit()
    conn.close()
    clear_fields()
    display_students()
    messagebox.showinfo("Success", "Student updated successfully")

# Function to Delete Student
def delete_student():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id_var.get(),))
    conn.commit()
    conn.close()
    clear_fields()
    display_students()
    messagebox.showinfo("Success", "Student deleted successfully")

# Function to Search Student
def search_student():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + search_var.get() + '%',))
    rows = cursor.fetchall()
    conn.close()
    update_treeview(rows)

# Function to Display Students
def display_students():
    rows = fetch_data()
    update_treeview(rows)

def update_treeview(rows):
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", END, values=row)

def clear_fields():
    id_var.set("")
    name_var.set("")
    age_var.set("")
    dept_var.set("")

# GUI Setup
root = Tk()
root.title("Student Management System")
root.geometry("600x400")

# Variables
id_var = StringVar()
name_var = StringVar()
age_var = StringVar()
dept_var = StringVar()
search_var = StringVar()

# Labels and Entry Fields
Label(root, text="Name").grid(row=0, column=0)
Entry(root, textvariable=name_var).grid(row=0, column=1)
Label(root, text="Age").grid(row=1, column=0)
Entry(root, textvariable=age_var).grid(row=1, column=1)
Label(root, text="Department").grid(row=2, column=0)
Entry(root, textvariable=dept_var).grid(row=2, column=1)

# Buttons
Button(root, text="Add", command=add_student).grid(row=3, column=0)
Button(root, text="Update", command=update_student).grid(row=3, column=1)
Button(root, text="Delete", command=delete_student).grid(row=3, column=2)
Button(root, text="Clear", command=clear_fields).grid(row=3, column=3)

# Search Bar
Entry(root, textvariable=search_var).grid(row=4, column=0)
Button(root, text="Search", command=search_student).grid(row=4, column=1)

# Table
columns = ("ID", "Name", "Age", "Department")
student_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=100)
student_table.grid(row=5, column=0, columnspan=4)
display_students()

# Run App
root.mainloop()
