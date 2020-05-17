<template>
  <div class="box">
    <div class="media">
      <div class="media-left">
        <figure style="width: 70px;">
          <img style="width: auto; height: auto;" :src="book.cover_url" :alt="book.title">
        </figure>
      </div>
      <div class="media-content">
        <div class="content">
          <div class="subtitle">{{book.title}}</div>
          <div>Published on
            <DateDisplay :date="book.pub_date" />
          </div>
          <div v-if="book.last_read_history">Last read on
            <DateDisplay :date="book.last_read_history.read_date" />
          </div>
          <div v-else>Not read yet</div>
        </div>

        <div class="field has-addons">
          <p class="control">
            <a v-if="book.read_online_url" target="_blank" :href="book.read_online_url" class="button">
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
  components: {DateDisplay},
  props: {
    book: {
      type: Object,
    },
  },
};
</script>
