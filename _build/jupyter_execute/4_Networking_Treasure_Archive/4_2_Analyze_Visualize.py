#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'inline')
from IPython.display import display, clear_output, Javascript
import numpy as np
from ipywidgets import interact, Layout
import ipywidgets as widgets
import itertools
import pandas as pd
import networkx.algorithms.community as nxcom
from pylab import *
import hvplot.networkx as hvnx
from bokeh.models import HoverTool
import decorator


# For this code to run properly it is imporatnt to have a version of decorator 5.0.7 or higher. If the version on your computer turns out to be lower, run
# ```bash
# !pip install decorator==5.0.9
# ```
# or upgrade decorator with the commands discussed in Chapter 1.

# In[2]:


decorator.__version__


#  Load the graph that was pickled in the previous notebook

# In[3]:


with open('pickle/treasury.p', 'rb') as p: 
    G = pickle.load(p)
file = 'csv/treasury_shoes2.txt'
tr_df = pd.read_csv(file, encoding='utf8')
ids = list(tr_df['id_text'])
ids.sort()


# # Visualization Functions
# This function helps to find the proportional size of the node, given a particular property (for instance degree). 

# In[4]:


def node_size_calculator(graph, property_name, minSize, maxSize):
    '''Given the graph, the property_name which we will use as a size reference, 
     and the minSze and maxSize, calculate the relative size of the nodes.
     Code by Colman Bouton.'''
    node_data = graph.nodes.data(data=property_name)
    data_max = max([v for k,v in node_data])
    data_min = min([v for k,v in node_data])
    return {k: int(minSize + v/(data_max-data_min)*(maxSize-minSize)) 
          for k,v in node_data}


# In order to visualize the graph we will use a spring layout. In a spring layout (also called Fruchterman-Reingold layout) the edges function as springs that draw the nodes together; the strength of the spring (`draw_weight`) often depends on the weight of the edge, but may also be calculated differently. The nodes themselves repel each other; the replling force is often by the degree. The spring layout may result in a slightly different visualization each time it is run, but the general relationships of nodes and edges will be approximately the same.
# 
# There are several things that are key to creating good positioning for a graph visualization using the spring layout. First, we must use an undirected version of the graph for spring calculations. Otherwise, nodes that have a single directed edge leading into them will not be attracted to any other node and simply fly off.
# 
# Additionally, unless the user specifies otherwise, we use the degree of the two nodes of an edge to weaken the strength of the spring. Generally, since degree represents the number of visual features around a node, this will produce the best visualisation.
# 
# A further consideration to be had is that if the graph is not connected, its components will fly away from each other without bound. Therefore, it is essential for any graph you might be drawing with spring_layout that it is connected. We will be addressing this issue in our own graph at a later step.

# In[5]:


def spring_position_calculator(graph, weight_property_name = None, 
                               spring_seed = None):
    """Function by Colman Bouton"""
    gcopy = graph.to_undirected()

    if weight_property_name == None:
        weight_property_name = 'degree'
        for node in gcopy.nodes:
            gcopy.nodes[node]['degree'] = gcopy.degree[node]
  
    avg_weight = np.median([v for k,v in gcopy.nodes().data(data = weight_property_name)]) #used for draw weight calculation
    overall_reduce = 1 / gcopy.number_of_nodes()**0.5
    for edge in gcopy.edges:
    #calculate draw_weight for each edge
        gcopy[edge[0]][edge[1]]['draw_weight'] = overall_reduce * avg_weight * gcopy[edge[0]][edge[1]]['weight'] / (min(gcopy.nodes[edge[0]][weight_property_name], 
                                                                                                                        gcopy.nodes[edge[1]][weight_property_name]) + 0.01 * avg_weight)
  
    pos = nx.spring_layout(gcopy, weight = 'draw_weight', 
                         iterations = 500, seed=spring_seed)
    return pos


# Now we can put all this to together and create a function that draws a pretty graph! We will default to using a spring graph, as well as taking in some arguments that will allow us to parameterize the size of the nodes and input which metric we will use to color code the nodes with.

# In[6]:


def draw_pretty_graph(graph, minSize, maxSize,
                            size_attr_name, figure, color_attr_name = 'degree',
                            spacing_attr_name = None, label_name = None, pos = None, 
                            label_cutoff = 1, spring_seed = None, Ego=None):
    '''Draw a pretty graph using the graph argument and resize the nodes using the
     minSize and maxSize arguments, while coloring the nodes by a determined metric.
     The argument Ego may be used to specifically label a particular node. Function
     adapted from a function by Colman Bouton.'''
  
  # first, we use our previously defined function to create a dict for the sizes
    node_sizes = node_size_calculator(graph, size_attr_name, minSize, maxSize)

  # then we create the list of values for our colormap
    color_values = list(nx.get_node_attributes(graph, color_attr_name).values())
    v_min = min(color_values)
    v_max = max(color_values)

  # if positions are not specified, calculate them using the previous function
    if pos == None:
        pos = spring_position_calculator(graph, spacing_attr_name)

    # we now position the labels:
    label_pos = {}
    num_labels = int(G.number_of_nodes() * label_cutoff) # calculate number of labels to show
    for node in sorted(node_sizes, key = node_sizes.get, reverse=True)[0:num_labels]:
      # set the label position to be slightly offset from the node position
        label_pos[node] = [pos[node][0], pos[node][1] + 0.03]
    if Ego:
        label_pos[Ego] = [pos[Ego][0], pos[Ego][1] + 0.03]

  # draw nodes and edges
    nx.draw_networkx_nodes(        
          graph,
          pos,
          node_size = [node_sizes[node] for node in graph],
          node_color= color_values,
          alpha = 1,
          cmap= plt.cm.plasma, 
          vmax = v_max,
          vmin = v_min,
          )
    nx.draw_networkx_edges(        
          graph,
          pos,
          node_size = [node_sizes[node] for node in graph],
          alpha = 0.5,
          edge_color = 'brown',
          width = 2,
          connectionstyle="arc3,rad=0.1"
          )
  
  # draw labels if provided
    if label_name == None:  # this the default option: use the node indexes
        labels = {k : k for k in label_pos}
    elif label_name != False: #if label_name is False, dont't draw labels
        labels = {k:graph.nodes.data(data = label_name)[k] for k in label_pos}
    if label_name != False:
        nx.draw_networkx_labels(graph, label_pos, labels = labels, 
                            font_size = 14, font_weight = 'bold', 
                            font_color = 'black')
    
  # draw the colorbar
    norm = mpl.colors.Normalize(vmin = v_min, vmax = v_max)
    options = {'label' : color_attr_name}
    figure.colorbar(mpl.cm.ScalarMappable(norm, plt.cm.plasma), **options)


# # Visualizing the Graph
# Generally speaking, we found setting the edges to be transparent made the graph easier to read, and that making the graph sufficiently large helped us see the individual nodes.
# 
# We also chose to color code the nodes based on an assignable metric, which we defaulted to node degree. This makes it easier to discern which nodes are more important. We added a colorbar as a legend for the metric.
# 
# In spring graphs, the nodes are set to pull apart from each other and the edges act as springs pulling the nodes together. When the positions are being calculated, the repellant forces and the attractant forces through the springs are added up over a series of iterations until the graph settles into a particular set of positions. In some cases, when there is a large set of data, you might see the nodes clump together, making the nodes difficult to interpret individually.
# 
# Here we take the largest connected subgraph and use the `draw_pretty_graph` helper function to draw our network using a spring graph. 
# 
# Most of the nodes in our graph are pretty small, meaning they have a pretty low degree, but we see some interesting main actors. These nodes end up at the center of our graph because they are fairly well connected and thus are only pulled apart by less connected nodes.
# 
# By Colman Bouton

# In[7]:


# remove nodes which have no connections to other nodes in the graph
mainc = max(nx.algorithms.components.connected_components(G.to_undirected()), 
            key = len)
I = G.subgraph(mainc).copy()
#degreelog = {name : np.log(I.degree[name]) for name in I.nodes}
#nx.set_node_attributes(I, degreelog, "degreelog")

# draw the graph using draw_pretty_graph helper function

fig = plt.figure(figsize=(25, 15))
draw_pretty_graph(I, 1, 1000, "degree", fig,
                  color_attr_name = 'eigenvector_centrality',
                  label_name = None, label_cutoff = 0.03, spring_seed=1);
plt.title('Puzriš-Dagan Treasure Archive');


# # Interactive Version of the Visualization
# Using the same `spring_position_calculator()` and `node_size_calculator()` functions as above, we may create essentially the same graph as an interactive visualization, using [hvPlot](https://hvplot.holoviz.org). HvPlot is built on top of [HolowViews](https://holoviews.org/index.html) and [Bokeh](https://docs.bokeh.org/en/latest/index.html) and offers interactive plotting for a number of important Python libraries, such as Pandas and NetworkX). The visualization comes standard with a number of tools, including Pan, Zoom and Reset and a Hover function, that displays the attributes of a node when hovering over it with the mouse. Clicking on a node will highlight the node and all of its edges, while graying all the other elements of the graph.

# In[8]:


mainc = max(nx.algorithms.components.connected_components(G.to_undirected()), 
            key = len)
K = G.subgraph(mainc).copy()   # create new version
pos = spring_position_calculator(K)
node_sizes = node_size_calculator(K, "degree", 5, 1000)
node_size_list = list(node_sizes.values())
number_of_names_to_display = 10
add_labels = sorted(node_sizes, key=node_sizes.get, reverse=True)[:number_of_names_to_display]
label_dict = {name : name if name in add_labels else "" for name in K.nodes}


# In[9]:


hvnx.draw(I,
         pos,
         height=800,
         width=800,
         node_size = node_size_list, 
         arrowhead_length=0.01,
         with_labels=True,
         labels=label_dict,
         edge_width='weight',
         edge_alpha= 0.7,
         edge_color='brown',
         node_color='eigenvector_centrality',
         node_cmap=plt.cm.plasma,
         )


# # Cliques
# Cliques are sets of nodes that are all connected to each other. That is, if we have four nodes, A, B, C, and D, all possible connections exist: 
# > A --- B</br>
# > A --- C</br>
# > A --- D</br>
# > B --- C</br>
# > B --- D</br>
# > C --- D</br>
# 
# Cliques may represent powerful centers in a graph, with  information flowing freely within each clique. Cliques are defined only for undirected graphs, so we first have to transform our graph. In order to compute cliques we need to decide the minimum number of nodes - in this case 4. 
# 
# A related concept is the k-clique community. A k-clique community consists of adjacent cliques of at least *k* members. Adjacent cliques share at least *k-1* nodes. As we will see, k-clique communities tend to overlap. That is, there are powerful actors who belong to multiple such communities and connect them to each other.
# 
# The code below is adapted from the blog post [Community Detection Using NetworkX](https://orbifold.net/default/community-detection-using-networkx/) by Francois Vanderseypen.

# **The following code needs more documentation.**
# 
# The output of k_clique_communities() is a list of frozen sets. The clique communities are sorted from largest to smallest.

# In[10]:


H = nx.DiGraph.to_undirected(G)
k_clique_com = sorted(nxcom.k_clique_communities(H, 4), key=len, reverse=True)
# Count the communities
N = len(k_clique_com)
for ind, names in enumerate(k_clique_com):
    print(f"Clique {str(ind+1)}: {list(names)}")


# Each node in the graph receives an attribute called `cliques`. The default is `{0}` (a set). In iterating through the nodes in the clique communities, the attribute `cliques` is updated so that all nodes that belong to the first k-clique community now have the attribute `cliques = {1}` (again, a set), etc. Nodes that belong to more than one clique community will have more than one clique number in the `cliques` attribute (for instance `{1, 3}`). Nodes that are not found in any clique community will keep the default value `{0}`. We will use this attribute below to color nodes and to mark internal edges (edges between nodes that belong to the same clique).

# In[11]:


nx.set_node_attributes(H, {0}, "cliques") # set {0} as default
for c, v_c in enumerate(k_clique_com):
    for v in v_c:
        if min(H.nodes[v]['cliques']) > 0:  # node is already in a clique
            H.nodes[v]['cliques'].add(c+1) # add clique no. to the set
        else:
            H.nodes[v]['cliques'] = {c+1}
        # Add 1 to save 0 for nodes that are not in a clique


# Set edge attributes with a similar method. The edge attribute `clique` defaults to zero. Edges between two nodes that belong to the same clique (internal edges) receive the value of that clique. This is done by finding the intersection of the `cliques` attributes of the two nodes. If that intersection is empty (the two nodes do not share membership of a clique community) the value remains 0. If the `cliques` attributes of two nodes do intersect (that is, they share membership of at least one k-clique community), the value of the edge attribute becomes the lowest value in the intersection.

# In[12]:


nx.set_edge_attributes(H, 0, "clique")  # default is 0
for v, w, in H.edges:
    c = H.nodes[v]['cliques'].intersection(H.nodes[w]['cliques']) # do the two nodes share a community?
    if c:
        # Internal edge, mark with community
        H.edges[v, w]['clique'] = min(c)


# The node attribute 'cliques' is a set, which is not allowed when displaying the graph in Bokeh. We do not need the sets anymore - if a node belongs to more than one clique the attribute will be N+1 (the number of cliques + 1), otherwise, the attribute is the lowest (and single) number in the set.

# In[13]:


for node in H.nodes:
    if len(H.nodes[node]['cliques']) > 1:
        H.nodes[node]['cliques'] = N+1
    else:
        H.nodes[node]['cliques'] = min(H.nodes[node]['cliques'])


# Select nodes to display. Nodes that belong to a k-clique community and nodes that have a degree greater than 8 are admitted. Nodes that belong to one or more k-clique communities have a value in the attribute `cliques` that is higher than 0.

# In[14]:


nodes = [x for x, y in H.nodes(data=True) if y["cliques"] > 0 or y["degree"] > 8] # select nodes
K = H.subgraph(nodes)


# For the color scheme we use a function for creating a discrete colormap, made available by Jake VanderPlas on his github account. The [tool](https://gist.github.com/jakevdp/91077b0cae40f8f8244a) is slightly adapted for the present purposes.

# In[15]:


def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map
    https://gist.github.com/jakevdp/91077b0cae40f8f8244a
    by Jake VanderPlas"""
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    color_list[0] = [0, 0, 0, 1] # = black
    color_list = [matplotlib.colors.rgb2hex(col) for col in color_list]
    return color_list


# In[16]:


colmap = discrete_cmap(N+2, "plasma")


# Use the resulting colormap to assign node colors and edge colors of our subgraph.

# In[17]:


pos2 = spring_position_calculator(K, "eigenvector_centrality")
node_sizes2 = node_size_calculator(K, "eigenvector_centrality", 5, 30)
number_of_names_to_display = 20
add_labels = sorted(node_sizes, key=node_sizes.get, reverse=True)[:number_of_names_to_display]
labels = [n if n in add_labels else '' for n in K.nodes]
category = [n.split(']')[1] for n in K.nodes]


# In[18]:


from bokeh.io import output_file, show
from bokeh.models import (Circle, HoverTool,
                          MultiLine, NodesAndLinkedEdges, TapTool,
                         GraphRenderer, LabelSet, ColumnDataSource)
from bokeh.plotting import figure, output_notebook, from_networkx
output_notebook()


# Part of the code below is inspired by [Introduction to Cultural Analytics and Python](https://melaniewalsh.github.io/Intro-Cultural-Analytics/Network-Analysis/Making-Network-Viz-with-Bokeh.html) (Chapter 6: Network Analysis) by Melanie Walsh (2021).

# In[19]:


# initiate the plot
plot2 = figure(width=1000, height = 600)
plot2.title.text = "Treasure Archive Drehem: Cliques"
plot2.grid.visible=False
plot2.xaxis.visible = False  
plot2.yaxis.visible = False  

# add tools
node_hover_tool = HoverTool(tooltips=[("name", "@index"), ("eigenvector centrality", "@eigenvector_centrality"), ("degree", '@degree')])
plot2.add_tools(node_hover_tool, TapTool())

# add the graph 
graph = from_networkx(K, pos2)

# add node renderers to the graph
graph.node_renderer.data_source.data['node_size'] = list(node_sizes2.values())
graph.node_renderer.data_source.data['node_color'] = [colmap[clique] for clique in graph.node_renderer.data_source.data['cliques']]
graph.node_renderer.glyph = Circle(fill_color = 'node_color',size = 'node_size', fill_alpha=.75)
graph.node_renderer.hover_glyph = Circle(size='node_size', fill_color='node_color')
graph.node_renderer.selection_glyph = Circle(size='node_size', fill_color='node_color')

# add the edge renderers to the graph
graph.edge_renderer.glyph = MultiLine(line_alpha=.5, line_width='weight')  
graph.edge_renderer.data_source.data['edge_color'] = [colmap[clique] for clique in graph.edge_renderer.data_source.data['clique']]
graph.edge_renderer.hover_glyph = MultiLine(line_color='edge_color', line_width='weight')
graph.edge_renderer.selection_glyph = MultiLine(line_color='edge_color', line_width='weight')

# add inspect/selection policy (hovering and clicking) to the graph
graph.inspection_policy = NodesAndLinkedEdges()
graph.selection_policy = NodesAndLinkedEdges()

# add graph to the plot
plot2.renderers.append(graph)

# add labels
x, y = zip(*pos2.values())
source2 = ColumnDataSource({'x': x, 'y': y, 'label': labels})
labelset2 = LabelSet(x='x', y='y', text='label', source=source2, background_fill_color='white', text_font_size='12px', background_fill_alpha=.7)
plot2.renderers.append(labelset2)

# add legend
clique_labels = {n : f"clique {str(n)}" for n in range(N+1)}
clique_labels[0] = "no clique"
clique_labels[N+1] = "multiple cliques"
legend_labels = [clique_labels[n[1]] for n in K.nodes(data="cliques")]
graph.node_renderer.data_source.data['legend_labels'] = legend_labels
plot2.circle(
    source = graph.node_renderer.data_source.data,
    legend_group="legend_labels",
    fill_color="node_color",
    size=80,
    )
plot2.legend.location = "center"
plot2.add_layout(plot2.legend[0], 'left')
show(plot2)


# In[ ]:




