class Api {
  constructor({$axios}) {
    this.$axios = $axios;
  }

  bookRead(book) {
    return this.$axios.$post('/book/' + book.id + '/read/', {});
  }
}

export default function (context, inject) {
  context.$api = new Api(context);
  inject('api', context.$api);

  context.$axios.onError(error => {
    const code = parseInt(error.response && error.response.status)
    if (code === 401) {
      context.$auth.logout();
      context.$router.push('login');
    }
  })
}
