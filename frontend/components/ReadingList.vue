<template>
  <div class="reading-list">
    <h2 class="reading-list-title">
      <b-icon v-if="list.series.length" icon="autorenew" title="This reading list is automatically filled with new releases." />
      <nuxt-link :to="{name:'reading-list-id', params: {id: list.id}}">{{list.title}}</nuxt-link>
      <span v-if="list.archived">(Archived)</span>
    </h2>

    <Progress class="progress-bar" :value="read/total*100">
      {{read}} / {{total}} read
    </Progress>

    <div v-if="read == total && total > 0">
      <h3 class="subtitle">Finished!</h3>
      <ReadingListEntryNormal :entry="first" @read="$emit('read', first.book)" />
    </div>
    <div v-else-if="read == total && total == 0">
      <h3 class="subtitle">Nothing to read.
        <nuxt-link :to="{name:'reading-list-id', params:{id:list.id}}">Add books now !</nuxt-link>
      </h3>
    </div>
    <div v-else-if="next">
      <ReadingListEntryNormal :entry="next" @read="$emit('read', next.book)" />
    </div>

  </div>
</template>

<script>
import ReadingListEntryNormal from "~/components/ReadingListEntryNormal";
import Progress from "~/components/Progress.vue";

export default {
  name: "ReadingList",
  components: {ReadingListEntryNormal, Progress},
  props: {
    list: {
      required: true,
    },
  },
  computed: {
    read() {
      return this.list.entries.filter(e => e.book.last_read_history && e.book.last_read_history.read_date && !e.book.last_read_history.want_to_reread).length;
    },
    total() {
      return this.list.entries.length;
    },
    first() {
      return this.list.entries?.[0];
    },
    next() {
      return this.list.entries.find(e => !e.book.last_read_history || !e.book.last_read_history.read_date || e.book.last_read_history.want_to_reread);
    },
  },
}
</script>

<style scoped>

</style>
