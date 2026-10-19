
import tkinter as tk

window = tk.Tk()
window.title("SpendWise")
window.geometry("500x300")

message = tk.Label(
    window,
    text="Welcome to SpendWise!",
    font=("Arial", 18)
)
message.pack(pady=40)

window.mainloop()
