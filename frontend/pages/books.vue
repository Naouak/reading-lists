<template>
  <section class="section">
    <h1 class="title">Books</h1>
    <div class="card">
      <div class="card-content">
        <Pagination :page="page" :next-page-url="nextPageUrl" :previous-page-url="previousPageUrl" />
      </div>
      <div class="card-content">
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <input v-model="search" type="text" class="input" placeholder="Filter" />
                <span class="icon is-left"><b-icon icon="magnify" /></span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <section v-if="books && books.length" class="section card-content">
        <Book v-for="book in books" :key="book.id" :book="book" />
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
import Book from '../components/Book';
import Pagination from "~/components/Pagination";

/**
 * @typedef {Object} Book
 * @typedef {String} Book.cover_url
 * @typedef {String} Book.title
 */

export default {
  name: 'Books',
  components: {
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
      books: [],
      hasNextPage: false,
      hasPreviousPage: false,
    };
  },
  computed: {
    previousPageUrl() {
      return this.hasPreviousPage && {
        name: 'books',
        query: {
          page: this.page - 1,
          search: this.search,
        }
      };
    },
    nextPageUrl() {
      return this.hasNextPage && {
        name: 'books',
        query: {
          page: this.page + 1,
          search: this.search,
        }
      };
    }
  },
  watch: {
    $route(to, from) {
      this.updateComponent(to);
    },
    search(to, from) {
      if (to && from && to.trim() === from.trim()) {
        return;
      }
      const query = {
        page: 1,
      };

      if (to && to.trim().length > 0) {
        query.search = to;
      }

      this.$router.push({
        name: 'books',
        query,
      });
    }
  },
  methods: {
    updateComponent(route) {
      this.page = parseInt(route.query.page || 1);

      if (route.query.search !== this.search) {
        this.search = route.query.search;
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
      return '/book/?' + params.join('&');
    }
  },

  beforeMount() {
    this.updateComponent(this.$route);
  },
};
</script>
