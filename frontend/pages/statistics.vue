<template>
  <div class="section">
    <h1 class="title">Statistics</h1>
    <div class="box">
      <h2 class="subtitle">Total Progress</h2>
      <Progress :value="read_progress">{{stats.read_books}} / {{stats.total_books}} read ({{read_progress}}%)</Progress>
    </div>

    <div class="box">
      <h2 class="subtitle">Reading progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Read last week</div>
          <div class="title">{{stats.read_last_week}} ({{read_last_week_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Read last month</div>
          <div class="title">{{stats.read_last_month}} ({{read_last_month_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Read last year</div>
          <div class="title">{{stats.read_last_year}} ({{read_last_year_progress}})</div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Available catalog progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Added and available last week</div>
          <div class="title">{{stats.available_last_week}} ({{available_last_week_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added and available last month</div>
          <div class="title">{{stats.available_last_month}} ({{available_last_month_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added and available last year</div>
          <div class="title">{{stats.available_last_year}} ({{available_last_year_progress}})</div>
        </div>
      </div>
    </div>
    <div class="box">
      <h2 class="subtitle">Catalog progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Added last week</div>
          <div class="title">{{stats.added_last_week}} ({{added_last_week_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added last month</div>
          <div class="title">{{stats.added_last_month}} ({{added_last_month_progress}})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added last year</div>
          <div class="title">{{stats.added_last_year}} ({{added_last_year_progress}})</div>
        </div>
      </div>
    </div>

    <div class="box">
      <a class="button is-primary" href="/reading-report/">Monthly Reports</a>
      <a class="button is-primary" :href="'/reading-report/'+(new Date().getFullYear())">Yearly Reports</a>
    </div>


  </div>
</template>

<script>

import Progress from "~/components/Progress.vue";

export default {
  name: "Statistics",
  components: {Progress},
  asyncData({$axios}) {
    return $axios.$get('/reading-statistics/').then(result => {
      return {
        'stats': result,
      };
    });
  },
  computed: {
    read_last_week_progress() {
      let progress = (this.stats.read_last_week / (this.stats.read_previous_week || this.stats.read_last_week || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    read_last_month_progress() {
      let progress = (this.stats.read_last_month / (this.stats.read_previous_month || this.stats.read_last_month || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    read_last_year_progress() {
      let progress = (this.stats.read_last_year / (this.stats.read_previous_year || this.stats.read_last_year || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    added_last_week_progress() {
      let progress = (this.stats.added_last_week / (this.stats.added_previous_week || this.stats.added_last_week || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    added_last_month_progress() {
      let progress = (this.stats.added_last_month / (this.stats.added_previous_month || this.stats.added_last_month || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    added_last_year_progress() {
      let progress = (this.stats.added_last_year / (this.stats.added_previous_year || this.stats.added_last_year || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    available_last_week_progress() {
      let progress = (this.stats.available_last_week / (this.stats.available_previous_week || this.stats.available_last_week || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    available_last_month_progress() {
      let progress = (this.stats.available_last_month / (this.stats.available_previous_month || this.stats.available_last_month || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    available_last_year_progress() {
      let progress = (this.stats.available_last_year / (this.stats.available_previous_year || this.stats.available_last_year || 1) * 100 - 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    read_progress() {
      return ((this.stats.read_books / this.stats.total_books * 10000) | 0) / 100;
    },
  },

}
</script>
