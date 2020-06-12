<template>
  <section class="section">
    <h1 class="title">Series</h1>
    <div class="card">
      <div class="card-content">
        <Pagination :page="page" :previous-page-url="previousPageUrl" :next-page-url="nextPageUrl" />
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

      <section class="card-content section columns is-multiline">
        <div v-for="series in seriesList" :key="series.id" class="column is-6">
          <Series :series="series" />
        </div>
      </section>
    </div>

  </section>
</template>

<script>
import Series from '../../components/Series';
import Pagination from "~/components/Pagination";

export default {
  name: 'SeriesPage',
  components: {
    Pagination,
    Series,
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
