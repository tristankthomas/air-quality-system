<template>
  <div>
    <Line id="chart" :options="chartOptions" :data="chartData" />
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

export default {
  name: 'ChartComponent',
  components: { Line },
  data() {
    return {
      chartData: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [
          {
            label: 'Sample Data', // Optional: Label for the dataset
            data: [40, 20, 12], // Y-axis data points
            borderColor: '#42A5F5', // Line color
            fill: false // Do not fill under the line
          }
        ]
      },
      chartOptions: {
        plugins: {
          legend: {
            position: 'right',
          }
        },
        title: {
          display: true,
          text: 'Real-Time User Data'
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
</script>

