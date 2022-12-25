<template>
  <div class="box column is-2">
    <h1 class="title">{{ year }}</h1>
    <div class="year-completion">
      <Progress :value="data.progress">{{ data.read }} / {{ data.books }} read</Progress>
    </div>
    <div class="month-completion">
      <div v-for="(_, month) in months.slice(1)" :key="month">
        <Progress :value="data.months[month+1]?.progress" :indeterminate="!(data.months[month+1]?.books)">
          {{ months[month+1] }} - {{ data.months[month+1]?.read || 0 }} / {{ data.months[month+1]?.books || 0 }} read
        </Progress>
      </div>
    </div>
  </div>
</template>

<script>
import Progress from "~/components/Progress.vue";

export default {
  name: "CompletionProgressFullYear",
  components: {
    Progress
  },
  props: {
    year: {
      required: true
    },
    data: {
      required: true
    }
  },
  data() {
    return {
      months: ["", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"],
    }
  }
}
</script>
