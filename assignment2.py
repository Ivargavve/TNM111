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

def calculateMaxMin(data):
    x_max = 0
    y_max = 0
    x_min = 0
    y_min = 0
    for point in data:
        if point.x > x_max:
            x_max = point.x
        if point.y > y_max:
            y_max = point.y
        if point.x < x_min:
            x_min = point.x
        if point.y < y_min:
            y_min = point.y
    return x_max, y_max, x_min, y_min

def draw_graph(canvas, maxT):
    canvas.create_line(50, 350, 650, 350, width=2)
    canvas.create_line(350, 50, 350, 650, width=2)

    # draw x axis and create text through iteration
    for i in range(0, 11):
        x_tick_position = 650 - i*60
        canvas.create_line(x_tick_position, 350, x_tick_position, 345, width=2)
        canvas.create_text(x_tick_position, 360, text=f'{maxT[0]-i*((maxT[0]-maxT[2])/ 10):.1f}', font=("Purisa", 10))
    # draw y axis and create text through iteration
    for i in range(0, 11):
        y_tick_position = 650 - i*60
        canvas.create_line(350, y_tick_position, 345, y_tick_position, width=2)
        canvas.create_text(370, y_tick_position, text=f'{maxT[3]-i*((maxT[3]-maxT[1])/10):.1f}', font=("Purisa", 10))
def drawDot(x,y):
    canvas.create_oval(x,y,x+5,y+5,fill="red")

def drawRect(x,y,):
    canvas.create_rectangle(x,y,x+5,y+5,fill="blue")

def drawCross(x,y):
    canvas.create_line(x,y,x+5,y+5,fill="yellow")

def scatterplot(data, maxT):
    for point in data:
        x_range = maxT[0] - maxT[2]
        y_range = maxT[1] - maxT[3]
        point.x = 350 + point.x * (600/x_range)
        point.y = 350 - point.y * (600/y_range)
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

# create a legend with information about the data
def create_legend(canvas):
    # Define your data types and corresponding colors
    data_types = ['a', 'b', 'c']
    colors = ['red', 'blue', 'yellow']

    # Set the starting coordinates for the legend
    x_start, y_start = 50, 50

    # Iterate through data types to create legend items
    for i, data_type in enumerate(data_types):
        # Draw colored rectangle
        canvas.create_rectangle(x_start, y_start + i * 30, x_start + 20, y_start + i * 30 + 20, fill=colors[i])

        # Display data type label next to the rectangle
        canvas.create_text(x_start + 30, y_start + i * 30 + 10, text=data_type, anchor=tk.W)

data = load_csv("data1.csv")
canvas = create_canvas()
maxT = calculateMaxMin(data)
draw_graph(canvas, maxT)
create_legend(canvas)
scatterplot(data, maxT)

tk.mainloop()
