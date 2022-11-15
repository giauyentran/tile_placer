// MultiStepper.pde
// -*- mode: C++ -*-
//
// Shows how to multiple simultaneous steppers
// Runs one stepper forwards and backwards, accelerating and decelerating
// at the limits. Runs other steppers at the same time
//
// Copyright (C) 2009 Mike McCauley
// $Id: MultiStepper.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>

// For RAMPS 1.4
#define X_STEP_PIN         A0
#define X_DIR_PIN          A1
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN          -1 //PIN 2 is used

#define Y_STEP_PIN         A6
#define Y_DIR_PIN          A7
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          -1 //PIN 15 is used

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62
#define Z_MIN_PIN          18
#define Z_MAX_PIN          -1 //PIN 19 is used

// Define some steppers and the pins the will use
AccelStepper Y_1(AccelStepper::FULL2WIRE, X_STEP_PIN, X_DIR_PIN);
AccelStepper Y_2(AccelStepper::FULL2WIRE, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper stepper3(AccelStepper::FULL2WIRE, Z_STEP_PIN, Z_DIR_PIN);

void setup()
{  
    Y_1.setMaxSpeed(200.0);
    Y_1.setAcceleration(100.0);
    Y_1.moveTo(24);
    
    Y_2.setMaxSpeed(300.0);
    Y_2.setAcceleration(100.0);
    Y_2.moveTo(1000000);
    /*
    stepper3.setMaxSpeed(300.0);
    stepper3.setAcceleration(100.0);
    stepper3.moveTo(1000000); 
    */
}

void loop()
{
    // Change direction at the limits
    if (Y_1.distanceToGo() == 0)
	  Y_1.moveTo(-Y_1.currentPosition());
    Y_1.run();
    Y_2.run();
    //stepper3.run();
}
