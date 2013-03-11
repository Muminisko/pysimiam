from khepera3 import K3Supervisor
from supervisor import Supervisor
from math import sqrt

class K3DefaultSupervisor(K3Supervisor):
    """K3Default supervisor creates two controllers: gotogoal and avoidobstacles. This module is intended to be a template for student supervisor and controller integration"""
    def __init__(self, robot_pose, robot_info):
        """Creates an avoid-obstacle controller and go-to-goal controller"""
        K3Supervisor.__init__(self, robot_pose, robot_info)

        #Add controllers ( go to goal is default)
        self.ui_params.sensor_angles = [pose.theta for pose in robot_info.ir_sensors.poses]
        self.avoid = self.add_controller('avoidobstacles.AvoidObstacles', self.ui_params)
        self.gtg = self.add_controller('gotogoal.GoToGoal', self.ui_params.gains)
        self.hold = self.add_controller('hold.Hold', None)

        #Week 5
        #Uncomment the next line if you want to add a hybrid controller
        #self.hyrbid = self.add_conroller('hybrid.Hybrid', None)

        self.current = self.gtg

    def set_parameters(self,params):
        K3Supervisor.set_parameters(self,params)
        self.gtg.set_parameters(params.pid.gains)
        self.avoid.set_parameters(self.ui_params)

    def process(self):
        """Selects the best controller based on ir sensor readings
        Updates ui_params.pose and ui_params.ir_readings"""

        #Get robot present pose
        self.ui_params.pose = self.pose_est

        #Determine if robot is at the goal
        distance_from_goal = sqrt((self.pose_est.x - self.ui_params.goal.x)**2 + (self.pose_est.y - self.ui_params.goal.y)**2)

        #Stop if at the goal
        if distance_from_goal < self.robot.wheels.base_length/2:
            if not self.current == self.hold:
                print "GOAL"
                self.current = self.hold
        else: #Here is where statemachine happens

            #Get IR distances
            self.ui_params.sensor_distances = self.get_ir_distances()
            distmin = min(self.ui_params.sensor_distances) 

            #Begin Week5 Exercise
            #Using the above distances, implement a statemachine that
            #'arbitrates' between the controllers available.

            if self.current == self.gtg:
                #Your code here
                pass  #this is just a placeholder (delete it when done)
            elif self.current == self.avoid:
                #Your code here
                pass #this is also a placeholder (delete when done)
            #elif self.current == self.hybrid: #uncomment to use
            #    pass

        #END Week5 Exercise
        return self.ui_params
