import tkinter as tk

def submit():
    field1_value = field1_entry.get()
    field2_value = field2_entry.get()
    print(f"Field 1 value: {field1_value}")
    print(f"Field 2 value: {field2_value}")


root = tk.Tk()
root.title("Field Values")

field1_label = tk.Label(root, text="Field 1:")
field1_label.pack()

field1_entry = tk.Entry(root)
field1_entry.pack()

field2_label = tk.Label(root, text="Field 2:")
field2_label.pack()

field2_entry = tk.Entry(root)
field2_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
