<template>
  <div class="section">
    <h1 class="title">Statistics</h1>

    <div class="box">
      <h2 class="subtitle">Set Target</h2>
      <div class="columns">
        <div class="column">
          <button class="button" @click="target_percentage=Math.ceil(read_progress)">Next % ({{ Math.ceil(read_progress) }}%)
          </button>
          <button class="button" @click="target_percentage=Math.ceil(read_progress)+1">
            Next + 1 % ({{ Math.ceil(read_progress) + 1 }}%)
          </button>
          <button class="button" @click="target_percentage=50">50%</button>
          <button class="button" @click="target_percentage=70">70%</button>
          <button class="button" @click="target_percentage=100">100%</button>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Total Progress</h2>
      <Progress :value="read_progress">{{ stats.read_books }} / {{ stats.total_books }} read ({{ read_progress }}%)
      </Progress>
    </div>

    <div class="box">
      <h2 class="subtitle">Reading progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Read last week</div>
          <div class="title">{{ stats.read_last_week }} ({{ read_last_week_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Read last month</div>
          <div class="title">{{ stats.read_last_month }} ({{ read_last_month_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Read last year</div>
          <div class="title">{{ stats.read_last_year }} ({{ read_last_year_progress }})</div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Time to read up to <input type="number" v-model="target_percentage"
                                                     step="10" min="10" max="100">%</h2>
      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Time to finish (based on last week)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_week,7,stats.read_books,stats.total_books,target_percentage / 100)" />
          </div>
        </div>
        <div class="column">
          <div class="subtitle">Time to finish (based on last month)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_month,30,stats.read_books,stats.total_books,target_percentage / 100)" />
          </div>
        </div>
        <div class="column">
          <div class="subtitle">Time to finish (based on last year)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_year,365,stats.read_books,stats.total_books,target_percentage / 100)" />
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Available catalog progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Added and available last week</div>
          <div class="title">{{ stats.available_last_week }} ({{ available_last_week_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added and available last month</div>
          <div class="title">{{ stats.available_last_month }} ({{ available_last_month_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added and available last year</div>
          <div class="title">{{ stats.available_last_year }} ({{ available_last_year_progress }})</div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Time to be up to date (target: <input type="number" v-model="target_percentage" step="10"
                                                                 min="10" max="100">%)</h2>
      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Time to finish (based on last week)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_week,7,stats.read_books,stats.total_books,target_percentage / 100,stats.available_last_week)" />
          </div>
        </div>
        <div class="column">
          <div class="subtitle">Time to finish (based on last month)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_month,30,stats.read_books,stats.total_books,target_percentage / 100,stats.available_last_month)" />
          </div>
        </div>
        <div class="column">
          <div class="subtitle">Time to finish (based on last year)</div>
          <div class="title">
            <TimeLeft
              :time_left="timeToReadEverything(stats.read_last_year,365,stats.read_books,stats.total_books,target_percentage / 100,stats.available_last_year)" />
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="subtitle">Catalog progress</h2>

      <div class="columns" style="text-align: center">
        <div class="column">
          <div class="subtitle">Added last week</div>
          <div class="title">{{ stats.added_last_week }} ({{ added_last_week_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added last month</div>
          <div class="title">{{ stats.added_last_month }} ({{ added_last_month_progress }})</div>
        </div>
        <div class="column">
          <div class="subtitle">Added last year</div>
          <div class="title">{{ stats.added_last_year }} ({{ added_last_year_progress }})</div>
        </div>
      </div>
    </div>

    <StatsFuture
      :total_book="stats.total_books"
      :total_read="stats.read_books"
      :read_per_month="stats.read_last_month"
      :added_per_month="stats.added_last_month"
    />

    <div class="box">
      <a class="button is-primary" href="/reading-report/">Monthly Reports</a>
      <a class="button is-primary" :href="'/reading-report/'+(new Date().getFullYear())">Yearly Reports</a>
    </div>


  </div>
</template>

<script>

import Progress from "~/components/Progress.vue";
import TimeLeft from "~/components/TimeLeft";
import StatsFuture from "~/components/StatsFuture.vue";


export default {
  name: "Statistics",
  components: { StatsFuture, TimeLeft, Progress },
  data() {
    return {
      "target_percentage": 100
    };
  },
  asyncData({ $axios }) {
    return $axios.$get("/reading-statistics/").then(result => {
      return {
        "stats": result
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
    }
  },
  methods: {
    timeToReadEverything(read, duration, done, total, targetRatio, added = 0) {
      // We're solving this equation (when the number read over time crosses the number added over time):
      // read * x / duration + done = (added * x / duration + total) * targetRatio
      // Which gives:
      // x = duration * (total * targetRatio - done) / (read - added * targetRatio )

      const daysLeft = Math.floor(duration * (total * targetRatio - done) / (read - added * targetRatio));

      if (daysLeft < 0 && done < total * targetRatio) {
        return 0;
      }

      return daysLeft;
    }
  }

};
</script>
