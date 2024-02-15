import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.gridspec import GridSpec

# Load the dataset
with open('starwars-interactions/starwars-full-interactions-allCharacters.json') as f:
    data = json.load(f)

# Create a graph
G = nx.Graph()

# Add nodes
for node in data['nodes']:
    G.add_node(node['name'], value=node['value'], color=node['colour'])

# Add edges
for link in data['links']:
    source = data['nodes'][link['source']]['name']
    target = data['nodes'][link['target']]['name']
    G.add_edge(source, target, weight=link['value'])

# Choose a layout algorithm and adjust parameters
pos = nx.fruchterman_reingold_layout(G, k=0.5)  # Fruchterman-Reingold layout with increased k value

# Create the figure and GridSpec
fig = plt.figure(figsize=(15, 9))
gs = GridSpec(3, 1, figure=fig, height_ratios=[1, 0.2, 1])

# Create subplots
ax1 = fig.add_subplot(gs[0])
ax_hover = fig.add_subplot(gs[1])
ax2 = fig.add_subplot(gs[2])

# Draw the first graph on the first axis
nx.draw(G, pos, node_color=[node[1]['color'] for node in G.nodes(data=True)], node_size=300, with_labels=False, ax=ax1)

# Draw the same content on the second axis for testing purposes
nx.draw(G, pos, node_color=[node[1]['color'] for node in G.nodes(data=True)], node_size=300, with_labels=False, ax=ax2)

# Add hover effect in the middle axis
ax_hover.axis('off')

def on_hover(event):
    x, y = event.xdata, event.ydata
    text = '                                    '
    if x is not None and y is not None:
        for node, coords in pos.items():
            distance = ((coords[0] - x) ** 2 + (coords[1] - y) ** 2) ** 0.5
            if distance < 0.05:  # Adjust this threshold as needed
                text = node
                break

    ax_hover.clear()
    ax_hover.text(0.5, 0.5, text, bbox=dict(facecolor='white', alpha=0.7), ha='center', va='center')
    ax_hover.axis('off')  # Turn off ticks and values
    fig.canvas.draw_idle()

def on_click(event):
    if event.inaxes == ax1:
        x, y = event.xdata, event.ydata
        for node, coords in pos.items():
            distance = ((coords[0] - x) ** 2 + (coords[1] - y) ** 2) ** 0.5
            if distance < 0.05:  # Adjust this threshold as needed
                print("Clicked node:", node)
                break

fig.canvas.mpl_connect('motion_notify_event', on_hover)
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
