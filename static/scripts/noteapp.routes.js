(function () {
  'use strict';

  angular
    .module('noteapp.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  function config($routeProvider) {

    $routeProvider.when('/', {
      controller: 'IndexController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/main.html'
    }).when('/register', {
        controller: 'RegisterController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/register.html'
    }).when('/login', {
        controller: 'LoginController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/login.html'
    }).when('/about', {
        controller: 'AboutController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/about.html'
    }).otherwise('/');

  }
})();