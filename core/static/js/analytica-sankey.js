import json_inputs from './data.js';
import json_inputs_simple from './example-data-simple.js';
/*
    GAUSSIAN COLORS
*/
const COLOUR_BLUE = '#5E17EB'
const COLOUR_RED = '#7ED957'
const COLOUR_YELLOW = '#02084B'
const COLOUR_GREEN = '#5E17EB'
const COLOUR_GREY = '#464243'
/*
    UTILITY FUNCTIONS
*/
function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            x = text.attr("x"),
            y = text.attr("y"),
            dy = 0, //parseFloat(text.attr("dy")),
            tspan = text.text(null)
                .append("tspan")
                .attr("x", x)
                .attr("y", y)
                .attr("dy", dy + "em");
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("dy", ++lineNumber * lineHeight + dy + "em")
                    .text(word);
            }
        }
    });
}

function add_type_as_property(inputs) {
    const mapped_inputs = {
        'problem_categories': inputs['problem_categories'].map(input => {
            input['type'] = 'problem_category'
            return input;
        }),
        'problems': inputs['problems'].map(input => {
            input['type'] = 'problem'
            return input;
        }),
        'solutions': inputs['solutions'].map(input => {
            input['type'] = 'solution'
            return input;
        }),
    }
    return mapped_inputs;
}
function create_nodes(inputs) {
    let nodes = [];
    inputs['problem_categories'].concat(inputs['problems']).concat(inputs['solutions']).forEach(element => {
        nodes.push({
            'node': element.id,
            'name': 'node'.concat(element.id),
            'text': element.text,
            'type': element.type,
        });
    });
    return nodes;
}

function create_links(inputs) {
    let links = [];
    inputs['problem_categories'].concat(inputs['problems']).concat(inputs['solutions']).forEach(element => {
        element.links.forEach(link => {
            links.push({
                'source': element.id,
                'target': link,
                'value': element.weight,
            });
        })
    });
    return links;
}

function get_color_based_on_type(d) {
    console.log('type', d);
    switch (d.type) {
        case 'problem_category':
            if (d.text === "Small capital inflows to the 'informal sector' ('Kasinomy')") {
                return 'red'
            }
            return COLOUR_YELLOW;
        case 'problem':
            return COLOUR_BLUE;
        case 'solution':
            return COLOUR_RED;
    }
}
/*
    CREATE GRAPH DATA
*/

const graph = {
    'nodes': create_nodes(add_type_as_property(json_inputs)),
    'links': create_links(add_type_as_property(json_inputs)),
}
console.log('Graph data', graph);

/* 
    DRAW GRAPH
*/
var units = "";

// set the dimensions and margins of the graph
var margin = { top: 10, right: 10, bottom: 10, left: 10 },
    width = 1400 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;

// format variables
var formatNumber = d3.format(",.0f"),    // zero decimal places
    // format = function (d) { return formatNumber(d) + " " + units; },
    format = function (d) { return "Weighting " + formatNumber(d) },
    color = d3.scaleOrdinal(d3.schemeCategory10);

// append the svg object to the body of the page
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Set the sankey diagram properties
const NODE_WIDTH = 380;
const NODE_PADDING = 10;

var sankey = d3.sankey()
    .nodeWidth(NODE_WIDTH)
    .nodePadding(NODE_PADDING)
    .size([width, height]);

var path = sankey.link();

// load the data

sankey
    .nodes(graph.nodes)
    .links(graph.links)
    .layout(32);


// add in the links
var link = svg.append("g").selectAll(".link")
    .data(graph.links)
    .enter().append("path")
    .attr("class", "link")
    .attr("d", path)
    .style("stroke-width", function (d) { return Math.max(1, d.dy); })
    .sort(function (a, b) { return b.dy - a.dy; });

// add the link titles
link.append("title")
    .text(function (d) {
        return d.source.name + " → " +
            d.target.name + "\n" + format(d.value);
    });

// add in the nodes
var node = svg.append("g").selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    })
    .call(d3.drag()
        .subject(function (d) {
            return d;
        })
        .on("start", function () {
            this.parentNode.appendChild(this);
        })
        .on("drag", dragmove));

// add the rectangles for the nodes
node.append("rect")
    .attr("height", (d) => {
        return d.dy + 8.1;
    })
    .attr("width", sankey.nodeWidth())
    .attr("rx", '2px')
    .attr("ry", '2px')
    .style("fill", function (d) {
        return d.color = get_color_based_on_type(d);
        // return d.color = color(d.name.replace(/ .*/, ""));
    })
    // .style("stroke", function (d) {
    //     return d3.rgb(d.color).darker(2);
    // })
    .append("title")
    .text(function (d) {
        const temp = String(d.type).toUpperCase()[0] + String(d.type).slice(1)
        return temp + ' ' + d.node + "\n\n" + d.text + "\n\n" + format(d.value);
        // return d.name + "\n" + format(d.value);
    })

const TEXT_PADDING = 3;
node.append('text')
    .attr("x", function (d) { return d.dx - NODE_WIDTH + TEXT_PADDING; })
    .attr("y", function (d) { return 0 + TEXT_PADDING*3; })
    .text(d => d.text)
    .attr("font-family", "sans-serif")
    .attr("font-size", d => {
        if (d.type === 'problem_category' || d.type === 'solution') {
            return "11px";
        } else {
            return "10px";
        }
    })
    .attr("fill", d => {
        if (d.type !== 'problem_category' || d.type !== 'problem') {
            return "white";
        } else {
            return "black";
        }
    })
    .call(wrap, Math.round(NODE_WIDTH*0.98));


// add in the title for the nodes
// node.append("text")
//     .attr("x", -6)
//     .attr("y", function (d) { return d.dy / 2; })
//     .attr("dy", ".35em")
//     .attr("text-anchor", "end")
//     .attr("transform", null)
//     .text(function (d) { 
//         const temp = String(d.type).toUpperCase()[0] + String(d.type).slice(1);
//         return temp + ' ' + d.node;
//      })
//     .filter(function (d) { return d.x < width / 2; })
//     .attr("x", 6 + sankey.nodeWidth())
//     .attr("text-anchor", "start");

// the function for moving the nodes
function dragmove(d) {
    d3.select(this)
        .attr("transform",
            "translate("
            + d.x + ","
            + (d.y = Math.max(
                0, Math.min(height - d.dy, d3.event.y))
            ) + ")");
    sankey.relayout();
    link.attr("d", path);
}
