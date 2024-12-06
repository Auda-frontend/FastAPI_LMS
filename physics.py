import matplotlib.pyplot as plt
import numpy as np

def hexagon(center, size=1, color='blue', edgecolor='black', label=None, alpha=0.5):
    """Draw a hexagon centered at a specific point."""
    x, y = center
    angles = np.linspace(0, 2 * np.pi, 7)
    x_hex = x + size * np.cos(angles)
    y_hex = y + size * np.sin(angles)
    plt.fill(x_hex, y_hex, color=color, edgecolor=edgecolor, alpha=alpha)
    if label is not None:
        plt.text(x, y, label, ha='center', va='center', fontsize=8, color='black')

def create_tessellation(rows, cols, size=1, freq_pattern=None):
    """Create a tessellated grid of hexagons."""
    grid = []
    dx = 3 * size / 2  # Horizontal distance between centers
    dy = np.sqrt(3) * size  # Vertical distance between centers
    for row in range(rows):
        for col in range(cols):
            x = col * dx
            y = row * dy
            if col % 2 == 1:
                y += dy / 2  # Offset odd columns
            freq = freq_pattern[(row * cols + col) % len(freq_pattern)]
            grid.append((x, y, freq))
    return grid

def plot_network(cells, selected_freq=None):
    """Plot the hexagonal cellular network and highlight reused frequencies."""
    for x, y, freq in cells:
        color = 'green' if freq == selected_freq else 'purple'
        alpha = 1.0 if freq == selected_freq else 0.6
        hexagon((x, y), size=1, color=color, label=f"{freq}", alpha=alpha)

# Parameters for the tessellation
rows = 5  # Number of rows of cells
cols = 6  # Number of columns of cells
freq_pattern = ['A', 'B', 'C', 'D']  # Frequency reuse pattern

# Create the tessellated grid
cells = create_tessellation(rows, cols, size=1, freq_pattern=freq_pattern)

# User selects a frequency to highlight
selected_freq = input("Enter the frequency to highlight (A, B, C, or D): ").strip().upper()

# Plot the network
plt.figure(figsize=(10, 10))
plot_network(cells, selected_freq)

# Add title and adjust the plot
plt.title("Hexagonal Cellular Network with Frequency Reuse", fontsize=14)
plt.axis('equal')
plt.axis('off')  # Turn off the axes for a clean look

# Display the plot
plt.show()