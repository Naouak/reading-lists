<template>
  <section class="section">
    Nothing yet here
  </section>
</template>

<script>
export default {
  name: 'HomePage',
  data(){
    return {
      selectedBooks: [],
    };
  },
  methods: {
    bookSelected(book){
      this.selectedBooks.push(book.id);
    },
  },
};
</script>
