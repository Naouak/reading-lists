<template>
  <div class="list-block">
    <table class="whats-next-full-list">
      <tr>
        <th>Title</th>
        <th>Read?</th>
        <th>Publication Date</th>
        <th>Reading Lists</th>
      </tr>
      <tr v-for="(entry) in booksToReadWithoutLists" :key="entry.id" :class="{
          read: !!entry.book.last_read_history
        }">
        <td>{{ entry.book.title }}</td>
        <td>{{ entry.book.last_read_history ? "Read" : "" }}</td>
        <td>{{ entry.book.pub_date }}</td>
        <td>{{ entry.lists.map(l => l.title).sort().join(", ") }}</td>
      </tr>
    </table>

  </div>
</template>
<script>
export default {
  name: "Table",
  props: {
    booksToReadWithoutLists: {}
  }
};
</script>
