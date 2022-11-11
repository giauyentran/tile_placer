/*
 * Tile Placer - Sprint 2
 *
 * Places tiles in a 5x5 grid binary configuration
 *
 *
 */
 
#include <Arduino.h>

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200

// Microstepping mode. If you hardwired it to save pins, set to the same value here.
#define MICROSTEPS 16

#define DIR A1
#define STEP A0
#define X_ENABLE_PIN 38

#include "A4988.h"
#define MS1 10
#define MS2 11
#define MS3 12
A4988 stepper(MOTOR_STEPS, DIR, STEP, X_ENABLE_PIN, MS1, MS2, MS3);

int test_array[5][5] = {{1,0,1,0,1}, {0,1,0,1,0}, {1,0,1,0,1}, {0,1,0,1,0}, {1,0,1,0,1}};
int gantry_zero[1][2] = {50,50};
float tile_size = 23; // mm
float tile_spacing = 2; // mm
int current_grid[5][5] = {{0,0,0,0,0}, {0,0,0,0,0}, {0,0,0,0,0}, {0,0,0,0,0}, {0,0,0,0,0}};

void setup() {
    /*
     * Set target motor RPM=1
     */
    stepper.begin(120, MICROSTEPS);

    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    stepper.setEnableActiveState(LOW);
    stepper.enable();
}

void loop() {

    // iterate through given image array
    for (int i = 0; i<5; i++){
      for (int j = 0; j<5; j++){
        int tile_location[1][2] = {i,j};
        // compare current and next grid
        if (current_grid[i][j] != test_array[i][j]){
          // TODO: refactor code for better declarations of grid position as it relates to
          // tile location
          float grid_position[1][2]; // {x,y} position of toolhead
          grid_position[1][1] = {gantry_zero[1][1] + tile_location[1][1] + tile_spacing};
          grid_position[1][2] = {gantry_zero[1][2] + tile_location[1][2] + tile_spacing};
          // TODO: x and y movement
          // move to x position @ grid_position[1][1]
          // move to y position @ grid_position[1][2]
        }
      } 
    }
    
    delay(500);
}

void go_distance_mm(int distance) {
  int degree = distance * 9;
  stepper.rotate(degree);
}
