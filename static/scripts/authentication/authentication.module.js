(function () {
  'use strict';

  angular
    .module('noteapp.authentication', [
      'noteapp.authentication.controllers',
      'noteapp.authentication.services'
    ]);

  angular
    .module('noteapp.authentication.controllers', []);

  angular
    .module('noteapp.authentication.services', ['ngCookies']);
})();