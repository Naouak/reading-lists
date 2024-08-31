<template>
  <nav class="pagination is-centered">
    <a class="pagination-previous" :disabled="!hasPreviousPage" @click="hasPreviousPage && $emit('input', value - 1)">Previous
      Page</a>
    <div class="pagination-list" @click="promptPageNumber">
      <span class="pagination-link is-current">{{ value }} / {{maxPage}}</span>
    </div>
    <a class="pagination-next" :disabled="!hasNextPage" @click="hasNextPage && $emit('input', value + 1 )">Next Page</a>
  </nav>
</template>
<script>
export default {
  name: "BookSelectorPagination",
  props: {
    hasNextPage: {},
    hasPreviousPage: {},
    maxPage: {},
    value: {}
  },
  methods: {
    promptPageNumber(){
      const pagePrompt = prompt("Page?");
      if(!pagePrompt){
        return;
      }
      const page = parseInt(pagePrompt, 10);
      if(page < 1 || page > this.maxPage){
        return;
      }
      this.$emit('input', page);
    }
  }
};
</script>
