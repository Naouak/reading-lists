<template>
  <div class="box">
    <div class="media">
      <div class="media-left">
        <figure style="width: 70px;">
          <img style="width: auto; height: auto;" :src="entry.book.cover_url" :alt="entry.book.title">
        </figure>
      </div>
      <div class="media-content">
        <div class="content">
          <div class="subtitle">{{entry.book.title}}</div>
          <div>Published on
            <DateDisplay :date="entry.book.pub_date" />
          </div>
          <div v-if="entry.read_date">Read on
            <DateDisplay :date="entry.read_date" />
          </div>
        </div>

        <div class="field has-addons">
          <p class="control">
            <a v-if="entry.book.read_online_url" target="_blank" :href="'https://www.marvel.com/comics/issue/' + entry.book.external_id + '/comics-collection'" class="button">
              <b-icon icon="book-open-page-variant" />
              <span>Read Online</span>
            </a>
          </p>

          <p class="control">
            <button class="button" @click="$emit('remove', entry)">
              <b-icon icon="delete" />
              <span>Remove from history</span>
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  name: "ReadingHistoryEntry",
  components: {DateDisplay},
  props: {
    entry: {
      required: true
    },
  },
};
</script>
