<template>
  <div class="">
    <div class="cover">
      <a target="_blank" :href="book.read_online_url">
        <img :src="book.cover_url" :alt="book.title">
        <div class="cover-title">
          <div class="book-title">{{ book.title }}</div>
        </div>
      </a>


      <div class="mark-as-read">
        <span class="book-pub-date"><DateDisplay :date="book.pub_date" /></span>

        <span v-if="book.last_read_history">Read on <DateDisplay :date="book.last_read_history.read_date" /></span>
        <span v-else>Not read yet</span>
      </div>
    </div>
  </div>

</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  components: {DateDisplay},
  props: {
    book: {
      type: Object,
    },
  },
};
</script>
