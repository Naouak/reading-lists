<template>
  <div class="section">
    <h1 class="title">Statistics</h1>
    <div class="box">
      <h2 class="subtitle">Total Progress</h2>
      <b-progress :value="read_progress" show-value type="is-info is-large" format="percent">
        {{stats.read_books}} / {{stats.total_books}} read ({{read_progress}}%)
      </b-progress>
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
      </div>
    </div>


  </div>
</template>

<script>

export default {
  name: "statistics",
  computed: {
    read_last_week_progress() {
      let progress = (this.stats.read_last_week / (this.stats.read_previous_week || this.stats.read_last_week || 1) * 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    read_last_month_progress() {
      let progress = (this.stats.read_last_month / (this.stats.read_previous_month || this.stats.read_last_month || 1) * 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    added_last_week_progress() {
      let progress = (this.stats.added_last_week / (this.stats.added_previous_week || this.stats.added_last_week || 1) * 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    added_last_month_progress() {
      let progress = (this.stats.added_last_month / (this.stats.added_previous_month || this.stats.added_last_month || 1) * 100) | 0;
      if (progress >= 0) {
        progress = "+" + progress;
      }
      return progress + "%";
    },
    read_progress() {
      return ((this.stats.read_books / this.stats.total_books * 10000) | 0) / 100;
    },
  },
  asyncData({$axios}) {
    return $axios.$get('/reading-statistics/').then(result => {
      return {
        'stats': result,
      };
    });
  }
}
</script>

<style scoped>

</style>
