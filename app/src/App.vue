<template>
  <div id="app">
    <SensorReadings />
    <ChartComponent />
  </div>
</template>

<script>
import ChartComponent from './components/ChartComponent.vue'
import SensorReadings from './components/SensorReadings.vue'

export default {
  name: 'App',
  components: { ChartComponent, SensorReadings }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
