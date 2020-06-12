<script>
import { Line } from 'vue-chartjs'

export default {
  name: 'BarChart',
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
      this.setImmediate(this.updateChart);
    }
  }
}
</script>
