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

<style>
.home-page .column{
  width: 100%;
}

.book-list{
  max-width: 100%;
  display: flex;
  overflow-x: auto;
}
.book-list > *{
  margin: 6px;
  min-width: 250px;
}

.recent-books-list{
  margin-bottom: 50px;
}
</style>

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
    const recentPromise = $axios.$get('/book/?limit=50&exclude_term=Infinity Comic&ordering=-availability_date').then(r => r.results);
    const newPromise = $axios.$get('/book/?limit=50&exclude_term=Infinity Comic&ordering=-pub_date,title').then(r => r.results);
    const infinityComicsPromise = $axios.$get('/book/?limit=50&search=Infinity Comic&ordering=-availability_date,title').then(r => r.results)

    return Promise.all([recentPromise, newPromise, infinityComicsPromise]).then(([recentBooks, newBooks, infinityComics]) => ({recentBooks, newBooks, infinityComics}));
  }
};
</script>
