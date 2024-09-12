<template>
  <section class="home-page section">
    <RecentBookList title="Recent additions" :books="recentBooks" />
    <RecentBookList title="New titles" :books="newBooks" />
    <RecentBookList title="New Infinity Comics" :books="infinityComics" />
  </section>
</template>

<script>
import RecentBookList from "~/components/RecentBookList.vue";

export default {
  name: 'HomePage',
  components: { RecentBookList},
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
