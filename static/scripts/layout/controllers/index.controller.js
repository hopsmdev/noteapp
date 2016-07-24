(function () {
  'use strict';

  angular
    .module('noteapp.layout.controllers')
    .controller('IndexController', IndexController);

  IndexController.$inject = ['$scope', 'Authentication', 'Notes', 'Tags'];

  function IndexController($scope, Authentication, Notes, Tags) {
    var vm = this;

    vm.isAuthenticated = Authentication.isAuthenticated();
    vm.notes = [];
    vm.tags = [];

    get_published_notes();
    get_tags()

    function get_published_notes() {

      Notes.get_published().then(notesSuccessFn, notesErrorFn);

      function notesSuccessFn(data, status, headers, config) {
        vm.notes = data.data;
        console.log(data.data)
      }

      function notesErrorFn(data, status, headers, config) {
         console.error(data.error);
      }
    }

    function get_tags() {

      Tags.all().then(tagsSuccessFn, tagsErrorFn);

      function tagsSuccessFn(data, status, headers, config) {
        vm.tags = data.data;
        console.log(data.data)
      }

      function tagsErrorFn(data, status, headers, config) {
         console.error(data.error);
      }
    }


  }
})();