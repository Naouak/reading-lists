<template>
  <section class="section" v-if="readingList">



    <div class="columns is-pulled-right">
      <div class="column field">
        <div class="control">
          <button v-if="!editMode" @click="editMode=!editMode" class="button is-primary">Edit</button>
          <button v-else @click="editMode=!editMode" class="button is-primary">End Edit</button>
          <button v-if="readingList.archived" class="button is-danger" @click="archive">Unarchive</button>
          <button v-else class="button is-danger" @click="archive">Archive</button>
          <button v-if="editMode" class="button is-danger" @click="deleteList()">Delete list</button>
          <button v-if="!enableReadBefore" class="button is-primary" @click="enableReadBefore=!enableReadBefore">Enable
            Read Before
          </button>
          <button v-else class="button is-primary" @click="enableReadBefore=!enableReadBefore">Disable Read Before
          </button>
          <button class="button is-danger" @click="markForReread">Reread list</button>
          <button class="button is-danger" @click="markForRead">Remove Reread</button>
        </div>
      </div>
    </div>

    <h1 class="title is-clearfix" v-if="!editMode">Reading list: {{ readingList.title }}</h1>
    <div v-else class="field has-addons is-clearfix" style="margin-bottom: 40px;">
      <div class="control is-expanded">
        <input type="text" v-model="readingList.title" class="input" />
      </div>
      <div class="control">
        <a @click="updateList" class="button is-primary" style="margin-right: 10px;">
          Save
        </a>
      </div>
    </div>

    <div style="margin-bottom: 24px;" v-if="nextEntry && !editMode">
      <h2 class="title">Next Title to read</h2>
      <ReadingListEntry :entry="nextEntry" @read="markAsRead(nextEntry.book)" />
    </div>

    <div class="reading-list" v-if="readingList.entries.length && !editMode">
      <Progress :value="progress">
        {{ readEntries }} / {{ readingList.entries.length }} read
      </Progress>
    </div>

    <div class="reading-lists columns is-multiline" v-if="!editMode">
      <div v-for="entry in readingList.entries" :key="entry.id" class="column">
        <ReadingListEntryNormal :entry="entry" @read="markAsRead(entry.book)" @want_to_reread="wantToReread(entry.book)" />
      </div>
    </div>

    <div v-if="editMode && loading && booksLeftToAdd > 0" class="box">
      <h2 class="subtitle">Importing Books</h2>
      <Progress :value="(1 - (booksLeftToAdd / booksTotalToAdd)) * 100">
        {{ booksLeftToAdd }} / {{ booksTotalToAdd }} books imported
      </Progress>
    </div>

    <div class="columns" v-if="editMode">
      <div class="column reading-list-editable-entries">
        <div v-if="readingList.series.length" class="card" style="margin-bottom: 24px;">
          <div class="card-header">
            <div class="card-header-title">Auto-fill Series</div>
          </div>
          <div class="card-content is-flex" v-for="series in readingList.series" :key="series.id"
               style="justify-content: space-between; padding: .6rem 1.5rem;">
            <span style="line-height: 36px;">{{ series.title }}</span>
            <button class="button is-pulled-right" @click="removeSeries(series)">
              <b-icon icon="delete" />
              <span>Remove</span>
            </button>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-title">In the list ({{ readingList.entries.length }} books)</div>

            <button class="button" @click="reverseEntriesOrder = !reverseEntriesOrder">
              <b-icon :icon="reverseEntriesOrder?'sort-descending':'sort-ascending'" />
            </button>

          </div>
          <div class="card-content" v-if="readingList.entries.length">
            <Progress :value="progress">
              {{ readEntries }} / {{ readingList.entries.length }} read
            </Progress>
          </div>
          <div class="card-content">
            <ReadingListEditableEntry v-for="entry in entries" :key="entry.id" :entry="entry"
                                      :enable-read-before="enableReadBefore"
                                      :edit-mode="editMode"
                                      :can-go-up="entry.position>1"
                                      :can-go-down="entry.position<readingList.entries.length"
                                      @read="markAsRead(entry.book)" @read-before="markAsReadBefore(entry.book)"
                                      @move-up="moveUp(entry)" @move-down="moveDown(entry)" @remove="remove(entry)"
                                      @move="move(entry, $event)" />
          </div>
        </div>


      </div>
      <div v-if="editMode" class="column is-6">
        <b-tabs v-model="activeTab" class="card">
          <b-tab-item label="Add Books">
            <BookSelector :selected-books="selectedBookIds" @book-selected="bookSelected" />
          </b-tab-item>
          <b-tab-item label="Add Series">
            <SeriesSelector :selected-series="selectedSeriesIds" @series-selected="addSeries"
                            @series-subscribed="subscribeSeries" />
          </b-tab-item>
        </b-tabs>


      </div>
    </div>
  </section>
</template>

<script>
import BookSelector from "~/components/BookSelector";
import ReadingListEntry from "~/components/ReadingListEntry";
import SeriesSelector from "~/components/SeriesSelector";
import ReadingListEntryNormal from "~/components/ReadingListEntryNormal";
import Progress from "~/components/Progress.vue";
import ReadingListEditableEntry from "~/components/ReadingListEditableEntry.vue";

export default {
  name: "readingListDetails",
  components: {
    ReadingListEditableEntry,
    Progress, SeriesSelector, ReadingListEntry, BookSelector, ReadingListEntryNormal
  },
  data() {
    return {
      readingListId: null,
      readingList: null,
      editMode: false,
      enableReadBefore: false,
      loading: false,
      booksLeftToAdd: 0,
      booksTotalToAdd: 1,
      reverseEntriesOrder: true,
    };
  },
  computed: {
    selectedBookIds() {
      return this.readingList?.entries.map(e => e.book.id);
    },
    selectedSeriesIds() {
      return this.readingList?.series.map(s => s.id);
    },
    readEntries() {
      return this.readingList?.entries.filter(e => e.book.last_read_history && e.book.last_read_history.read_date && !e.book.last_read_history.want_to_reread).length;
    },
    progress() {
      if (this.readingList?.entries.length === 0) {
        return 0;
      }
      return this.readEntries / this.readingList?.entries.length * 100;
    },
    nextEntry() {
      return this.readingList?.entries?.find((e) => !e.book.last_read_history || !e.book.last_read_history.read_date  || e.book.last_read_history.want_to_reread);
    },
    seriesNames() {
      return this.readingList?.series.map(s => s.title).join(", ");
    },
    entries() {
      const entries = [...this.readingList.entries];
      if(this.reverseEntriesOrder){
        entries.reverse();
      }
      return entries;
    }
  },
  loading: true,
  methods: {
    updateComponent(route = this.$route) {
      this.readingListId = route.params.id;

      this.$axios.$get(this.getApiUrl()).then(response => {
        this.readingList = response;
      });
    },
    getApiUrl() {
      return "/reading-list/" + this.readingListId + "/";
    },
    bookSelected(book) {
      return this.$axios.$post("/reading-list/" + this.readingListId + "/entries/", {
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

      this.$axios.$put("/reading-list/" + this.readingListId + "/entries/" + entry.id + "/", {
        position: parseInt(position, 10)
      }).then(() => this.updateComponent());
    },
    markAsRead(book) {
      this.$api.bookRead(book).then(() => this.updateComponent());
    },
    markAsReadBefore(book) {
      // Just put them as read some time before the tool was developed
      this.$api.bookRead(book, "2020-02-01T00:00:00Z").then(() => this.updateComponent());
    },
    wantToReread(book, wantToReread = true){
      return this.$api.bookWantToReread(book, wantToReread).then(() => this.updateComponent());
    },
    remove(entry) {
      this.$axios.$delete("/reading-list/" + this.readingListId + "/entries/" + entry.id + "/")
        .then(() => this.updateComponent());
    },
    archive() {
      this.$axios.$patch("/reading-list/" + this.readingListId + "/", {
        "archived": !this.readingList.archived
      }).then(() => this.updateComponent());
    },
    massUpdateReread(books, wantToReread){
      return books.reduce(
        (promise, entry, index) =>
          promise
            // Update regularly the UI
            .then(() => index % 10 === 0 && this.updateComponent())
            // Update next book in the list
            .then(() => this.$api.bookWantToReread(entry.book, wantToReread)),
        Promise.resolve()
      )
        .then(() => this.updateComponent());
    },
    markForReread() {
      if (!confirm("Are you sure you want to reread this list?")) {
        return;
      }
      const toUpdate = this.readingList.entries.filter(
        entry => entry.book.last_read_history && !entry.book.last_read_history.want_to_reread
      );
      return this.massUpdateReread(toUpdate, true);
    },
    markForRead() {
      if(!confirm("Are you sure you want to mark as read again books this list?")){
        return;
      }
      const toUpdate = this.readingList.entries.filter(
        entry => entry.book.last_read_history && entry.book.last_read_history.want_to_reread
      );
      return this.massUpdateReread(toUpdate, false);
    },
    addSeries(series) {
      this.loading = true;
      this.$axios.$get("/book/?limit=1000&series=" + series.id).then(({ count, results }) => {
        this.booksLeftToAdd = count;
        this.booksTotalToAdd = count;
        const pushNextBook = () => {
          const book = results.shift();
          return this.$axios.$post("/reading-list/" + this.readingListId + "/entries/", {
            book: book.id
          });
        };
        // This function go through every books in the series and add them one by one to the list
        const pushUntilDone = () => {
          return pushNextBook()
            .catch(() => true) // This catch the case when you have a book already in the list
            .then(() => {
              this.booksLeftToAdd = results.length;
              if (results.length > 0) {
                return pushUntilDone();
              }
            });
        };
        return pushUntilDone();

      })
        .catch(() => true) // Prevent locking in loading if there is any error
        .then(() => {
          this.loading = false;
          this.booksLeftToAdd = 0;
          this.updateComponent();
        });
    },
    subscribeSeries(series) {
      this.$axios.$post("/reading-list/" + this.readingListId + "/series/", {
        series_id: series.id
      }).then(() => this.updateComponent());
    },
    removeSeries(series) {
      this.$axios.$delete("/reading-list/" + this.readingListId + "/series/" + series.id + "/")
        .then(() => this.updateComponent());
    },
    updateList() {
      this.$axios.$patch("/reading-list/" + this.readingListId + "/", {
        "title": this.readingList.title
      }).then(() => this.updateComponent());
    },
    deleteList() {
      if(!confirm(`Are you sure you want to delete the list "${this.readingList.title}"?`)){
        return;
      }

      this.$axios.$delete("/reading-list/" + this.readingListId + "/")
        .then(() => {
          this.$router.push('/reading-list/');
        });
    }
  },
  beforeMount() {
    this.updateComponent(this.$route);
  }
};
</script>
