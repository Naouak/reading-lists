<template>
  <section class="section">
    <h1 class="title">History</h1>

    <div class="box">
      <h2>All time</h2>
      <bar-chart :data="readSummary" :options="{
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'day'
                }
            }]
        }
    }" />
    </div>

    <div class="box">
      <h2>In the last <input type="number" v-model="recentHistoryDays"> days</h2>
      <bar-chart :data="recentReadSummary" :options="{
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'day'
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
      recentHistoryDays: 100,
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
        ],
      };
    }
  },

  methods: {
    fetchReadSummary() {
      this.$axios.$get('/reading-history-summary/').then(result => {
        this.readSummary = result.reduce((acc, data) => {
          acc.datasets[0].data.push({t: new Date(data.date), y: data.read});
          return acc;
        }, {
          datasets: [
            {
              label: "Read",
              data: [],
              borderColor: "#42a131",
              backgroundColor: "rgba(78,189,58,0.5)"
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
