<script>
import axios from 'axios';  // Import axios for making HTTP requests

export default {
  name: 'GasReading',
  data() {
    return {
      sensorData: null,  // Store sensor data
      intervalId: null,  // Store the interval ID for clearing later
    };
  },
  methods: {
    fetchSensorData() {
      // Make an HTTP GET request to fetch sensor data
      axios.get('http://192.168.0.245:8000/gas-reading')
        .then((response) => {
          this.sensorData = response.data;  // Update the sensorData with the response
          console.log('Sensor Data:', this.sensorData);
        })
        .catch((error) => {
          console.error('Failed to fetch sensor data:', error);
        });
    }
  },
  mounted() {
    // Fetch data immediately when the component is mounted
    this.fetchSensorData();

    // Set up polling to fetch data every 1 second (1000ms)
    this.intervalId = setInterval(() => {
      this.fetchSensorData();
    }, 1000);
  },
  beforeUnmount() {
    // Clear the polling interval when the component is unmounted
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
};
</script>

<template>
  <div>
    <h1>Gas Reading from MQ-2 Sensor</h1>
    <div v-if="sensorData">
      <p>Gas: {{ sensorData.data.gas }}</p>
      <p>Air: {{ sensorData.data.air }}</p>
      <p>Temperature: {{ sensorData.data.temp }} °C</p>
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
