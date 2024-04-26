import matplotlib
matplotlib.use('TkAgg')  # Or use 'Qt5Agg', 'Agg', etc.
import matplotlib.pyplot as plt
"""
Helper script for displaying evaluation data for trained models.
"""

# Sample data: evaluation losses for each epoch
eval_losses = [3.72330305253854e-07, 1.2795129578080378e-07, 5.801518909720471e-08, 3.973643103449831e-08,
               3.973643103449831e-08]
epochs = [0.67, 1.33, 2.00, 2.67, 3.00]

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


# # KOMMENTERA IN DETTA ISTÄLLET OM MAN HAN PYTTESMÅ TAL ex e-7
# import matplotlib
# matplotlib.use('TkAgg')  # Or use 'Qt5Agg', 'Agg', etc.
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
#
# # Sample data: evaluation losses for each epoch
# eval_losses = [3.72330305253854e-07, 1.2795129578080378e-07, 5.801518909720471e-08, 3.973643103449831e-08,
#                3.973643103449831e-08]
# epochs = [0.67, 1.33, 2.00, 2.67, 3.00]
#
# # Create a plot
# plt.figure(figsize=(8, 5))  # Set the figure size
# plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')
# plt.title('Evaluation Loss per Epoch')  # Title of the plot
# plt.xlabel('Epoch')  # X-axis label
# plt.ylabel('Loss')  # Y-axis label
#
# # Format y-axis to scientific notation
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
#
# plt.xticks(epochs)  # Ensure we have a tick for each epoch
# plt.legend()  # Add a legend
# plt.grid(True)  # Turn on the grid lines
# plt.show()  # Display the plot
