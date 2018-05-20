/* eslint-env es6 */

function selectedReference() {
    return Number($("select option:selected").val());
}

function bindHandlers() {
    $("#flot-placeholder").bind("plothover", function(event, pos, item) {
        if (!item) {
            $("#tooltip").hide();
            return;
        }

        var x = item.datapoint[0].toFixed(0);
        var y = item.datapoint[1].toFixed(2);

        var string = item.series.label;
        if (y === 0) {
            string += ": leader";
        } else {
            string += ": " + y + "";
        }
        string += " at stage " + x;

        $("#tooltip").html(string)
            .css({top:item.pageY+5, left: item.pageX+5})
            .fadeIn(200);
    });
}

/**
 * Ajudsts obj data member with the difference to the reference dataseries
 */
function adjust(obj, reference) {
    var newdata = new Array();
    obj.data.map(function(datapoint, index) {
        var stage = datapoint[0];
        var gap = datapoint[1];
        var refGap = reference.data[index][1];
        newdata.push([stage, gap - refGap]);
    });
    obj.data = newdata;
}

function plotAccordingToChoices(dataset) {
    var data = [];
    var reference = selectedReference();
    var referenceData = dataset.get(reference);
    $("#checkboxes").find("input:checked").each(function(){
        var key = Number($(this).attr("name"));
        console.log(key);
        if (dataset.has(key)) {
            var currentData = jQuery.extend(true, {}, dataset.get(key));
            if (reference >= 0) { // -1 reserved for the leader after each stage.
                adjust(currentData, referenceData);
            }
            data.push(currentData);
        }
    });

    if (data.length > 0) {
        $.plot("#flot-placeholder", data, {
            legend: {
                position: "sw"
            },
            yaxis: {
                tickSize:60,
                transform: (v) => -v,
                inverseTransform: (v) => -v,
            },
            grid: {
                hoverable: true
            }
        });
    }
}

function getColor(team, teams)
{
    if (teams.has(team)) {
        return teams.get(team)["color"];
    } else {
        return "#222222";
    }
}

function appendRiderTime(riderData)
{
    return function(timeBehindLeader, stage) {
        riderData.data.push([stage+1, timeBehindLeader]);
    };
}

function filterTopRiders(n, json, teams)
{
    var dataset = new Array(n);
    var map = new Map(json);
    map.forEach(function(rider, key) {

        if (rider.pos > n) {
            return;
        }

        var riderData = { data: [], label: rider.name };
        rider.time.forEach(appendRiderTime(riderData));
        riderData["color"] = getColor(rider.team, teams);
        riderData["gcplace"] = rider.pos - 1;
        dataset[rider.pos-1] = [rider.pos - 1, riderData];
    });
    return new Map(dataset);
}

function fillCheckboxes(dataset) {
    var choicesContainer = $("#checkboxes");
    dataset.forEach(function(rider){
        choicesContainer.append("<br/><input type='checkbox' name='" + rider.gcplace + "' checked='checked' id='id" + rider.label + "'></input>" +
            "<label for='id" + rider.label + "'>" +  (rider.gcplace + 1) + ": "+ rider.label + "</label>");
    });

    choicesContainer.find("input").click(function () {
        plotAccordingToChoices(dataset);
    });

}

function fillReferenceCombo(dataset) {
    var combo = $("#reference");
    combo.append(new Option("Leader after each stage", -1));
    dataset.forEach(function(rider, pos) {
        combo.append(new Option(rider.label, rider.gcplace));
    });

    combo.change(function(){
        plotAccordingToChoices(dataset);
    });
}
