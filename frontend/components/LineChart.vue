<script>
import { Line } from 'vue-chartjs'

export default {
  name: 'LineChart',
  extends: Line,
  props: ['data', 'options'],
  mounted () {
    this.renderChart(this.data, this.options)
  },
  methods: {
    updateChart(){
      this.renderChart(this.data, this.options);
    }
  },
  watch: {
    data(){
      setImmediate(this.updateChart);
    }
  }
}
</script>
