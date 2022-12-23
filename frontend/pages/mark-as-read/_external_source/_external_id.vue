<template>
  <section></section>
</template>

<script>
export default {
    name: "_external_id.vue",
  beforeMount() {
    const externalSource = this.$route.params.external_source;
    const externalId = this.$route.params.external_id;

    this.$axios.$get('/book/?external_source='+externalSource+'&external_id='+externalId)
      .then(result => {
        if(result.results.length === 0){
          throw new Error("No books to mark as read");
        }
        const book = result.results[0];
        return this.$api.bookRead(book);
      }).then(_ => {
        window.close();
    });
  }
}
</script>
