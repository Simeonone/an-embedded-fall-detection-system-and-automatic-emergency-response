/* Edge Impulse ingestion SDK
 * Copyright (c) 2022 EdgeImpulse Inc.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Include necessary libraries
#include <ArduinoBLE.h>  // For Bluetooth Low Energy functionality
#include <Fall_Detection_system_inferencing.h>  // Custom library for fall detection inference
#include <Arduino_LSM9DS1.h>  // For IMU (Inertial Measurement Unit) functionality
#include <ArduinoJson.h>  // For JSON data formatting

// Define constants
#define CONVERT_G_TO_MS2    9.80665f  // Conversion factor from g to m/s^2
#define MAX_ACCEPTED_RANGE  2.0f  // Maximum accepted range for acceleration values

// Global variables
static bool debug_nn = false;  // Flag for neural network debugging
static uint32_t run_inference_every_ms = 20;  // Run inference every 20 ms
static rtos::Thread inference_thread(osPriorityLow);  // Create a low priority thread for inference
static float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };  // Buffer to store sensor data
static float inference_buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE];  // Buffer for inference calculations
static int sample_num = 0;  // Counter for samples

// Function declaration
void run_inference_background();

// Set up BLE service and characteristic
BLEService fallDetectionService("19B10000-E8F2-537E-4F6C-D104768A1214");  // Custom service UUID
BLECharacteristic fallDataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 200);  // Custom characteristic UUID

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    
    // Blink LED 3 times to indicate power-on
    for(int i=0; i<3; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
    }

    delay(1000);  // Wait for 1 second after power-on

    // Initialize IMU, if fails, blink LED continuously
    if (!IMU.begin()) {
        while (1) {
            digitalWrite(LED_BUILTIN, HIGH);
            delay(500);
            digitalWrite(LED_BUILTIN, LOW);
            delay(500);
        }
    }

    // Check if the classifier is configured correctly
    if (EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME != 3) {
        while (1) {
            digitalWrite(LED_BUILTIN, HIGH);
            delay(200);
            digitalWrite(LED_BUILTIN, LOW);
            delay(200);
        }
    }

    // Start the inference thread
    inference_thread.start(mbed::callback(&run_inference_background));

    // Initialize BLE, if fails, blink LED rapidly
    if (!BLE.begin()) {
        while (1) {
            digitalWrite(LED_BUILTIN, HIGH);
            delay(100);
            digitalWrite(LED_BUILTIN, LOW);
            delay(100);
        }
    }

    // Set BLE connection parameters for faster data transfer
    BLE.setConnectionInterval(0x0006, 0x0010);  // Min and max interval (7.5ms to 20ms)
    BLE.setSupervisionTimeout(100);  // 1 second (10ms units)

    fallDataCharacteristic.writeValue("");  // Initialize with an empty string

    // Set up BLE advertising
    BLE.setDeviceName("FallDetector");
    BLE.setLocalName("FallDetector");
    BLE.setAdvertisedService(fallDetectionService);
    fallDetectionService.addCharacteristic(fallDataCharacteristic);
    BLE.addService(fallDetectionService);
    BLE.advertise();

    // Blink LED 5 times to indicate successful BLE advertising
    for(int i=0; i<5; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200);
        digitalWrite(LED_BUILTIN, LOW);
        delay(200);
    }
}

// Helper function to get the sign of a number
float ei_get_sign(float number) {
    return (number >= 0.0) ? 1.0 : -1.0;
}

// Function to run inference in the background
void run_inference_background() {
    // Initial delay to allow sensor data to accumulate
    delay((EI_CLASSIFIER_INTERVAL_MS * EI_CLASSIFIER_RAW_SAMPLE_COUNT) + 100);

    // Initialize smooth classifier
    ei_classifier_smooth_t smooth;
    ei_classifier_smooth_init(&smooth, 10, 7, 0.8, 0.3);

    while (1) {
        // Copy data from buffer to inference_buffer
        memcpy(inference_buffer, buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE * sizeof(float));

        // Create a signal from the buffer
        signal_t signal;
        int err = numpy::signal_from_buffer(inference_buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
        if (err != 0) {
            continue;
        }

        // Run the classifier
        ei_impulse_result_t result = { 0 };
        err = run_classifier(&signal, &result, debug_nn);
        if (err != EI_IMPULSE_OK) {
            continue;
        }

        // Get the smoothed prediction
        const char *prediction = ei_classifier_smooth_update(&smooth, &result);

        // Create a JSON document with the results
        StaticJsonDocument<200> doc;
        doc["sample_num"] = sample_num++;
        doc["predicted_activity"] = prediction;
        doc["accel_x"] = buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3];
        doc["accel_y"] = buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2];
        doc["accel_z"] = buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1];

        String jsonString;
        serializeJson(doc, jsonString);

        // If BLE is connected, send the data
        if (BLE.connected()) {
            fallDataCharacteristic.writeValue(jsonString.c_str());
        }

        // Wait before next inference
        delay(run_inference_every_ms);
    }

    // Free the smooth classifier
    ei_classifier_smooth_free(&smooth);
}

void loop() {
    BLE.poll();  // Handle BLE events
    static bool wasConnected = false;

    if (BLE.connected()) {
        // If just connected, turn on LED
        if (!wasConnected) {
            digitalWrite(LED_BUILTIN, HIGH);
            wasConnected = true;
        }

        // Calculate next sample time
        uint64_t next_tick = micros() + (EI_CLASSIFIER_INTERVAL_MS * 1000);

        // Shift existing data in buffer
        numpy::roll(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, -3);

        // Read new accelerometer data
        IMU.readAcceleration(
            buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3],
            buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2],
            buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1]
        );

        // Clamp acceleration values to MAX_ACCEPTED_RANGE
        for (int i = 0; i < 3; i++) {
            if (fabs(buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i]) > MAX_ACCEPTED_RANGE) {
                buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i] = ei_get_sign(buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i]) * MAX_ACCEPTED_RANGE;
            }
        }

        // Convert acceleration from g to m/s^2
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3] *= CONVERT_G_TO_MS2;
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2] *= CONVERT_G_TO_MS2;
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1] *= CONVERT_G_TO_MS2;

        // Wait until next sample time
        uint64_t time_to_wait = next_tick - micros();
        delay((int)floor((float)time_to_wait / 1000.0f));
        delayMicroseconds(time_to_wait % 1000);
    } else {
        // If just disconnected, turn off LED and start advertising
        if (wasConnected) {
            digitalWrite(LED_BUILTIN, LOW);
            wasConnected = false;
            BLE.advertise();
        }
        delay(500);
    }

    // Blink LED periodically to show the device is still running
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    delay(100);
}

// Ensure the correct sensor is being used for the model
#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_ACCELEROMETER
#error "Invalid model for current sensor"
#endif