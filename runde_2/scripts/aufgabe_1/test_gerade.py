import tkinter as tk
import numpy as np
import sys #eventuell optional


def pusten(position, richtung):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    richtung = np.subtract(richtung,position)
    
    def istImHof(feld):
        if feld[0] < groessen[0] and feld[1] < groessen[1]:
            return 1
        else:
            return 0
    
    position = np.add(position, richtung)
    ziel = np.add(position, richtung)#ziel bestimmt.
    ziel_links = np.add(ziel, [richtung[1], richtung[0]])
    ziel_rechts = np.add(ziel, [richtung[1]*-1, richtung[0]*-1])
    neuesziel = np.add(ziel, richtung)
    
    if istImHof (ziel_links) and istImHof(ziel_rechts):
        schulhof[tuple(neuesziel)] += schulhof[tuple(ziel)]*0.1    
        schulhof[tuple(ziel)] = schulhof[tuple(ziel)]*0.9

    if istImHof(ziel_links) and istImHof(ziel_rechts) and istImHof(ziel):
        schulhof[tuple(ziel_links)] = schulhof[tuple(ziel_links)] + schulhof[tuple(position)]*0.1
        schulhof[tuple(ziel_rechts)] = schulhof[tuple(ziel_rechts)] + schulhof[tuple(position)]*0.1
        schulhof[tuple(ziel)] = schulhof[tuple(ziel)] + schulhof[tuple(position)]*0.8
    schulhof[tuple(position)] = 0.0
    
    # Update the grid
    update_grid()

def update_grid():
    for row in range(12):
        for col in range(12):
            canvas.itemconfig(texts[row][col], text=np.round(schulhof[row, col], 1))
            canvas.itemconfig(rectangles[row][col], fill = get_custom_color(schulhof[row, col]))
            
def get_custom_color(value):
    # Example implementation to generate custom color based on the value
    red = value*205/20+50 # Adjust the formula based on your preference
    green = value*205/20+50
    blue = value * 205/20+50
    return "#{:02X}{:02X}{:02X}".format(int(red), int(green), int(blue))

def on_box_click(row, col):
    global c
    c += 1
    print(c)
    global click_count, first_click
    if click_count == 0:
        first_click = (row, col)
        click_count += 1
    elif click_count == 1:
        second_click = (row, col)
        click_count = 0
        pusten(first_click, second_click)

# Create a 5x5 NumPy array
groessen = (12,12)

schulhof = np.full((groessen), 1.0)

root = tk.Tk()
root.title("Grid Clicker")

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

rectangles = [[None] * 12 for _ in range(12)]
texts = [[None] * 12 for _ in range(12)]

for row in range(12):
    for col in range(12):
        x1, y1 = col * 50, row * 50
        x2, y2 = x1 + 50, y1 + 50
        rectangles[row][col] = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
        texts[row][col] = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=schulhof[row, col], font=("Arial", 12), fill="black")
        canvas.tag_bind(rectangles[row][col], "<Button-1>", lambda event, r=row, c=col: on_box_click(r, c))

click_count = 0
c=0
first_click = None  # Initialize the variable
root.mainloop()
