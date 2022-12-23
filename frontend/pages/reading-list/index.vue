<template>
  <div class="">
    <div class="page-header reading-lists-header section">
      <h1 class="title">Reading lists</h1>
      <nav class="navbar">
        <div class="navbar-menu">
          <div class="navbar-start">
            <nuxt-link v-if="$route.query.archived" :to="{query: {}}" class="navbar-item button is-link">
              Active lists
            </nuxt-link>
            <nuxt-link v-else :to="{query: {archived: (!$route.query.archived)?1:0}}"
                       class="navbar-item button is-link">
              Archived lists
            </nuxt-link>
          </div>
          <div class="navbar-end">
            <nuxt-link class="button is-link" :to="{name:'reading-list-new'}">
              <b-icon icon="plus" />
              <span>Create a list</span>
            </nuxt-link>
          </div>
        </div>
      </nav>
    </div>

    <div class="reading-lists columns is-multiline">
      <div v-for="list in readingLists" :key="list.id" class="column">
        <ReadingList :list="list" @read="markAsRead" />
      </div>
    </div>
  </div>
</template>

<script>
import ReadingList from "~/components/ReadingList";

export default {
  name: "reading-list",
  components: {
    ReadingList,
  },
  data() {
    return {
      readingLists: [],
    };
  },
  watch: {
    $route(to) {
      this.updateComponent(to)
    },
  },
  beforeMount() {
    this.updateComponent(this.$route);
  },
  methods: {
    updateComponent(route = this.$route) {
      this.readingLists = [];
      this.$axios.$get(this.getApiUrl(route)).then(response => {
        this.readingLists = response.results.sort(
          (a, b) => {
            const nextA = a.entries.find(e => !e.book.last_read_history || !e.book.last_read_history.read_date);
            const nextB = b.entries.find(e => !e.book.last_read_history || !e.book.last_read_history.read_date);

            if(!nextA){
              return 1;
            }

            if(!nextB){
              return -1;
            }

            const dateA = new Date(nextA.book.pub_date).getTime();
            const dateB = new Date(nextB.book.pub_date).getTime();

            return dateA >= dateB ? 1 : -1;
          }
        );
      });
    },
    getApiUrl(route = this.$route) {
      const params = [];
      if (parseInt(route.query.archived) === 1) {
        params.push(['archived', '1']);
      } else {
        params.push(['archived', '0']);
      }

      const queryString = params.map(([a, b]) => encodeURIComponent(a) + '=' + encodeURIComponent(b)).join('&');
      return '/reading-list/?' + queryString;
    },
    markAsRead(book) {
      this.$api.bookRead(book).then(() => this.updateComponent());
    }
  },

}
</script>
