/*
 * Multi-motor control (experimental)
 *
 * Move two or three motors at the same time.
 * This module is still work in progress and may not work well or at all.
 *
 * Copyright (C)2017 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include <Arduino.h>
#include "MultiDriver.h"
#include "SyncDriver.h"

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200

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
//#define SLEEP 13 // optional (just delete SLEEP f+rom everywhere if not used)

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
A4988 Y_1(MOTOR_STEPS, X_DIR_PIN, X_STEP_PIN, X_ENABLE_PIN, MS1, MS2, MS3);
A4988 Y_2(MOTOR_STEPS, Y_DIR_PIN, Y_STEP_PIN, Y_ENABLE_PIN, MS1, MS2, MS3);
A4988 X(MOTOR_STEPS, Z_STEP_PIN, Z_STEP_PIN, Z_ENABLE_PIN, MS1, MS2, MS3);

// If microstepping is set externally, make sure this matches the selected mode
// 1=full step, 2=half step etc.
#define MICROSTEPS 16

// Pick one of the two controllers below
// each motor moves independently, trajectory is a hockey stick
// MultiDriver controller(stepperX, stepperY);
// OR
// synchronized move, trajectory is a straight line
SyncDriver controller(Y_1, Y_2);

void setup() {
    /*
     * Set target motors RPM.
     */
    stepperY1.begin(MOTORSTEPS, MICROSTEPS);
    stepperY2.begin(MOTORSTEPS, MICROSTEPS);
    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next two lines
    // stepperX.setEnableActiveState(LOW);
    // stepperY.setEnableActiveState(LOW);
}

void loop() {

    controller.rotate(90*5, 60*15);
    delay(1000);
    controller.rotate(-90*5, -30*15);
    delay(1000);
    controller.rotate(0, -30*15);
    delay(30000);
}
