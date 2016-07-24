(function () {
  'use strict';

  angular
    .module('noteapp.notes.controllers')
    .controller('TagsController', TagsController);

  TagsController.$inject = ['$scope', 'Notes'];

  function TagsController($scope, Tags) {
    var vm = this;
  }
})();