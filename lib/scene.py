import avango
import avango.gua

from lib.physics import create_physics_graph
from lib.skeleton import HumanSkeleton
from lib.BallSpawner import BallSpawner

def create_scene(parent_node, physics, physics_root, graph):
    loader = avango.gua.nodes.TriMeshLoader()

    light = avango.gua.nodes.LightNode(
            Name="sun_light",
            Type=avango.gua.LightType.SUN,
            Color=avango.gua.Color(1.0, 1.0, 0.7),
            EnableShadows=True,
            ShadowMapSize=1024,
            ShadowOffset=0.0005,
            ShadowCascadedSplits=[0.1, 4, 7, 20],
            ShadowMaxDistance=30,
            ShadowNearClippingInSunDirection=100,
            ShadowFarClippingInSunDirection=100,
            Brightness=3,
            Transform=avango.gua.make_rot_mat(50, 0, 1, 0) *
            avango.gua.make_rot_mat(-40.0, 1.0, 0.0, 0.0))
    parent_node.Children.value.append(light)

    physics_dict = create_physics_graph(physics, physics_root)

    # create ball
    ball = loader.create_geometry_from_file("sphere_geometry", "data/objects/sphere.obj")
    ball_node = avango.gua.nodes.TransformNode()
    ball_node.Children.value.append(ball)
    ball_parent = avango.gua.nodes.TransformNode()
    ball_parent.Transform.value = avango.gua.make_scale_mat(0.5)
    ball_parent.Children.value.append(ball_node)
    #ball.Transform.value = avango.gua.make_trans_mat(30.0,0,0)*avango.gua.make_scale_mat(0.25)
    parent_node.Children.value.append(ball_parent)

    ##load goal geometry
    goal_group = loader.create_geometry_from_file("goal_geometry", "data/arrrscene/objects/arrrscene.obj", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)# | avango.gua.LoaderFlags.MAKE_PICKABLE)
    goal_group.Transform.value = avango.gua.make_scale_mat(0.95) * avango.gua.make_trans_mat(-0.5,-0.85,1)
    parent_node.Children.value.append(goal_group)
    for _node in goal_group.Children.value:
        _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
        _node.Material.value.EnableBackfaceCulling.value = False

    ##skybox
    #sky = loader.create_geometry_from_file("skybox", "data/objects/cube.obj")
    #sky.Material.value.set_uniform("ColorMap", "data/textures/skymap.jpg")
    #sky_node = avango.gua.nodes.TransformNode()
    #sky_node.Transform.value = avango.gua.make_scale_mat(30)
    #sky_node.Children.value.append(sky)
    #parent_node.Children.value.append(sky_node)


    timer = avango.nodes.TimeSensor()
    #connect_ball = connect_transform_node_to_transform_node(timer=timer, model3d=ball, rigid_body=physics_dict["sphere_body"])
    ball_node.Transform.connect_from(physics_dict["sphere_body"].Transform)

    # skeleton
    skel_trans = avango.gua.nodes.TransformNode(
        Name="skel_trans")
    parent_node.Children.value.append(skel_trans)
    skeleton = HumanSkeleton(PARENT_NODE = skel_trans)

    connect_matrix_to_matrix(timer = timer, mat1 = physics_dict["skel_body"].Transform, mat2 = skeleton.joints[0].Mat)
    skel_trans.Transform.connect_from(physics_dict["skel_body"].Transform)

    #spawner = BallSpawner()
    #spawner.TimeIn.connect_from(timer.Time)
    #spawner.SceneGraph.value = graph
    #spawner.Physics.value = physics

    
    return (light, physics_dict, ball, skeleton, timer)

def viveMonkey():
    #hmd test
    hmd_service = avango.daemon.DeviceService()
    hmd = avango.daemon.nodes.DeviceSensor( \
            DeviceService = hmd_service)
    hmd.Station.value = "hmd-1"

    monkey = loader.create_geometry_from_file(
            "monkey", "data/objects/monkey.obj", \
            avango.gua.LoaderFlags.NORMALIZE_SCALE)
    monkey.Material.value.set_uniform("Color",
            avango.gua.Vec4(1.0, 0.75, 0.75, 1.0))
    monkey.Material.value.set_uniform("Roughness", 0.3)
    monkey.Material.value.set_uniform("Metalness", 1.0)

    hmd_transform = avango.gua.nodes.TransformNode( \
            Transform = avango.gua.make_trans_mat(0.0,1.0,-4.0), \
            Children = [monkey])

    hmd_transform.Transform.connect_from(hmd.Matrix)
    parent_node.Children.value.append(hmd_transform)

def connect_matrix_to_matrix(timer, mat1, mat2):
    connector = MatrixConnector()
    connector.Matrix1 = mat1
    connector.Matrix2 = mat2
    connector.TimeIn.connect_from(timer.Time)
    return connector

# temporary solution for physics field connection avango bug
class TransformNodeConnector(avango.script.Script):
    sphere_body = None
    ball1 = None
    TimeIn = avango.SFFloat()

    def evaluate(self):
        self.ball1.Transform.value = self.sphere_body.Transform.value

class MatrixConnector(avango.script.Script):
    Matrix1 = None
    Matrix2 = None
    TimeIn = avango.SFFloat()

    def evaluate(self):
        self.Matrix1.value = self.Matrix2.value
