<template>
  <span>{{formattedDate}}</span>
</template>

<script>
export default {
  name: "DateDisplay",
  props: {
    date: {
      required: true,
    },
  },
  computed: {
    formattedDate() {
      const date = new Date(this.date);
      return date.toLocaleDateString();
    },
  },
}
</script>
