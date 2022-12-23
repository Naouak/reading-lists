<template>
  <section class="section">
    <button @click="login">LOGIN</button>
  </section>
</template>

<script>
export default {
  name: "login",
  methods: {
    login(){
      this.$auth.loginWith('api');
    }
  },
}
</script>
