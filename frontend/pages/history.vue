<template>
  <section class="section">
    <h1 class="title">History</h1>

    <div class="section" v-for="h in history" :key="h.date">
      <h2 class="title">
        {{h.date}}
      </h2>
      <ReadingHistoryEntry v-for="entry in h.entries" :key="entry.id" :entry="entry" @remove="remove" />
    </div>

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

  computed: {
    history(){
      return this.entries.reduce((acc, entry) => {
        const date = new Date(entry.read_date);
        const isodate = [date.getFullYear(),("0"+(date.getUTCMonth()+1)).substr(-2),("0"+date.getDate()).substr(-2)].join('-');
        let current = acc[acc.length-1];
        if(!current || current?.date !== isodate){
          current = {date: isodate, entries: []};
          acc.push(current);
        }
        current.entries.push(entry);
        return acc;
      }, []);
    },
  },

  methods: {
    updateComponent(route = this.$route) {
      this.$axios.$get('/reading-history/').then(
        response => {
          this.entries = response.results;
        }
      );
    },
    remove(entry){
      this.$axios.$delete('/reading-history/'+entry.id+'/').then(() => this.updateComponent());
    }
  },

  beforeMount() {
    this.updateComponent();
  }
}
</script>
