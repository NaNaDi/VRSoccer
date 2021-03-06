#!/usr/bin/python
import sys

import avango
import avango.script
import avango.gua as agua

from utils import *
from lib.scene import viveMonkey

from lib.OculusViewingSetup import OculusViewingSetup

# Map internal host names to their IP’s in the cluster
kinect_hosts = {
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
    'oelze':    '141.54.172.157',
    'apollo':   '141.54.172.230',
    'minos':    '141.54.147.49'
}

def main(SERVER_IP, CLIENT_IP):
    graph = agua.nodes.SceneGraph(Name="scenegraph")
    nettrans = agua.nodes.NetTransform(
        Name="nettrans",
        Groupname="AVCLIENT|{0}|7432".format(SERVER_IP))
    graph.Root.value.Children.value.append(nettrans)

    ## init viewer
    viewer = avango.gua.nodes.Viewer()
    viewer.SceneGraphs.value = [graph]

    # #                                                                  /!\
    _loader = avango.gua.nodes.TriMeshLoader()
    # Somehow necessary to initialize `_loader`
    dummy_geometry = _loader.create_geometry_from_file(
        "dummy", "data/objects/cube.obj",
        avango.gua.LoaderFlags.DEFAULTS
    )
    dummy_geometry.Transform.value = avango.gua.make_trans_mat(0.0, -0.105, 0.0) * \
                                          avango.gua.make_scale_mat(0.00000005, 0.00000001, 0.0000005)
    graph.Root.value.Children.value.append(dummy_geometry)
    '''
    # self.nettrans.Children.value.append(self.dummy_geometry)
    '''
    if CLIENT_IP == kinect_hosts['demeter']:
        viveMonkey()

    elif CLIENT_IP == kinect_hosts['pan']:
        # Oculus CV Setup
        viewingSetup = OculusViewingSetup(
            SCENEGRAPH = graph,
            BLACK_LIST = [],
        )
        #testMonkey = _loader.create_geometry_from_file("monkey", "data/objects/monkey.obj", avango.gua.LoaderFlags.DEFAULTS)
    elif CLIENT_IP == kinect_hosts['boreas']:
        # viewing setup
        size = agua.Vec2ui(1024, 768)
        window = agua.nodes.GlfwWindow(Size=size, LeftResolution=size)
        agua.register_window("window", window)
        cam = create_camera_with_res_passes(
            left_screen_path="/screen",
            scene_graph_name="scenegraph",
            resolution=size,
            output_window_name="window")
    
        #todo: fix light
        light = avango.gua.nodes.LightNode(
            Type=avango.gua.LightType.POINT,
            Name="light",
            Color=avango.gua.Color(1.0, 1.0, 1.0),
            Brightness=100.0,
            Transform=(avango.gua.make_trans_mat(0.25, 5.0, 5.0) *
                       avango.gua.make_scale_mat(100)))

        screen = create_screen(name="screen", children=[cam, light])

        graph.Root.value.Children.value.append(screen)
        viewer = create_viewer(graph=graph, window=window)



    # Triggers framewise evaluation of respective callback method
    init_trigger = avango.script.nodes.Update(Callback = init_callback, Active = True)


    while True:
        viewer.frame()

def create_camera_with_res_passes(
    #change camera position for Athena here
    left_screen_path,
    scene_graph_name,
    resolution,
    output_window_name):
    cam = agua.nodes.CameraNode(DisplayBoundingBox=True,
                                LeftScreenPath=left_screen_path,
                                SceneGraph=scene_graph_name,
                                Resolution=resolution,
                                OutputWindowName=output_window_name,
                                Transform=agua.make_trans_mat(0.25, 2.5, 5.0))

    res_pass = agua.nodes.ResolvePassDescription()
    res_pass.EnableSSAO.value = True
    res_pass.SSAOIntensity.value = 4.0
    res_pass.SSAOFalloff.value = 10.0
    res_pass.SSAORadius.value = 7.0

    res_pass.EnvironmentLightingColor.value = agua.Color(0.02, 0.02, 0.02)
    res_pass.ToneMappingMode.value = agua.ToneMappingMode.UNCHARTED
    res_pass.Exposure.value = 1.0
    res_pass.BackgroundColor.value = agua.Color(0.45, 0.5, 0.6)

    anti_aliasing = agua.nodes.SSAAPassDescription()

    pipeline_description = agua.nodes.PipelineDescription(Passes=[
        agua.nodes.TriMeshPassDescription(),
        agua.nodes.LightVisibilityPassDescription(),
        agua.nodes.BBoxPassDescription(),
        res_pass,
        anti_aliasing,
        agua.nodes.TexturedScreenSpaceQuadPassDescription()   
    ])

    cam.PipelineDescription.value = pipeline_description

    return cam


def create_screen(name, children):
    screen = agua.nodes.ScreenNode(
        Name=name,
        Width=2,
        Height=1.5,
        Transform=agua.make_trans_mat(0, 5.0, 10),
        Children=children)
    return screen

def init_callback():
        """
        Callback function
        """
        # print("frame", time.clock(), len(self.nettrans.Children.value))

        # Wait for distributed scenegraph to arrive
        if len(nettrans.Children.value) > 0:
            _client_group = nettrans.Children.value[0]
            if _client_group.Name.value == "client_group":
                # Identify the corresponding navigation node for this client
                for _node in _client_group.Children.value:
                    if _node.Name.value.count(self.client_ip) > 0:
                        viewingSetup.navigation_node.Transform.connect_from(_node.Transform)
                        scenegraph.Root.value.Children.value.remove(dummy_geometry)

                        break  # break smallest enclosing loop

            print_graph(nettrans)

            init_trigger.Active.value = False # disable init callback


if __name__ == '__main__':
    server_ip = kinect_hosts[sys.argv[1]]
    client_ip = kinect_hosts[sys.argv[2]]
    main(server_ip, client_ip)
