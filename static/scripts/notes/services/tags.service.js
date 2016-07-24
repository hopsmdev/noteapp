(function () {
  'use strict';

  angular
    .module('noteapp.notes.services')
    .factory('Tags', Tags);

  Tags.$inject = ['$http'];

  function Tags($http) {
    var Tags = {
      all: all,
      create: create
    };

    return Tags;

    function all() {
      return $http({
        method: "GET",
        url: '/api/v1/tags/',
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