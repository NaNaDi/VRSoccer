import avango
import avango.gua as agua

### helper tools ###

# print the subgraph under a given node to the console
def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])


# print all fields of a fieldcontainer to the console
def print_fields(node, print_values = False):
  for i in range(node.get_num_fields()):
    field = node.get_field(i)
    print("→ {0} <{1}>".format(field._get_name(), field.__class__.__name__))
    if print_values:
      print("  with value '{0}'".format(field.value))


def create_viewer(graph, window, physics = None):
    viewer = agua.nodes.Viewer()
    viewer.SceneGraphs.value = [graph]
    if physics is not None:
        viewer.Physics.value = physics
    viewer.Windows.value = [window]
    return viewer


# Map internal host names to their IP’s in the cluster
hosts = {
    'arachne':  '141.54.147.27',
    'artemis':  '141.54.147.28',
    'atalante': '141.54.147.29',
    'athena':   '141.54.147.30',
    'boreas':   '141.54.147.32',
    'charon':   '141.54.147.33',
    'eris':     '141.54.147.37',
    'hektor':   '141.54.147.43',
    'demeter':  '141.54.147.35',  # Oculus workstation 1
    'pan':      '141.54.147.52',  # Oculus workstation 2
    'perseus':  '141.54.147.64',
    'oelze':    '141.54.172.157',
    'apollo':   '141.54.172.230',
}
