<template>
  <div class="progress-bar">
    <div v-if="indeterminate" class="progress-indeterminate"></div>
    <progress v-else class="progress" :max="max" :value="value"></progress>
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
    "max": {
      default: 100
    },
    "indeterminate": {
      default: false,
    },
  }
}
</script>
