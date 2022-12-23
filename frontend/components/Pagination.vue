<template>
  <nav class="pagination is-centered">
    <nuxt-link class="pagination-previous" :disabled="!previousPageUrl" :to="previousPageUrl">
      Previous page
    </nuxt-link>
    <div class="pagination-list">
      <span class="pagination-link is-current">{{page}}</span>
    </div>
    <nuxt-link class="pagination-next" :disabled="!nextPageUrl" :to="nextPageUrl">
      Next Page
    </nuxt-link>
  </nav>
</template>

<script>
export default {
  name: "Pagination",
  props: {
    previousPageUrl: {
      default: null,
    },
    nextPageUrl: {
      default: null,
    },
    page: {
      default: 1,
    }
  }
}
</script>
