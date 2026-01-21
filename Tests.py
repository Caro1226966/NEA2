import tkinter as tk

root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()

BASE_MOVEMENT_SPEED = 600
print(BASE_MOVEMENT_SPEED,' = Base movement speed')
health = 6000
print(BASE_MOVEMENT_SPEED * (500/health))
