<template>
  <div class="card">
    <div class="card-content">
      <div class="field is-horizontal">
        <div class="field-body">
          <div class="field">
            <p class="control has-icons-left">
              <input v-model="search" type="text" class="input" placeholder="Filter" />
              <span class="icon is-left">
                <b-icon icon="magnify" />
              </span>
            </p>
          </div>
        </div>
      </div>
      <label class="checkbox">
        <input type="checkbox" v-model="hideSelectedItems">
        Hide selected items
      </label>
    </div>
    <div class="card-content">
      <nav class="pagination is-centered">
        <a class="pagination-previous" :disabled="!hasPreviousPage" @click="hasPreviousPage && (page=page-1)">Previous
          Page</a>
        <div class="pagination-list">
          <span class="pagination-link is-current">{{page}}</span>
        </div>
        <a class="pagination-next" :disabled="!hasNextPage" @click="hasNextPage && (page=page+1)">Next Page</a>
      </nav>
    </div>
    <ul class="card-content">
      <li class="box" v-for="book in availableBooks" :key="book.id">
        <div class="media">
          <div class="media-left">
            <figure style="width: 70px;">
              <img style="width: auto; height: auto;" :src="book.cover_url" :alt="book.title">
            </figure>
          </div>
          <div class="media-content">
            <div class="content">
              <div class="subtitle">{{book.title}}</div>
              <div>Published on
                <DateDisplay :date="book.pub_date" />
              </div>
            </div>

            <div class="field has-addons">
              <p class="control">
                <button class="button" v-if="!selectedBooks.includes(book.id)" @click="selectBook(book)">
                  <b-icon icon="plus" />
                  <span>Select</span>
                </button>
              </p>
              <p class="control">
                <a :href="book.read_online_url" target="_blank" class="button">
                  <b-icon icon="book-open-page-variant" />
                  <span>Read online</span></a>
              </p>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  name: "BookSelector",
  components: {DateDisplay},
  /**
   * @returns {{books: Book[]}}
   */
  props: {
    selectedBooks: {
      default: [],
    },
  },
  data() {
    return {
      page: 1,
      search: '',
      books: [],
      hasNextPage: false,
      hasPreviousPage: false,
      isScheduledForUpdate: false,
      hideSelectedItems: false,
    };
  },
  computed: {
    availableBooks() {
      if (!this.books) {
        return [];
      }
      let books = this.books;

      if (this.hideSelectedItems) {
        books = books.filter(b => !this.selectedBooks.includes(b.id));
      }

      return books;
    }
  },
  watch: {
    search(to, from) {
      if (to && from && to.trim() === from.trim()) {
        return;
      }
      this.page = 1;
      this.scheduleUpdate();
    },
    page() {
      this.scheduleUpdate();
    },
  },
  methods: {
    scheduleUpdate() {
      if (this.isScheduledForUpdate) {
        return;
      }
      this.isScheduledForUpdate = true;
      this.$nextTick(this.updateComponent);
    },
    updateComponent() {
      this.isScheduledForUpdate = false;
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
    },
    selectBook(book) {
      this.$emit('book-selected', book);
    }
  },

  beforeMount() {
    this.updateComponent();
  },
}
</script>

<style scoped>

</style>
