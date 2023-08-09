<script lang="ts">
    import { onMount } from "svelte";
    import {
        rotation_vector_0,
        position_vector_0,
        rotation_vector_1,
        position_vector_1,
    } from "../stores/vectors.js";
    import { state, raw_data } from "../stores/server_stats.js";
    let socket: WebSocket;
    onMount(() => {
        const accelerometer_weight = 0.1;
        const gyroscope_weight = 1 - accelerometer_weight;
        const rotation_vector = [0, 0, 0];

        function update_rotation_vector(
            gyroscope: number[],
            accelerometer: number[]
        ) {
            rotation_vector[0] =
                gyroscope[0] * gyroscope_weight +
                accelerometer[0] * accelerometer_weight;
            rotation_vector[1] =
                gyroscope[1] * gyroscope_weight +
                accelerometer[1] * accelerometer_weight;
            rotation_vector[2] =
                gyroscope[2] * gyroscope_weight +
                accelerometer[2] * accelerometer_weight;
        }
        socket = new WebSocket("ws://localhost:5000/ws");
        let delta_time = 0;
        let last_time = Date.now();
        const ACCELEROMETER_WEIGHT = 0.1;
        const GYROSCOPE_WEIGHT = 1 - ACCELEROMETER_WEIGHT;
        let sensorFusion = new SensorFusion();
        socket.onmessage = function (event) {
            try {
                let data = JSON.parse(event.data);
                // console.log(data);
                raw_data.set(data);
                //Raw data: Raw data: {"id":0,"accelerometer":{"x":0.35,"y":0.48,"z":0.89},"gyroscope":{"x":-242,"y":-248,"z":161},"type":"accelerometer-gyroscope-vector"}
                if (data.type === "accelerometer-gyroscope-vector") {
                    delta_time = Date.now() - last_time;
                    last_time = Date.now();
                    if (data.id === 0) {
                        delta_time = (Date.now() - last_time) / 1000;
                        last_time = Date.now();
                        let accelerometer = [
                            data.accelerometer.x,
                            data.accelerometer.y,
                            data.accelerometer.z,
                        ];
                        let gyroscope = [
                            data.gyroscope.x,
                            data.gyroscope.y,
                            data.gyroscope.z,
                        ];

                        let orientation = sensorFusion.updateOrientation(
                            accelerometer[0],
                            accelerometer[1],
                            accelerometer[2],
                            gyroscope[0],
                            gyroscope[1],
                            gyroscope[2],
                            delta_time
                        );

                        rotation_vector_0.set([
                            orientation.roll,
                            orientation.pitch,
                            orientation.yaw,
                        ]);
                        console.log(orientation);
                    }
                }
            } catch (error) {
                console.log(event.data);
                console.log(error);
            }
        };
        socket.onopen = function (event) {
            state.set("🟢");
        };
        socket.onclose = function (event) {
            state.set("🔴");
        };
        socket.onerror = function (event) {
            state.set("🚩");
            console.log(event);
        };
    });

    export function send(message: string) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(message);
        } else {
            alert("Not connected to server");
        }
    }



    class SensorFusion {
        // Gravity constant
        private static G: number = 9.81;

        // Current orientation
        private orientation = { roll: 0, pitch: 0, yaw: 0 };

        // Convert degrees to radians
        private static degToRad(deg: number): number {
            return deg * (Math.PI / 180);
        }

        // Convert radians to degrees
        private static radToDeg(rad: number): number {
            return rad * (180 / Math.PI);
        }

        // Calculate roll (phi), pitch (theta) and yaw (psi)
        public updateOrientation(
            ax: number,
            ay: number,
            az: number,
            gx: number,
            gy: number,
            gz: number,
            dt: number
        ): { roll: number; pitch: number; yaw: number } {
            // Convert accelerometer measurements to m/s^2
            ax *= SensorFusion.G;
            ay *= SensorFusion.G;
            az *= SensorFusion.G;

            // Convert gyroscope measurements to rad/s
            gx = SensorFusion.degToRad(gx);
            gy = SensorFusion.degToRad(gy);
            gz = SensorFusion.degToRad(gz);

            // normalize accelerometer measurements
            let norm = Math.sqrt(ax * ax + ay * ay + az * az);
            ax /= norm;
            ay /= norm;
            az /= norm;

            // calculate roll (phi) and pitch (theta) from accelerometer data
            let rollAcc = Math.atan2(ay, az);
            let pitchAcc = Math.atan2(-ax, Math.sqrt(ay * ay + az * az));

            // integrate gyroscope data
            this.orientation.roll += gx * dt; // angle around X-axis
            this.orientation.pitch -= gy * dt; // angle around Y-axis

            // apply a complementary filter to fuse the accelerometer and gyroscope data
            const alpha = 0.98; // filter coefficient
            this.orientation.roll = alpha * this.orientation.roll + (1 - alpha) * rollAcc;
            this.orientation.pitch = alpha * this.orientation.pitch + (1 - alpha) * pitchAcc;

            // Yaw: With only an accelerometer and a gyroscope you can't estimate yaw
            // You would need a magnetometer or another way to get an absolute reference
            this.orientation.yaw = 0; // no way to update yaw from gyro or accel data

            // convert to degrees
            this.orientation.roll = SensorFusion.radToDeg(this.orientation.roll);
            this.orientation.pitch = SensorFusion.radToDeg(this.orientation.pitch);
            this.orientation.yaw = SensorFusion.radToDeg(this.orientation.yaw);

            return this.orientation;
        }
        }
    

</script>

<button on:click={() => send("Hello")}>Send</button>
