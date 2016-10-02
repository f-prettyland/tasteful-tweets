
var itemSize = 18,
  cellSize = itemSize-1,
  margin = {top:20,right:20,bottom:20,left:25};


var quantize = d3.scaleQuantize()
    .domain([-40, 40])
    .range(d3.range(6).map(function(i) { return "q" + i + "-9"; }));

var svg = d3.select("#main_canvas"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var colorCalibration = ['#f6faaa','#FEE08B','#FDAE61','#F46D43','#D53E4F','#9E0142'];

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("force.json", function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line");
      // .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    // .attr("id", function(d) { return quantize(d.score); })
    // .attr("class", function(d) { return quantize(d.score); })
    .enter().append("circle")
      .attr("class", function(d) { return quantize(d.score); })
      .attr("r", 5)
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

                // .append("title")
                //     .text(function(d) { return d.id; })

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function renderColor(){
  var renderByCount = document.getElementsByName('displayType')[0].checked;

  rect
    .filter(function(d){
      return (d.value['PM2.5']>=0);
    })
    .transition()
    .delay(function(d){
      return (dayFormat(d.date)-dayOffset)*15;
    })
    .duration(500)
    .attrTween('fill',function(d,i,a){
      //choose color dynamicly
      var colorIndex = d3.scale.quantize()
        .range([0,1,2,3,4,5])
        .domain((renderByCount?[0,500]:dailyValueExtent[d.day]));

      return d3.interpolate(a,colorCalibration[colorIndex(d.value['PM2.5'])]);
    });
}

function initCalibration(){
  d3.select("#key")
   .selectAll('rect').data(colorCalibration).enter()
  .append('rect')
   .attr('width',cellSize)
   .attr('height',cellSize)
   .attr('x',function(d,i){
     return i*itemSize;
   })
   .attr('fill',function(d){
     return d;
   });

  //bind click event
  d3.select("#key").on('click',function(){
    renderColor();
  });
}

function renderColor(){
 var renderByCount = document.getElementsByName('displayType')[0].checked;

 rect
   .filter(function(d){
     return (d.value['PM2.5']>=0);
   })
   .transition()
   .delay(function(d){
     return (dayFormat(d.date)-dayOffset)*15;
   })
   .duration(500)
   .attrTween('fill',function(d,i,a){
     //choose color dynamicly
     var colorIndex = d3.scale.quantize()
       .range([0,1,2,3,4,5])
       .domain((renderByCount?[0,500]:dailyValueExtent[d.day]));

     return d3.interpolate(a,colorCalibration[colorIndex(d.value['PM2.5'])]);
   });
}

initCalibration();

function pressed(){
  // if(document.getElementById('filter')){
  //   alert("hello");
  // }
  var circle = d3.selectAll("circle");
  circle.style("fill", "steelblue");
  circle.attr("r", 30);
}
// var width = 960,
//     height = 500
//
// var svg = d3.select("body").append("svg")
//     .attr("width", width)
//     .attr("height", height);
//
// var force = d3.layout.force()
//     .gravity(0.05)
//     .distance(100)
//     .charge(-100)
//     .size([width, height]);
//
// d3.json("force.json", function(error, json) {
//   if (error) throw error;
//
//   force
//       .nodes(json.nodes)
//       .links(json.links)
//       .start();
//
//   var link = svg.selectAll(".link")
//       .data(json.links)
//     .enter().append("line")
//       .attr("class", "link");
//
//   var node = svg.selectAll(".node")
//       .data(json.nodes)
//     .enter().append("g")
//       .attr("class", "node")
//       .call(force.drag);
//
//   node.append("circle")
//       .attr("r", 8);
//       // .attr("fill", color(6));
//       // .attr("fill", function(d) { return color(d.group); })
//
//   node.append("text")
//       .attr("dx", 12)
//       .attr("dy", ".35em")
//       .text(function(d) { return d.name });
//
//   force.on("tick", function() {
//     link.attr("x1", function(d) { return d.source.x; })
//         .attr("y1", function(d) { return d.source.y; })
//         .attr("x2", function(d) { return d.target.x; })
//         .attr("y2", function(d) { return d.target.y; });
//
//     node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
//   });
// });


// var w = 400,
//     h = 400,
//     fill = d3.scale.category20();
//
// var vis = d3.select("#chart")
//   .append("svg:svg")
//     .attr("width", w)
//     .attr("height", h);
//
// d3.json("force.json", function(json) {
//   var force = d3.layout.force()
//       .charge(-120)
//       .linkDistance(30)
//       .nodes(json.nodes)
//       .links(json.links)
//       .size([w, h])
//       .start();
//
//   var link = vis.selectAll("line.link")
//       .data(json.links)
//     .enter().append("svg:line")
//       .attr("class", "link")
//       .style("stroke-width", function(d) { return Math.sqrt(d.value); })
//       .attr("x1", function(d) { return d.source.x; })
//       .attr("y1", function(d) { return d.source.y; })
//       .attr("x2", function(d) { return d.target.x; })
//       .attr("y2", function(d) { return d.target.y; });
//
//   var node = vis.selectAll("circle.node")
//       .data(json.nodes)
//     .enter().append("svg:circle")
//       .attr("class", "node")
//       .attr("cx", function(d) { return d.x; })
//       .attr("cy", function(d) { return d.y; })
//       .attr("r", 5)
//       .style("fill", function(d) { return fill(d.group); })
//       .call(force.drag);
//
//   node.append("svg:title")
//       .text(function(d) { return d.name; });
//
//   vis.style("opacity", 1e-6)
//     .transition()
//       .duration(1000)
//       .style("opacity", 1);
//
//   force.on("tick", function() {
//     link.attr("x1", function(d) { return d.source.x; })
//         .attr("y1", function(d) { return d.source.y; })
//         .attr("x2", function(d) { return d.target.x; })
//         .attr("y2", function(d) { return d.target.y; });
//
//     node.attr("cx", function(d) { return d.x; })
//         .attr("cy", function(d) { return d.y; });
//   });
// });
