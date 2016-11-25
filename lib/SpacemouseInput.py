#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon




class SpacemouseInput(avango.script.Script):

    ### input fields ###

    sf_value0 = avango.SFFloat()
    sf_value1 = avango.SFFloat()
    sf_value2 = avango.SFFloat()
    sf_value3 = avango.SFFloat()
    sf_value4 = avango.SFFloat()
    sf_value5 = avango.SFFloat()


    ### output fields ###

    sf_output_mat = avango.gua.SFMatrix4()
    sf_output_mat.value = avango.gua.make_identity_mat()


    ## constructor
    def __init__(self):
        self.super(SpacemouseInput).__init__()


        ### parameters ###
        self.translation_factor = 0.01
        self.rotation_factor = 0.01


        ### resources ###

        ## init sensor
        self.spacemouse_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.spacemouse_sensor.Station.value = "device-spacemouse"

        ## init field connections
        self.sf_value0.connect_from(self.spacemouse_sensor.Value0)
        self.sf_value1.connect_from(self.spacemouse_sensor.Value1)
        self.sf_value2.connect_from(self.spacemouse_sensor.Value2)
        self.sf_value3.connect_from(self.spacemouse_sensor.Value3)
        self.sf_value4.connect_from(self.spacemouse_sensor.Value4)
        self.sf_value5.connect_from(self.spacemouse_sensor.Value5)



    ### callback functions ###

    def evaluate(self): # evaluated every frame if any input field has changed

        ## map input
        # self.sf_output_mat.value = \
        #     self.sf_output_mat.value * \
        #     avango.gua.make_trans_mat(self.sf_value0.value * self.translation_factor, self.sf_value1.value * self.translation_factor * -1.0, self.sf_value2.value * self.translation_factor) * \
        #     avango.gua.make_rot_mat(self.sf_value3.value * self.rotation_factor,1,0,0) * \
        #     avango.gua.make_rot_mat(self.sf_value4.value * self.rotation_factor,0,-1,0) * \
        #     avango.gua.make_rot_mat(self.sf_value5.value * self.rotation_factor,0,0,1)

        self.sf_output_mat.value = \
            self.sf_output_mat.value * \
            avango.gua.make_rot_mat(self.sf_value4.value * self.rotation_factor,0,-1,0) * \
            avango.gua.make_trans_mat(0,self.sf_value1.value * self.translation_factor * -1,0)

