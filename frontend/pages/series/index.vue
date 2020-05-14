<template>
  <div>
    <h1>Series</h1>
    <section class="section">
      <Pagination :page="page" :previous-page-url="previousPageUrl" :next-page-url="nextPageUrl" />
      <input type="search" v-model="search">
      <div class="columns is-multiline">
        <Card v-for="series in seriesList" :key="series.id" :title="series.title + '(' + series.book_count + ' books)' "
              class="is-3">
          <img :src="series.cover_url" />
          <nuxt-link :to="{name:'series-id-books', params: {id: series.id}}">
            GO TO
          </nuxt-link>
        </Card>
      </div>
    </section>
  </div>
</template>

<script>
import Card from '../../components/Card';
import Pagination from "~/components/Pagination";

export default {
  name: 'Series',
  components: {
    Pagination,
    Card,
  },
  data() {
    return {
      page: null,
      search: '',
      seriesList: [],
      hasPreviousPage: false,
      hasNextPage: false,
    };
  },
  computed: {
      nextPageUrl(){
        return this.hasNextPage && {
          to: 'series',
          query: {
            page: this.page+1,
            search: this.search,
          },
        };
      },
      previousPageUrl(){
        return this.hasPreviousPage && {
          to: 'series',
          query: {
            page: this.page-1,
            search: this.search,
          },
        };
      },
  },
  watch: {
    $route(to, from) {
      this.updateComponent(to);
    },
    search(to, from) {
      if(to && from && to.trim() === from.trim()){
        return;
      }

      this.$router.push({
        to: 'series',
        query: {
          page: 1,
          search: to,
        },
      });
    },
  },
  methods: {
    updateComponent(route) {
      this.page = parseInt(route.query.page || 1);

      if(route.query.search !== this.search){
        this.search = route.query.search;
      }

      this.$axios.$get(this.getApiUrl()).then(response => {
        this.hasNextPage = !!response.next;
        this.hasPreviousPage = !!response.previous;
        this.seriesList = response.results;
      });
    },
    getApiUrl(){
      const params = [];
      if(this.page>1){
        params.push("page="+this.page);
      }
      if(this.search && this.search.trim().length > 0){
        params.push("search="+encodeURIComponent(this.search));
      }
      return '/series/?'+params.join('&');
    }
  },

  beforeMount() {
    this.updateComponent(this.$route);
  },
};
</script>
