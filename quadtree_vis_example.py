import pr_quadtree as pr
import matplotlib.pyplot as plt

tree = pr.quadtree_root(10, (0, 0), 1)

tree.pr.insert_point('a', (1, 4))
tree.pr.insert_point('b', (2, 3))
tree.pr.insert_point('c', (6, 1))
tree.pr.insert_point('d', (2, 8))
tree.pr.insert_point('e', (3, 6))
tree.pr.insert_point('f', (0.2, 4))

tree.pr.make_plot()
plt.savefig('before_delete.png', dpi = 350)
plt.show()


tree.pr.delete((1, 4))
tree.pr.delete((0.2, 4))
tree.make_plot()
plt.savefig('after_delete.png', dpi = 350)
plt.show()
