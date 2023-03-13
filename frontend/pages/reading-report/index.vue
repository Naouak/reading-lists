<template>
  <div></div>
</template>

<script>
export default {
  name: "ReadingReportRedirect",
  beforeMount() {
    const year = new Date().getFullYear();
    const month = new Date().getMonth()+1;
    this.$router.push("/reading-report/"+year+"/"+month);
  }
}
</script>

<style scoped>

</style>
