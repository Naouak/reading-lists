class Api {
  constructor({$axios}) {
    this.$axios = $axios;
  }

  bookRead(book, readDate = null) {
    const data = {};
    if (readDate) {
      data.read_date = readDate;
    }
    return this.$axios.$post('/book/' + book.id + '/read/', data);
  }

  bookWantToReread(book, wantToReread = true) {
    return this.$axios.$post('/book/' + book.id + '/want_to_reread/', {want_to_reread: wantToReread});
  }
}

export default function (context, inject) {
  context.$api = new Api(context);
  inject('api', context.$api);

  context.$axios.onError(error => {
    const code = parseInt(error.response && error.response.status)
    if (code === 401) {
      context.$auth.logout();
      context.redirect('/login');
    }
  })
}
