<template>
  <div>
    <nav
      class="nav-bar navbar header has-shadow is-primary"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <nuxt-link class="navbar-item" :to="item.to" v-for="(item, key) of items" :key="key" :title="item.title">
          <span>
            <b-icon :icon="item.icon" />
            <span class="is-hidden-mobile">{{ item.title }}</span>
          </span>
        </nuxt-link>
      </div>
    </nav>

    <section class="main-content">
      <div class="">
        <nuxt />
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuVisible: false,
      items: [
        {
          title: 'New Releases',
          icon: 'home',
          to: {name: 'index'},
        },
        {
          title: 'Books',
          icon: 'book-open-page-variant',
          to: {name: 'books'},
        },
        {
          title: 'Series',
          icon: 'lightbulb',
          to: {name: 'series'},
        },
        {
          title: 'Reading Lists',
          icon: 'bookshelf',
          to: {name: 'reading-list'},
        },
        {
          title: 'History',
          icon: 'history',
          to: {name: 'history'}
        },
        {
          title: 'Statistics',
          icon: 'chart-line',
          to: {name: 'statistics'}
        },
        {
          title: 'Completion Stats',
          icon: 'chart-histogram',
          to: {name: 'completion'}
        },
        {
          title: 'Issue Relations',
          icon: 'link-variant',
          to: {name: 'book-links'}
        }
      ],
    };
  },
};
</script>
