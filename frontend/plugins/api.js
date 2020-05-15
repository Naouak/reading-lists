class Api{
  constructor({$axios}){
    this.$axios = $axios;
  }

  bookRead(book){
    return this.$axios.$post('/book/' + book.id + '/read/', {});
  }
}

export default function (context, inject) {
  context.$api = new Api(context);
  inject('api', context.$api);
}
