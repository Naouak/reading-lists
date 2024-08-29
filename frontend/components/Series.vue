<template>
  <div class="box">
    <nuxt-link :to="{name:'series-id-books', params: {id: series.id}}">
      <div class="media">
        <div class="media-left">
          <figure style="width: 70px;">
            <img style="width: auto; height: auto;" :src="series.cover_url" :alt="series.title">
          </figure>
        </div>
        <div class="media-content">
          <div class="content">
            <div class="subtitle">{{series.title}}</div>
            <div class="subtitle">{{series.book_count}} issues</div>
          </div>
        </div>
      </div>
    </nuxt-link>
  </div>

</template>

<script>

export default {
  components: {},
  props: {
    series: {
      type: Object,
    },
  },
};
</script>
