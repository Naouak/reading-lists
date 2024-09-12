<template>
  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
          <p class="control has-icons-left">
            <input :value="value" type="text" class="input" placeholder="Filter" @input="$emit('input', $event.target.value)" />
            <span class="icon is-left"><b-icon icon="magnify" /></span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "SearchCard",
  props: {
    value: {}
  }
};
</script>
