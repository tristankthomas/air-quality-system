<script>
import axios from 'axios';

export default {
  name: 'GasReading',
  data() {
    return {
      gasReading: null,
    };
  },
  methods: {
    fetchGasReading() {
      axios.get('http://172.20.10.2:8000/gas-reading')
        .then(response => {
          this.gasReading = response.data.gas;
        })
        .catch(error => {
          console.error('Error fetching gas reading:', error);
        });
    }
  },
  mounted() {
    // Fetch gas reading when the component is mounted
    this.fetchGasReading();

    // Optionally, poll for new data every 2 seconds
    setInterval(() => {
      this.fetchGasReading();
    }, 2000);
  }
};
</script>

<template>
  <div>
    <h1>Gas Reading from MQ-2 Sensor</h1>
    <p v-if="gasReading">Gas Reading: {{ gasReading }}</p>
    <p v-else>Loading...</p>
  </div>
</template>


<style scoped>
h1 {
  margin: 20px 0;
}
p {
  font-size: 24px; /* Optional: increase font size for the temperature display */
  color: #42b983; /* Optional: color for better visibility */
}
</style>
