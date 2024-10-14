<script>
// import axios from 'axios';

export default {
  name: 'GasReading',
  data() {
    return {
      sensorData: null,  // Changed from gasReading to sensorData for clarity
      socket: null,
    };
  },
  methods: {
    connectWebSocket() {
      // Replace with your WebSocket URL
      this.socket = new WebSocket('ws://192.168.0.245:8000/ws/gas-sensor');

      // Listen for messages from the WebSocket
      this.socket.onmessage = (event) => {
        // Parse the received JSON data
        try {
          this.sensorData = JSON.parse(event.data);
        } catch (e) {
          console.error('Failed to parse JSON:', e);
        }
      };

      // Handle WebSocket connection errors
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      // Handle WebSocket closure
      this.socket.onclose = () => {
        console.log('WebSocket connection closed');
      };
    }
  },
  mounted() {
    // Establish WebSocket connection when the component is mounted
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  }
};
</script>

<template>
  <div>
    <h1>Gas Reading from MQ-2 Sensor</h1>
    <div v-if="sensorData">
      <p>Gas: {{ sensorData.gas }}</p>
      <p>Air: {{ sensorData.air }}</p>
      <p>Temperature: {{ sensorData.temp }} °C</p>
    </div>
    <p v-else>Loading...</p>
  </div>
</template>

<style scoped>
h1 {
  margin: 20px 0;
}
p {
  font-size: 24px; /* Optional: increase font size for the display */
  color: #42b983; /* Optional: color for better visibility */
}
</style>
