<template>
  <div class="reading-list-entry" :class="{read: !want_to_read}">
    <div class="cover">
      <a target="_blank" :href="read_url">
        <img :src="entry.book.cover_url" :alt="entry.book.title" />

        <div v-if="entry.position" class="reading-list-position">
          <b-icon
            icon="check"
            :class="{
              'has-text-success': !entry.book.last_read_history.want_to_reread,
              'has-text-warning': entry.book.last_read_history.want_to_reread,
            }"
            v-if="read"
          />
          # {{ entry.position }}
        </div>

        <div class="cover-title">
          <div class="book-title">{{ entry.book.title }}</div>
        </div>
      </a>

      <div class="mark-as-read">
        <span class="book-pub-date"><DateDisplay :date="entry.book.pub_date"/></span>
        <button v-if="can_read" class="mark-as-read-button button" @click="$emit('read')">
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
import DateDisplay from '~/components/DateDisplay';

export default {
  name: 'ReadingListEntry',
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
    },
  },
  computed: {
    want_to_read() {
      return !this.read || this.entry.book?.last_read_history?.want_to_reread;
    },
    can_read() {
      return this.readable && this.want_to_read;
    },
    read() {
      return this.entry.book.last_read_history && this.entry.book.last_read_history.read_date;
    },
    read_url() {
      if (navigator.userAgent.match(/Android/i)) {
        return `https://marvel.smart.link/fiir7ec77?type=issue&drn=drn:src:marvel:unison::prod:0aead151-0467-480a-9682-7bb9073b7693&sourceId=${this.entry.book.external_id}`;
      }
      return `https://www.marvel.com/comics/issue/${this.entry.book.external_id}/comics-collection`;
    },
  },
};
</script>
