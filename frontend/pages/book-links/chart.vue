<template>
  <div class="scape">
    <pre>{{bookLinks}}</pre>
  </div>
</template>

<script>

export default {
  name: "BookLinksChart",
  data(){
    return {
      bookLinks: null,
    }
  },
  beforeMount() {
    this.updateComponent();
  },
  methods: {
    updateComponent(route = this.$route) {
        this.$axios.$get(this.getApiUrl(route)).then(response => {
          this.bookLinks = response;
        });
    },
    getApiUrl(route = this.$route) {
      return '/book-link-graph/?limit=10000';
    }
  }
}
</script>
