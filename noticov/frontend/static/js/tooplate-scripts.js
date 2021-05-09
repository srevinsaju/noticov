const width_threshold = 480;

// How long you want the animation to take, in ms
const animationDuration = 2000;
// Calculate how long each ‘frame’ should last if we want to update the animation 60 times per second
const frameDuration = 1000 / 60;
// Use that to calculate how many frames we need to complete the animation
const totalFrames = Math.round( animationDuration / frameDuration );
// An ease-out function that slows the count as it progresses
const easeOutQuad = t => t * ( 2 - t );


// The animation function, which takes an Element
const animateCountUp = el => {
	let frame = 0;
	const countTo = parseInt( el.innerHTML, 10 );
	// Start the animation running 60 times per second
	const counter = setInterval( () => {
		frame++;
		// Calculate our progress as a value between 0 and 1
		// Pass that value to our easing function to get our
		// progress on a curve
		const progress = easeOutQuad( frame / totalFrames );
		// Use the progress value to calculate the current count
		const currentCount = Math.round( countTo * progress );

		// If the current count has changed, update the element
		if ( parseInt( el.innerHTML, 10 ) !== currentCount ) {
			el.innerHTML = currentCount;
		}

		// If we’ve reached our last frame, stop the animation
		if ( frame === totalFrames ) {
			clearInterval( counter );
		}
	}, frameDuration );
};

// Run the animation on all elements with a class of ‘countup’
const runAnimations = () => {
	const countupEls = document.querySelectorAll( '.countup' );
	countupEls.forEach( animateCountUp );

	$.getJSON("/api/in/latest/states", function (data) {
	  let i = 0

	  data.data.forEach(function (cd) {
	    let status_condition = ""
        if (cd["total_cases"] > cd["discharged"]) {
          status_condition = "worse"
        } else {
          status_condition = "getting better"
        }
        let d = new Date(0);
        let today = new Date();
        d.setUTCSeconds(cd["timestamp"]);

        $("#current_status").append(
              `
            <tr>
                <th scope="row"><b>#${i}</b></th>
                <td>
                    <div class="tm-status-circle moving">
                    </div>${status_condition}
                </td>
                <td><b>${cd["location"]}</b></td>
                
                <td><b>${cd["total_cases"]}/b></td>
                <td>${cd["deaths"]}</td>
                <td>${cd["discharged"]}</td>
                <td>${timeDifference(today.getMilliseconds(), d.getMilliseconds())}</td>
            </tr>
              `
          )
        i++;
        })
      })

};



// relative time convertor

function timeDifference(current, previous) {

    var msPerMinute = 60 * 1000;
    var msPerHour = msPerMinute * 60;
    var msPerDay = msPerHour * 24;
    var msPerMonth = msPerDay * 30;
    var msPerYear = msPerDay * 365;

    var elapsed = current - previous;

    if (elapsed < msPerMinute) {
          console.log(elapsed)
         return Math.round(elapsed/1000) + ' seconds ago';
    }

    else if (elapsed < msPerHour) {
         return Math.round(elapsed/msPerMinute) + ' minutes ago';
    }

    else if (elapsed < msPerDay ) {
         return Math.round(elapsed/msPerHour ) + ' hours ago';
    }

    else if (elapsed < msPerMonth) {
        return 'approximately ' + Math.round(elapsed/msPerDay) + ' days ago';
    }

    else if (elapsed < msPerYear) {
        return 'approximately ' + Math.round(elapsed/msPerMonth) + ' months ago';
    }

    else {
        return 'approximately ' + Math.round(elapsed/msPerYear ) + ' years ago';
    }
}

function drawLineChart() {
  if ($("#lineChart").length) {
    ctxLine = document.getElementById("lineChart").getContext("2d");
    optionsLine = {
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Hits"
            }
          }
        ]
      }
    };

    // Set aspect ratio based on window width
    optionsLine.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    $.getJSON( "/api/in/summary", function( data ) {

      let x_axis = [];
      let total_cases = [];
      let discharged = [];
      let deaths = [];
      let today = new Date();
      data.data.forEach(function(x) {
        let d = new Date(0); // The 0 there is the key, which sets the date to the epoch

        d.setUTCSeconds(x["timestamp"]);
        console.log(d.toUTCString(), x["deaths"], x["total_cases"], x["discharged"])

        x_axis.push(timeDifference(today.getMilliseconds(), d.getMilliseconds()));

        deaths.push(x["deaths"]);
        total_cases.push(x["total_cases"]);
        discharged.push(x["discharged"]);
      })



      configLine = {
        type: "line",
        data: {
          labels: x_axis,
          datasets: [
            {
              label: "Total Cases",
              data: total_cases,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              cubicInterpolationMode: "monotone",
              pointRadius: 0
            },
            {
              label: "Deaths",
              data: deaths,
              fill: false,
              borderColor: "rgba(255,99,132,1)",
              cubicInterpolationMode: "monotone",
              pointRadius: 0
            },
            {
              label: "Discharged",
              data: discharged,
              fill: false,
              borderColor: "rgba(153, 102, 255, 1)",
              cubicInterpolationMode: "monotone",
              pointRadius: 0
            }
          ]
        },
        options: optionsLine
      };

      lineChart = new Chart(ctxLine, configLine);
    });

  }
}

function drawBarChart() {
  if ($("#barChart").length) {
    ctxBar = document.getElementById("barChart").getContext("2d");

    optionsBar = {
      responsive: true,
      scales: {
        yAxes: [
          {
            barPercentage: 0.2,
            ticks: {
              beginAtZero: true
            },
            scaleLabel: {
              display: true,
              labelString: "Hits"
            }
          }
        ]
      }
    };

    optionsBar.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    /**
     * COLOR CODES
     * Red: #F7604D
     * Aqua: #4ED6B8
     * Green: #A8D582
     * Yellow: #D7D768
     * Purple: #9D66CC
     * Orange: #DB9C3F
     * Blue: #3889FC
     */
    $.getJSON( "/api/in/top_covid_cases", function( data ) {

      console.log(data);

      let x_axis = [];
      let y_axis = [];
      data.data.forEach(function (covidData) {
            x_axis.push(covidData["location"])
            y_axis.push(covidData["total_cases"])
          }
      )

      configBar = {
        type: "horizontalBar",
        data: {
          labels: x_axis,
          datasets: [
            {
              label: "# of Hits",
              data: y_axis,
              backgroundColor: [
                "#F7604D",
                "#4ED6B8",
                "#A8D582",
                "#D7D768",
                "#9D66CC",
                "#DB9C3F",
                "#3889FC"
              ],
              borderWidth: 0
            }
          ]
        },
        options: optionsBar
      };

      barChart = new Chart(ctxBar, configBar);
    });



  }
}

function drawPieChart() {
  if ($("#pieChart").length) {
    var chartHeight = 300;

    $("#pieChartContainer").css("height", chartHeight + "px");

    ctxPie = document.getElementById("pieChart").getContext("2d");

    optionsPie = {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      legend: {
        position: "top"
      }
    };

    $.getJSON( "/api/in/latest", function( data ) {

      console.log(data);
      configPie = {
        type: "pie",
        data: {
          datasets: [
            {
              data: [ data.data["deaths"],  data.data["total_cases"],  data.data["discharged"]],
              backgroundColor: ["#F7604D", "#4ED6B8", "#A8D582"],
              label: "Storage"
            }
          ],
          labels: [
            "Deaths",
            "Total Cases",
            "Discharged"
          ]
        },
        options: optionsPie
      };

      pieChart = new Chart(ctxPie, configPie);
    })

  }
}

function updateLineChart() {
  if (lineChart) {
    lineChart.options = optionsLine;
    lineChart.update();
  }
}

function updateBarChart() {
  if (barChart) {
    barChart.options = optionsBar;
    barChart.update();
  }
}
