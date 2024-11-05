import tkinter as tk
import math
import time

# Create the root window
root = tk.Tk()
root.title("Animated Fading Circle Canvas")

# Create a canvas widget
canvas_size = 500  # Width and height of the canvas
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()

# Circle parameters
radius = 100
center_x, center_y = canvas_size // 2, canvas_size // 2  # Center of the canvas
num_points = 360  # Number of points to draw the circle

# List to store the colors for fading effect
circle_color = ['#000000' for _ in range(num_points)]  # Start with black circles

# Function to draw the circle using sin and cos
def draw_circle():
    for angle in range(num_points):
        # Convert the angle to radians
        theta = math.radians(angle) * 10

        # Calculate x and y using parametric equations of a circle
        x = center_x + (radius + theta * 6) * math.cos(theta)
        y = center_y + (radius + theta * 6) * math.sin(theta)

        # Draw a small point (1x1 rectangle) using the current color
        canvas.create_rectangle(x, y, x + 1, y + 1, outline=circle_color[angle], fill=circle_color[angle])


# Function to fade colors gradually
def fade_circle():
    for i in range(num_points):
        # Extract the current color
        color = circle_color[i]

        # Convert hex color to RGB
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)

        # Increase brightness (towards white) to simulate fading
        red = min(red + 5, 255)
        green = min(green + 5, 255)
        blue = min(blue + 5, 255)

        # Update the color back to hex format
        circle_color[i] = f'#{red:02x}{green:02x}{blue:02x}'

# Continuous animation loop
def animate():
    while True:
        # Draw the circle
        draw_circle()

        # Update the canvas
        root.update()

        # Pause for a short time (speed of animation)
        time.sleep(0.01)

# Run the animation in a separate loop
root.after(0, animate)

# Run the Tkinter main loop
root.mainloop()
