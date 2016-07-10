(function () {
  'use strict';

  angular
    .module('noteapp', [
      'noteapp.routes',
      'noteapp.authentication'
    ]);

  angular.module('noteapp.routes', ['ngRoute']);

  angular.module('noteapp.config', []);

   angular.module('noteapp').run(run);

  run.$inject = ['$http'];

  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }

})();