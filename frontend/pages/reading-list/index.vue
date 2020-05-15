<template>
  <div class="">
    <div class="hero is-clearfix">
      <div class="hero-body">
        <div class="container">
          <div class="field is-pulled-right">
            <div class="control">
              <nuxt-link class="button is-link" :to="{name:'reading-list-new'}">
                <b-icon icon="plus" />
                <span>Create a list</span></nuxt-link>
            </div>
          </div>

          <h1 class="title">Reading lists</h1>
        </div>
      </div>
    </div>

    <section>
      <div class="container columns is-multiline">
        <div class="column is-6" v-for="list in readingLists" :key="list.id">
          <ReadingList  :list="list" @read="markAsRead" />
        </div>
      </div>
    </section>
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
  methods: {
    updateComponent(route = this.$route) {
      this.loading = true;
      this.$axios.$get(this.getApiUrl()).then(response => {
        this.loading = false;
        this.readingLists = response.results;
      });
    },
    getApiUrl() {
      return '/reading-list/';
    },
    markAsRead(book){
      this.loading = true;
      this.$api.bookRead(book).then(() => this.updateComponent());
    }
  },
  beforeMount() {
    this.updateComponent(this.$route);
  }

}
</script>
