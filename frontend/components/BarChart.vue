<script>
import { Bar } from 'vue-chartjs'

export default {
  name: 'BarChart',
  extends: Bar,
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
