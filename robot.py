#!/usr/bin/env python3
"""
    This is a demo program showing the use of the DifferentialDrive class,
    specifically it contains the code necessary to operate a robot with
    a single joystick
"""

import wpilib
import wpilib.drive
import ctre

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # create motor controller objects
        #m_left_front = wpilib.Talon(11)
        #self.m_right_front = wpilib.Talon(22)
        #m_left_rear = wpilib.VictorSPX(33)
        #m_right_rear = wpilib.VictorSPX(44)
        
        self.m_left_front = ctre.WPI_VictorSPX(22)
        self.m_right_front = ctre.WPI_VictorSPX(33)
        self.m_left_rear = ctre.WPI_VictorSPX(11)
        self.m_right_rear = ctre.WPI_VictorSPX(44)
        
        self.m_left = wpilib.SpeedControllerGroup(self.m_left_front, self.m_left_rear)
        self.m_right = wpilib.SpeedControllerGroup(self.m_right_front, self.m_right_rear)
        # object that handles basic drive operations
        self.myRobot = wpilib.drive.DifferentialDrive(self.m_left, self.m_right)
        self.myRobot.setExpiration(0.1)

        # joystick #0
        self.stick = wpilib.Joystick(0)

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        """Runs the motors with tank steering"""
        self.myRobot.arcadeDrive(
            self.stick.getRawAxis(1), self.stick.getRawAxis(0), True
            #self.stick.getRawAxis(0), self.stick.getRawAxis(1), True
            
            #self.stick.getRawAxis(0), self.stick.getRawAxis(1), True
            #self.stick.getRawAxis(0), self.stick.getRawAxis(1), True
            #self.stick.getRawAxis(0), self.stick.getRawAxis(1), True
        )

        #self.m_left_front.set(0.5)


if __name__ == "__main__":
    wpilib.run(MyRobot)
