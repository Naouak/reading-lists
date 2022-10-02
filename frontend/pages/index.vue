<template>
  <section class="home-page section">
    <div class="">
      <h2 class="title">New titles</h2>
      <div class="book-list">
        <Book v-for="book in newBooks" :key="book.id" :book="book" />
      </div>
    </div>
    <div class="">
      <h2 class="title">Recent additions</h2>
      <div class="book-list">
        <Book v-for="book in recentBooks" :key="book.id" :book="book" />
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
    };
  },
  asyncData({$axios}) {
    const recentPromise = $axios.$get('/book/?limit=50&ordering=-availability_date').then(r => r.results);
    const newPromise = $axios.$get('/book/?limit=50&ordering=-pub_date,title').then(r => r.results);

    return Promise.all([recentPromise, newPromise]).then(([recentBooks, newBooks]) => ({recentBooks, newBooks}));
  }
};
</script>
