(function () {
  'use strict';

  angular
    .module('noteapp.notes.services')
    .factory('Notes', Notes);

  Notes.$inject = ['$http'];

  function Notes($http) {
    var Notes = {
      get_published: get_published,
      get: get,
      create: create
    };

    return Notes;

    function get_published() {
      return $http({
        method: "GET",
        url: '/api/v1/notes/published/',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
      })
    }


    /** TODO **/
    function create(content) {
      return $http.post('/api/v1/notes/', {
        content: content
      });
    }

    /** TODO **/
    function get(id) {
      return $http.get('/api/v1/accounts/' + id + '/posts/');
    }
  }
})();