import avango
import avango.gua as agua
import math


def create_physics_graph(physics, physics_root):
    #First we create a ground floor

    #physics.Gravity.value = agua.Vec3(0,-9.18,0)

    agua.create_box_shape("box", agua.Vec3(1000, 1.0, 1000))
    floor_collision_shape = agua.nodes.CollisionShapeNode(
        Name="floor_shape",
        ShapeName="box")

    floor_body = agua.nodes.RigidBodyNode(
        Name="floor_body",
        Mass=0,
        Friction=0.5,
        DisplayBoundingBox=True,
        Restitution=0.7,
        Transform = agua.make_trans_mat(-0.5,-2.5,1),
        Children=[floor_collision_shape])

    physics.add_rigid_body(floor_body)
    physics_root.Children.value.append(floor_body)

    ##skybox
    #agua.create_box_shape("box", agua.Vec3(50,50,50))
    #sky_collision_shape = agua.nodes.CollisionShapeNode(
    #    Name="sky_shape",
    #    ShapeName="box")

    #sky_body = agua.nodes.RigidBodyNode(
    #    Name="sky_body",
    #    Mass=0,
    #    Friction=0.5,
    #    Restitution=0.7,
    #    #Transform = agua.make_scale_mat(0,-0.5,0),
    #    Children=[sky_collision_shape])

    #physics.add_rigid_body(sky_body)
    #physics_root.Children.value.append(sky_body)
#
    #plane_left
    #agua.create_box_shape("plane-left", agua.Vec3(1.0, 1000, 1000))
    #plane_left_collision_shape = agua.nodes.CollisionShapeNode(
    #    Name="plane-left-shape",
    #    ShapeName="box")
    
    #plane_left_body = agua.nodes.RigidBodyNode(
    #    Name="plane-left-body",
    #    Mass=0,
    #    Friction=0.5,
    #    Restitution=0.7,
    #    Transform = agua.make_trans_mat(-1,0,0),
    #    Children=[plane_left_collision_shape])

    #physics.add_rigid_body(plane_left_body)
    #physics_root.Children.value.append(plane_left_body)


    ##plane_right#
    #agua.create_box_shape("plane-right", agua.Vec3(1.0, 1000, 1000))
    #plane_right_collision_shape = agua.nodes.CollisionShapeNode(
    #    Name="plane-right-shape",
    #    ShapeName="box")
    
    #plane_right_body = agua.nodes.RigidBodyNode(
    #    Name="plane-right-body",
    #    Mass=0,
    #    Friction=0.5,
    #    Restitution=0.7,
    #    Transform = agua.make_trans_mat(1,0,0),
    #    Children=[plane_right_collision_shape])

    #physics.add_rigid_body(plane_right_body)
    #physics_root.Children.value.append(plane_right_body)

    #plane_top
    agua.create_box_shape("plane-top", agua.Vec3(1000, 1, 1000))
    plane_top_collision_shape = agua.nodes.CollisionShapeNode(
        Name="plane-top-shape",
        ShapeName="box")
    
    plane_top_body = agua.nodes.RigidBodyNode(
        Name="plane-top-body",
        Mass=0,
        Friction=0.5,
        DisplayBoundingBox=True,
        Restitution=0.7,
        Transform = agua.make_trans_mat(-0.5,30,1),
        Children=[plane_top_collision_shape])

    physics.add_rigid_body(plane_top_body)
    physics_root.Children.value.append(plane_top_body)

    #ball
    agua.create_sphere_shape("sphere", 0.5)
    sphere_collision_shape = agua.nodes.CollisionShapeNode(
        Name="sphere_collision_shape",
        ShapeName="sphere")

    sphere_body = agua.nodes.RigidBodyNode(
        Name="sphere_body",
        Mass=2.0,
        Friction=0.6,
        RollingFriction=0.03,
        DisplayBoundingBox=True,
        Restitution=0.7,
        Transform=agua.make_trans_mat(0.0, 20.0, 3.0),
        Children=[sphere_collision_shape])
    physics.add_rigid_body(sphere_body)
    physics_root.Children.value.append(sphere_body)
    
    #skeleton
    skel_sphere_shape = agua.nodes.CollisionShapeNode(
        Name="skel_sphere_shape",
        ShapeName="sphere")

    skel_right_hand_body = agua.nodes.RigidBodyNode(
        Name="sphere_body",
        IsKinematic=True,
        DisplayBoundingBox=True,
        Mass=2.0,
        Friction=0.6,
        RollingFriction=0.03,
        Children=[skel_sphere_shape])
    physics.add_rigid_body(skel_right_hand_body)
    physics_root.Children.value.append(skel_right_hand_body)

    skel_left_hand_body = agua.nodes.RigidBodyNode(
        Name="sphere_body",
        IsKinematic=True,
        DisplayBoundingBox=True,
        Mass=2.0,
        Friction=0.6,
        RollingFriction=0.03,
        Children=[skel_sphere_shape])
    physics.add_rigid_body(skel_left_hand_body)
    physics_root.Children.value.append(skel_left_hand_body)

    return {"floor_body": floor_body,
            "sphere_body": sphere_body,
            "skel_right_hand": skel_right_hand_body,
            "skel_left_hand": skel_left_hand_body
            }


