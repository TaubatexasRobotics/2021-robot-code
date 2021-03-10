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
        
        # motor controllers for traction
        self.m_left_front = ctre.WPI_VictorSPX(22)
        self.m_right_front = ctre.WPI_VictorSPX(33)
        self.m_left_rear = ctre.WPI_VictorSPX(11)
        self.m_right_rear = ctre.WPI_VictorSPX(44)
        
        self.shooter = ctre.WPI_VictorSPX(9)
        self.track_ball = ctre.WPI_VictorSPX(8)
        self.ball_catcher = ctre.WPI_VictorSPX(55)

        self.m_left = wpilib.SpeedControllerGroup(self.m_left_front, self.m_left_rear)
        self.m_right = wpilib.SpeedControllerGroup(self.m_right_front, self.m_right_rear)
        # object that handles basic drive operations
        self.myRobot = wpilib.drive.DifferentialDrive(self.m_left, self.m_right)
        self.myRobot.setExpiration(0.1)

        # joystick #0
        self.stick = wpilib.Joystick(0)

        # init camera
        wpilib.CameraServer.launch()

        #criandoinputs
        self.entraInput = wpilib.DigitalInput(0)
        self.entraAnalog = wpilib.AnalogInput(1)
        self.entraEncoder = wpilib.Encoder(0,1)

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        """Runs the motors with tank steering"""
        self.myRobot.arcadeDrive(
            self.stick.getRawAxis(1), self.stick.getRawAxis(0), True
        )

        #testanto input digital
        if self.entraInput.get() == True:
            self.shooter.set(1)
        else:
            self.shooter.set(-1)

        #testando input analógico
        if self.entraAnalog.getValue()>= 2048:
            self.track_ball.set(1)
        else:
            self.track_ball.set(-1) 
        
        #testando encoder
        if self.entraEncoder.get() >= 5:
            self.ball_catcher.set(1)
        else:
            self.ball_catcher.set(-1)

if __name__ == "__main__":
    wpilib.run(MyRobot)
