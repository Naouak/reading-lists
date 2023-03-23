<template>
  <div class="report-stats-lists">
    <div class="list-block">
      <h2 class="subtitle">Read by Series</h2>
      <table>
        <tr v-for="(data, index) in read_series" :key="data.title">
          <th class="list-item-index">#{{ index + 1 }}</th>
          <th class="list-item-title">{{ data.title }}</th>
          <td class="list-item-value">{{ data.read.length }}</td>
        </tr>
      </table>
    </div>

    <div class="list-block">
      <h2 class="subtitle">Read by reading list</h2>

      <table>
        <tr v-for="(data, index) in read_lists" :key="data.title">
          <th class="list-item-index">#{{ index + 1 }}</th>
          <th class="list-item-title">{{ data.title }}</th>
          <td class="list-item-value">{{ data.read.length }} / {{ data.total_count }}</td>
        </tr>
      </table>
    </div>

    <div class="list-block">
      <h2 class="subtitle">Read by publication year</h2>

      <table>
        <tr v-for="(count, year) in read_per_year" :key="year">
          <th class="list-item-title">{{ year }}</th>
          <td class="list-item-value">{{ count }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReadingReportLists",

  props: {
    read_series: [],
    read_lists: [],
    read_per_year: {}
  }
}
</script>

<style scoped>

</style>
