<template>
  <section class="section">
    <h1 class="title">History</h1>

    <label>
      <input type="radio" v-model="displayedChart" value="all-time" /> All time
    </label>
    <label>
      <input type="radio" v-model="displayedChart" value="recent" /> Recent
    </label>
    <label>
      <input type="radio" v-model="displayedChart" value="none" /> Don't show
    </label>

    <div class="box" v-if="displayedChart === 'all-time'">
      <h2>All time</h2>
      <bar-chart :data="readSummary" :options="{
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'day'
                }
            }],
            yAxes: [{
              ticks: {
                suggestedMin: 0
              }
            }]
        }
    }" />
    </div>

    <div class="box" v-if="displayedChart === 'recent'">
      <h2>In the last <input type="number" v-model="recentHistoryDays"> days</h2>
      <bar-chart :data="recentReadSummary" :options="{
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'day'
                }
            }],
            yAxes: [{
              ticks: {
                suggestedMin: 0
              }
            }]
        }
    }" />
    </div>

    <div class="section" v-for="h in history" :key="h.date">
      <h2 class="title">
        <RelativeDateDisplay :date="h.date" />
        ({{ h.entries.length }} entries)
      </h2>
      <ReadingHistoryEntry v-for="entry in h.entries" :key="entry.id" :entry="entry" @remove="remove" />
    </div>

  </section>
</template>

<script>
import ReadingHistoryEntry from "~/components/ReadingHistoryEntry";
import RelativeDateDisplay from "~/components/RelativeDateDisplay";
import BarChart from "~/components/BarChart";

export default {
  name: "history",
  components: {RelativeDateDisplay, ReadingHistoryEntry, BarChart},
  data() {
    return {
      readSummary: null,
      recentHistoryDays: 180,
      displayedChart: 'recent',
      entries: [],
    };
  },

  computed: {
    history() {
      return this.entries.reduce((acc, entry) => {
        const date = new Date(entry.read_date);
        const isodate = [date.getFullYear(), ("0" + (date.getUTCMonth() + 1)).substr(-2), ("0" + date.getDate()).substr(-2)].join('-');
        let current = acc[acc.length - 1];
        if (!current || current?.date !== isodate) {
          current = {date: isodate, entries: []};
          acc.push(current);
        }
        current.entries.push(entry);
        return acc;
      }, []);
    },
    recentReadSummary() {
      const recentCutOff = new Date();
      recentCutOff.setDate(recentCutOff.getDate() - this.recentHistoryDays); // 100 days ago

      return {
        datasets: [
          {
            label: "Read",
            data: this.readSummary?.datasets[0]?.data?.filter(data => {
              return data.t.getTime() > recentCutOff.getTime();
            }) || [],
            borderColor: "#42a131",
            backgroundColor: "rgba(78,189,58,0.5)"
          },
          {
            label: "7 Days average",
            type: 'line',
            data: this.readSummary?.datasets[1]?.data?.filter(data => {
              return data.t.getTime() > recentCutOff.getTime();
            }) || [],
            borderWidth: 0,
            pointRadius: 1,
            borderColor: "#478da6",
            fill: false
          },
            {
              label: "30 Days average",
              type: 'line',
              data:  this.readSummary?.datasets[2]?.data?.filter(data => {
              return data.t.getTime() > recentCutOff.getTime();
            }) || [],
              borderWidth: 0,
              pointRadius: 1,
              borderColor: "#0b2796",
              fill: false
            },
        ],
      };
    }
  },

  methods: {
    fetchReadSummary() {
      this.$axios.$get('/reading-history-summary/').then(result => {
        let sevenDaysAverage = [];
        let thirtyDaysAverage = [];
        this.readSummary = result.reduce((acc, data) => {
          const date = new Date(data.date);

          const lastWeek = new Date();
          lastWeek.setTime(date.getTime() - 6*24*3600*1000);

          const lastMonth = new Date();
          lastMonth.setTime(date.getTime() - 29*24*3600*1000);

          sevenDaysAverage = sevenDaysAverage.filter(d => {
            return d.t.getTime() >= lastWeek.getTime();
          });

          thirtyDaysAverage = thirtyDaysAverage.filter(d => {
            return d.t.getTime() >= lastMonth.getTime();
          });

          const dataPoint = {t: date, y: data.read};
          sevenDaysAverage.push(dataPoint);
          thirtyDaysAverage.push(dataPoint);
          acc.datasets[0].data.push(dataPoint);
          acc.datasets[1].data.push({
            t: date,
            y: sevenDaysAverage.reduce((acc, data) => acc + data.y, 0) / 7
          });
          acc.datasets[2].data.push({
            t: date,
            y: thirtyDaysAverage.reduce((acc, data) => acc + data.y, 0) / 30
          });
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
              label: "7 Days average",
              type: 'line',
              data: [],
              borderWidth: 0,
              pointRadius: 1,
              borderColor: "#478da6",
              fill: false
            },
            {
              label: "30 Days average",
              type: 'line',
              data: [],
              borderWidth: 0,
              pointRadius: 1,
              borderColor: "#0b2796",
              fill: false
            },
          ],
        });
      });
    },
    updateComponent(route = this.$route) {
      this.$axios.$get('/reading-history/').then(
        response => {
          this.entries = response.results;
        }
      );
    },
    remove(entry) {
      this.$axios.$delete('/reading-history/' + entry.id + '/').then(() => this.updateComponent());
    }
  },

  beforeMount() {
    this.updateComponent();
    this.fetchReadSummary();
  }
}
</script>
