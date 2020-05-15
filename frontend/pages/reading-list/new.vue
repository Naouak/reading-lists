<template>
  <section class="section">
    <h1 class="title">New Reading List</h1>

    <div class="field">
      <label for="reading-list-title" class="label">Title</label>
      <div class="control">
          <input class="input" id="reading-list-title" type="text" v-model="title" placeholder="Reading List Title" required />
      </div>
    </div>

    <div class="field">
      <div class="control">
        <button class="button is-link" @click="createList" :disabled="inProgress || title.trim().length === 0">CREATE</button>
      </div>
    </div>


  </section>
</template>

<script>
export default {
  name: "new",
  data() {
    return {
      inProgress: false,
      title: '',
    };
  },
  methods: {
    createList() {
      if(this.inProgress){
        return;
      }

      this.inProgress = true;
      this.$axios.$post('/reading-list/', {
        title: this.title
      }).then(response => {
        this.$router.push({name: 'reading-list-id', params: {id: response.id}});
      })
    }
  }
}
</script>

<style scoped>

</style>
