window.addEventListener('load', function () {
    console.log("Starting function");
    fetch('/sports')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(data);
            var sportsTypeDropdown = document.getElementById('sportsType');
            data.forEach((sport) => {
                var option = document.createElement('option');
                option.text = sport.title;
                option.value = sport.key;
                sportsTypeDropdown.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
})


function findBestBookmaker() {
    var sportsType = document.getElementById("sportsType").value;
    var region = document.getElementById("region").value;

    fetch('/get_odds?sports_type=' + sportsType + '&region=' + region)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(data);
            document.getElementById("bookmaker").value = data.bookmaker;
            document.getElementById("averageMargins").value = data.margin;
        })
        .catch(error => console.error('Error:', error));
};
