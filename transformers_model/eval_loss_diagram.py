import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
"""
Helper script for displaying evaluation data for trained models.
"""

matplotlib.rcParams.update({'font.size': 12})

eval_losses = [1.4558498151018284e-05, 3.541656724337372e-06, 2.6403126867080573e-06, 2.8146262138761813e-06, 2.8165950425318442e-06, 2.656338438100647e-06, 2.6504342258704128e-06]
epochs = [0.47, 0.94, 1.42, 1.89, 2.36, 2.83, 3.00]

# Create a plot
plt.figure(figsize=(8, 5))
plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')
plt.title('Evaluation Loss per Epoch', fontsize=20)
plt.xlabel('Epoch', fontsize=18)
plt.ylabel('Loss', fontsize=18)
plt.xticks(epochs, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()


# # Use this instead if the values are very small like e-6.
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
#
# # Sample data: evaluation losses for each epoch
# eval_losses = [3.72330305253854e-07, 1.2795129578080378e-07, 5.801518909720471e-08, 3.973643103449831e-08,
#                3.973643103449831e-08]
# epochs = [0.67, 1.33, 2.00, 2.67, 3.00]
#
# # Create a plot
# plt.figure(figsize=(8, 5))
# plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')

# plt.title('Evaluation Loss per Epoch', fontsize=20)
# plt.xlabel('Epoch', fontsize=18)
# plt.ylabel('Loss', fontsize=18)
# plt.xticks(epochs, fontsize=12)
# plt.yticks(fontsize=12)
# plt.legend(fontsize=12)

# # Format y-axis to scientific notation
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
# plt.grid(True)
# plt.show()
