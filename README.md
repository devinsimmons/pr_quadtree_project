This code implements the PR-Quadtree data structure, which is useful for indexing spatial data. The data structure has 
defined boundaries and a capacity for each node. Points are inserted into the nodes, and once the capacity is exceeded,
the node decomposes into four children and its points are then reinserted into these new leaf nodes

It also includes a visualizer tool built on matplotlib

Below are some examples from the visualizer.
This quadtree has a capacity of 1 and a width of 10. Below is a visualization of the tree after points are inserted:
![Alt text](/before_delete.png)

Then, after the green and red points are deleted:
![Alt text](/after_delete.png)
