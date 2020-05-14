<template>
  <div class="column">
    <div class="card">
      <div class="card-content">
        <slot />
      </div>
      <footer class="card-footer">
        <p class="card-header-title has-text-grey">
          {{ title }}
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
  },
};
</script>
