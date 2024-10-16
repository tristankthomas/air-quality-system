<script>
import axios from 'axios';  // Import axios for making HTTP requests

export default {
  name: 'SensorReadings',
  data() {
    return {
      sensorData: null,  // Store sensor data
      intervalId: null,  // Store the interval ID for clearing later
      ws: null,
      ipAddress: '172.20.10.2',
      wsMessage: '',
    };
  },
  methods: {
    fetchSensorData() {
      // Make an HTTP GET request to fetch sensor data
      axios.get('http://192.168.0.245:8000/sensor-readings')
        .then((response) => {
          this.sensorData = response.data;  // Update the sensorData with the response
          console.log('Sensor Data:', this.sensorData);
        })
        .catch((error) => {
          console.error('Failed to fetch sensor data:', error);
        });
    },
    setupWebSocket() {
      // Create WebSocket connection
      this.ws = new WebSocket('ws://192.168.0.245:8000/ws/alerts');

      this.ws.onmessage = (event) => {
        const message = event.data;
        console.log('Received WebSocket message:', message);
        this.wsMessage = message;
        // You can handle the message, e.g., display an alert or update the UI
      };

      this.ws.onclose = () => {
        console.log('WebSocket connection closed. Attempting to reconnect...');
        // Optionally implement reconnection logic here
      };
    }
  },
  mounted() {
    // Fetch data immediately when the component is mounted
    this.fetchSensorData();

    // Set up polling to fetch data every 1 second (1000ms)
    this.intervalId = setInterval(() => {
      this.fetchSensorData();
    }, 1000);
    

    // Set up WebSocket connection
    this.setupWebSocket();
  },
  beforeUnmount() {
    // Clear the polling interval when the component is unmounted
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    // Close WebSocket connection
    if (this.ws) {
      this.ws.close();
    }
  }
};
</script>

<template>
  <div>
    <h1>Sensor Readings</h1>
    <div v-if="sensorData">
      <p>Gas: {{ sensorData.data.gas }}</p>
      <p>Air: {{ sensorData.data.air }}</p>
      <p>Temperature: {{ sensorData.data.temp }} °C</p>
    </div>
    <p v-else>Loading...</p>
    <p v-if="wsMessage" class="ws-message">{{ wsMessage }}</p>
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
