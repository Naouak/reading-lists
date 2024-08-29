<template>
  <div class="section">
    <h1 class="title">{{series.title}}</h1>
     <section v-if="books && books.length" class="books-books section card-content">
        <Book class="books-book" v-for="book in books" :key="book.id" :book="book" />
      </section>
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
