<template>
  <div class="">
    <div class="cover">
      <a target="_blank" :href="entry.book.read_online_url">
        <img :src="entry.book.cover_url" :alt="entry.book.title">
        <div class="cover-title">
          <div class="book-title">{{ entry.book.title }}</div>
        </div>
      </a>


      <div class="mark-as-read">
          <span class="book-pub-date"><DateDisplay :date="entry.book.pub_date" /></span>
          <button class="mark-as-read-button button" @click="$emit('read')">
            <b-icon icon="check" />
            <span>Mark as read <span v-if="entry.book.last_read_history">again</span></span>
          </button>
        </div>
    </div>


  </div>
</template>

<style>
.cover {
  position: relative;
  width: 100%;
}

.cover a{
  position:relative;
}

.cover img {
  width: 100%;
}

.cover-title {
  position: absolute;
  bottom: 0;
  width: 100%;
  color: white;
  padding: 5px;
  background: rgba(1, 1, 1, 0.5);
}

.book-title{
  font-size: larger;
  font-weight: bolder;
}

.book-pub-date{
  display: inline-block;
  padding-left: 10px;
  padding-top: calc(0.375em - 1px);
  padding-bottom: calc(0.375em - 1px);
}

.mark-as-read{
  width: 100%;
  padding: 5px;
  display: flex;
  justify-content: space-between;
}

.mark-as-read-button{
}


</style>

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
  }
};
</script>
