<template>
  <div class="">
    <div class="page-header reading-lists-header section">
      <h1 class="title">What's next?</h1>
    </div>

    <div class="box">
      <label>
        <input type="checkbox" v-model="fullView"> FULL VIEW
      </label>

      <label>
        <input type="number" v-model="numberToShow"> books shown
      </label>
    </div>

    <div class="whats-next-list">
      <div class="whats-next-loader" v-if="status">
        <span class="loader-container"><span class="loader"></span></span> {{ status }}...
      </div>

      <BlockedBooks v-if="blockedBooks" :blocked-books="blockedBooks" />

      <Books :entries="booksToReadToDisplay"
             @read="markAsRead" v-if="!fullView" />
      <Table :books-to-read-without-lists="booksToReadWithoutLists" v-else />
    </div>

  </div>
</template>

<script>

import BlockedBooks from "~/components/BlockedBooks";
import { sortReadingLists } from "~/utils/reading-list-sort";
import Books from "~/components/WhatsNext/Books.vue";
import Table from "~/components/WhatsNext/Table.vue";

export default {
  name: "reading-list",
  components: {
    Table,
    Books,
    BlockedBooks
  },
  data() {
    return {
      booksToRead: [],
      filterRead: true,
      fullView: false,
      blockedBooks: null,
      numberToShow: 50,
      status: null
    };
  },
  computed: {
    booksToReadWithoutLists() {
      return this.booksToRead.filter(b => b.book);
    },
    booksToReadToDisplay() {
      let booksToRead = this.booksToRead;

      if (this.filterRead) {
        booksToRead = booksToRead.filter(b =>
          !b?.book?.last_read_history ||
          !b?.book?.last_read_history?.read_date ||
          b?.book?.last_read_history?.want_to_reread
        );
      }

      return booksToRead.slice(0, this.numberToShow);
    }
  },
  watch: {
    $route(to) {
      this.updateComponent(to);
    }
  },
  beforeMount() {
    this.updateComponent(this.$route);
  },
  methods: {
    updateComponent(route = this.$route) {
      this.readingLists = [];
      this.blockedBooks = null;
      this.status = "loading";
      this.$axios.$get(this.getApiUrl(route)).then(response => {
        this.status = "sorting";
        [this.booksToRead, this.blockedBooks] = sortReadingLists(response.results);
        this.status = null;
      })
    },
    getApiUrl(route = this.$route) {
      const params = [];
      if (parseInt(route.query.archived) === 1) {
        params.push(["archived", "1"]);
      } else {
        params.push(["archived", "0"]);
      }

      const queryString = params.map(([a, b]) => encodeURIComponent(a) + "=" + encodeURIComponent(b)).join("&");
      return "/reading-list/?" + queryString;
    },
    markAsRead(book) {
      this.status = 'updating';
      this.$api.bookRead(book).then(() => this.updateComponent());
    }
  }

};
</script>
