<template>
  <div class="container">
    <div class="section">
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

    <div class="columns is-multiline">
      <div class="column is-6" v-for="list in readingLists" :key="list.id">
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
  methods: {
    updateComponent(route = this.$route) {
      this.loading = true;
      this.$axios.$get(this.getApiUrl()).then(response => {
        this.loading = false;
        this.readingLists = response.results;
      });
    },
    getApiUrl() {
      const params = [];
      if (this.$route.query.archived === 1) {
        params.push(['archived', '1']);
      } else {
        params.push(['archived', '0']);
      }

      const queryString = params.map(([a, b]) => encodeURIComponent(a) + '=' + encodeURIComponent(b)).join('&');
      return '/reading-list/?' + queryString;
    },
    markAsRead(book) {
      this.loading = true;
      this.$api.bookRead(book).then(() => this.updateComponent());
    }
  },
  beforeMount() {
    this.updateComponent(this.$route);
  }

}
</script>
