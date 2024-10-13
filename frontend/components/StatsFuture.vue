<script>
export default {
  name: "StatsFuture",
  props: {
    total_book: {},
    total_read: {},
    read_per_month: {},
    added_per_month: {},
  },
  methods: {
    progress_in(months = 1, added = 0) {
      return ((this.total_read + months * this.read_per_month) / (Math.max(this.total_book, 1) + months * added) * 10000 | 0) / 100;
    }
  }
};
</script>

<template>
  <div class="box">
    <h2 class="subtitle">In the future</h2>

    <div class="columns" style="text-align: center">
      <div class="column">
        <div class="subtitle">In a month</div>
        <div class="title">{{ progress_in(1) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 3 months</div>
        <div class="title">{{ progress_in(3) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 6 months</div>
        <div class="title">{{ progress_in(6) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In a year</div>
        <div class="title">{{ progress_in(12) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 5 years</div>
        <div class="title">{{ progress_in(60) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 10 years</div>
        <div class="title">{{ progress_in(120) }}%</div>
      </div>
    </div>

    <div class="columns" style="text-align: center">
      <div class="column">
        <div class="subtitle">In a month</div>
        <div class="title">{{ progress_in(1, added_per_month) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 3 months</div>
        <div class="title">{{ progress_in(3, added_per_month) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 6 months</div>
        <div class="title">{{ progress_in(6, added_per_month) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In a year</div>
        <div class="title">{{ progress_in(12, added_per_month) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 5 years</div>
        <div class="title">{{ progress_in(60, added_per_month) }}%</div>
      </div>
      <div class="column">
        <div class="subtitle">In 10 years</div>
        <div class="title">{{ progress_in(120, added_per_month) }}%</div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
