<template>
  <div>
    <nav
      class="navbar header has-shadow is-primary"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          My Library
        </a>

        <div class="navbar-burger">
          <span />
          <span />
          <span />
        </div>
      </div>
    </nav>

    <section class="main-content columns">
      <aside class="column is-2 section">
        <p class="menu-label is-hidden-touch">
          Menu
        </p>
        <ul class="menu-list">
          <li v-for="(item, key) of items" :key="key">
            <nuxt-link :to="item.to" exact-active-class="is-active">
              <b-icon :icon="item.icon" />
              {{ item.title }}
            </nuxt-link>
          </li>
        </ul>
      </aside>

      <div class="column is-10">
        <nuxt />
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          title: 'Home',
          icon: 'home',
          to: {name: 'index'},
        },
        {
          title: 'Books',
          icon: 'lightbulb',
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
          icon: 'chart-line',
          to: {name: 'completion'}
        },
      ],
    };
  },
};
</script>
