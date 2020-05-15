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

    <section class="">

      <div class="container">
        <div class="box" v-for="list in readingLists" :key="list.id">
          <h2 class="subtitle">
            <nuxt-link :to="{name:'reading-list-id', params: {id: list.id}}">{{list.title}}</nuxt-link>
          </h2>

          <div class="content" v-if="list.entries.length">
            <p>
              Contains {{list.entries.length}} books:
            </p>
            <ol>
              <li v-for="entry in list.entries" :key="entry.id">{{entry.book.title}}</li>
            </ol>
          </div>
          <div class="content" v-else>
            <p>
              Contains no books.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "reading-list",
  data() {
    return {
      readingLists: [],
    };
  },
  methods: {
    updateComponent(route) {
      this.$axios.$get(this.getApiUrl()).then(response => {
        this.readingLists = response.results;
      });
    },
    getApiUrl() {
      return '/reading-list/';
    },
  },
  beforeMount() {
    this.updateComponent(this.$route);
  }

}
</script>
