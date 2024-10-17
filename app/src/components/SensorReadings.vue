<template>
  <div>
    <h1>Sensor Readings</h1>
    <div v-if="sensorData">
      <p>Gas: {{ sensorData.data.gas }} ppm</p>
      <p>Air: {{ sensorData.data.air }} ppm</p>
      <p>Temperature: {{ sensorData.data.temp }} °C</p>
      <p>Fan Speed: {{ sensorData.data.speed }} %</p>
    </div>
    <p v-else>Loading...</p>
    <p v-if="wsMessage" class="ws-message" :style="{ color: messageColour + ' !important', fontSize: '22px' }">{{ wsMessage }}</p>
    <div style="max-width: 900px; max-height: 700px; overflow: hidden; margin: 22px auto;">
    <Line
      v-if="readings.length > 0"
      :key="chartKey"
      :data="chartData"
      :options="chartOptions"
      ref="lineChart"
    />
    </div >
  </div>
</template>


<script>
import axios from 'axios';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js';

// register chartjs components for line graph
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);


export default {
  name: 'SensorReadings',
  components: { Line },
  data() {
    return {
      chartKey: 0, // forces update of chart
      sensorData: null,
      intervalId: null,
      ws: null,
      ipAddress: '172.20.10.3', // backend ip address
      wsMessage: '',
      messageColour: '',
      readings: [],
      chartData: {
        labels: [], // timestamps
        datasets: [
          {
            label: 'Temperature (°C)', 
            data: [],
            borderColor: '#42A5F5', // blue
            fill: false,
            tension: 0.1
          },
          {
            label: 'Gas Level (ppm)',
            data: [],
            borderColor: '#FF6384', // red
            fill: false,
            tension: 0.1
          },
          {
            label: 'Air Quality (ppm)',
            data: [],
            borderColor: '#FFCE56', // yellow
            fill: false,
            tension: 0.1
          }
        ]
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            min: 0
          }
        }
      }
    };
  },
  methods: {
    fetchSensorData() {
      // get sensor readings from server using get request
      axios.get(`http://${this.ipAddress}:8000/sensor-readings`)
        .then((response) => {
          // update data
          this.sensorData = response.data;  
          console.log('Sensor Data:', this.sensorData);
          // update chart with data
          this.updateChartData(this.sensorData.data);
        })
        .catch((error) => {
          console.error('Failed to fetch sensor data:', error);
        });
    },
    setupWebSocket() {
      // create WebSocket connection with server
      this.ws = new WebSocket(`ws://${this.ipAddress}:8000/ws/alerts`);

      this.ws.onmessage = (event) => {
         const message = JSON.parse(event.data);
         console.log('Received WebSocket message:', message);
         
         // unpack contents
         this.wsMessage = message.data;
         this.messageColour = message.colour; 
      };
    
      this.ws.onclose = () => {
        console.log('WebSocket connection closed.');
      };
    },
    updateChartData(data) {
      // add data to readings
       this.readings.push({
        temp: data.temp,
        gas: data.gas,
        air: data.air,
        timestamp: new Date().toLocaleTimeString(), // Store the timestamp
      });

      // only present last 20 readings
      if (this.readings.length > 20) {
        this.readings.shift();
      }
      
      // reactivity notation used to help update chart when changed
      this.chartData.labels = [...this.readings.map(reading => reading.timestamp)];
      this.chartData.datasets[0].data = [...this.readings.map(reading => reading.temp)];
      this.chartData.datasets[1].data = [...this.readings.map(reading => reading.gas)];
      this.chartData.datasets[2].data = [...this.readings.map(reading => reading.air)];
      // forces chart to update
      this.chartKey++;
    }
  },
  mounted() {

    this.fetchSensorData();

    // polls for data every second
    this.intervalId = setInterval(() => {
      this.fetchSensorData();
    }, 1000);
    

    // creates WebSocket connection
    this.setupWebSocket();
  },
  beforeUnmount() {
    // clear polling interval
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    // close WebSocket connection
    if (this.ws) {
      this.ws.close();
    }
  }
};
</script>


<style scoped>
h1 {
  margin: 10px 0;
}
p {
  font-size: 18px;
  color: #0f9ed5;
}

</style>
