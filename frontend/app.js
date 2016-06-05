var app = angular.module('myapp',['ui.router','services','starter']);
//this is used to control the route for different pages
app.config(function($stateProvider, $urlRouterProvider,$httpProvider) {

$stateProvider.state('main', {
        url: '/main',
        templateUrl: 'main.html',
        controller: 'MainCtrl'
      });

 $stateProvider.state('company', {
        url: '/company/:companyName',
        templateUrl: 'company.html',
        controller: 'CompanyCtrl'
      });

 $urlRouterProvider.otherwise('/main');



});
