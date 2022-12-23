<template>
  <section class="section">
    <h1 class="title">New Book Links</h1>


    <div class="three-columns">
      <BookSelector @book-selected="bookSelectedSource" />

      <div class="book-link-form">
        <div class="card">
          <div class="source-book">
            <h2>Source Book</h2>
            <Book v-if="sourceBook" :book="sourceBook" />
          </div>
          <div class="book-link-form-link">
            <h2><b-icon icon="arrow-right-box" /> References <b-icon icon="arrow-right-box" /></h2>
            <div>
              <input type="text" v-model="linkText" placeholder="Link title" class="input">
            </div>
            <button class="book-link-create-button button is-primary" :disabled="!sourceBook || inProgress" @click="createLink">Create Link</button>
          </div>
          <div class="target-book">
            <h2>Mentioned Book</h2>
            <Book v-if="targetBook" :book="targetBook" />
          </div>
        </div>
      </div>

      <BookSelector @book-selected="bookSelectedTarget" />
    </div>
  </section>
</template>

<script>
import BookSelector from "~/components/BookSelector.vue";
import Book from "~/components/Book.vue";

export default {
  name: "BookLinksNew",
  components: {Book, BookSelector},
  data() {
    return {
      sourceBook: null,
      targetBook: null,
      linkText: "",
      inProgress: false,
    }
  },
  computed: {},
  watch: {},
  methods: {
    bookSelectedSource(book) {
      this.sourceBook = book;
    },
    bookSelectedTarget(book) {
      this.targetBook = book;
    },
    createLink(){
      if(this.inProgress){
        return;
      }

      this.inProgress = true;
      this.$axios.$post('/book-link/', {
        source: this.sourceBook.id,
        target: this.targetBook?.id,
        link_text: this.linkText,
      }).then(response => {
        this.inProgress = false;
        this.targetBook = null;
        this.linkText = "";
      })
    }
  }
};
</script>
