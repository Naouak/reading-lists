<template>
  <div class="weekly-heatmap stat-block">
      <h2>When I read</h2>
      <table>
        <tr>
          <th></th>
          <th v-for="hour in [...Array(24).keys()]" :key="hour">{{ ("00" + hour).slice(-2) }}:00</th>
        </tr>
        <tr v-for="(hours, day) in weekly_heatmap" :key="day">
          <th>{{ days[day] }}</th>
          <td v-for="(read_per_hour, hour) in hours" :key="hour"
              :style="{'backgroundColor':'rgba(0,255,0,'+(read_per_hour*(1/max_weekly_heatmap))+')'}">
            {{ read_per_hour }}
          </td>
        </tr>
      </table>
    </div>
</template>

<script>
export default {
  name: "ReadingWeeklyHeatmap",
  props: {
    read_books: []
  },
  data(){
    return {
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"],
    }
  },
  computed: {
    weekly_heatmap() {
      return this.read_books.reduce((acc, item) => {
        const date = new Date(item.read_date);
        const day = (date.getDay()+13)%7;
        const hour = date.getHours();
        if (!acc[day]) {
          acc[day] = new Array(24).fill(0);
        }
        acc[day][hour] = (acc[day][hour] || 0) + 1;
        return acc;
      }, []);
    },
    max_weekly_heatmap() {
      return Math.max(...this.weekly_heatmap.map((perHours) => Math.max(...perHours)));
    }
  }
}
</script>

<style scoped>

</style>
