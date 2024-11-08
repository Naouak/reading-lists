<template>
  <div class="">
    <div class="cover">
      <a target="_blank" :href="'https://www.marvel.com/comics/issue/' + book.external_id + '/comics-collection'">
        <img :src="book.cover_url" :alt="book.title">
        <div class="cover-title">
          <div class="book-title">{{ book.title }}</div>
        </div>
      </a>

      <div class="mark-as-read">
        <div>
          <select>
            <option class="book-pub-date">
              Published:
              <DateDisplay :date="book.pub_date" />
            </option>
            <option class="book-pub-date">
              Created:
              <DateDisplay :date="book.created_date" />
            </option>
            <option class="book-pub-date">
              Available:
              <DateDisplay v-if="book.available_online" :date="book.availability_date" />
              <span v-else>Not Available</span>
            </option>
            <option class="book-pub-date">
              Found:
              <DateDisplay v-if="book.available_online" :date="book.availability_last_check" />
              <span v-else>Not Available</span>
            </option>
          </select>

        </div>
        <span v-if="book.last_read_history">Read on <DateDisplay :date="book.last_read_history.read_date" /></span>
        <span v-else>Not read yet</span>
      </div>
    </div>
  </div>

</template>

<script>
import DateDisplay from "~/components/DateDisplay";

export default {
  components: { DateDisplay },
  props: {
    book: {
      type: Object
    }
  }
};
</script>
