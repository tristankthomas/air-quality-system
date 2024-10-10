<template>
  <div class="gas-display">
    <h1>Current Gas Reading</h1>
    <p>{{ gas }} °C</p>
  </div>
</template>

<script>
export default {
  name: 'GasDisplay',
  data() {
    return {
      // Set a dummy temperature value for testing
      gas: 25 // You can change this value to test different temperatures
    };
  }
}
</script>

<style scoped>
h1 {
  margin: 20px 0;
}
p {
  font-size: 24px; /* Optional: increase font size for the temperature display */
  color: #42b983; /* Optional: color for better visibility */
}
</style>
