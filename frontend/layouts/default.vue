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

        <button class="navbar-menu-button" @click="menuVisible=!menuVisible">
          <b-icon icon="menu" />
        </button>
      </div>
    </nav>

    <section class="main-content">
      <div class="">
        <nuxt />
      </div>

      <aside class="nav-menu column section" v-if="menuVisible" @click="menuVisible=false">
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
        {
          title: 'Issue Relations',
          to: {name: 'book-links'}
        }
      ],
    };
  },
};
</script>
