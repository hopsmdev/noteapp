(function () {
  'use strict';

  angular
    .module('noteapp.layout.controllers')
    .controller('IndexController', IndexController);

  IndexController.$inject = ['$scope', 'Authentication', 'Notes'];

  function IndexController($scope, Authentication, Notes) {
    var vm = this;

    vm.isAuthenticated = Authentication.isAuthenticated();
    vm.notes = [];

    activate();

    function activate() {

      Notes.get_published().then(notesSuccessFn, notesErrorFn);

      function notesSuccessFn(data, status, headers, config) {
        vm.notes = data.data;
        console.log(data.data)
      }

      function notesErrorFn(data, status, headers, config) {
         console.error(data.error);
      }

    }
  }
})();