<template>
  <div class="box">

    <h2 class="subtitle">
      <nuxt-link :to="{name:'reading-list-id', params: {id: list.id}}">{{list.title}}</nuxt-link>
      <span v-if="list.archived">(Archived)</span>
    </h2>

    <b-progress :value="read/total*100" show-value type="is-info is-large" format="percent">
      {{read}} / {{total}} read
    </b-progress>

    <div v-if="read == total && total > 0">
      <h3 class="subtitle">Finished!</h3>
      <ReadingListEntry :entry="first" @read="$emit('read', first.book)" />
    </div>
    <div v-else-if="read == total && total == 0">
      <h3 class="subtitle">Nothing to read.
        <nuxt-link :to="{name:'reading-list-id', params:{id:list.id}}">Add books now !</nuxt-link>
      </h3>
    </div>
    <div v-else-if="next">
      <h3 class="subtitle">Next Title</h3>
      <ReadingListEntry :entry="next" @read="$emit('read', next.book)" />
    </div>

  </div>
</template>

<script>
import ReadingListEntry from "~/components/ReadingListEntry";

export default {
  name: "ReadingList",
  components: {ReadingListEntry},
  props: {
    list: {
      required: true,
    },
  },
  computed: {
    read() {
      return this.list.entries.filter(e => e.book.last_read_history && e.book.last_read_history.read_date).length;
    },
    total() {
      return this.list.entries.length;
    },
    first() {
      return this.list.entries?.[0];
    },
    next() {
      return this.list.entries.find(e => !e.book.last_read_history || !e.book.last_read_history.read_date);
    },
  },
}
</script>

<style scoped>

</style>
