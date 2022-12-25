<template>
  <div class="section">
    <h1 class="title">Library completion stats</h1>

    <div class="box">
      <form action="/completion" method="get">
        <input type="datetime-local" v-model="from" name="from" />
        <input type="datetime-local" v-model="to" name="to" />
        <div class="button" @click="updateComponent">FILTER</div>
      </form>
    </div>

    <div style="" class="box">
      <line-chart :data="barChartYearly" :options="{
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'year'
                }
            }]
        }
    }" />
    </div>

    <div class="columns">
      <div class="year-completion column is-2">
        <h1 class="title">Completion per year</h1>
        <Progress v-for="(data, year) in stats" :data="data" :year="year" :key="year" :value="data.progress">{{year}} - {{ data.read }} / {{ data.books }} read</Progress>
      </div>

      <div class="columns is-multiline column is-10">
        <CompletionProgressFullYear v-for="(data, year) in stats" :data="data" :year="year" :key="year" />
      </div>
    </div>


  </div>
</template>

<script>

import LineChart from "~/components/LineChart";
import CompletionProgressFullYear from "~/components/CompletionProgressFullYear.vue";
import Progress from "~/components/Progress.vue";

export default {
  name: "completion",
  components: {CompletionProgressFullYear, Progress, LineChart},
  computed: {},
  data() {
    return {
      stats: null,
      barChartMonthly: null,
      barChartYearly: null,
      months: ["", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"],
      from: this.$route.query.from,
      to: this.$route.query.to,
    };
  },
  beforeMount() {
    this.updateComponent();
  },
  methods: {
    updateComponent() {
      const $axios = this.$axios;

      const apiParams = new URLSearchParams();

      if (this.from) {
        apiParams.append('from', this.from);
      }
      if (this.to) {
        apiParams.append('to', this.to);
      }

      $axios.$get('/completion-statistics/?' + apiParams.toString()).then(result => {
        const filteredResult = result.filter((o) => {
          return o.year !== 1900 && o.year <= (new Date()).getFullYear();
        });

        const stats = filteredResult.reduce((acc, o) => {
          acc[o.year] = acc[o.year] || {
            books: 0,
            read: 0,
            progress: 0,
            months: {}
          };
          acc[o.year].months[o.month] = {
            books: o.books,
            read: o.read,
            progress: o.read / o.books * 100,
          };
          acc[o.year].books += o.books;
          acc[o.year].read += o.read;
          acc[o.year].progress = acc[o.year].read / acc[o.year].books * 100;

          return acc;
        }, {});

        const barChartMonthly = filteredResult.reduce((acc, o) => {
          acc.datasets[0].data.push({t: new Date(o.year, o.month), y: o.read});
          acc.datasets[1].data.push({t: new Date(o.year, o.month), y: o.books});
          return acc;
        }, {
          datasets: [
            {
              label: "Read",
              data: [],
              borderColor: "#42a131",
              backgroundColor: "#1c4917"
            },
            {
              label: "Books",
              data: [],
              borderColor: "#3e95cd",
              backgroundColor: "#3e95cd"
            },
          ],
        });

        const yearlyData = filteredResult.reduce((acc, o) => {
          acc[o.year] = acc[o.year] || {books: 0, read: 0};
          acc[o.year].books += o.books;
          acc[o.year].read += o.read;
          return acc;
        }, {});

        const barChartYearly = Object.keys(yearlyData).reduce((acc, y) => {
          const d = yearlyData[y];
          acc.datasets[0].data.push({t: new Date(y, 1), y: d.read});
          acc.datasets[1].data.push({t: new Date(y, 1), y: d.books});
          return acc;
        }, {
          datasets: [
            {
              label: "Read",
              data: [],
              borderColor: "#42a131",
              backgroundColor: "rgba(78,189,58,0.5)"
            },
            {
              label: "Books",
              data: [],
              borderColor: "#3e95cd",
              backgroundColor: "rgba(71,169,232,0.5)"
            },
          ],
        })

        this.stats = stats;
        this.barChartMonthly = barChartMonthly;
        this.barChartYearly = barChartYearly;
      });

    }
  }
}
</script>
