<template>
  <div class="section">

    <h1 class="title">Series Progress</h1>

    <div class="list-block">
      <h2>Filters</h2>
      <div>
        <label><input type="checkbox" v-model="show_in_progress"> Show series in progress</label>
        <label><input type="checkbox" v-model="show_completed"> Show series completed</label>
        <label><input type="checkbox" v-model="show_not_started"> Show series not started</label>
      </div>
      <div>
        <label>
          Show series with at least <input type="number" v-model="min_book_count" /> books
        </label>
      </div>

    </div>

    <div class="list-block">
      <table class="series-read">
        <tr>
          <th>Series</th>
          <th>Start</th>
          <th>End</th>
          <th>Progress</th>
        </tr>
        <tr v-for="series in data" :key="series.series" class="series-read-entry">
          <td class="series-read-title">{{ series.series }}</td>
          <td class="series-read-start">{{ series.first_book }}</td>
          <td class="series-read-end">{{ series.last_book }}</td>
          <td class="series-read-progress">
            <Progress :value="series.book_read" :max="series.book_count">
              {{ series.book_read }} / {{ series.book_count }}
            </Progress>

          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import Progress from "~/components/Progress.vue";

export default {
  name: "completion",
  components: {Progress},
  computed: {
    data() {
      if (!this.stats) {
        return [];
      }
      let series = [...this.stats];

      if (!this.show_not_started) {
        series = series.filter(a => a.book_read > 0);
      }
      if (!this.show_in_progress) {
        series = series.filter(a => !(a.book_read > 0 && a.book_read < a.book_count));
      }
      if (!this.show_completed) {
        series = series.filter(a => a.book_read < a.book_count);
      }

      if (this.min_book_count > 0) {
        series = series.filter(a => a.book_count >= this.min_book_count);
      }

      if (this.sort_by === "start") {
        series.sort((a, b) => a.first_book < b.first_book ? -1 : a.first_book > b.first_book ? 1 : 0);
      } else if (this.sort_by === "progress") {
        series.sort((a, b) => a.progress < b.progress ? 1 : a.progress > b.progress ? -1 : 0);
      }

      return series;

    }
  },
  data() {
    return {
      stats: null,
      show_not_started: true,
      show_in_progress: true,
      show_completed: true,
      min_book_count: 50,
      sort_by: "progress",
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

      $axios.$get('/completion-series/?' + apiParams.toString()).then(result => {
        this.stats = result.map((a) => ({
          ...a,
          progress: a.book_read / a.book_count,
        }));
      });

    }
  }
}
</script>
