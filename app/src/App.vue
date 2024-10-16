<template>
  <div id="app">
    <SensorReadings />
  </div>
</template>

<script>
import SensorReadings from './components/SensorReadings.vue'

export default {
  name: 'App',
  components: { SensorReadings }
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
