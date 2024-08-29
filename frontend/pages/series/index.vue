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
      <div class="card-content">
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <select v-model="available">
                  <option :value="null">All</option>
                  <option :value="1">Only Available</option>
                  <option :value="0">Only non Available</option>
                </select>
              </p>
            </div>
          </div>
        </div>
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <input type="number" min="0" v-model="book_count">
              </p>
            </div>
          </div>
        </div>
        <div class="field is-horizontal">
          <div class="field-body">
            <div class="field">
              <p class="control has-icons-left">
                <select v-model="ordering">
                  <option value="title">Title (A -> Z)</option>
                  <option value="-title">Title (Z -> A)</option>
                  <option value="-pub_date">Publication (Newest first)</option>
                  <option value="pub_date">Publication (Oldest first)</option>
                </select>
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
      book_count: 1,
      seriesList: [],
      available: 1,
      ordering: "pub_date",
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
      this.$router.push(this.buildRoute({page: 1}));
    },
    available(){
      this.$router.push(this.buildRoute({page: 1}));
    },
    ordering(){
      this.$router.push(this.buildRoute({page: 1}));
    },
    book_count(){
      this.$router.push(this.buildRoute({page: 1}));
    }
  },
  beforeMount() {
    this.updateComponent(this.$route);
  },
  methods: {
    updateComponent(route) {
      const page =  parseInt(route.query.page || "1");
      if (this.page !== page){
        this.page = page;
      }
      if(route.query.search !== undefined && route.query.search !== this.search){
        this.search = route.query.search;
      }
      if(route.query.book_count !== undefined && route.query.book_count !== this.book_count){
        this.book_count = route.query.book_count;
      }
      if(route.query.available !== undefined && route.query.available !== this.available){
        this.available = route.query.available;
      }
      if(route.query.ordering !== undefined && route.query.ordering !== this.ordering){
        this.ordering = route.query.ordering;
      }

      this.$axios.$get(this.getApiUrl()).then(response => {
        this.hasNextPage = !!response.next;
        this.hasPreviousPage = !!response.previous;
        this.seriesList = response.results;
      });
    },
    buildRoute(changes = {}){
      return {
        to: 'series',
        query: {
          page: changes.page || this.page,
          search: changes.search || this.search,
          available: changes.available || this.available,
          book_count: changes.book_count || this.book_count,
          ordering: changes.ordering || this.ordering,
        }
      }
    },
    getApiUrl(){
      const params = [];
      if(this.page>1){
        params.push("page="+this.page);
      }
      if(this.search && this.search.trim().length > 0){
        params.push("search="+encodeURIComponent(this.search));
      }
      if (this.available !== null) {
        params.push("available=" + (this.available ? "1" : "0"));
      }
      params.push("book_count=" + this.book_count);

      params.push("ordering="+ this.ordering);

      return '/series/?'+params.join('&');
    }
  },


};
</script>
