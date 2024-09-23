<script>
export default {
  name: "StatsBlock",
  props: {
    title: null,
    value: null,
    unit: null
  }
};
</script>

<template>
  <div class="stat-block">
    <h2>{{ title }}</h2>
    <div class="stats-full-value">
      <span class="stats-value">{{ value }}</span> {{ unit }}
    </div>
  </div>
</template>

<style scoped>

</style>
