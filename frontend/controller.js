angular.module('starter', [])
.controller('MainCtrl', function($scope,$http,Data,$q) {
// get information of all companies
  if (Data.getLoad()) {
  $http.get('companyList.json').success(function(data) {
    Data.setList(data.records);
    var group = setGroup(data.records);
    Data.setGroup(group);
    $scope.companies= Data.getGroup();
    Data.setLoad(false); 
  })
}
//group the companies in alphabet order
  var setGroup = function(records) {
    records.sort(function(a, b){
     var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase()
     if (nameA < nameB) //sort string ascending
      return -1 
     if (nameA > nameB)
      return 1
     return 0 //default return value (no sorting)
    });
    var nameSort = [];
    var objList = records;
        if (objList.length>0) {
          var tag = objList[0].name;
          var sameGroup = [objList[0]];
          for (i = 1; i < objList.length; i++) {
            if (objList[i].name.charAt(0).toUpperCase() == objList[i].name.charAt(0).toLowerCase())
            { 
              sameGroup.push(objList[i]);
            }
            else if (objList[i].name.charAt(0).toUpperCase() == tag.charAt(0).toUpperCase()) {
              sameGroup.push(objList[i]);
            }
            else {
              if (sameGroup[0].name.charAt(0).toUpperCase() == sameGroup[0].name.charAt(0).toLowerCase())
                nameSort.push(["#",sameGroup]);
              else nameSort.push([sameGroup[0].name.charAt(0).toUpperCase(),sameGroup]);
              sameGroup = [objList[i]];
              tag = objList[i].name;
            }
          }
          nameSort.push([sameGroup[0].name.charAt(0).toUpperCase(),sameGroup]);
        }
      return nameSort;

  }
//send requests to get the number of tweets based on different requirements for companies from CouchDB
  var sendRequest = function(requestType) {
        var deferred = $q.defer();
        var httpString = "http://115.146.89.12:5984/tweets/_design/company/_view/" + requestType + "?group=true";
        $http.get(httpString)
  .success(function (response) {var data = response.rows;
               for (var i = 0; i < data.length; i++) {
                  Data.addInfo(data[i].key, data[i].value, requestType)
                }
                console.log(requestType+ " OK");
                deferred.resolve("success");              
  });
  return deferred.promise;

  }
  $scope.companies = Data.getGroup();
  $scope.names = [];
  if (Data.get()){
//send request to CouchDB and get the number of tweets for positive before, positive after, negative before, negative after, neutral before, neutral after
    $q.all([sendRequest("positiveBefore"),sendRequest("positiveAfter"),sendRequest("negativeBefore"),sendRequest("negativeAfter"),sendRequest("neutralBefore"),sendRequest("neutralAfter")])
    .then(function(value) {
    //draw chart
    Data.drawBarChart();
    Data.drawBigPieChart();
    Data.drawTotalNumBar();
    $scope.names = Data.getList();
    Data.setDataStatus(true);
    })
  Data.set(false);
}
  if (Data.getDataStatus()) {
    Data.drawBarChart();
    Data.drawBigPieChart();
    Data.drawTotalNumBar();
    $scope.names = Data.getList();
    }

  })

.controller('CompanyCtrl', function($scope,$stateParams,$http,Data) {

//show the detailed information of a company
  var companyAccount = $stateParams.companyName;
  var company = Data.getCompany(companyAccount);
  $scope.account = company.account;
  $scope.companyLink = company.website;
  $scope.date = company.dateCertified;
  $scope.Cname = company.name;
  $scope.positiveBefore = company.positiveBefore;
  $scope.positiveAfter = company.positiveAfter;
  $scope.negativeBefore = company.negativeBefore;
  $scope.negativeAfter = company.negativeAfter;
  $scope.neutralBefore = company.neutralBefore;
  $scope.neutralAfter = company.neutralAfter;
  Data.drawChart(companyAccount);

  });

