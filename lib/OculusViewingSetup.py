#!/usr/bin/python
# -*- coding: utf-8 -*-

### import guacamole libraries
import avango
import avango.gua
import avango.oculus

### import application libraries
from lib.GuaVE import GuaVE
#from lib.FPSGui import FPSGui


### import python libraries
import time


## print all fields of a fieldcontainer to the console
def print_fields(node, print_values = False):
    for i in range(node.get_num_fields()):
        field = node.get_field(i)
        print("-> {0} <{1}>".format(field._get_name(), field.__class__.__name__))
        if print_values:
            print("  with value '{0}'".format(field.value))


class OculusViewingSetup:

    ### constructor
    def __init__(self,
        SCENEGRAPH = None,
        BLACK_LIST = [],
        #PHYSICS = None,
        NAVIGATION_TRANSFORM = None
        ):

        ## parameter quards
        if SCENEGRAPH is None:
            print("ERROR: scengraph instance missing")
            quit()

        # if PHYSICS is None:
        #     print("ERROR: OculusViewingSetup is missing physics.")
        #     quit()

        ### parameters ###
        self.printout_intervall = 1.0 # in seconds


        ### variables ###
        self.sav_time = time.clock()

        ### resources ###

        self.shell = GuaVE()

        ## init window
        self.window = avango.oculus.nodes.OculusWindow()

        #notice, that the oculus screen transforms and translations are automatically
        #computed by the oculus. do not try to enter them yourself, or you will
        #most likely get a wrong result due to influence of the lenses

        #accessible fields:
        #    SensorOrientation ##head pose (rotation and translation)
        #    Resolution ##window resolution
        #    EyeResolution ##recommended eye resolution (behaves strange so far)
        #    LeftScreenSize  ## size of left screen in meters
        #    RightScreenSize ## size of right screen in meters
        #    LeftScreenTranslation  ## translation of left screen in meters
        #    RightScreenTranslation ## translation of right screen in meters
        #    EyeDistance ## distance between both eyes in meters. for SDKs < v0.6, this is fixed to 0.064

        # start the window in fullscreen and with the oculus window as primary display in order to fit the
        # window nicely on the HMD

        self.window.Size.value = self.window.Resolution.value
        self.window.EnableVsync.value = False
        self.window.EnableFullscreen.value = False

        avango.gua.register_window(self.window.Title.value, self.window)


        ## init navigation node
        self.navigation_node = avango.gua.nodes.TransformNode(Name = "navigation_node")
        SCENEGRAPH.Root.value.Children.value.append(self.navigation_node)

        ## init head node
        self.head_node = avango.gua.nodes.TransformNode(Name = "head_node")
        self.navigation_node.Children.value.append(self.head_node)
        # connect orientation/position data from oculus sensor

        # This little bugger resets any transformations we do                                    /!\
        self.head_node.Transform.connect_from(self.window.SensorOrientation)



        ## init screen nodes
        self.left_screen_node = avango.gua.nodes.ScreenNode(
            Name="left_screen_node",
            Width=self.window.LeftScreenSize.value.x,
            Height=self.window.LeftScreenSize.value.y,
            Transform=avango.gua.make_trans_mat(self.window.LeftScreenTranslation.value)
            )
        self.head_node.Children.value.append(self.left_screen_node)

        self.right_screen_node = avango.gua.nodes.ScreenNode(
            Name="right_screen_node",
            Width=self.window.RightScreenSize.value.x,
            Height=self.window.RightScreenSize.value.y,
            Transform=avango.gua.make_trans_mat(self.window.RightScreenTranslation.value)
            )
        self.head_node.Children.value.append(self.right_screen_node)


        ## init camera node
        self.camera_node = avango.gua.nodes.CameraNode(
            Name="camera_node",
            LeftScreenPath=self.left_screen_node.Path.value,
            RightScreenPath=self.right_screen_node.Path.value,
            SceneGraph=SCENEGRAPH.Name.value,
            Resolution=self.window.Resolution.value,
            OutputWindowName=self.window.Title.value,
            EyeDistance=self.window.EyeDistance.value,
            EnableStereo=True,
            BlackList = BLACK_LIST,
            )
        self.head_node.Children.value.append(self.camera_node)


        ## init viewer
        self.viewer = avango.gua.nodes.Viewer()
        self.viewer.SceneGraphs.value = [SCENEGRAPH]
        self.viewer.Windows.value = [self.window]
        self.viewer.DesiredFPS.value = 200.0 # in Hz
        #self.viewer.Physics.value = PHYSICS


        ## init passes & render pipeline description
        self.resolve_pass = avango.gua.nodes.ResolvePassDescription()
        self.resolve_pass.EnableSSAO.value = False
        self.resolve_pass.SSAOIntensity.value = 3.0
        self.resolve_pass.SSAOFalloff.value = 10.0
        self.resolve_pass.SSAORadius.value = 2.0
        #self.resolve_pass.EnableScreenSpaceShadow.value = True
        self.resolve_pass.EnvironmentLightingColor.value = avango.gua.Color(0.2, 0.2, 0.2)
        self.resolve_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
        self.resolve_pass.Exposure.value = 1.0

        self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.COLOR
        self.resolve_pass.BackgroundColor.value = avango.gua.Color(0.45, 0.5, 0.6)
        # self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
        # self.resolve_pass.BackgroundTexture.value = "data/textures/DH216SN.png"
        #self.resolve_pass.BackgroundTexture.value = "/opt/guacamole/resources/skymaps/DH216SN.png"
        #self.resolve_pass.BackgroundTexture.value = "/opt/guacamole/resources/skymaps/warehouse.jpg"

        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes = [])
        self.pipeline_description.EnableABuffer.value = False
        self.pipeline_description.Passes.value.append(avango.gua.nodes.TriMeshPassDescription())
        #self.pipeline_description.Passes.value.append(avango.gua.nodes.TexturedQuadPassDescription())
        self.pipeline_description.Passes.value.append(avango.gua.nodes.Video3DPassDescription())
        self.pipeline_description.Passes.value.append(avango.gua.nodes.LightVisibilityPassDescription())
        #self.pipeline_description.Passes.value.append(avango.gua.nodes.BBoxPassDescription())
        self.pipeline_description.Passes.value.append(self.resolve_pass)
        self.pipeline_description.Passes.value.append(avango.gua.nodes.TexturedScreenSpaceQuadPassDescription())
        self.pipeline_description.Passes.value.append(avango.gua.nodes.SSAAPassDescription())
        # self.pipeline_description.EnableABuffer.value = True # enable transparency support

        self.camera_node.PipelineDescription.value = self.pipeline_description


        # Triggers framewise evaluation of respective callback method
        self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)


    ### functions ###
    def set_eye_distance(self, FLOAT):
        self.camera_node.EyeDistance.value = FLOAT


    def run(self, LOCALS, GLOBALS):
        self.shell.start(LOCALS, GLOBALS)
        self.viewer.run()


    def list_variabels(self):
        self.shell.list_variables()


    def get_head_position(self): # get relative head position (towards screen)
        return self.head_node.Transform.value.get_translate()


    ### callback functions ###
    def frame_callback(self):
        if time.clock() - self.sav_time > self.printout_intervall:
            self.sav_time = time.clock()

            # print("FPS", self.viewer.ApplicationFPS.value, self.window.RenderingFPS.value)
            # print("POS", self.get_head_position())
