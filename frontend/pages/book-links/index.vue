<template>
  <section class="section">
    <h1 class="title">Book Links</h1>

    <div>
      <nuxt-link class="button is-link" :to="{name:'book-links-new'}">
        <b-icon icon="plus" />
        <span>Create a link</span>
      </nuxt-link>
      <nuxt-link class="button is-link" :to="{name: 'book-links-chart'}">
        <span>Chart Data</span>
      </nuxt-link>
    </div>

    <div class="links">
      <div class="link" v-for="link in bookLinks" :key="link.id">
        <div class="link-content">
          <div class="source">
            <Book :book="link.source" />
          </div>
          <div class="link-text">
            {{ link.link_text || " Refers to " }}
          </div>
          <div class="target">
            <Book v-if="link.target" :book="link.target" />
          </div>
        </div>
        <div class="link-actions">
          <button @click="removeLink(link.id)">
            <b-icon icon="delete" /> Delete link
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>

import Book from "~/components/Book.vue";

export default {
  name: "BookLinks",
  components: {Book},
  data() {
    return {
      bookLinks: [],
    }
  },
  computed: {},
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
        this.bookLinks = response.results;
      });
    },
    getApiUrl(route = this.$route) {
      return '/book-link/';
    },
    removeLink(id) {
      if (confirm("Are you sure you want to delete that link?")) {
        this.$axios.$delete('/book-link/' + id).then(() => {
          this.updateComponent(this.$route);
        });
      }
    }
  }
};
</script>
