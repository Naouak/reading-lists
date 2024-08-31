<template>
  <div class="reading-list">
    <h2 class="reading-list-title">{{ entry.lists.map(l => l.title).sort().join(", ") }}</h2>
    <ReadingListEntryNormal :entry="entry" @read="$emit('read', entry.book)" />
  </div>
</template>
<script>
import ReadingListEntryNormal from "~/components/ReadingListEntryNormal.vue";

export default {
  name: "Book",
  components: { ReadingListEntryNormal },
  props: {
    entry: {}
  }
};
</script>
