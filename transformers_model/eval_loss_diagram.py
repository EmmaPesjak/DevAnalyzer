import matplotlib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.use('TkAgg')
"""
Helper script for displaying evaluation data for trained models.
"""

matplotlib.rcParams.update({'font.size': 12})

# eval_losses = [1.4558498151018284e-05, 3.541656724337372e-06, 2.6403126867080573e-06, 2.8146262138761813e-06,
#                2.8165950425318442e-06, 2.656338438100647e-06, 2.6504342258704128e-06]

epochs = [0.47, 0.94, 1.42, 1.89, 2.36, 2.83, 3.00]

# # 0
# eval_losses = [0.5886886715888977, 0.31592312455177307, 0.23720403015613556, 0.19622649252414703,
#                0.16727674007415771, 0.1592748910188675, 0.15706244111061096]

# # 1
# eval_losses = [0.08212236315011978, 0.058618608862161636, 0.03900374099612236, 0.0380522795021534,
#                0.03040939010679722, 0.023363716900348663, 0.02355825901031494]
#
# # 2
# eval_losses = [0.002106106374412775, 0.013125240802764893, 0.013916535302996635, 0.004383038263767958,
#                0.03519832715392113, 0.0013968938728794456, 0.00141288957092911]
#
# # 3
# eval_losses = [0.00026503377011977136, 0.0004852231068070978, 0.0009189813281409442, 0.000742386793717742,
#                0.0003100765752606094, 0.00019629468442872167, 0.00019702287681866437]
#
# # 4
# eval_losses = [0.001464273314923048, 0.07157374173402786, 0.007442273199558258, 4.882318899035454e-05,
#                0.0001414348225807771, 5.0113423640141264e-05, 4.565097697195597e-05]
#
# # 5
# eval_losses = [2.2745560272596776e-05, 0.0011987891048192978, 1.826021798478905e-05, 1.6695928934495896e-05,
#                1.5824105503270403e-05, 1.5947813153616153e-05, 1.5853069271543063e-05]
#
# # 6
# eval_losses = [7.716747859376483e-06, 9.546989531372674e-06, 1.4912218830431812e-05, 1.1971560525125824e-05,
#                9.679688446340151e-06, 9.326851795776747e-06, 9.322634468844626e-06]
#
# # 7
# eval_losses = [2.97459382636589e-06, 3.012274419234018e-06, 4.461337084649131e-06, 4.4301286834524944e-06,
#                3.5962323181593092e-06, 3.397176215003128e-06, 3.380869202374015e-06]
#
# # 8
# eval_losses = [0.022580239921808243, 1.5626517324562883e-06, 1.0439239304105286e-06, 7.928538252599537e-07,
#                7.695181807321205e-07, 7.495562499570951e-07, 7.478693078155629e-07]
#
# # 9
# eval_losses = [3.0083467095209926e-07, 1.8612388430483406e-07, 1.5885196091858234e-07, 1.2736273902191897e-07,
#                1.1077464989739383e-07, 9.306194925784439e-08, 9.2218492397933e-08]
#
# # 10
# eval_losses = [4.948309850760779e-08, 3.205154897045759e-08, 8.11409734069457e-07, 5.805827072435932e-07,
#                3.4328894571444835e-07, 5.596044047706528e-06, 5.624158347927732e-06]
#
# # 11
# eval_losses = [3.4980332657141844e-06, 1.194338778987003e-06, 8.566745464122505e-07, 8.684833119332325e-07,
#                7.253764806591789e-07, 6.919191264387337e-07, 6.893887416481448e-07]
#
# 12
eval_losses = [5.623078447314356e-09, 2.5303856787672885e-09, 1.4057698338731939e-09, 0.0,
               0.0, 0.0, 0.0]
#
# # 13
# eval_losses = [0.0, 0.0, 2.8115396122352365e-10, 0.0,
#                0.0, 0.0, 0.0]
#
# # 14
# eval_losses = [0.0, 0.0, 0.0, 0.02527116984128952,
#                0.0, 0.0, 0.0]

# # Create a plot
# plt.figure(figsize=(8, 5))
# plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')
# plt.title('Evaluation Loss per Epoch', fontsize=20)
# plt.xlabel('Epoch', fontsize=18)
# plt.ylabel('Loss', fontsize=18)
# plt.xticks(epochs, fontsize=12)
# plt.yticks(fontsize=12)
# plt.legend(fontsize=12)
# plt.grid(True)
# plt.show()


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

# Create a plot
plt.figure(figsize=(8, 5))
plt.plot(epochs, eval_losses, marker='o', linestyle='-', color='b', label='Evaluation Loss')

plt.title('Evaluation Loss per Epoch', fontsize=20)
plt.xlabel('Epoch', fontsize=18)
plt.ylabel('Loss', fontsize=18)
plt.xticks(epochs, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)

# Format y-axis to scientific notation
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
plt.grid(True)
plt.show()
