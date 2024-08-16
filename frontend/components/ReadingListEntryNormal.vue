<template>
  <div class="reading-list-entry" :class="{'read': entry.book.last_read_history}">
    <div class="cover">
      <a target="_blank" :href="read_url">
        <img :src="entry.book.cover_url" :alt="entry.book.title">

        <div v-if="entry.position" class="reading-list-position">
          <b-icon icon="check" class="has-text-success" v-if="entry.book.last_read_history" /> # {{entry.position}}
        </div>

        <div class="cover-title">
          <div class="book-title">{{ entry.book.title }}</div>
        </div>
      </a>


      <div class="mark-as-read">
          <span class="book-pub-date"><DateDisplay :date="entry.book.pub_date" /></span>
          <button v-if="readable && (!entry.book.last_read_history || entry.book?.last_read_history?.want_to_reread)" class="mark-as-read-button button" @click="$emit('read')">
            <b-icon icon="check" />
            <span>Mark as read</span>
          </button>
          <button v-else-if="readable" class="mark-as-read-button button" @click="$emit('want_to_reread')">
            <b-icon icon="book" />
            <span>Reread this</span>
          </button>
        </div>
    </div>


  </div>
</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  name: "ReadingListEntry",
  components: {DateDisplay},
  props: {
    entry: {
      required: true,
    },
    enableReadBefore: {
      default: false,
    },
    readable: {
      default: true,
    }
  },
  computed: {
    read_url() {
      if (navigator.userAgent.match(/Android/i)){
        return `https://www.marvel.com/comics/issue/${this.entry.book.external_id}/comics-collection`;
      }
      return this.entry.book.read_online_url;
    }
  }
};
</script>
