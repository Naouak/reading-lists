<template>
  <section class="section columns">
    <div class="column">
      <h2 class="title">New titles</h2>
      <Book v-for="book in newBooks" :key="book.id" :book="book" />
    </div>
    <div class="column">
      <h2 class="title">Recent additions</h2>
      <Book v-for="book in recentBooks" :key="book.id" :book="book" />
    </div>
  </section>
</template>

<script>
import Book from "~/components/Book";
export default {
  name: 'HomePage',
  components: {Book},
  data(){
    return {
      recentBooks: [],
      newBooks: [],
    };
  },
  methods: {
    updateComponent(route = this.$route){
      this.$axios.$get('/book/?limit=50&ordering=-availability_date').then(
        response => {
          this.recentBooks = response.results
        }
      );
      this.$axios.$get('/book/?limit=50&ordering=-pub_date,title').then(
        response => {
          this.newBooks = response.results
        }
      );
    }
  },

  beforeMount() {
    this.updateComponent();
  }
};
</script>
