var ctx = document.getElementById("myChart").getContext("2d");

var myChart = new Chart(ctx, {
    type: "line",
    options: {
        responsive: false,
        maintainAspectRatio: false,
    },
    data: {
    //labels: [new Date("2015-3-15 13:3").toLocaleString(), new Date("2015-3-25 13:2").toLocaleString(), new Date("2015-4-25 14:12").toLocaleString()],
    labels: [1,2,3,4,5],
    datasets: [{
        label: "prueba",
        fill: false,
        lineTension: 0.5,
        data: [10,20,1,50,40
        ],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)"
        ],
        borderColor: [
          "rgba(255,99,132,1)"
        ],
        borderWidth: 1
      }]
    }
});
