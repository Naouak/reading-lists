<template>
  <div class="media">
    <div class="media-left">
      <figure style="width: 70px;">
        <img style="width: auto; height: auto;" :src="book.cover_url" :alt="book.title" loading="lazy" />
      </figure>
    </div>
    <div class="media-content">
      <div class="content">
        <div class="subtitle">
          <b-icon v-if="!book.available_online" icon="cancel" />
          {{ book.title }}
        </div>
        <div>
          Published on
          <DateDisplay :date="book.pub_date" />
        </div>
      </div>

      <div class="field has-addons">
        <p class="control">
          <button class="button" v-if="!selected" @click="selectBook">
            <b-icon icon="plus" />
            <span>Select</span>
          </button>
        </p>
        <p class="control">
          <a :href="'https://www.marvel.com/comics/issue/' + book.external_id + '/comics-collection'" target="_blank" class="button">
            <b-icon :icon="book.available_online?'book-open-page-variant':'cancel'" />
            <span>Read online</span></a>
        </p>
      </div>
    </div>
  </div>
</template>
<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  name: "BookSelectorResult",
  components: { DateDisplay },
  props: {
    book: {},
    selected: {}
  },
  methods: {
    selectBook(){
      this.$emit('selected', this.book);
    }
  }
};
</script>
