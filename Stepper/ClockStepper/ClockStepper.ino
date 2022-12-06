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
#define MICROSTEPS 16

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

int initial_pos = 10;
int destination_pos = 20; 
//int x_dist = 0;
int num_mm = 0; 
int mm_taken = 0; 
int max_mm = 20; 
// #include "BasicStepperDriver.h" // generic
// BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP);

void setup() {
    /*
     * Set target motor RPM=1
     */
    //X.begin(120, MICROSTEPS);
    X.begin(120, MICROSTEPS);
    //Y_2.begin(120, MICROSTEPS);
    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    //X.setEnableActiveState(LOW);
    X.setEnableActiveState(LOW);
    //Y_2.setEnableActiveState(LOW);
    //X.enable();
    X.enable();
    //Y_2.enable();
}

void loop() {
    /*
     * The easy way is just tell the motor to rotate 360 degrees at 1rpm
     */
     /*
    //go_distance_mm(0);
    // x_dist = destination_pos - initial_pos; 
    go_distance_mm(0);
    delay(500);
    mm_taken = mm_taken + x_dist;
    if (mm_taken > max_mm) {
      go_distance_mm(0);
    }
   */
   go_distance_mm(50);
   delay(500);
   go_distance_mm(100);
   delay(500);
   go_distance_mm(150);
   delay(500);
   go_distance_mm(200);
   delay(500);
   go_distance_mm(250);
   delay(500);
   go_distance_mm(300);
   delay(500);
}

void go_distance_mm(int dist) {
  int degree = dist * 9;
  //X.rotate(degree);
  X.rotate(degree);
  //Y_2.rotate(degree);
  //Y_2.rotate(degree);
}
