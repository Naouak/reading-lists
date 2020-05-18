<template>
  <span>{{formattedDate}}</span>
</template>

<script>
function toIsoDate(date) {
  return [date.getFullYear(), ("0" + (date.getUTCMonth() + 1)).substr(-2), ("0" + date.getDate()).substr(-2)].join('-');
}

export default {
  name: "RelativeDateDisplay",
  props: {
    date: {
      required: true,
    },
  },
  computed: {
    formattedDate() {
      const today = new Date();
      const isoToday = toIsoDate(today);
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const isoYesterday = toIsoDate(yesterday);

      const isoDate = toIsoDate(new Date(this.date));

      if(isoDate === isoToday){
        return 'Today';
      } else if (isoDate === isoYesterday){
        return 'Yesterday';
      } else {
        return isoDate;
      }
    },
  },
}
</script>

<style scoped>

</style>
