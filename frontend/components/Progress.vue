<template>
  <div class="progress-bar">
    <div v-if="indeterminate" class="progress-indeterminate"></div>
    <progress v-else class="progress" max="100" :value="value"></progress>
    <p class="progress-value"><slot></slot></p>
  </div>
</template>

<script>
export default {
  name: "Progress",
  props: {
    "value": {
      default: "",
    },
    "indeterminate": {
      default: false,
    },
  }
}
</script>
