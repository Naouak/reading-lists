<template>
  <div class="reading-report">
    <div class="page-header">
      <div class="navigation">
        <a class="button is-primary" :href="previous_period">Previous Period</a> <a class="button is-primary"
                                                                                  :href="next_period">Next Period</a>
      </div>
      <h1 class="title">Reading Report - {{ months[month] }} {{ year }}</h1>
    </div>


    <div class="global-stats">
      <div class="stat-block">
        <h2>Books Read</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ stats.read_books.length }}</span> books
        </div>
      </div>
      <div class="stat-block">
        <h2>Books Read per day</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ read_per_day }}</span> books
        </div>
      </div>
      <div class="stat-block">
        <h2>Max read in a day</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ max_read_in_a_day }}</span> books
        </div>
      </div>
      <div class="stat-block">
        <h2>Min read in a day</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ min_read_in_a_day }}</span> books
        </div>
      </div>
      <div class="stat-block">
        <h2>Days skipped</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ skipped_days }}</span> days
        </div>
      </div>
      <div class="stat-block">
        <h2>Series Read</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ read_series.length }}</span> series
        </div>
      </div>
      <div class="stat-block">
        <h2>Reading List Read</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ read_lists.length }}</span> lists
        </div>
      </div>
      <div class="stat-block">
        <h2>Publication Years</h2>
        <div class="stats-full-value">
          <span class="stats-value">{{ Math.min(...Object.keys(read_per_year)) }}</span>
          -
          <span class="stats-value">{{ Math.max(...Object.keys(read_per_year)) }}</span>
        </div>
      </div>
    </div>

    <ReadingReportLists :read_lists="read_lists" :read_series="read_series" :read_per_year="read_per_year"/>
    <ReadingWeeklyHeatmap :read_books="stats.read_books" />
    <ReadingReportWhatBook :read_books="stats.read_books" />

  </div>
</template>

<script>
import ReadingReportLists from "~/components/ReadingReportLists.vue";
import ReadingWeeklyHeatmap from "~/components/ReadingWeeklyHeatmap.vue";
import ReadingReportWhatBook from "~/components/ReadingReportWhatBook.vue";

export default {
  name: "ReadingReport",
  components: {ReadingReportWhatBook, ReadingWeeklyHeatmap, ReadingReportLists},
  props: {
    year: {
      default() {
        return parseInt(this.$route.params.year);
      },
      type: Number
    },
    month: {
      default() {
        if(this.$route.params.month){
          return parseInt(this.$route.params.month);
        }
        return null;
      },
      type: Number,
      required: false,
    }
  },
  data() {
    return {
      stats: {
        read_books: [],
        read_lists: {},
        read_series: {},
      },
      months: ["", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"],
    }
  },
  computed: {
    read_series() {
      const series = Object.keys(this.stats.read_series).reduce((acc, item) => {
        acc.push({
          title: item,
          read: this.stats.read_series[item]
        });
        return acc;
      }, []);
      series.sort((a, b) => b.read.length - a.read.length);
      return series;
    },
    read_lists() {
      const lists = Object.keys(this.stats.read_lists).reduce((acc, title) => {
        acc.push({
          title,
          ...this.stats.read_lists[title]
        });
        return acc;
      }, []);
      lists.sort((a, b) => b.read.length - a.read.length);
      return lists;
    },
    read_per_year() {
      return this.stats.read_books.reduce((acc, item) => {
        const year = new Date(item.book.pub_date).getFullYear();
        acc[year] = (acc[year] || 0) + 1;
        return acc
      }, {});
    },
    read_per_day() {
      return Math.round(this.stats.read_books.length / this.number_of_days * 100) / 100;
    },
    read_each_day() {
      return this.stats.read_books.reduce((acc, item) => {
        const date = new Date(item.read_date);
        const textDate = [date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()].join("-");
        acc[textDate] = (acc[textDate] || 0) + 1;
        return acc;
      }, {});
    },
    max_read_in_a_day() {
      return Math.max(...Object.values(this.read_each_day));
    },
    min_read_in_a_day() {
      return Math.min(...Object.values(this.read_each_day));
    },
    skipped_days() {
      return this.number_of_days - Object.values(this.read_each_day).length;
    },

    number_of_days() {
      if(this.month !== null){
        return new Date(this.year, this.month, 0).getDate();
      }
      return [...Array(12)].reduce((acc, _, month) => acc + new Date(this.year, month, 0).getDate(), 0);
    },
    previous_period() {
      if(this.month !== null){
        const month = (this.month - 1) || 12;
        const year = month === 12 ? this.year - 1 : this.year;
        return "/reading-report/" + year + "/" + month;
      }
      return "/reading-report/" + (this.year - 1) + "/";

    },
    next_period() {
      if(this.month !== null){
        const month = parseInt(this.month) === 12 ? 1 : (this.month - -1);
        const year = month === 1 ? this.year - -1 : this.year;
        return "/reading-report/" + year + "/" + month;
      }
      return "/reading-report/" + (this.year + 1) + "/";
    }
  },
  beforeMount() {
    this.updateComponent();
  },
  methods: {
    updateComponent() {
      const $axios = this.$axios;

      const apiParams = new URLSearchParams();
      if(this.month!== null){
        apiParams.append('month', this.month);
      }
      apiParams.append('year', this.year);

      $axios.$get('/reading-report/?' + apiParams.toString()).then(res => {
        this.stats = res;
      })
    }
  }
}
</script>

<style scoped>

</style>
