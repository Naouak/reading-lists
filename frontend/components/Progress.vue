<template>
  <div class="progress-bar">
    <progress class="progress" max="100" :value="value"></progress>
    <p class="progress-value"><slot></slot></p>
  </div>
</template>

<script>
export default {
  name: "Progress",
  props: {
    "value": {
      default: ""
    }
  }
}
</script>

<style scoped>

</style>
