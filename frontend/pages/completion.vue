<template>
  <div class="section">
    <h1 class="title">Library completion stats</h1>

    <div style="" class="box">
      <bar-chart :data="barChartYearly" :options="{
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

    <div class="columns is-multiline">
      <div class="box column is-2" v-for="(data, year) in stats" :key="year">
        <h1 class="title">{{year}}</h1>
        <b-progress :value="data.progress" show-value type="is-success is-info is-large" format="percent">
            {{data.read}} / {{data.books}} read
        </b-progress>
        <div v-for="(stat, month) in data.months" :key="month">
          <b-progress :value="stat.progress" show-value type="is-info is-large" format="percent">
            {{months[month]}} - {{stat.read}} / {{stat.books}} read
          </b-progress>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import BarChart from "~/components/BarChart";
export default {
  name: "completion",
  components: {BarChart},
  computed: {},
  data() {
    return {
      stats: null,
      barChart: null,
      months: ["", "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"]
    };
  },
  asyncData({$axios}) {
    return $axios.$get('/completion-statistics/').then(result => {
      const stats = result.reduce((acc, o) => {
        acc[o.year] = acc[o.year] || {
          books: 0,
          read: 0,
          progress: 0,
          months: {

          }
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

      const barChartMonthly = result.reduce((acc, o) => {
        acc.datasets[0].data.push({t: new Date(o.year, o.month),y:o.books});
        acc.datasets[1].data.push({t: new Date(o.year, o.month), y:o.read});
        return acc;
      }, {
        datasets: [
          {
            label: "Books",
            data: [],
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd"
          },
          {
            label: "Read",
            data: [],
            borderColor: "#42a131",
            backgroundColor: "#42a131"
          }
        ],
      });

      const yearlyData = result.reduce((acc, o) => {
        acc[o.year] = acc[o.year] || {books:0, read: 0};
        acc[o.year].books += o.books;
        acc[o.year].read += o.read;
        return acc;
      }, {});

      const barChartYearly = Object.keys(yearlyData).reduce((acc, y) => {
        const d = yearlyData[y];
        acc.datasets[0].data.push({t: new Date(y, 1),y:d.books});
        acc.datasets[1].data.push({t: new Date(y, 1), y:d.read});
        return acc;
      }, {
        datasets: [
          {
            label: "Books",
            data: [],
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd"
          },
          {
            label: "Read",
            data: [],
            borderColor: "#42a131",
            backgroundColor: "#42a131"
          }
        ],
      })

      return {
        stats,
        barChartMonthly,
        barChartYearly,
      };
    });
  }
}
</script>

<style scoped>

</style>
