import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class ScatterPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Scatter Plot")
        self.root.geometry("850x850")

        self.data = None
        self.scatter_plot_shapes = []
        self.left_selected = None
        self.right_selected = None
        self.typeOfData = 0

        self.create_widgets()

    def create_widgets(self):
        self.load_data_button = tk.Button(
            self.root, text="Load Data", command=self.load_data
        )
        self.load_data_button.pack(pady=10)

        self.plot_button = tk.Button(
            self.root, text="Plot Scatter Plot", command=self.plot_scatter_plot
        )
        self.plot_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV file", filetypes=[("CSV files", "*.csv")]
        )

        if file_path:
            self.data = pd.read_csv(file_path)
            messagebox.showinfo("Info", "Data loaded successfully!")

    def plot_scatter_plot(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please load data first.")
            return
        #Clears canvas and resets scatterplot shapes
        self.canvas.delete("all")
        self.scatter_plot_shapes = []
        shape_dict = {
            category: shape
            for category, shape in zip(
                self.data.iloc[:, 2].unique(),
                ["circle", "triangle", "square"],
            )
        }

        for _, row in self.data.iterrows():
            x, y, category = row[0], row[1], row[2]
            x_pixel = self.map_x_to_pixel(x, self.data.iloc[:, 0].min(), self.data.iloc[:, 0].max())
            y_pixel = self.map_y_to_pixel(y, self.data.iloc[:, 1].min(), self.data.iloc[:, 1].max())
            shape = shape_dict.get(category, "circle")
            #To identufy shapes for later
            shape_id = self.plot_shape(x_pixel, y_pixel, shape, fill="blue")
            #Adds it to the list for later
            self.scatter_plot_shapes.append((shape_id, (x, y, category)))

        self.draw_axes()

    def create_info_square(self, type):
        tyke = ["Baz", "Bar", "Foo"]

        if(type ==0):
            tyke = ["a", "b", "c"]

        self.canvas.create_text(
            650, 80, anchor=tk.N, text = tyke[0]
            )
        self.plot_shape(670, 88, "circle", fill="black")

        self.canvas.create_text(
            650, 100, anchor=tk.N, text = tyke[1]
            )
        self.plot_shape(670, 108, "triangle", fill="black")

        self.canvas.create_text(
            650, 120, anchor=tk.N, text = tyke[2]
            )
        self.plot_shape(670, 128, "square", fill="black")

        square = self.canvas.create_rectangle(625, 70, 700, 140, outline="black")

    def map_x_to_pixel(self, x, x_min, x_max):
        return 70 + (x - x_min) * (800 - 2 * 70) / (x_max - x_min)

    def map_y_to_pixel(self, y, y_min, y_max):
        return 600 - 70 - (y - y_min) * (600 - 2 * 70) / (y_max - y_min)

    def plot_shape(self, x, y, shape, **kwargs):
        half_size = 3
        if shape == "circle":
            return self.canvas.create_oval(
                x - half_size, y - half_size, x + half_size, y + half_size, **kwargs
            )
        elif shape == "triangle":
            return self.create_triangle(x, y, half_size, **kwargs)
        elif shape == "square":
            return self.canvas.create_rectangle(
                x - half_size, y - half_size, x + half_size, y + half_size, **kwargs
            )

    def create_triangle(self, x, y, size, **kwargs):
        x0, y0 = x, y - size
        x1, y1 = x - size, y + size
        x2, y2 = x + size, y + size
        return self.canvas.create_polygon(
            x0, y0, x1, y1, x2, y2, outline="black", **kwargs
        )
    
    def draw_axes(self):
        x_min = self.data.iloc[:, 0].min()
        x_max = self.data.iloc[:, 0].max()
        y_min = self.data.iloc[:, 1].min()
        y_max = self.data.iloc[:, 1].max()
        
        x_axis_y_pos = self.map_y_to_pixel(0, y_min, y_max)
        y_axis_x_pos = self.map_x_to_pixel(0, x_min, x_max)
        line_extensionX = 0
        line_extensionY = 0
        

        if(y_axis_x_pos<70):
            x_axis_y_pos = x_axis_y_pos -210
            line_extensionX = 10
            line_extensionY = 20
            self.typeOfData = 1
        
        self.create_info_square(self.typeOfData)
        line_thickness = 2

        print(y_max)
        self.canvas.create_line(
            70-line_extensionX, x_axis_y_pos, 800 - 70, x_axis_y_pos, fill="black", width=line_thickness
        )  # x-axis
        self.canvas.create_line(
            y_axis_x_pos, 70, y_axis_x_pos, 600 - 70+line_extensionY, fill="black", width=line_thickness
        )  # y-axis

        y_tick_spacing = 10
        y_range = range(int(y_min), int(y_max)+ 1, y_tick_spacing)

        for y_tick_value in y_range:
            y_tick_pixel = self.map_y_to_pixel(y_tick_value, y_min, y_max)
            self.canvas.create_line(
                y_axis_x_pos - 5, y_tick_pixel, y_axis_x_pos + 5, y_tick_pixel, fill="black"
            )
            self.canvas.create_text(
                y_axis_x_pos - 20, y_tick_pixel, anchor=tk.E, text=str(y_tick_value)
            )

        # Draw ticks and labels on x-axis
        x_tick_spacing = 10
        x_range = range(int(x_min), int(x_max) + 1, x_tick_spacing)
        
        for x_tick_value in x_range:
            x_tick_pixel = self.map_x_to_pixel(x_tick_value, x_min, x_max)
            self.canvas.create_line(
                x_tick_pixel, x_axis_y_pos - 5, x_tick_pixel, x_axis_y_pos + 5, fill="black"
            )
            self.canvas.create_text(
                x_tick_pixel, x_axis_y_pos + 20, anchor=tk.N, text=str(x_tick_value)
            )

    def left_click(self, event):
        x, y = event.x, event.y

        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            x_pixel = self.map_x_to_pixel(x_data, self.data.iloc[:, 0].min(), self.data.iloc[:, 0].max())
            y_pixel = self.map_y_to_pixel(y_data, self.data.iloc[:, 1].min(), self.data.iloc[:, 1].max())

            if (
                x_pixel - 3 <= x <= x_pixel + 3
                and y_pixel - 3 <= y <= y_pixel + 3
            ):
                if self.left_selected == shape_id:
                    self.clear_quadrant_axes()
                    self.left_selected = None
                    self.reset_shape_colors()
                else:
                    self.left_selected = shape_id
                    self.clear_quadrant_axes()
                    self.draw_quadrant_axes(x_pixel, y_pixel)
                    self.color_by_quadrant(x_pixel, y_pixel)
                break

    def right_click(self, event):
        x, y = event.x, event.y

        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            x_pixel = self.map_x_to_pixel(x_data, self.data.iloc[:, 0].min(), self.data.iloc[:, 0].max())
            y_pixel = self.map_y_to_pixel(y_data, self.data.iloc[:, 1].min(), self.data.iloc[:, 1].max())

            if (
                x_pixel - 3 <= x <= x_pixel + 3
                and y_pixel - 3 <= y <= y_pixel + 3
            ):
                if self.right_selected == shape_id:
                    self.unhighlight_points()
                    self.right_selected = None
                else:
                    self.right_selected = shape_id
                    neighbors = self.find_neighbors((x_data, y_data), num_neighbors=6)
                    self.highlight_points(neighbors)
                break

    def clear_quadrant_axes(self):
        self.canvas.delete("quad_axis")

    def draw_quadrant_axes(self, x, y):
        self.canvas.create_line(
            70, y, 800 - 70, y, fill="gray", tags="quad_axis"
        )  # horizontal axis
        self.canvas.create_line(
            x, 70, x, 600 - 70, fill="gray", tags="quad_axis"
        )  # vertical axis

    def color_by_quadrant(self, x, y):
        colors = {1: "green", 2: "blue", 3: "red", 4: "yellow"}

        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            x_pixel = self.map_x_to_pixel(x_data, self.data.iloc[:, 0].min(), self.data.iloc[:, 0].max())
            y_pixel = self.map_y_to_pixel(y_data, self.data.iloc[:, 1].min(), self.data.iloc[:, 1].max())

            quadrant = self.get_quadrant((x_pixel, y_pixel), (x, y))
            self.canvas.itemconfig(shape_id, fill=colors.get(quadrant, "black"))

    def get_quadrant(self, pos, origin):
        if pos[0] >= origin[0] and pos[1] >= origin[1]:
            return 1
        elif pos[0] < origin[0] and pos[1] >= origin[1]:
            return 2
        elif pos[0] < origin[0] and pos[1] < origin[1]:
            return 3
        elif pos[0] >= origin[0] and pos[1] < origin[1]:
            return 4
        return 0

    def find_neighbors(self, center_point, num_neighbors=5):
        distances = [
            (
                self.calculate_distance(center_point, (x_data, y_data)),
                (x_data, y_data),
            )
            for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes
        ]
        distances.sort()  # Sort by distance
        neighbors = [point[1] for point in distances[:num_neighbors]]
        return neighbors

    def calculate_distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def highlight_points(self, points):
        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            if (x_data, y_data) in points:
                self.canvas.itemconfig(shape_id, outline="red")

    def unhighlight_points(self):
        #itemconfig modifies items on canvas
        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            self.canvas.itemconfig(shape_id, outline="black")

    def reset_shape_colors(self):
        for shape_id, (x_data, y_data, category) in self.scatter_plot_shapes:
            self.canvas.itemconfig(shape_id, fill="blue")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScatterPlotApp(root)
    root.mainloop()
