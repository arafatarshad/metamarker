  let margin = {top: 30, right: 10, bottom: 10, left: 0};

 	const minwidth= 3000;

	const zoom_in = () =>{
		remove_svg();
		generate_svg(5000,0);
	}

	const zoom_out= () =>{
		let width= (width<4500) ? minwidth : width-100;
		remove_svg();
		generate_svg(0);
	}









const generate_svg= (new_width=0,new_height=0) =>{
 d3.json("{% url "api_parallel_plot" %}", function(error, data) {

  data=JSON.parse(data);
  console.log(data.length);
  dimensions = d3.keys(data[0]).filter(function(d) { return d });
  let labelcolumn=dimensions[dimensions.length-1];
  let width =dimensions.length*70,height=1000;



 let svg = d3.select("#my_dataviz")
  .append("svg")
  .attr("width", width+new_width)
  .attr("height", height+new_height)
  .append("g")
  .attr("transform","translate(" + margin.left + "," + margin.top + ")");


let classlabels=[];
let colorcodes=[];

 for(i in data){
 	let value=data[i][labelcolumn];
 	if(classlabels.indexOf(value)== -1){
        classlabels.push(value);
    }
 }
colorcodes=classlabels.map(()=>{return '#'+(Math.random()*0xFFFFFF<<0).toString(16);});

let color = d3.scaleOrdinal()
    .domain(classlabels)
    .range(colorcodes);

  let y = {}
  for (i in dimensions) {
    name = dimensions[i]
    y[name] = d3.scaleLinear()
      .domain( d3.extent(data, function(d) { return +d[name]; }) )
      .range([height, 0])
  }


  x = d3.scalePoint().range([0, width]).padding(1).domain(dimensions);

  function path(d) {
      let line = d3.line()(dimensions.map(function(p) {
        return [x(p), y[p](d[p])]; }));
      return line;
  }

  // Highlight the specie that is hovered
  let highlight = function(d){
    // selected_specie = d.Species

    // first every group turns grey
    d3.selectAll(".line")
      .transition().duration(200)
      .style("stroke", "lightgrey")
      .style("opacity", "0.2")
    // Second the hovered specie takes its color
    d3.selectAll("." + d[labelcolumn])
      .transition().duration(200)
      .style("stroke", color(d[labelcolumn]))
      .style("opacity", "1")
  }

  // Unhighlight
  var doNotHighlight = function(d){
    d3.selectAll(".line")
      .transition().duration(200).delay(1000)
      .style("stroke", function(d){ return( color(d[labelcolumn]))} )
      .style("opacity", "1")
  }




  svg.selectAll("myPath")
    .data(data)
    .enter().append("path")
    .attr("d",  path)
    .attr("class", function (d) { return "line " + d[labelcolumn] } )
    .style("fill", "none")
    .style("stroke", function(d){console.log(d[labelcolumn]); return color(d[labelcolumn]);} )
    .style("opacity", 0.5)
    .on("mouseover", highlight)
      .on("mouseleave", doNotHighlight );

  svg.selectAll("myAxis")
    .data(dimensions).enter()
    .append("g")
    .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
    .each(function(d) { d3.select(this).call(d3.axisLeft().scale(y[d])); })
    .append("text")
      .style("text-anchor", "middle")
      .attr("y", -9)
      .text(function(d) { return d; })
      .style("fill", "black")
 });




}
const remove_svg =() =>{
	 $("#my_dataviz").html("");
}

	generate_svg();
