<template>
  <div class="box">
    <div class="media">
      <div v-if="!condensed" class="media-left">
        <figure style="width: 128px;">
          <img style="width: auto; height: auto;" :src="entry.book.cover_url" :alt="entry.book.title" loading="lazy">
        </figure>
      </div>
      <div class="media-content" :class="{'columns': condensed}">
        <div v-if="!condensed" class="content">
          <div class="title">
            <b-icon icon="check" class="has-text-success" v-if="entry.book.last_read_history" />
            #{{entry.position}}
          </div>
          <div class="subtitle">{{entry.book.title}}</div>
          <div>Published on
            <DateDisplay :date="entry.book.pub_date" />
          </div>
          <div v-if="entry.book.last_read_history">Last Read on
            <DateDisplay :date="entry.book.last_read_history.read_date" />
          </div>
          <div v-else>
            <br />
          </div>
        </div>
        <div v-else class="content">
            <b-icon icon="check" class="has-text-success" v-if="entry.book.last_read_history" />
            #{{entry.position}}
            -
            {{entry.book.title}}
        </div>

        <div v-if="editMode" class="field has-addons" style="flex-grow: 0">
          <p class="control" v-if="canGoUp">
            <button class="button" @click="$emit('move-up')">
              <b-icon icon="arrow-up-thick" />
              <span>Up</span>
            </button>
          </p>
          <p class="control" v-if="canGoUp || canGoDown">
            <button class="button" @click="move">
              Quick Move
            </button>
          </p>
          <p class="control" v-if="canGoDown">
            <button class="button" @click="$emit('move-down')">
              <b-icon icon="arrow-down-thick" />
              <span>Down</span>
            </button>
          </p>
          <p class="control">
            <button class="button" @click="$emit('remove')">
              <b-icon icon="delete" />
              <span>Remove</span>
            </button>
          </p>
        </div>
        <div v-else class="field has-addons" style="flex-grow: 0">
          <p class="control">
            <a v-if="entry.book.read_online_url" target="_blank" :href="'https://www.marvel.com/comics/issue/' + entry.book.external_id + '/comics-collection'" class="button">
              <b-icon icon="book-open-page-variant" />
              <span>Read Online</span>
            </a>
          </p>
          <p class="control">
            <button class="button" @click="$emit('read')">
              <b-icon icon="check" />
              <span>Mark as read <span v-if="entry.book.last_read_history">again</span></span>
            </button>
          </p>

          <p class="control" v-if="enableReadBefore && !entry.book.last_read_history">
            <button class="button" @click="$emit('read-before')">
              <b-icon icon="check"/>
              <span>Mark as read before</span>
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
  name: "ReadingListEntry",
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
    editMode: {
      default: false,
    },
    condensed: {
      default: false,
    },
    enableReadBefore: {
      default: false,
    },
  },
  methods: {
    move(){
      const position = prompt('Move to position?', this.entry.position);
      if(position === this.entry.position){
        return;
      }
      this.$emit('move', position);
    }
  }
};
</script>
