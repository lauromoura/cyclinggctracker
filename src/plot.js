function plotAccordingToChoices(dataset) {
    var data = []
    $("#checkboxes").find("input:checked").each(function(){
        var key = $(this).attr('name');
        if (key && dataset[key])
            data.push(dataset[key]);
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
