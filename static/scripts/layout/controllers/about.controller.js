(function () {
  'use strict';

  angular
    .module('noteapp.layout.controllers')
    .controller('AboutController', IndexController);

  IndexController.$inject = ['$scope'];

  function AboutController($scope) {
    var vm = this;

  }
})();