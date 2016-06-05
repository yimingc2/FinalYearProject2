angular.module('services', [])
.factory('Data', function() {

  var update = true;
  var dataFinished = false;
  var loadList = true;
  var allCompany = [];
  var groupCompany = [];
  var totalPositiveBefore = 0;
  var totalNegativeBefore = 0;
  var totalNeutralBefore = 0;
  var totalPositiveAfter = 0;
  var totalNegativeAfter = 0;
  var totalNeutralAfter = 0;
  var bar1Positive = [];
  var bar1Negative = [];
  var bar1Neutral = [];
  var bar2Positive = [];
  var bar2Negative = [];
  var bar2Neutral = [];
  var bar3Positive = [];
  var bar3Negative = [];
  var bar3Neutral = [];
  var bar4Positive = [];
  var bar4Negative = [];
  var bar4Neutral = [];

// This function is used to draw a bar chart
 var setBar = function(id,positiveList,negativeList,neutralList,comment) {
          var chart = new CanvasJS.Chart(id,
    {
      title:{
      text: "Total number of tweets retrieved of each company" + comment   
      },
      axisY:{
        title:"number of tweets"   
      },
      axisX:{
        title:"company"
      }, 
      animationEnabled: true,
      data: [
      {        
        type: "stackedColumn",
        toolTipContent: "{label}<br/><span style='\"'color: '#EDCA93';'\"'><strong>{name}</strong></span>: {y}",
        name: "positive",
        showInLegend: "true",
        color: "#EDCA93",
        dataPoints: positiveList
      },  {        
        type: "stackedColumn",
        toolTipContent: "{label}<br/><span style='\"'color: '#695A42';'\"'><strong>{name}</strong></span>: {y}",
        name: "negative",
        showInLegend: "true",
        color:"#695A42",
        dataPoints: negativeList
      }, {        
        type: "stackedColumn",
        toolTipContent: "{label}<br/><span style='\"'color: '#B6B1A8';'\"'><strong>{name}</strong></span>: {y}",
        name: "neutral",
        showInLegend: "true",
        indexLabel: "#total",
        color:"#B6B1A8",
        dataPoints: neutralList
      }                       
      ]
      ,
      legend:{
        cursor:"pointer",
        itemclick: function(e) {
          if (typeof (e.dataSeries.visible) ===  "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
          }
          else
          {
            e.dataSeries.visible = true;
          }
          chart.render();
        }
      }
    });
    chart.render();
  }
	
return {
    get: function() {
      return update;
    },
    set: function(value) {
      update = value;
    },
    getLoad: function() {
      return loadList;
    },
    setLoad: function(value) {
      loadList = value;
    },
    setGroup: function(value) {
      groupCompany = value;
    },
    getGroup: function() {
      return groupCompany;
    },
    getDataStatus: function() {
      return dataFinished;
    },
    setDataStatus: function(value) {
      dataFinished = value;
    },
    setList: function(value) {
      var tmp = value;
      for (var i = 0;i < tmp.length;i++) {
          tmp[i].positiveBefore = '0';
          tmp[i].positiveAfter = '0';
          tmp[i].negativeBefore = '0';
          tmp[i].negativeAfter = '0';
          tmp[i].neutralBefore = '0';
          tmp[i].neutralAfter = '0';
      }
      allCompany = tmp;
    },
    getList: function() {
      return allCompany;
    },
//store the number of tweets based on different conditions
    addInfo: function(key, value, InfoType) {
        if (InfoType == 'positiveBefore') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].positiveBefore = value;
              break;
            }
          }
        }
        if (InfoType == 'positiveAfter') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].positiveAfter = value;
              break;
            }
          }
        }
        if (InfoType == 'negativeBefore') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].negativeBefore = value;
              break;
            }
          }
        }
        if (InfoType == 'negativeAfter') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].negativeAfter = value;
              break;
            }
          }
        }
        if (InfoType == 'neutralBefore') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].neutralBefore = value;
              break;
            }
          }
        }
        if (InfoType == 'neutralAfter') {
          for (var i=0;i<allCompany.length;i++) {
            if (allCompany[i].account == key) {
              allCompany[i].neutralAfter= value;
              break;
            }
          }
        }
    },

    getCompany: function(account) {
      for (var i=0;i<allCompany.length;i++) {
        if (allCompany[i].account == account) {
          return allCompany[i];
        }
      }

    },
//This function is used to draw pie charts for each company
    drawChart: function(account) {
      var positiveBefore = 0;
      var positiveAfter = 0;
      var negativeBefore = 0;
      var negativeAfter = 0;
      var neutralBefore = 0;
      var neutralAfter = 0;
      for (var i=0;i<allCompany.length;i++) {
        if (allCompany[i].account == account) {
          positiveBefore = parseInt(allCompany[i].positiveBefore);
          positiveAfter = parseInt(allCompany[i].positiveAfter);
          negativeBefore = parseInt(allCompany[i].negativeBefore);
          negativeAfter = parseInt(allCompany[i].negativeAfter);
          neutralBefore = parseInt(allCompany[i].neutralBefore);
          neutralAfter = parseInt(allCompany[i].neutralAfter);
          break;
        }
      }
      var beforeSum = positiveBefore + negativeBefore + neutralBefore;
      var afterSum = positiveAfter + negativeAfter + neutralAfter;
      
  var chart1 = new CanvasJS.Chart("chartContainer1",
  {
    title:{
      text: "Sentimental Analysis Before"
    },
                animationEnabled: true,
    legend:{
      verticalAlign: "center",
      horizontalAlign: "left",
      fontSize: 20,
      fontFamily: "Helvetica"        
    },
    theme: "theme2",
    data: [
    {        
      type: "pie",       
      indexLabelFontFamily: "Garamond",       
      indexLabelFontSize: 20,
      indexLabel: "{label} {y}%",
      startAngle:-20,      
      showInLegend: true,
      toolTipContent:"{legendText} {y}%",
      dataPoints: [
        {  y: (positiveBefore/beforeSum * 100).toFixed(2), legendText:"Positive", label: "Positive" },
        {  y: (negativeBefore/beforeSum * 100).toFixed(2), legendText:"Negative", label: "Negative" },
        {  y: (neutralBefore/beforeSum * 100).toFixed(2), legendText:"Neutral", label: "Neutral" },
      ]
    }
    ]
  });
     chart1.render();
    var chart2 = new CanvasJS.Chart("chartContainer2",
  {
    title:{
      text: "Sentimental Analysis After"
    },
                animationEnabled: true,
    legend:{
      verticalAlign: "center",
      horizontalAlign: "left",
      fontSize: 20,
      fontFamily: "Helvetica"        
    },
    theme: "theme2",
    data: [
    {        
      type: "pie",       
      indexLabelFontFamily: "Garamond",       
      indexLabelFontSize: 20,
      indexLabel: "{label} {y}%",
      startAngle:-20,      
      showInLegend: true,
      toolTipContent:"{legendText} {y}%",
      dataPoints: [
        {  y: (positiveAfter/afterSum * 100).toFixed(2), legendText:"Positive", label: "Positive" },
        {  y: (negativeAfter/afterSum * 100).toFixed(2), legendText:"Negative", label: "Negative" },
        {  y: (neutralAfter/afterSum * 100).toFixed(2), legendText:"Neutral", label: "Neutral" },
      ]
    }
    ]
  });
    chart2.render(); 
    },
//This function is used to draw bar charts for the total number of tweets retrieved of all companies
  drawBarChart: function() {

  totalPositiveBefore = 0;
  totalNegativeBefore = 0;
  totalNeutralBefore = 0;
  totalPositiveAfter = 0;
  totalNegativeAfter = 0;
  totalNeutralAfter = 0;

    for (var i = 0;i < allCompany.length;i++) {
        totalPositiveBefore = totalPositiveBefore + parseInt(allCompany[i].positiveBefore);
        totalNegativeBefore = totalNegativeBefore + parseInt(allCompany[i].negativeBefore);
        totalNeutralBefore = totalNeutralBefore + parseInt(allCompany[i].neutralBefore);
        totalPositiveAfter = totalPositiveAfter + parseInt(allCompany[i].positiveAfter);
        totalNegativeAfter = totalNegativeAfter + parseInt(allCompany[i].negativeAfter);
        totalNeutralAfter = totalNeutralAfter + parseInt(allCompany[i].neutralAfter);
    }
    var chart = new CanvasJS.Chart("barChart1",
    {
      title:{
        text: "Total number of tweets retrieved before and after being certified"
      },
      animationEnabled: true,
      legend: {
        cursor:"pointer",
        itemclick : function(e) {
          if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
              e.dataSeries.visible = false;
          }
          else {
              e.dataSeries.visible = true;
          }
          chart.render();
        }
      },
      axisY: {
        title: "Number of Tweets"
      },
      toolTip: {
        shared: true,  
        content: function(e){
          var str = '';
          var total = 0 ;
          var str3;
          var str2 ;
          for (var i = 0; i < e.entries.length; i++){
            var  str1 = "<span style= 'color:"+e.entries[i].dataSeries.color + "'> " + e.entries[i].dataSeries.name + "</span>: <strong>"+  e.entries[i].dataPoint.y + "</strong> <br/>" ; 
            total = e.entries[i].dataPoint.y + total;
            str = str.concat(str1);
          }
          str2 = "<span style = 'color:DodgerBlue; '><strong>"+e.entries[0].dataPoint.label + "</strong></span><br/>";
          str3 = "<span style = 'color:Tomato '>Total: </span><strong>" + total + "</strong><br/>";
          
          return (str2.concat(str)).concat(str3);
        }

      },
      data: [
      {        
        type: "bar",
        showInLegend: true,
        name: "Positive",
        color: "gold",
        dataPoints: [
        { y: totalPositiveBefore, label: "before"},
        { y: totalPositiveAfter, label: "after"}                 
        ]
      },
      {        
        type: "bar",
        showInLegend: true,
        name: "Negative",
        color: "silver",          
        dataPoints: [
        { y: totalNegativeBefore, label: "before"},
        { y: totalNegativeAfter, label: "after"},             
        ]
      },
      {        
        type: "bar",
        showInLegend: true,
        name: "Neutral",
        color: "#A57164",          
        dataPoints: [
        { y: totalNeutralBefore, label: "before"},
        { y: totalNeutralAfter, label: "after"},             
        ]
      }

      ]
    });

chart.render();
  },
//This function is used to draw pie charts for sentiment analysis before and after being certified for all companies
  drawBigPieChart: function() {

    var sumBefore = totalPositiveBefore + totalNegativeBefore + totalNeutralBefore;
    var sumAfter = totalPositiveAfter + totalNegativeAfter + totalNeutralAfter;

  var chart1 = new CanvasJS.Chart("bigPieChartBefore",
  {
    title:{
      text: "Sentimental Analysis Before companies being certified"
    },
                animationEnabled: true,
    legend:{
      verticalAlign: "center",
      horizontalAlign: "right",
      fontSize: 20,
      fontFamily: "Helvetica"        
    },
    theme: "theme2",
    data: [
    {        
      type: "pie",       
      indexLabelFontFamily: "Garamond",       
      indexLabelFontSize: 20,
      indexLabel: "{label} {y}%",
      startAngle:-20,      
      showInLegend: true,
      toolTipContent:"{legendText} {y}%",
      dataPoints: [
        {  y: (totalPositiveBefore/sumBefore * 100).toFixed(2), legendText:"Positive", label: "Positive" },
        {  y: (totalNegativeBefore/sumBefore * 100).toFixed(2), legendText:"Negative", label: "Negative" },
        {  y: (totalNeutralBefore/sumBefore * 100).toFixed(2), legendText:"Neutral", label: "Neutral" },
      ]
    }
    ]
  });
     chart1.render();

     var chart2 = new CanvasJS.Chart("bigPieChartAfter",
  {
    title:{
      text: "Sentimental Analysis After companies being certified"
    },
                animationEnabled: true,
    legend:{
      verticalAlign: "center",
      horizontalAlign: "right",
      fontSize: 20,
      fontFamily: "Helvetica"        
    },
    theme: "theme2",
    data: [
    {        
      type: "pie",       
      indexLabelFontFamily: "Garamond",       
      indexLabelFontSize: 20,
      indexLabel: "{label} {y}%",
      startAngle:-20,      
      showInLegend: true,
      toolTipContent:"{legendText} {y}%",
      dataPoints: [
        {  y: (totalPositiveAfter/sumAfter * 100).toFixed(2), legendText:"Positive", label: "Positive" },
        {  y: (totalNegativeAfter/sumAfter * 100).toFixed(2), legendText:"Negative", label: "Negative" },
        {  y: (totalNeutralAfter/sumAfter * 100).toFixed(2), legendText:"Neutral", label: "Neutral" },
      ]
    }
    ]
  });
     chart2.render();
  },
//This function is used to draw a bar chart showing the total number of tweets before and after all companies joining B Corp
  drawTotalNumBar: function() {
       bar1Positive = [];
       bar1Negative = [];
       bar1Neutral = [];
       bar2Positive = [];
       bar2Negative = [];
       bar2Neutral = [];
       bar3Positive = [];
       bar3Negative = [];
       bar3Neutral = [];
       bar4Positive = [];
       bar4Negative = [];
       bar4Neutral = [];
      for (var i = 0;i<allCompany.length;i++) {
        var objPositive = {y: 0,label:"",name:""};
        var objNegative = {y: 0,label:"",name:""};
        var objNeutral = {y: 0,label:"",name:""};
        objPositive.name = allCompany[i].name;
        objPositive.label = (i+1).toString();
        objPositive.y = parseInt(allCompany[i].positiveBefore) + parseInt(allCompany[i].positiveAfter);
        objNegative.name = allCompany[i].name;
        objNegative.label = (i+1).toString();
        objNegative.y = parseInt(allCompany[i].negativeBefore) + parseInt(allCompany[i].negativeAfter);
        objNeutral.name = allCompany[i].name;
        objNeutral.label = (i+1).toString();
        objNeutral.y = parseInt(allCompany[i].neutralBefore) + parseInt(allCompany[i].neutralAfter);
        var sum = objPositive.y + objNegative.y + objNeutral.y;
        if (sum <= 5000) {
         bar1Positive.push(objPositive);
         bar1Negative.push(objNegative);
         bar1Neutral.push(objNeutral);
        }
        if (sum > 5000 && sum < 10000){
         bar2Positive.push(objPositive);
         bar2Negative.push(objNegative);
         bar2Neutral.push(objNeutral);
        }
        if (sum > 10000 && sum <= 100000){
         bar3Positive.push(objPositive);
         bar3Negative.push(objNegative);
         bar3Neutral.push(objNeutral);
        }
        if (sum > 100000){
         bar4Positive.push(objPositive);
         bar4Negative.push(objNegative);
         bar4Neutral.push(objNeutral);
        }

      }

      setBar("totalNumBar1",bar1Positive,bar1Negative,bar1Neutral," #tweets: <5000");
      setBar("totalNumBar2",bar2Positive,bar2Negative,bar2Neutral," #tweets: 5000 - 10,000");
      setBar("totalNumBar3",bar3Positive,bar3Negative,bar3Neutral," #tweets: 10,000 - 100,000");
      setBar("totalNumBar4",bar4Positive,bar4Negative,bar4Neutral," #tweets: >100,000");
  }
  };
})