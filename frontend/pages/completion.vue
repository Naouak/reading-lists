<template>
  <div class="section">
    <h1 class="title">Library completion stats</h1>
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

export default {
  name: "completion",
  computed: {},
  data() {
    return {
      stats: null,
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


      return {
        stats,
      };
    });
  }
}
</script>

<style scoped>

</style>
