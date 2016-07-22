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
        logout: logout,
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

         return $http({
            method: 'POST',
            url: '/api/v1/auth/register/',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': $cookies['csrftoken']
            },
            data: {
                username: username,
                password: password,
                email: email
            }
    }).then(registerSuccessFn, registerErrorFn);

        function registerSuccessFn(data, status, headers, config) {
            Authentication.login(username, password);
        }

        function registerErrorFn(data, status, headers, config) {
            console.error('Cannot register', data, status, headers);
        }
    }

    function login(username, password) {
        return $http({
            method: 'POST',
            url: '/api/v1/auth/login/',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': $cookies['csrftoken']
            },
            data: {
                username: username,
                password: password
            }
    }).then(loginSuccessFn, loginErrorFn);


        function loginSuccessFn(data, status, headers, config) {
            Authentication.setAuthenticatedAccount(data.data);
            window.location = '/';
        }

        function loginErrorFn(data, status, headers, config) {
            console.error('Cannot login!', data, headers);
        }
    }

    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);


      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();

        window.location = '/';
      }

      function logoutErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }



  }
})();