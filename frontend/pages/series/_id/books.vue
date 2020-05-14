<template>
  <div class="section">
    <h1 class="title">{{series.title}}</h1>
    <Book v-for="book in books" :key="book.id" :book="book" class="" />
  </div>
</template>

<script>
import Book from "~/components/Book";

/**
 * @typedef {Object} Book
 * @typedef {String} Book.cover_url
 * @typedef {String} Book.title
 */

export default {
  name: 'Books',
  components: {
    Book,
  },
  /**
   * @returns {{books: Book[]}}
   */
  data() {
    return {
      series: {},
      books: [],
    };
  },
  beforeMount() {
    this.$axios.$get('/series/'+this.$route.params.id+'/').then(response => {
      this.series = response;
    });

    this.$axios.$get('/book/?series='+this.$route.params.id).then(response => {
      this.books = response.results;
    });
  },
};
</script>
