<template>
  <div class="box blocked-books">
    <div class="error">There was an error while trying to merge all the reading lists. Some reading lists have circular
      dependencies.
    </div>
    <div class="blockers">
      <div class="box blocker" v-for="[book, blockers] in blockedBooks" :key="book.book.id">
        <h3>{{ book.book.title }}</h3>
        <div>is blocked by</div>
        <table>
          <tr v-for="[readingList, book] in blockers" :key="readingList.id">
            <td class="blocker-book">{{ book.book.title }}</td>
            <td class="blocker-reading-list" align="right">in {{ readingList.title }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>
<style>
.blocked-books {
  border: solid red 1px;
  border-radius: 6px;
  padding: 6px;
  background: #ffd8da;
}

.error {
  font-weight: bold;
}
.blockers{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.blocker {
  display: inline-block;
  min-width: 200px;
}

.blocker h3{
  text-align: center;
  font-weight: bold;
}

h3+div{
  text-align: center;
  border-bottom: solid 1px #c1c1c1;
}

td{
  padding: 6px;
}
</style>
<script>
export default {
  name: "BlockedBooks",
  props: {
    blockedBooks: {}
  }
};
</script>
