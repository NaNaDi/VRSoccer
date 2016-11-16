import avango
import avango.daemon
import os

#Skeleton input
# head_station0 = avango.daemon.Station('kinect-head-0')

# skeleton0 = avango.daemon.SkeletonTrack()
# skeleton0.port = "7700"
# skeleton0.server = "141.54.147.35"

# skeleton0.stations[0] = head_station0

# avango.daemon.run([skeleton0])


#Spacemouse init for calibrator.py
def init_spacemouse():
    _string = os.popen("python find_device.py 1 3Dconnexion SpaceNavigator").read()

    if len(_string) == 0:
        _string = os.popen("python find_device.py 1 3Dconnexion SpaceTraveler USB").read()

    _string = _string.split()
    if len(_string) > 0:

        _string = _string[0]

        # create a station to propagate the input events
        _spacemouse = avango.daemon.HIDInput()
        _spacemouse.station = avango.daemon.Station('device-spacemouse')
        _spacemouse.device = _string

        # map incoming spacemouse events to station values
        _spacemouse.values[0] = "EV_ABS::ABS_X"   # trans X
        _spacemouse.values[1] = "EV_ABS::ABS_Z"   # trans Y
        _spacemouse.values[2] = "EV_ABS::ABS_Y"   # trans Z
        _spacemouse.values[3] = "EV_ABS::ABS_RX"  # rotate X
        _spacemouse.values[4] = "EV_ABS::ABS_RZ"  # rotate Y
        _spacemouse.values[5] = "EV_ABS::ABS_RY"  # rotate Z

        # buttons
        _spacemouse.buttons[0] = "EV_KEY::BTN_0"  # left button
        _spacemouse.buttons[1] = "EV_KEY::BTN_1"  # right button

        device_list.append(_spacemouse)
        print("SpaceMouse started at:", _string)

    else:
        print("SpaceMouse NOT found !")


def init_new_spacemouse():

    _string = os.popen("python find_device.py 1 3Dconnexion SpaceNavigator for ").read()

    _string = _string.split()
    if len(_string) > 0:
        _string = _string[0]

        # create a station to propagate the input events
        _spacemouse = avango.daemon.HIDInput()
        _spacemouse.station = avango.daemon.Station('device-spacemouse-new')
        _spacemouse.device = _string
        _spacemouse.timeout = '10'

        # map incoming spacemouse events to station values
        _spacemouse.values[0] = "EV_REL::REL_X"   # trans X
        _spacemouse.values[1] = "EV_REL::REL_Z"   # trans Y
        _spacemouse.values[2] = "EV_REL::REL_Y"   # trans Z
        _spacemouse.values[3] = "EV_REL::REL_RX"  # rotate X
        _spacemouse.values[4] = "EV_REL::REL_RZ"  # rotate Y
        _spacemouse.values[5] = "EV_REL::REL_RY"  # rotate Z

        # buttons
        _spacemouse.buttons[0] = "EV_KEY::BTN_0"  # left button
        _spacemouse.buttons[1] = "EV_KEY::BTN_1"  # right button

        device_list.append(_spacemouse)
        print("NewSpaceMouse started at:", _string)

    else:
        print("NewSpaceMouse NOT found !")


def init_xbox_controller():

    _string = os.popen("python find_device.py 1 Xbox 360 Wireless Receiver").read()

    _string = _string.split()
    if len(_string) > 0:
        _string = _string[0]

        # create a station to propagate the input events
        _xbox = avango.daemon.HIDInput()
        _xbox.station = avango.daemon.Station('device-xbox')
        _xbox.device = _string
        #_xbox.timeout = '10'

        # map incoming xbox events to station values
        _xbox.values[0] = "EV_ABS::ABS_X"   # trans X
        _xbox.values[1] = "EV_ABS::ABS_Y"   # trans Y
        _xbox.values[3] = "EV_ABS::ABS_Z"   # trans Z up
        _xbox.values[4] = "EV_ABS::ABS_RZ"  # trans Z down

        _xbox.values[2] = "EV_ABS::ABS_RX"


        device_list.append(_xbox)
        print("Xbox-360 Controller started at:", _string)

    else:
        print("Xbox-360 Controller NOT found !")

def init_kinect_skeleton():
    joint_stations = {}
    for i in range(25):
        joint_stations[i] = avango.daemon.Station('kinect-joint-{0}'.format(str(i)))

    skeleton0 = avango.daemon.SkeletonTrack()
    skeleton0.port = "7700"
    skeleton0.server = "141.54.147.35"
    for i in range(25):
        skeleton0.stations[i] = joint_stations[i]

    device_list.append(skeleton0)
    print("Kinect Skeleton started!")

def init_keyboard():

  _string = os.popen("ls /dev/input/by-id | grep \"-event-kbd\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
  
  _string = _string.split()
  
  if len(_string) > 0:
    _string = _string[0]
    
    _keyboard = avango.daemon.HIDInput()
    _keyboard.station = avango.daemon.Station('device-keyboard')
    _keyboard.device = "/dev/input/by-id/" + _string
    
    _keyboard.buttons[9] = "EV_KEY::KEY_RIGHT"
    _keyboard.buttons[10] = "EV_KEY::KEY_UP"
    _keyboard.buttons[11] = "EV_KEY::KEY_DOWN"
    
    device_list.append(_keyboard)
    
    print("Keyboard started at:", _string)
  
  else:
    print("Keyboard NOT found !")

def init_hmd_tracking():
    hmd_stations = {}
    for i in range(7):
        hmd_stations[i] = avango.daemon.Station('hmd-{0}'.format(str(i)))

    hmd0 = avango.daemon.HMDTrack()
    hmd0.server = "141.54.147.35"
    hmd0.port = "7770"

    for i in range(7):
        hmd0.stations[i] = hmd_stations[i]

    device_list.append(hmd0)


device_list = []

init_spacemouse()
init_new_spacemouse()
init_xbox_controller()
init_kinect_skeleton()
init_keyboard()
init_hmd_tracking()

avango.daemon.run(device_list)
