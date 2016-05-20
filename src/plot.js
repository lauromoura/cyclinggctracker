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
                position: "nw"
            },
            yaxis: {
                tickSize:60,
            }
        });
    }
}

function filter_riders(names, json) {
    var dataset = {};
    for (var i=0; i < names.length; i++) {
        console.log("Getting " + names[i]);
        rider = json[names[i]];
        if (!rider) {
            console.log("Missing " + names[i])
            continue
        }
        var riderData = { data: [], label: rider.name }
        rider.time.forEach(function(timeBehindLeader, stage){
            riderData.data.push([stage+1, timeBehindLeader]);
        });
        dataset[rider.name] = riderData;
    }
    return dataset;
}

function fillCheckboxes(dataset) {
    var choicesContainer = $("#checkboxes");
    $.each(dataset, function(key, val){
        choicesContainer.append("<br/><input type='checkbox' name='" + key + "' checked='checked' id='id" + key + "'></input>" +
            "<label for='id" + key + "'>" + val.label + "</label>");
    });

    choicesContainer.find("input").click(function () {
        plotAccordingToChoices(dataset);
    });

}
