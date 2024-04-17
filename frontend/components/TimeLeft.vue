<script>
export default {
  name: "TimeLeft",
  props: {
    time_left: {
      default: 0
    }
  },
  computed: {
    time_left_human() {
      let timeLeft = this.time_left;

      if (timeLeft < 0) {
        return "Done Already";
      }

      const humanDisplay = [];
      if (timeLeft > 365) {
        const years = timeLeft / 365 | 0;
        humanDisplay.push(years, "years");
        timeLeft -= years*365;
      }
      if (timeLeft > 30) {
        const months = timeLeft / 30 | 0;
        humanDisplay.push(months, "months");
        timeLeft -= months * 30;
      }
      if (timeLeft > 0) {
        humanDisplay.push(timeLeft | 0, "days");
      }

      if(humanDisplay.length === 0){
        return "Never";
      }

      return humanDisplay.join(" ");
    }
  }
};
</script>

<template>
<span>
  {{ time_left_human }}
</span>
</template>

<style scoped>

</style>
