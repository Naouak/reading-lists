<template>
  <div class="weekly-heatmap stat-block">
    <h2>When I read</h2>

    <svg width="100%" height="300">
      <!-- Hours -->
      <svg viewBox="0 0" x="10%" width="90%" height="10%">
        <text
          v-for="hour in [...Array(24).keys()]" :key="hour"
          text-anchor="middle" dominant-baseline="auto" :x="100*((hour+.5)/24)+'%'" y="90%">
          {{ ("00" + hour).slice(-2) }}:00
        </text>
      </svg>


      <!-- Days -->
      <svg viewBox="0 0" x="0" width="10%" y="10%" height="90%">
        <g v-for="(_, day) in weekly_heatmap" :key="day">
          <svg x="0" :y="(day)*(100/weekly_heatmap.length)+'%'" :height="(100/weekly_heatmap.length)+'%'" width="100%">
            <text text-anchor="end" dominant-baseline="middle" x="90%" y="50%">
              {{ days[day] }}
            </text>
          </svg>
        </g>
      </svg>


      <!-- Data -->
      <svg viewBox="0 0" x="10%" width="90%" y="10%" height="90%">
        <!-- Tick Line Hours -->
        <rect v-for="hour in [...Array(24).keys()]" :key="hour" width="1" height="100%" :x="100*((hour+.5)/24)+'%'"
              y="0%" fill="RGBA(0,0,0,.1)" />

        <g v-for="(hours, day) in weekly_heatmap" :key="day">
          <!-- Tick Line Days -->
          <rect width="100%" height="1" x="0%" :y="(day+.5)*(100/weekly_heatmap.length)+'%'" fill="RGBA(0,0,0,.1)" />

          <svg v-for="(read_per_hour, hour) in hours" :key="hour"
               viewBox="0 0 100 100"
               :x="100*((hour)/24)+'%'"
               :y="(day)*(100/weekly_heatmap.length)+'%'"
               :height="(100/weekly_heatmap.length)+'%'"
               :width="100/24+'%'"
          >
            <circle
              v-if="read_per_hour>0"
              :r="(50*read_per_hour/max_weekly_heatmap)+'%'"
              cx="50%"
              cy="50%"
              fill="RGBA(0,255,0,.7)" />
            <text fill="white" v-if="read_per_hour>0" :font-size="(50*read_per_hour/max_weekly_heatmap)"
                  text-anchor="middle" dominant-baseline="middle" x="50%" y="50%">{{ read_per_hour }}
            </text>
          </svg>
        </g>
      </svg>


    </svg>
  </div>
</template>

<script>
export default {
  name: "ReadingWeeklyHeatmap",
  props: {
    read_books: []
  },
  data() {
    return {
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    };
  },
  computed: {
    weekly_heatmap() {
      return this.read_books.reduce((acc, item) => {
        const date = new Date(item.read_date);
        const day = (date.getDay() + 13) % 7;
        const hour = date.getHours();
        if (!acc[day]) {
          acc[day] = new Array(24).fill(0);
        }
        acc[day][hour] = (acc[day][hour] || 0) + 1;
        return acc;
      }, Array(7).fill(null).map(_ => Array(24).fill(0)));
    },
    max_weekly_heatmap() {
      console.log(this.weekly_heatmap)
      return Math.max(1,...this.weekly_heatmap.map((perHours) => Math.max(...perHours)));
    }
  }
};
</script>

<style scoped>

</style>
