<template>
  <section class="section">
    <h1 class="title">History</h1>

    <ReadingHistoryEntry v-for="entry in entries" :key="entry.id" :entry="entry" />
  </section>
</template>

<script>

import ReadingHistoryEntry from "~/components/ReadingHistoryEntry";
export default {
  name: "history",
  components: {ReadingHistoryEntry},
  data() {
    return {
      entries: [],
    };
  },

  methods: {
    updateComponent(route = this.$route) {
      this.$axios.$get('/reading-history/').then(
        response => {
          console.log(response);
          this.entries = response.results;
        }
      );
    },
  },

  beforeMount() {
    this.updateComponent();
  }
}
</script>
