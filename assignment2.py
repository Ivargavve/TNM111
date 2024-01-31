import tkinter as tk
import numpy as np
import math

class Point:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.highlighted = False  # Added the highlighted attribute
    
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
    canvas.bind("<Button-1>", left_click)
    canvas.bind("<Button-3>", right_click)  # Right click for highlighting nearest points
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

def calculateEuclideanDistance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def find_nearest_points(data, selected_point):
    distances = []
    for point in data:
        if point != selected_point:
            distance = calculateEuclideanDistance(selected_point, point)
            distances.append((point, distance))
    distances.sort(key=lambda x: x[1])
    return distances[:5]

def highlight_nearest_points(nearest_points):
    for point, _ in nearest_points:
        canvas.create_oval(point.x - 2, point.y - 2, point.x + 7, point.y + 7, outline="white", width=2)

def clear_highlighted_points():
    for point in data:
        if point.highlighted:
            canvas.create_oval(point.x - 2, point.y - 2, point.x + 7, point.y + 7, outline="black", width=2)
            point.highlighted = False

def left_click(event):
    print("Left click")
    global selected_point, use_new_grid
    x, y = event.x, event.y

    if selected_point is None:
        # Find the selected point
        for point in data:
            if point.x - 2 <= x <= point.x + 7 and point.y - 2 <= y <= point.y + 7:
                selected_point = point
                break

        if selected_point is not None:
            # Activate new grid system with selected point as the new origin
            use_new_grid = True
            clear_highlighted_points()
            highlight_selected_point(selected_point)
            redraw_graph(canvas, maxT, selected_point)

    else:
        # Deactivate new grid system and reset selected_point
        if selected_point.x - 2 <= x <= selected_point.x + 7 and selected_point.y - 2 <= y <= selected_point.y + 7:
            use_new_grid = False
            clear_highlighted_points()
            selected_point = None
            redraw_graph(canvas, maxT, selected_point)

def redraw_graph(canvas, maxT, selected_point):
    canvas.delete("all")
    draw_graph(canvas, maxT)
    create_legend(canvas)
    scatterplot(data, maxT, selected_point)

def highlight_selected_point(point):
    canvas.create_oval(point.x - 2, point.y - 2, point.x + 7, point.y + 7, outline="white", width=2)

def scatterplot(data, maxT, selected_point=None):
    for point in data:
        x_range = maxT[0] - maxT[2]
        y_range = maxT[1] - maxT[3]
        
        if selected_point is not None and use_new_grid:
            point.x = 350 + (point.x - selected_point.x) * (600 / x_range)
            point.y = 350 - (point.y - selected_point.y) * (600 / y_range)
        else:
            point.x = 350 + point.x * (600 / x_range)
            point.y = 350 - point.y * (600 / y_range)

        if point.id == "a":
            draw_dot_with_quadrant_color(point, selected_point)
        elif point.id == "b":
            draw_rect_with_quadrant_color(point, selected_point)
        elif point.id == "c":
            draw_cross_with_quadrant_color(point, selected_point)

def draw_dot_with_quadrant_color(point, selected_point):
    color = determine_quadrant_color(point, selected_point)
    canvas.create_oval(point.x, point.y, point.x + 5, point.y + 5, fill=color)

def draw_rect_with_quadrant_color(point, selected_point):
    color = determine_quadrant_color(point, selected_point)
    canvas.create_rectangle(point.x, point.y, point.x + 5, point.y + 5, fill=color)

def draw_cross_with_quadrant_color(point, selected_point):
    color = determine_quadrant_color(point, selected_point)
    canvas.create_line(point.x, point.y, point.x + 5, point.y + 5, fill=color)

def determine_quadrant_color(point, selected_point):
    if selected_point is not None and use_new_grid:
        x = point.x - selected_point.x
        y = point.y - selected_point.y
    else:
        x = point.x - 350
        y = 350 - point.y

    if x >= 0 and y >= 0:
        return "green"
    elif x < 0 and y >= 0:
        return "blue"
    elif x < 0 and y < 0:
        return "red"
    elif x >= 0 and y < 0:
        return "yellow"

def right_click(event):
    print("Right click")
    x, y = event.x, event.y
    for point in data:
        if point.x - 2 <= x <= point.x + 7 and point.y - 2 <= y <= point.y + 7:
            if not point.highlighted:
                nearest_points = find_nearest_points(data, point)
                highlight_nearest_points(nearest_points)
                point.highlighted = True
            else:
                clear_highlighted_points()
                point.highlighted = False

# Initialize global variables
selected_point = None
use_new_grid = False

data = load_csv("data1.csv")
canvas = create_canvas()
maxT = calculateMaxMin(data)
draw_graph(canvas, maxT)
create_legend(canvas)
scatterplot(data, maxT)

tk.mainloop()
