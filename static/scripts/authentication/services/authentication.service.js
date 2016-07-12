(function () {
  'use strict';

  angular
    .module('noteapp.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  function Authentication($cookies, $http) {

    var Authentication = {

        register: register,
        login: login,

        getAuthenticatedAccount: getAuthenticatedAccount,
        isAuthenticated: isAuthenticated,
        setAuthenticatedAccount: setAuthenticatedAccount,
        unauthenticate: unauthenticate
    };

    return Authentication;

    function getAuthenticatedAccount() {
        if (!$cookies.authenticatedAccount) {
            return;
        }
        return JSON.parse($cookies.authenticatedAccount);
    }

    function isAuthenticated() {
        return !!$cookies.authenticatedAccount;
    }

    function setAuthenticatedAccount(account) {
        $cookies.authenticatedAccount = JSON.stringify(account);
    }

    function unauthenticate() {
        delete $cookies.authenticatedAccount;
    }

    function register(email, password, username) {
        return $http.post('/api/v1/account/register/', {
            'username': username,
            'password': password,
            'email': email
    }).then(registerSuccessFn, registerErrorFn);

        function registerSuccessFn(data, status, headers, config) {
            Authentication.login(email, password);
        }

        function registerErrorFn(data, status, headers, config) {
            console.error('Cannot register', data, status, headers);
        }
    }

    function login(username, password) {
        return $http.post('/api/v1/auth/login/', {
            username: username,
            password: password
    }).then(loginSuccessFn, loginErrorFn);


        function loginSuccessFn(data, status, headers, config) {
            Authentication.setAuthenticatedAccount(data.data);
            window.location = '/';
        }

        function loginErrorFn(data, status, headers, config) {
            console.error('Epic failure!');
        }
    }
  }
})();