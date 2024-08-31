<template>
  <div class="reading-lists columns is-multiline">
    <div v-for="(entry) in entries" :key="entry.id" class="column">
      <Book :entry="entry"  v-if="entry.type !== 'empty_list' " @read="$emit('read', entry.book)"  />
      <ReadingListEnd :entry="entry" v-else />
    </div>
  </div>
</template>
<script>
import ReadingListEnd from "~/components/WhatsNext/ReadingListEnd.vue";
import Book from "~/components/WhatsNext/Book.vue";

export default {
  name: "Books",
  components: { Book, ReadingListEnd },
  props: {
    entries: {}
  }
};
</script>
