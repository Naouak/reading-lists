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
      <li class="box" v-for="series in availableSeries" :key="series.id">
        <div class="media">
          <div class="media-left">
            <figure style="width: 70px;">
              <img style="width: auto; height: auto;" :src="series.cover_url" :alt="series.title">
            </figure>
          </div>
          <div class="media-content">
            <div class="content">
              <div class="subtitle">{{series.title}}</div>
              <div>Contains {{series.book_count}} books</div>
            </div>

            <div class="field has-addons">
              <p class="control">
                <button class="button" v-if="!selectedSeries.includes(series.id)" @click="subscribeSeries(series)">
                  <b-icon icon="plus" />
                  <span>Subscribe</span>
                </button>
              </p>
              <p class="control">
                <button class="button" @click="addSeries(series)">
                  <b-icon icon="plus" />
                  <span>Add every books</span>
                </button>
              </p>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: "SeriesSelector",
  props: {
    selectedSeries: {
      default: [],
    },
  },
  data() {
    return {
      page: 1,
      search: '',
      series: [],
      hasNextPage: false,
      hasPreviousPage: false,
      isScheduledForUpdate: false,
      hideSelectedItems: false,
    };
  },
  computed: {
    availableSeries() {
      if (!this.series) {
        return [];
      }
      let series = this.series;

      if (this.hideSelectedItems) {
        series = series.filter(b => !this.selectedSeries.includes(b.id));
      }

      return series;
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
        this.series = response.results;
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
      return '/series/?' + params.join('&');
    },
    subscribeSeries(series) {
      this.$emit('series-subscribed', series);
    },
    addSeries(series) {
      this.$emit('series-selected', series);
    }
  },

  beforeMount() {
    this.updateComponent();
  },
}
</script>
