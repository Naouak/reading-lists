<template>
  <div class="">
    <div class="page-header reading-lists-header section">
      <h1 class="title">What's next?</h1>
    </div>

    <div class="box">
      <label>
      <input type="checkbox" v-model="fullView"> FULL VIEW
      </label>
    </div>

    <div class="reading-lists columns is-multiline" v-if="!fullView">
      <div v-for="(entry) in booksToReadToDisplay" :key="entry.book.id" class="column">
        <div class="reading-list">
          <h2 class="reading-list-title">{{entry.lists.map(l => l.title).sort().join(', ')}}</h2>
          <ReadingListEntryNormal :entry="entry" @read="markAsRead(entry.book)" />
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
        <tr v-for="(entry) in booksToRead" :key="entry.book.id" :class="{
          read: !!entry.book.last_read_history
        }">
          <td>{{entry.book.title}}</td>
          <td>{{entry.book.last_read_history?"Read":""}}</td>
          <td>{{entry.book.pub_date}}</td>
          <td>{{entry.lists.map(l => l.title).sort().join(', ')}}</td>
        </tr>
      </table>

    </div>
  </div>
</template>

<script>

import ReadingListEntryNormal from "~/components/ReadingListEntryNormal";

export default {
  name: "reading-list",
  components: {
    ReadingListEntryNormal
  },
  data() {
    return {
      booksToRead: [],
      filterRead: true,
      fullView: false,
    };
  },
  computed: {
    booksToReadToDisplay() {
      let booksToRead = this.booksToRead;

      if (this.filterRead) {
        booksToRead = booksToRead.filter(b => b.book.last_read_history === null);
      }

      return booksToRead.slice(0, 50);
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
      this.$axios.$get(this.getApiUrl(route)).then(response => {
        const readingLists = response.results;
        // Make a reference of each objects
        const originalReadingLists = JSON.parse(JSON.stringify(response.results));

        const booksToRead = [];

        while (true) {
          // Fetch the next book in each list sorted by date
          const nextBooks = readingLists
            // Take the next entry of each reading list
            .map(list => {
              return list.entries.length > 0 ? list.entries[0] : null;
            })
            // Remove empty reading list entries
            .filter(a => a)
            // Sort books by pub date
            .sort((a, b) => {
              if (!a.book.pub_time) {
                a.book.pub_time = new Date(a.book.pub_date).getTime();
              }
              if (!b.book.pub_time) {
                b.book.pub_time = new Date(b.book.pub_date).getTime();
              }

              return a.book.pub_time >= b.book.pub_time ? 1 : -1;
            });

          // No books left
          if (nextBooks.length === 0) {
            break;
          }

          let nextBook = nextBooks.find(entry => {
            // Check if book is not in another reading list
            // If it's the first entry of a list, we don't care about it. (as it is also a candidate for next book)
            return !readingLists.find(
              r => r.entries.map(e => e.book.id).indexOf(entry.book.id) > 0
            );
          });

          if (!nextBook) {
            // This is an edge case if there is two lists with circular dependency
            // If no book was the first of every list, we just take the older one first
            nextBook = nextBooks[0];
          }

          nextBook.lists = [];

          // Clean the selected books from all readinglists
          readingLists.forEach((r, i) => {
            const entries = r.entries.map(e => e.book.id);
            const index = entries.indexOf(nextBook.book.id);
            if (index >= 0) {
              r.entries.splice(index, 1);
              nextBook.lists.push(originalReadingLists[i]);
            }
          });

          booksToRead.push(nextBook);
        }

        this.booksToRead = booksToRead;
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
