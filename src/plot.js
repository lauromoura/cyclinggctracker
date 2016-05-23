function bind_handlers() {
    $("#flot-placeholder").bind("plothover", function(event, pos, item) {
        if (!item) {
            $("#tooltip").hide();
            return;
        }

        var x = item.datapoint[0].toFixed(0);
        var y = item.datapoint[1].toFixed(2);

        var string = item.series.label;
        if (y == 0)
            string += ": leader";
        else
            string += ": " + y + "";
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
        var ref_gap = reference.data[index][1];
        newdata.push([stage, gap - ref_gap]);
    })
    obj.data = newdata
}

function plotAccordingToChoices(dataset) {
    var data = [];
    var reference = selected_reference();
    var referenceData = dataset[reference];
    console.log(referenceData);
    $("#checkboxes").find("input:checked").each(function(){
        var key = $(this).attr('name');
        if (key && dataset[key]) {
            var currentData = jQuery.extend(true, {}, dataset[key]);
            if (reference != 0)
                adjust(currentData, referenceData)
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
                transform: function(v) { return -v; },
                inverseTransform: function(v) { return -v; }
            },
            grid: {
                hoverable: true
            }
        });
    }
}

function filter_top_riders(n, json, teams)
{
    var dataset = [];
    for (var key in json) {
        if (!json.hasOwnProperty(key))
            continue;

        if (json[key].pos > n)
            continue;

        var rider = json[key];
        var riderData = { data: [], label: rider.name }
        rider.time.forEach(function(timeBehindLeader, stage){
            riderData.data.push([stage+1, timeBehindLeader]);
        });
        riderData['color'] = teams[rider.team]['color'];
        riderData['gcplace'] = rider.pos - 1;
        dataset[rider.pos-1] = riderData;
    }
    return dataset;
}

function fillCheckboxes(dataset) {
    var choicesContainer = $("#checkboxes");
    $.each(dataset, function(idx){
        var rider = dataset[idx];
        choicesContainer.append("<br/><input type='checkbox' name='" + rider.gcplace + "' checked='checked' id='id" + rider.label + "'></input>" +
            "<label for='id" + rider.label + "'>" + rider.label + "</label>");
    });

    choicesContainer.find("input").click(function () {
        plotAccordingToChoices(dataset);
    });

}

function selected_reference() {
    return $("select option:selected").val();
}

function fillReferenceCombo(dataset) {
    var combo = $("#reference");
    $.each(dataset, function(idx) {
        var rider = dataset[idx];
        combo.append(new Option(rider.label, rider.gcplace));
    });

    combo.change(function(){
        plotAccordingToChoices(dataset);
    });
}
