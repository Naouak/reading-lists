<script>
export default {
  name: "VSelect",
  props: {
    value: {},
    options: [],
  },
  computed: {
    selectedValue(){
      return this.options.map(option => option.value).indexOf(this.value);
    }
  },
  methods: {
    updateValue(newValue){
      this.$emit('input', this.options[newValue].value);
    }
  }
};
</script>

<template>
  <select :value="selectedValue" @input="updateValue($event.target.value)">
    <option v-for="(option, i) in options" :key="i" :value="i">{{option.text}}</option>
  </select>
</template>

<style scoped>

</style>
