<template>
  <section class="section">
    <h1 class="title">History</h1>

    <ReadingHistoryEntry v-for="entry in entries" :key="entry.id" :entry="entry" @remove="remove" />
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
      this.loading = true;
      this.$axios.$get('/reading-history/').then(
        response => {
          this.loading = false;
          this.entries = response.results;
        }
      );
    },
    remove(entry){
      this.loading = true;
      this.$axios.$delete('/reading-history/'+entry.id+'/').then(() => this.updateComponent());
    }
  },

  beforeMount() {
    this.updateComponent();
  }
}
</script>
