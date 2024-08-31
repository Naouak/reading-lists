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

    <BlockedBooks v-if="blockedBooks" :blocked-books="blockedBooks" />

    <div class="reading-lists columns is-multiline" v-if="!fullView">
      <div v-for="(entry) in booksToReadToDisplay" :key="entry.id" class="column">
        <div class="reading-list" v-if="entry.type !== 'empty_list' ">
          <h2 class="reading-list-title">{{ entry.lists.map(l => l.title).sort().join(", ") }}</h2>
          <ReadingListEntryNormal :entry="entry" @read="markAsRead(entry.book)" />
        </div>
        <div class="reading-list-end" v-else>
          <h2 class="reading-list-title">{{ entry.list.title }}</h2>
          <div>
            <div class="reading-list-entry">
              <div class="cover">
                <nuxt-link class="reading-list-end-cover" :to="{name:'reading-list-id', params: {id: entry.list.id}}">
                  The reading list {{ entry.list.title }} is done.
                </nuxt-link>


                <div class="mark-as-read">
                  <span class="book-pub-date"></span>
                  <nuxt-link class="mark-as-read-button button"
                             :to="{name:'reading-list-id', params: {id: entry.list.id}}">
                    <b-icon icon="check" />
                    <span>Edit List</span>
                  </nuxt-link>
                </div>
              </div>


            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="list-block" v-else>
      <table class="whats-next-full-list">
        <tr>
          <th>Title</th>
          <th>Read?</th>
          <th>Publication Date</th>
          <th>Reading Lists</th>
        </tr>
        <tr v-for="(entry) in booksToReadWithoutLists" :key="entry.id" :class="{
          read: !!entry.book.last_read_history
        }">
          <td>{{ entry.book.title }}</td>
          <td>{{ entry.book.last_read_history ? "Read" : "" }}</td>
          <td>{{ entry.book.pub_date }}</td>
          <td>{{ entry.lists.map(l => l.title).sort().join(", ") }}</td>
        </tr>
      </table>

    </div>
  </div>
</template>

<script>

import ReadingListEntryNormal from "~/components/ReadingListEntryNormal";
import BlockedBooks from "~/components/BlockedBooks";
import { sortReadingLists } from "~/utils/reading-list-sort";

export default {
  name: "reading-list",
  components: {
    BlockedBooks,
    ReadingListEntryNormal
  },
  data() {
    return {
      booksToRead: [],
      filterRead: true,
      fullView: false,
      blockedBooks: null,
      numberToShow: 50,
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
      this.$axios.$get(this.getApiUrl(route)).then(response => {
        [this.booksToRead, this.blockedBooks] = sortReadingLists(response.results);
      });
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
      this.$api.bookRead(book).then(() => this.updateComponent());
    }
  }

};
</script>
