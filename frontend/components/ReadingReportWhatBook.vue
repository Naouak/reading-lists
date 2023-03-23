<template>
  <div class="report-which-read">
    <div v-if="read_books.length > 0" class="report-which-read-first">
      <h2>First Read</h2>

      <ReadingListEntry :entry="read_books[0]" :readable="false" />
    </div>
    <div class="report-which-read-last" v-if="read_books.length > 0">
      <h2>Last Read</h2>
      <ReadingListEntry :entry="read_books[read_books.length - 1]" :readable="false" />
    </div>
  </div>
</template>

<script>
import ReadingListEntry from "~/components/ReadingListEntryNormal.vue";

export default {
  name: "ReadingReportWhatBook",
  components: {ReadingListEntry},
  props: {
    read_books: [],
  }
}
</script>

<style scoped>

</style>
