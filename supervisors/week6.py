#
# (c) PySimiam Team 2013
# 
# Contact person: Tim Fuchs <typograph@elec.ru>
#
# This class was implemented for the weekly programming excercises
# of the 'Control of Mobile Robots' course by Magnus Egerstedt.
#
from khepera3 import K3Supervisor
from helpers import Struct
from numpy import array, dot

from math import pi, sin, cos, log1p, sqrt, atan2

class K3WallSupervisor(K3Supervisor):
    """K3Wall supervisor uses a follow-wall controller to make the robot drive at a certain distance from obstacles."""
    def __init__(self, robot_pose, robot_info):
        """Create the controller"""
        K3Supervisor.__init__(self, robot_pose, robot_info)

        # Fill in poses for the controller
        self.parameters.sensor_poses = robot_info.ir_sensors.poses[:]
        
        # Create and set the controller
        self.current = self.create_controller('week6.FollowWall', self.parameters)

    def set_parameters(self,params):
        """Set parameters for itself and the controllers"""
        self.parameters.direction = params.wall.direction
        self.parameters.distance = params.wall.distance
        self.parameters.velocity = params.velocity
        self.parameters.gains = params.gains
        self.current.set_parameters(self.parameters)
    
    def get_parameters(self):
        """Return a structure with current parameters"""
        p = Struct()
        p.wall = Struct()
        p.wall.direction = self.parameters.direction
        p.wall.distance = self.parameters.distance
        p.velocity = self.parameters.velocity
        p.gains = self.parameters.gains
        return p        

    def get_ui_description(self,p = None):
        """Returns the UI description for the docker"""
        if p is None:
            p = self.parameters
        
        return [
            (('wall', "Follow wall"), [
                ('direction', (p.direction,['left','right'])),
                (('distance','Distance to wall'), p.distance)]),
            ('velocity', [('v',p.velocity.v)]),
            (('gains',"PID gains"), [
                (('kp','Proportional gain'), p.gains.kp),
                (('ki','Integral gain'), p.gains.ki),
                (('kd','Differential gain'), p.gains.kd)])]
                    
    def init_default_parameters(self):
        """Init parameters with default values"""
        self.parameters = Struct()
        self.parameters.direction = 'left'
        self.parameters.distance = 0.2
        self.parameters.velocity = Struct()
        self.parameters.velocity.v = 0.2
        self.parameters.gains = Struct()
        self.parameters.gains.kp = 10.0
        self.parameters.gains.ki = 2.0
        self.parameters.gains.kd = 0.0

    def process_state_info(self,state):
        """Update state parameters for the controllers and self"""

        K3Supervisor.process_state_info(self,state)
        
        # Sensor readings in world units
        self.parameters.sensor_distances = self.get_ir_distances()
   
    def draw(self, renderer):
        """Draw controller info"""
        
        """Draw follow wall"""
        renderer.set_pose(self.pose_est)
        arrow_length = self.robot.wheels.base_length*5
        
        # Draw vector to wall:
        if self.current.to_wall_vector is not None:
            renderer.set_pen(0x0000FF)
            renderer.draw_arrow(0,0,
                self.current.to_wall_vector[0],
                self.current.to_wall_vector[1])
            # Draw 
            if self.current.along_wall_vector is not None:
                renderer.set_pen(0xFF00FF)
                renderer.push_state()
                renderer.translate(self.current.to_wall_vector[0], self.current.to_wall_vector[1])
                renderer.draw_arrow(0,0,
                    self.current.along_wall_vector[0],
                    self.current.along_wall_vector[1])
                renderer.pop_state()

        # Draw heading
        renderer.set_pen(0x000000)
        renderer.draw_arrow(0,0,
            arrow_length*cos(self.current.heading_angle),
            arrow_length*sin(self.current.heading_angle))

        # Important sensors
        renderer.set_pen(0)
        for v in self.current.vectors:
            x,y,z = v
            
            renderer.push_state()
            renderer.translate(x,y)
            renderer.rotate(atan2(y,x))
        
            renderer.draw_line(0.01,0.01,-0.01,-0.01)
            renderer.draw_line(0.01,-0.01,-0.01,0.01)
            
            renderer.pop_state()                           
        