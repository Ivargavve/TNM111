import tkinter as tk
import numpy as np
import math

class Point:
  def __init__(self,x,y,id):
    self.x = x
    self.y = y
    self.id = id
    
def load_csv(file):
    data = []
    with open(file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            data.append(Point(
                float(values[0]),
                float(values[1]),
                values[2]
            ))
    return data

def calculateMax(data):
    x_max = 0
    y_max = 0
    for point in data:
        if point.x > x_max:
            x_max = point.x
        if point.y > y_max:
            y_max = point.y
    return x_max, y_max

def draw_graph(canvas, maxT):
    canvas.create_line(50, 350, 650, 350, width=2)
    canvas.create_line(350, 50, 350, 650, width=2)

    # draw x axis and create text through iteration
    for i in range(1, 9):
        canvas.create_line(50 + 100 * i, 350, 50 + 100 * i, 345, width=2)
        canvas.create_text(50 + 100 * i, 360, text=round((maxT[0] + i * (abs(maxT[0]) / 8))), anchor='w', font=("Purisa", 10))

    # draw y axis and create text through iteration
    for i in range(1, 9):
        canvas.create_line(350, 350 - 100 * i, 345, 350 - 100 * i, width=2)
        canvas.create_text(350, 700 - 100 * i, text=round((maxT[1] + i * (abs(maxT[1]) / 8))), anchor='w', font=("Purisa", 10))

def drawDot(x,y):
    canvas.create_oval(x,y,x+5,y+5,fill="red")

def drawRect(x,y,):
    canvas.create_rectangle(x,y,x+5,y+5,fill="blue")

def drawCross(x,y):
    canvas.create_line(x,y,x+5,y+5,fill="yellow")

def scatterplot(data):
    for point in data:
        point.x = 350 + point.x * (350/100)
        point.y = 350 - point.y * (350/100)
        if point.id == "a":
            drawDot(point.x, point.y)
        elif point.id == "b":
            drawRect(point.x, point.y)
        elif point.id == "c":
            drawCross(point.x, point.y)

# create a canvas
def create_canvas():
    window = tk.Tk()
    window.title("Scatter Plot")
    canvas = tk.Canvas(window, width=700, height=700, bg="black")
    canvas.pack()
    return canvas

data = load_csv("data1.csv")
canvas = create_canvas()
maxT = calculateMax(data)
draw_graph(canvas, maxT)
scatterplot(data)

tk.mainloop()
