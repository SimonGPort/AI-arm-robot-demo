import sys
vortex_folder = r'C:\CM Labs\Vortex Studio 2020b\bin'
sys.path.append(vortex_folder)


import Vortex #main Vortex library
import vxatp3 #Automated Test Platform, additional API for automated testing

class env():

    def __init__(self):

        self.setup_file = 'setup.vxc'
        self.arm_file = 'robot_arm.vxmechanism'

        #Create Vortex application using setup file
        self.application = vxatp3.VxATPConfig.createApplication(self, "arm robot app", self.setup_file)

        #Load the robot arm mechanism
        self.vx_robot_arm = self.application.getSimulationFileManager().loadObject(self.arm_file)
        self.robot_arm = Vortex.MechanismInterface(self.vx_robot_arm)
        self.robot_interface = self.robot_arm.findExtensionByName('Robot Arm Interface')
        print(dir(self.vx_robot_arm))

        #Switch to simulation mode
        vxatp3.VxATPUtils.requestApplicationModeChangeAndWait(self.application, Vortex.kModeSimulating)

    #call this to run for n steps
    def run_for_n_steps(self, n_steps):
        for _ in range(n_steps):
            self.application.update()

    #call this to apply action (legnth 4 array)
    def apply_actions(self, actions):
        i = 0
        for action in actions:
            self.robot_interface.getInputContainer()['input ' + str(i)].value = float(action).

    #call this to move and rotate robot mechanism
    def move_arm_to(self, x, y, z, rx, ry, rz):
        local_transform = self.robot_arm.inputLocalTransform.value
        local_transform = Vortex.rotateTo(local_transform, Vortex.VxVector3(x,y,z))
        local_transform = Vortex.translateTo(local_transform, Vortex.VxVector3(rx,ry,rz))
        self.robot_arm.inputLocalTransform.value = local_transform

env = env()
env.move_arm_to(2,2,0,0,90,0)
env.apply_actions([1,1,1,1])
env.run_for_n_steps(500)