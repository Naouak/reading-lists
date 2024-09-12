<template>
  <section class="section">
    <h1 class="title">Books</h1>
    <div class="card">
      <div class="card-content">
        <Pagination :page="page" :next-page-url="nextPageUrl" :previous-page-url="previousPageUrl" />
      </div>
      <SearchCard v-model="search" />
      <div class="card-content">
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <select v-model="available_online">
                  <option :value="null">All</option>
                  <option :value="1">Only Available</option>
                  <option :value="0">Only non Available</option>
                </select>
              </p>
            </div>
          </div>
        </div>
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <select v-model="ordering">
                  <option value="-created_date">Creation (Newest first)</option>
                  <option value="created_date">Creation (Oldest first)</option>
                  <option value="-pub_date">Publication (Newest first)</option>
                  <option value="pub_date">Publication (Oldest first)</option>
                  <option value="-availability_date">Availability (Newest first)</option>
                  <option value="availability_date">Availability (Oldest first)</option>
                  <option value="-availability_last_check">Found (Newest first)</option>
                  <option value="availability_last_check">Found (Oldest first)</option>
                </select>
              </p>
            </div>
          </div>
        </div>
      </div>

      <section v-if="books && books.length" class="books-books section card-content">
        <Book class="books-book" v-for="book in books" :key="book.id" :book="book" />
      </section>
      <section v-else class="section card-content">
        No results
      </section>

      <div class="card-content">
        <Pagination :page="page" :next-page-url="nextPageUrl" :previous-page-url="previousPageUrl" />
      </div>
    </div>


  </section>
</template>

<script>
import Book from "../components/Book";
import Pagination from "~/components/Pagination";
import SearchCard from "~/components/SearchCard.vue";

/**
 * @typedef {Object} Book
 * @typedef {String} Book.cover_url
 * @typedef {String} Book.title
 */

export default {
  name: 'Books',
  components: {
    SearchCard,
    Pagination,
    Book,
  },
  /**
   * @returns {{books: Book[]}}
   */
  data() {
    return {
      page: null,
      search: '',
      available_online: 1,
      ordering: "-availability_last_check",
      books: [],
      hasNextPage: false,
      hasPreviousPage: false,
    };
  },
  computed: {
    previousPageUrl() {
      return this.hasPreviousPage && this.buildRoute({page: this.page - 1});
    },
    nextPageUrl() {
      return this.hasNextPage && this.buildRoute({page: this.page + 1});
    }
  },
  watch: {
    $route(to) {
      this.updateComponent(to);
    },
    search(to, from) {
      if (to && from && to.trim() === from.trim()) {
        return;
      }
      this.$router.push(this.buildRoute({page: 1, search: to}))
    },
    available_online(to){
      this.$router.push(this.buildRoute({page: 1, available_online: to}))
    },
    ordering(to){
      this.$router.push(this.buildRoute({page: 1, ordering: to}))
    }
  },
  methods: {
    buildRoute(change){
      const query = {};
      query.page = change.page || this.page;
      query.search = change.search || this.search;
      query.available_online = change.available_online || this.available_online;
      query.ordering = change.ordering || this.ordering;
      return {name: 'books', query};
    },
    updateComponent(route) {
      this.page = parseInt(route.query.page || "1");

      if (route.query.search !== this.search) {
        this.search = route.query.search;
      }

      if(route.query.ordering !== undefined && route.query.ordering !== this.ordering){
        this.ordering = route.query.ordering;
      }
      if(route.query.available_online !== undefined && route.query.available_online !== this.available_online){
        this.available_online = route.query.available_online;
      }

      this.$axios.$get(this.getApiUrl()).then(response => {
        this.hasNextPage = !!response.next;
        this.hasPreviousPage = !!response.previous;
        this.books = response.results;
      });
    },
    getApiUrl() {
      const params = [];
      if (this.page > 1) {
        params.push("page=" + this.page);
      }
      if (this.search && this.search.trim().length > 0) {
        params.push("search=" + encodeURIComponent(this.search));
      }
      if (this.available_online !== null ) {
        params.push("available_online="+ (this.available_online?"1":"0"));
      }

      params.push("ordering="+this.ordering);
      params.push("limit=120");
      return '/book/?' + params.join('&');
    }
  },

  beforeMount() {
    this.updateComponent(this.$route);
  },
};
</script>
