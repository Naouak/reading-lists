<template>
  <div class="recent-books-list">
    <h1 class="title">{{title}}</h1>
    <div class="book-list">
      <Book v-for="book in books" :key="book.id" :book="book" />
    </div>
  </div>
</template>
<script>
import Book from "~/components/Book.vue";

export default {
  name: "RecentBookList",
  components: { Book },
  props: {
    title: {},
    books: {}
  }
};
</script>
