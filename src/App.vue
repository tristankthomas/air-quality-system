<template>
  <div id="app">
    <GasDisplay />
  </div>
</template>

<script>
import GasDisplay from './components/GasDisplay.vue';

export default {
  name: 'App',
  components: {
    GasDisplay
  }
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
