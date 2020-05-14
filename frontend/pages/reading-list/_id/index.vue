<template>
  <section class="section" v-if="readingList">
    <h1 class="title">Reading list: {{readingList.title}}</h1>
    <div class="field">
      <label class="checkbox">
        <input type="checkbox" v-model="editMode">
        Edit mode
      </label>
    </div>
    <div class="field">
      <label class="checkbox">
        <input type="checkbox" v-model="condensed">
        Condensed mode
      </label>
    </div>

    <div class="section" v-if="nextEntry && !editMode">
      <h2 class="title">Next Title to read</h2>
      <ReadingListEntry :entry="nextEntry" @read="markAsRead(nextEntry.book)" />
    </div>

    <div class="columns">
      <div class="column" :class="{'is-6':editMode}">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">In the list ({{readingList.entries.length}} books)</div>
          </div>
          <div class="card-content" v-if="readingList.entries.length">
            <b-progress :value="progress" show-value type="is-info is-large" format="percent">
              {{readEntries}} / {{readingList.entries.length}} read
            </b-progress>
          </div>
          <div class="card-content">
            <ReadingListEntry v-for="entry in readingList.entries" :key="entry.id" :entry="entry"
                              :edit-mode="editMode" :condensed="condensed"
                              :can-go-up="entry.position>1" :can-go-down="entry.position<readingList.entries.length"
                              @read="markAsRead(entry.book)"
                              @move-up="moveUp(entry)" @move-down="moveDown(entry)" />
          </div>
        </div>


      </div>
      <div v-if="editMode" class="column is-6">
        <BookSelector :selected-books="selectedBookIds" @book-selected="bookSelected" />
      </div>
    </div>
  </section>
</template>
<script>
import BookSelector from "~/components/BookSelector";
import ReadingListEntry from "~/components/ReadingListEntry";

export default {
  name: "readingListDetails",
  components: {ReadingListEntry, BookSelector},
  data() {
    return {
      readingListId: null,
      readingList: null,
      editMode: false,
      condensed: false,
    };
  },
  computed: {
    selectedBookIds() {
      return this.readingList?.entries.map(e => e.book.id);
    },
    readEntries() {
      return this.readingList?.entries.filter(e => e.book.read).length;
    },
    progress() {
      if(this.readingList?.entries.length === 0){
        return 0;
      }
      return this.readEntries / this.readingList?.entries.length * 100;
    },
    nextEntry(){
      return this.readingList?.entries?.find((e) => !e.book.read);
    },
  },
  loading: true,
  methods: {
    updateComponent(route = this.$route) {
      this.readingListId = route.params.id;
      this.loading = true;

      this.$axios.$get(this.getApiUrl()).then(response => {
        this.readingList = response;
        this.loading = false;
      });
    },
    getApiUrl() {
      return '/reading-list/' + this.readingListId + '/';
    },
    bookSelected(book) {
      this.loading = true;
      this.$axios.$post('/reading-list/' + this.readingListId + '/entries/', {
        book: book.id
      }).then(() => {
        this.updateComponent(this.$route);
      });
    },
    moveUp(entry) {
      this.move(entry, Math.max(entry.position - 1, 1));
    },
    moveDown(entry) {
      this.move(entry, Math.min(entry.position + 1, this.readingList.entries.length));
    },
    move(entry, position) {
      if (position === entry.position) {
        return;
      }
      this.loading = true;
      this.$axios.$put('/reading-list/' + this.readingListId + '/entries/' + entry.id + '/', {
        position
      }).then(() => this.updateComponent());
    },
    markAsRead(book) {
      this.loading = true;
      this.$axios.$post('/book/' + book.id + '/read/', {}).then(() => this.updateComponent());
    },
  },
  beforeMount() {
    this.updateComponent(this.$route);
  }
}
</script>
