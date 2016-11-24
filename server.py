import avango
import avango.gua

###import application libraries
from lib.ViewingSetup import ViewingSetup
from lib.scene import create_scene

from utils import *

import argparse

# Map internal host names to their IP’s in the cluster
host_to_ip = {
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
    'perseus':  '141.54.147.54',
    'oelze':    '141.54.172.157',
    'apollo':   '141.54.172.230',
    #'teichel':  '141.54.172.25'
    'minos':    '141.54.147.49'
}

class Server:
    def __init__(self, SERVER_IP):
        self.scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
        physics = avango.gua.nodes.Physics()

        ## init server viewing setup
        self.serverViewingSetup = ViewingSetup(
            SCENEGRAPH = self.scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1200, 1200),
            SCREEN_DIMENSIONS = avango.gua.Vec2(10.0, 10.0),
            NAVIGATION_MATRIX = \
                avango.gua.make_trans_mat(0.0,10.0,0.0) * \
                avango.gua.make_rot_mat(90.0,-1,0,0),
            PROJECTION_MODE = avango.gua.ProjectionMode.ORTHOGRAPHIC,
            PHYSICS = physics
            )

        #physics
        
        physics_root = avango.gua.nodes.TransformNode(Name = "physica_root")
        self.scenegraph.Root.value.Children.value.append(physics_root)
        scene_root = avango.gua.nodes.TransformNode(Name = "scene_root")

        timer = avango.nodes.TimeSensor()

        #init scene
        scene_tuple = create_scene(
        	parent_node=scene_root, physics = physics, physics_root=physics_root, graph=self.scenegraph)

        skeleton = scene_tuple[-2]

        ## init distribution
        self.nettrans = avango.gua.nodes.NetTransform(Name = "nettrans", Groupname = "AVSERVER|{0}|7432".format(SERVER_IP))
        self.nettrans.Children.value.append(scene_root)
        self.scenegraph.Root.value.Children.value.append(self.nettrans)

        self.client_group = avango.gua.nodes.TransformNode(Name = "client_group")
        self.nettrans.Children.value.append(self.client_group)

        # Client 1
        # Oculus CV
        self.client_demeter = ClientSetup(
            PARENT_NODE = self.client_group,
            CLIENT_IP = host_to_ip['demeter'],
            KINECT_FILENAME = "kr/surface_23_24_25_26.ks"
        )


        # Client 2
        # 3D Monitor
        self.client_eris = ClientSetup(
            PARENT_NODE = self.client_group,
            CLIENT_IP = host_to_ip['eris']
        )


        # Client 3
        # LCD Wall
        self.client_athena = ClientSetup(
            PARENT_NODE = self.client_group,
            CLIENT_IP = host_to_ip['athena']
        )

        # Client 4
        # Oculus DK2
        self.client_pan = ClientSetup(
            PARENT_NODE = self.client_group,
            CLIENT_IP = host_to_ip['pan'],
            #KINECT_FILENAME = "kr/surface_50_51_52_54.ks"
        )

        # distribute complete scenegraph
        distribute_all_nodes_below(NETTRANS = self.nettrans, NODE = self.nettrans)

        # Start application/render loop
        self.serverViewingSetup.run(locals(), globals())

class ClientSetup:
    number_of_instances = 0

    color_list = [
        avango.gua.Color(1.0, 0.0, 0.0),
        avango.gua.Color(0.0, 1.0, 0.0),
        avango.gua.Color(0.0, 0.0, 1.0),
        avango.gua.Color(1.0, 1.0, 0.0),
        avango.gua.Color(0.0, 1.0, 1.0),
        avango.gua.Color(1.0, 0.0, 1.0)
    ]

    def __init__(self, PARENT_NODE = None, CLIENT_IP = None, KINECT_FILENAME = None):
        ## parameter quards
        if PARENT_NODE is None:
            print("ERROR: Parent node missing")
            quit()

        if CLIENT_IP is None:
            print("ERROR: Client IP missing")
            quit()

        self.id = ClientSetup.number_of_instances
        ClientSetup.number_of_instances += 1

        self.color = ClientSetup.color_list[self.id % len(ClientSetup.color_list)]

## Registers a scenegraph node and all of its children at a NetMatrixTransform node for distribution.
# @param NET_TRANS_NODE The NetMatrixTransform node on which all nodes should be marked distributable.
# @param PARENT_NODE The node that should be registered distributable with all of its children.
def distribute_all_nodes_below(NETTRANS = None, NODE = None):

    # do not distribute the nettrans node itself
    if NODE != NETTRANS:
        NETTRANS.distribute_object(NODE)

    # iterate over children and make them distributable
    for _child_node in NODE.Children.value:
        distribute_all_nodes_below(NETTRANS, _child_node)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'Start the server for a distributed Avango application.'
    parser.add_argument('server', choices=list(host_to_ip.keys()),
                        help='Hostname of the server')
    args = parser.parse_args()

    server = Server(SERVER_IP = host_to_ip[args.server])

    ## print the subgraph under a given node to the console
def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])

## print all fields of a fieldcontainer to the console
def print_fields(node, print_values = False):
  for i in range(node.get_num_fields()):
    field = node.get_field(i)
    print("→ {0} <{1}>".format(field._get_name(), field.__class__.__name__))
    if print_values:
      print("  with value '{0}'".format(field.value))
