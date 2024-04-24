import matplotlib
matplotlib.use('TkAgg')  # Or use 'Qt5Agg', 'Agg', etc.
import matplotlib.pyplot as plt
"""
Helper script for displaying evaluation data for trained models.
"""

# Sample data: evaluation losses for each epoch
eval_losses = [0.73, 0.25, 0.16, 0.07, 0.08, 0.08, 0.08, 0.08]
epochs = [0.67, 1.33, 2.00, 2.67, 3.33, 4.00, 4.67, 5.00]

# Create a plot
plt.figure(figsize=(8, 5))  # Set the figure size
plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')
plt.title('Evaluation Loss per Epoch')  # Title of the plot
plt.xlabel('Epoch')  # X-axis label
plt.ylabel('Loss')  # Y-axis label
plt.xticks(epochs)  # Ensure we have a tick for each epoch
plt.legend()  # Add a legend
plt.grid(True)  # Turn on the grid lines
plt.show()  # Display the plot
