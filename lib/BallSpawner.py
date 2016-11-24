import math
import avango
import avango.script
import avango.gua
import avango.gua as av

SPAWN_TIME = 0.4


class BallSpawner(avango.script.Script):

    TimeIn = avango.SFFloat()
    SceneGraph = avango.gua.SFSceneGraph()
    Physics = avango.gua.SFPhysics()
    MaxBallCount = avango.SFFloat()

    def __init__(self):

        self.super(BallSpawner).__init__()

        self.MaxBallCount.value = 50

        self.__last_spawn_time = -1
        self.__loader = avango.gua.nodes.TriMeshLoader()

        self.__spawned_balls = []
        self.red = True

    def evaluate(self):
        global SPAWN_TIME
        current_time = self.TimeIn.value

        if self.__last_spawn_time == -1 or current_time - self.__last_spawn_time >= SPAWN_TIME:
            self.__last_spawn_time = current_time

            if self.red:
                body = avango.gua.nodes.RigidBodyNode(
                    Name="body",
                    Mass=1.5,
                    Friction=0.7,
                    RollingFriction=0.04,
                    Restitution=0.8,
                    Transform=avango.gua.make_trans_mat(
                        math.sin(3 * current_time), 7.0, math.cos(3 *
                                                                  current_time)))
            else:
                body = avango.gua.nodes.RigidBodyNode(
                    Name="body",
                    Mass=2.0,
                    Friction=0.6,
                    RollingFriction=0.03,
                    Restitution=0.3,
                    Transform=avango.gua.make_trans_mat(
                        math.sin(3 * current_time), 7.0, math.cos(3 *
                                                                  current_time)))

            sphere_geometry = self.__loader.create_geometry_from_file(
                "sphere_geometry", "data/objects/sphere.obj")

            sphere_geometry.Transform.value = avango.gua.make_scale_mat(
                0.5, 0.5, 0.5)

            if self.red:
                sphere_geometry.Material.value.set_uniform(
                    #"Color", av.Vec4(0.08, 0.08, 0.09, 1.0))
                    "Color",
                    av.Vec4(0.9, 0.266, 0.136, 1.0))
                sphere_geometry.Material.value.set_uniform("Roughness", 0.75)
                sphere_geometry.Material.value.set_uniform("Metalness", 0.0)

            else:
                sphere_geometry.Material.value.set_uniform(
                    "Color", av.Vec4(1.0, 1.0, 1.0, 1.0))
                sphere_geometry.Material.value.set_uniform("Roughness", 0.2)
                sphere_geometry.Material.value.set_uniform("Metalness", 0.0)

            self.red = not self.red

            collision_shape_node = avango.gua.nodes.CollisionShapeNode(
                Name="collision_shape_node",
                ShapeName="sphere")

            collision_shape_node.Children.value.append(sphere_geometry)
            body.Children.value.append(collision_shape_node)
            self.SceneGraph.value.Root.value.Children.value.append(body)
            self.Physics.value.add_rigid_body(body)

            self.__spawned_balls.append(body)

            if len(self.__spawned_balls) > self.MaxBallCount.value:
                to_remove = self.__spawned_balls.pop(0)
                self.Physics.value.remove_rigid_body(to_remove)
                self.SceneGraph.value.Root.value.Children.value.remove(
                    to_remove)
