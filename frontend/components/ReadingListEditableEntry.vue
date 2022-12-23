<template>
  <div class="reading-list-editable-entry">
    <img class="reading-list-editable-entry-cover" :src="entry.book.cover_url"
         :alt="entry.book.title" loading="lazy">

    <div class="reading-list-editable-entry-metas">
      <div class="reading-list-editable-entry-position">
        <b-icon icon="check" class="has-text-success" v-if="entry.book.last_read_history" />
        #{{ entry.position }}
      </div>

      <div class="reading-list-editable-entry-title">
        {{ entry.book.title }}
      </div>

      <div class="reading-list-editable-entry-publication-date">
        Published on
        <DateDisplay :date="entry.book.pub_date" />
      </div>

      <div v-if="entry.book.last_read_history" class="reading-list-editable-entry-read-date">Last Read on
        <DateDisplay :date="entry.book.last_read_history.read_date" />
      </div>
    </div>

    <div class="reading-list-editable-entry-actions">
      <button :disabled="!canGoUp" @click="$emit('move-up')">
        <b-icon icon="arrow-up-thick" />
        <span>Up</span>
      </button>
      <button :disabled="!canGoUp && !canGoDown" @click="move">
        Quick Move
      </button>
      <button :disabled="!canGoDown" @click="$emit('move-down')">
        <b-icon icon="arrow-down-thick" />
        <span>Down</span>
      </button>
      <button @click="$emit('remove')">
        <b-icon icon="delete" />
        <span>Remove</span>
      </button>
    </div>
  </div>
</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  name: "ReadingListEditableEntry",
  components: {DateDisplay},
  props: {
    entry: {
      required: true,
    },
    canGoUp: {
      default: false,
    },
    canGoDown: {
      default: false,
    },
  },
  methods: {
    move() {
      const position = prompt('Move to position?', this.entry.position);
      if (position === this.entry.position) {
        return;
      }
      this.$emit('move', position);
    }
  }
};
</script>
