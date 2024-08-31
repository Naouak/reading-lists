<template>
  <div class="card">
    <div class="card-content">
      <div class="field is-horizontal">
        <div class="field-body">
          <div class="field">
            <p class="control has-icons-left">
              <input v-model="search" type="text" class="input" placeholder="Filter" v-on:keyup.enter="selectTarget" v-on:keyup.down="target+=1" v-on:keyup.up="target = Math.max(target - 1, 0)" />
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
      <label class="checkbox">
        <input type="checkbox" v-model="available_only">
        Show Only available online books
      </label>
    </div>
    <div class="card-content">
      <BookSelectorPagination :has-next-page="hasNextPage" :has-previous-page="hasPreviousPage" :max-page="maxPage" v-model="page" />
    </div>
    <ul class="card-content">
      <li class="box" v-for="(book, index) in availableBooks" :key="book.id" :class="{'book-selector-target': index === target}">
        <BookSelectorResult :book="book" :selected="selectedBooks.includes(book.id)" @selected="selectBook(book)"  />
      </li>
    </ul>
  </div>
</template>

<script>
import BookSelectorResult from "~/components/BookSelectorResult.vue";
import BookSelectorPagination from "~/components/BookSelectorPagination.vue";

export default {
  name: "BookSelector",
  components: { BookSelectorPagination, BookSelectorResult },
  /**
   * @returns {{books: Book[]}}
   */
  props: {
    selectedBooks: {
      default: []
    }
  },
  data() {
    return {
      page: 1,
      search: "",
      books: [],
      hasNextPage: false,
      hasPreviousPage: false,
      isScheduledForUpdate: false,
      hideSelectedItems: true,
      cancelToken: null,
      available_only: true,
      target: 0,
      limit: 100,
      maxPage: null,
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
    available_only() {
      this.scheduleUpdate();
    }
  },
  methods: {
    selectTarget() {
      if (this.cancelToken) {
        // Still loading some results
        return;
      }
      if (this.availableBooks.length === 0) {
        // Nothing to select
        return;
      }

      const book = this.availableBooks[this.target];

      if(this.selectedBooks.includes(book.id)){
        // Already in the list
        return;
      }

      this.selectBook(book);
    },
    scheduleUpdate() {
      if (this.isScheduledForUpdate) {
        return;
      }
      this.isScheduledForUpdate = true;
      this.$nextTick(this.updateComponent);
    },
    updateComponent() {
      this.isScheduledForUpdate = false;

      if (this.cancelToken) {
        this.cancelToken();
      }
      this.$axios.$get(
        this.getApiUrl(),
        {
          cancelToken: new this.$axios.CancelToken(c => {
            this.cancelToken = c;
          })
        }
      ).then(response => {
        this.hasNextPage = !!response.next;
        this.hasPreviousPage = !!response.previous;
        this.maxPage = Math.ceil(response.count / this.limit);
        this.books = response.results;
        this.cancelToken = null;
        this.target = 0;
      });
    },
    getApiUrl() {
      const params = [];
      if (this.page > 1) {
        params.push("page=" + this.page);
      }
      if (this.available_only) {
        params.push("available_online=1");
      }
      if (this.search && this.search.trim().length > 0) {
        params.push("search=" + encodeURIComponent(this.search));
      }
      params.push("limit=" + this.limit);

      return "/book/?" + params.join("&");
    },
    selectBook(book) {
      this.$emit("book-selected", book);
    }
  },

  beforeMount() {
    this.updateComponent();
  }
};
</script>
