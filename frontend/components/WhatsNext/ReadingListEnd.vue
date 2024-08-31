<template>
  <div class="reading-list-end">
    <h2 class="reading-list-title">{{ entry.list.title }}</h2>
    <div>
      <div class="reading-list-entry">
        <div class="cover">
          <nuxt-link class="reading-list-end-cover" :to="{name:'reading-list-id', params: {id: entry.list.id}}">
            The reading list {{ entry.list.title }} is done.
          </nuxt-link>

          <div class="mark-as-read">
            <span class="book-pub-date"></span>
            <nuxt-link class="mark-as-read-button button"
                       :to="{name:'reading-list-id', params: {id: entry.list.id}}">
              <b-icon icon="check" />
              <span>Edit List</span>
            </nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "ReadingListEnd",
  props: {
    entry: {}
  }
};
</script>
