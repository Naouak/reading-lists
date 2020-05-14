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
            <a v-if="entry.book.read_online_url" target="_blank" :href="entry.book.read_online_url" class="button">
              <b-icon icon="book-open-page-variant" />
              <span>Read Online</span>
            </a>
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
