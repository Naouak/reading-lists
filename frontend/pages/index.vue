<template>
  <section class="home-page section">
    <div class="recent-books-list">
      <h1 class="title">Recent additions</h1>
      <div class="book-list">
        <Book v-for="book in recentBooks" :key="book.id" :book="book" />
      </div>
    </div>
    <div class="recent-books-list">
      <h1 class="title">New titles</h1>
      <div class="book-list">
        <Book v-for="book in newBooks" :key="book.id" :book="book" />
      </div>
    </div>
    <div class="recent-books-list">
      <h1 class="title">New Infinity Comics</h1>
      <div class="book-list">
        <Book v-for="book in infinityComics" :key="book.id" :book="book" />
      </div>
    </div>
  </section>
</template>

<script>
import Book from "~/components/Book";

export default {
  name: 'HomePage',
  components: {Book},
  data() {
    return {
      recentBooks: [],
      newBooks: [],
      infinityComics: [],
    };
  },
  asyncData({$axios}) {
    const recentPromise = $axios.$get('/book/?limit=50&exclude_term=Infinity Comic&available_online=1&ordering=-availability_last_check').then(r => r.results);
    const newPromise = $axios.$get('/book/?limit=50&exclude_term=Infinity Comic&available_online=1&ordering=-pub_date,title').then(r => r.results);
    const infinityComicsPromise = $axios.$get('/book/?limit=50&search=Infinity Comic&available_online=1&ordering=-availability_date,title').then(r => r.results)

    return Promise.all([recentPromise, newPromise, infinityComicsPromise]).then(([recentBooks, newBooks, infinityComics]) => ({recentBooks, newBooks, infinityComics}));
  }
};
</script>
