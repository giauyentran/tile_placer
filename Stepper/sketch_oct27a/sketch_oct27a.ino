/*
 * Clock Microstepping demo
 *
 * Moves the stepper motor like the seconds hand of a watch.
 *
 * Copyright (C)2015-2017 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include <Arduino.h>

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200

// Microstepping mode. If you hardwired it to save pins, set to the same value here.
#define MICROSTEPS 3

#define DIR A1
#define STEP A0
#define SLEEP 13 // optional (just delete SLEEP from everywhere if not used)

/*
#include "A4988.h"
#define M0 10
#define M1 11
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1); 

#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN          -1 //PIN 2 is used

//extruder 1
#define E0_STEP_PIN        26
#define E0_DIR_PIN         28
#define E0_ENABLE_PIN      24
 */


#include "A4988.h"
#define MS1 10
#define MS2 11
#define MS3 12
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);

// #include "DRV8825.h"
// #define MODE0 10
// #define MODE1 11
// #define MODE2 12
// DRV8825 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MODE0, MODE1, MODE2);

// #include "DRV8880.h"
// #define M0 10
// #define M1 11
// #define TRQ0 6
// #define TRQ1 7
// DRV8880 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1, TRQ0, TRQ1);

// #include "BasicStepperDriver.h" // generic
// BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP);

void setup() {
    /*
     * Set target motor RPM=1
     */
    pinMode(A0,OUTPUT);
    pinMode(A1,OUTPUT);
    //stepper.begin(1, MICROSTEPS);

    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    // stepper.setEnableActiveState(LOW);
    
}

void loop() {
    analogWrite(A0,HIGH);
    analogWrite(A1,HIGH);
    /*stepper.enable();
     * The easy way is just tell the motor to rotate 360 degrees at 1rpm
     */
    
}
