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
    <Line
      :key="chartKey"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>


<script>
import axios from 'axios';  // Import axios for making HTTP requests
import { Line } from 'vue-chartjs';  // Import the Line chart component
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);


export default {
  name: 'SensorReadings',
  components: { Line },
  data() {
    return {
      chartKey: 0,
      sensorData: null,  // Store sensor data
      intervalId: null,  // Store the interval ID for clearing later
      ws: null,
      ipAddress: '172.20.10.2',
      wsMessage: '',
      readings: [10,5,2,12,5],
      chartData: {
        labels: ['1', '2', '3', '4', '5'], // X-axis labels (timestamps)
        datasets: [
          {
            label: 'Temperature (°C)', // Data label
            data: [10,5,2,12,5], // Y-axis data points for temperature
            borderColor: '#42A5F5', // Line color
            fill: false, // Do not fill under the line
            tension: 0.1 // Smooth line
          },
        ]
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            display: true, // Display the legend
          },
          title: {
            display: true,
            text: 'Sensor Readings Over Time' // Title of the chart
          }
        }
      }
    };
  },
  methods: {
    fetchSensorData() {
      // Make an HTTP GET request to fetch sensor data
      axios.get('http://192.168.0.245:8000/sensor-readings')
        .then((response) => {
          this.sensorData = response.data;  // Update the sensorData with the response
          console.log('Sensor Data:', this.sensorData);

          this.updateChartData(this.sensorData.data);
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
    },
    updateChartData(data) {
      // Push new readings to the readings array
      // Push new temperature reading to the readings array
      this.readings.push(data.temp);

      // Limit to the last 5 readings
      if (this.readings.length > 5) {
        this.readings.shift(); // Remove the oldest reading
      }

      // Update chart data
      this.chartData.datasets[0].data = [...this.readings]; // Use spread operator for reactivity
      console.log('Chart data updated:', this.chartData);
      this.chartKey++;
      //this.chartData.datasets[1].data = this.readings.map(reading => reading.gas);
      //this.chartData.datasets[2].data = this.readings.map(reading => reading.air);
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


<style scoped>
h1 {
  margin: 20px 0;
}
p {
  font-size: 24px; /* Optional: increase font size for the display */
  color: #42b983; /* Optional: color for better visibility */
}

</style>
