(function () {
  'use strict';

  angular
    .module('noteapp.notes.controllers')
    .controller('NotesController', NotesController);

  NotesController.$inject = ['$scope', 'Notes'];


  function NotesController($scope, Notes) {
    var vm = this;
  }
})();