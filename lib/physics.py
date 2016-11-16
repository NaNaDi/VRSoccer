import avango
import avango.gua as agua
import math


def create_physics_graph(physics, physics_root):
    #First we create a ground floor
    agua.create_box_shape("box", agua.Vec3(10, 1, 10))
    floor_collision_shape = agua.nodes.CollisionShapeNode(
        Name="floor_shape",
        ShapeName="box")

    floor_body = agua.nodes.RigidBodyNode(
        Name="floor_body",
        Mass=0,
        Friction=0.5,
        Restitution=0.7,
        Transform = agua.make_trans_mat(-0.5,-1.5,1),
        Children=[floor_collision_shape])

    physics.add_rigid_body(floor_body)
    physics_root.Children.value.append(floor_body)

    ##skybox
    #agua.create_box_shape("box", agua.Vec3(30,30,30))
    #sky_collision_shape = agua.nodes.CollisionShapeNode(
    #    Name="sky_shape",
    #    ShapeName="box")

    #sky_body = agua.nodes.RigidBodyNode(
    #    Name="sky_body",
    #    Mass=0,
    #    Friction=0.5,
    #    Restitution=0.7,
    #    Transform = agua.make_scale_mat(0,-0.5,0),
    #    Children=[sky_collision_shape])

    #physics.add_rigid_body(sky_body)
    #physics_root.Children.value.append(sky_body)

    agua.create_sphere_shape("sphere", 0.5)
    sphere_collision_shape = agua.nodes.CollisionShapeNode(
        Name="sphere_collision_shape",
        ShapeName="sphere")

    sphere_body = agua.nodes.RigidBodyNode(
        Name="sphere_body",
        Mass=2.0,
        Friction=0.6,
        RollingFriction=0.03,
        Restitution=0.7,
        Transform=agua.make_trans_mat(0.0, 3.0, 0.0),
        Children=[sphere_collision_shape])
    physics.add_rigid_body(sphere_body)
    physics_root.Children.value.append(sphere_body)

    skel_sphere_shape = agua.nodes.CollisionShapeNode(
        Name="skel_sphere_shape",
        ShapeName="sphere")

    skel_sphere_body = agua.nodes.RigidBodyNode(
        Name="sphere_body",
        IsKinematic=True,
        Mass=2.0,
        Friction=0.6,
        RollingFriction=0.03,
        Restitution=10.0,
        Children=[skel_sphere_shape])
    physics.add_rigid_body(skel_sphere_body)
    physics_root.Children.value.append(skel_sphere_body)

    return {#"floor_body": floor_body,
            "sphere_body": sphere_body,
            "skel_body": skel_sphere_body}


