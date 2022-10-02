<template>
  <div class="reading-list">
    <h2 class="reading-list-title">
      <b-icon v-if="list.series.length" icon="autorenew" title="This reading list is automatically filled with new releases." />
      <nuxt-link :to="{name:'reading-list-id', params: {id: list.id}}">{{list.title}}</nuxt-link>
      <span v-if="list.archived">(Archived)</span>
    </h2>

    <b-progress class="reading-list-progress" :value="read/total*100" show-value type="is-info is-large" format="percent">
      {{read}} / {{total}} read
    </b-progress>

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

<style>
.reading-list{
  box-shadow: 0 2px 3px rgb(10 10 10 / 10%), 0 0 0 1px rgb(10 10 10 / 10%);
  border-radius: 5px;
  min-width: 250px;
  overflow: clip;
}

.reading-list-title{
  padding: 5px;
  text-align: center;
  font-weight: bolder;
}

.reading-list-title a{
  color: #363636;
}

.reading-list .reading-list-progress{
  margin-bottom: 0;
}

.reading-list .reading-list-progress progress::-webkit-progress-bar{
  background-color: #f0e0e0;
}

.reading-list .reading-list-progress progress::-webkit-progress-value{
  background-color: red;
}

.reading-list .reading-list-progress .progress-value{
  color: #363636;
}

.reading-list .reading-list-progress .progress{
    border-radius: 0;

  }
</style>

<script>
import ReadingListEntryNormal from "~/components/ReadingListEntryNormal";

export default {
  name: "ReadingList",
  components: {ReadingListEntryNormal},
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
