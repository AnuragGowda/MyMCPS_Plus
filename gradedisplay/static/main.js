// Set an overlay variable which will be useful later
var overlay = jQuery('<div id="overlay"> </div>');
// When the submit button is clicked
$("#submit").click(function() {
    // Show the div, which is the overlay
    $("div").show();
    // Set the variable of selected in the session to the name grades-color, this is important later on 
    sessionStorage.setItem('selected', 'grades-color')
});
// This is a simple function that removes the active traits of the headers of the website
function clearAll(){
    // Remove the about-color, this corresponds to the about button in the header
    document.getElementById("about-color").classList.remove('active');
    // Remove the grades-color, this corresponds to the about button in the header
    document.getElementById("grades-color").classList.remove('active');
    // Remove the contact-color, this corresponds to the about button in the header
    document.getElementById("contact-color").classList.remove('active');
}
// When the page loads
$( document ).ready(function() {
    // Set an interval that occurs every 100 miliseconds which is 1/10 of a second that checks if the document title is that of the login page or the grade page, sets everything accordingly 
    /*var setScreen = setInterval(function(){
        // If the title is the login page one
        if (document.title == 'MyMCPS++ - Login'){
            // Clear all of the headers active states with the function we defined above
            clearAll();
            // Clear the interval as well
            clearInterval(setScreen)
        }
        // If the title is the grade page 
        else if (document.title == 'MyMCPS++ - Grades'){
            clearAll();
            document.getElementById("grades-color").classList.add('active');
            clearInterval(setScreen)
        }
    }, 100);*/
    if (sessionStorage.getItem('selected') != null){
        if (sessionStorage.getItem('selected') == 'grades-color'){
            clearAll();
            document.getElementById("grades-color").classList.add('active');
        }
        else if (sessionStorage.getItem('selected') == 'contact-color'){
            clearAll();
            document.getElementById("contact-color").classList.add('active');
        }
        else{
            clearAll();
            document.getElementById("about-color").classList.add('active');
        }
    }
});
$("#grades-btn").click(function() {
    if (document.title != 'MyMCPS++ - Login'){
        sessionStorage.setItem('selected', 'grades-color');
    }
});
$("#about-btn").click(function() {
    sessionStorage.setItem('selected', 'about-color')
});
$("#contact-btn").click(function() {
    sessionStorage.setItem('selected', 'contact-color')
});
var headers = [];
function addDropdown(text){
    var dropdown = '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">';
    for (var i = 0; i < headers.length; i++) {
        //if(text!=headers[i]){
        dropdown+="<a class=\"dropdown-item\">"+headers[i]+"</a>";
        //}
    }
    return dropdown+"</div></td>"
}
function updateGrades(){
    for (var i = 0; i < headers.length; i++) {
        type = headers[i]
        var colOne = 0,
            colTwo = 0
            doPercent = true
            btn = 'success'
            grade = 'A'

        $('.types').each(function(index, obj) {
            if ($(this).text() == type){
                colOne += parseFloat($(this).closest('tr').find('.one').val())
                colTwo += parseFloat($(this).closest('tr').find('.two').val())
            }
        });
        if (colTwo == 0){doPercent = false}else if (colOne/colTwo >= .795 && colOne/colTwo < .895){btn = 'info', grade = 'B'}else if (colOne/colTwo > .695 && colOne/colTwo < .895){btn = 'primary', grade = 'C'}else if (colOne/colTwo > .595 && colOne/colTwo < .895){btn = 'warning', grade = 'D'}else if (colOne/colTwo < .595){btn = 'danger', grade = 'E'}
        doPercent?percent = String((colOne/colTwo*100).toFixed(1))+'%':percent = '100%'
        $('.header').each(function(index, obj) {
            if ($(this).text() == type){
                $(this).closest('tr').find('button').text(grade+' - '+percent)
                $(this).closest('tr').find('button').prop("disabled", false).removeClass().addClass('btn btn-'+btn+' gradeLetter')
                $(this).closest('tr').find('.headerInfo').text(String(colOne)+'/'+String(colTwo))
            }
        });  
    }
    updateTotalGrade()
}
function updateTotalGrade(){
    var gradeVal = 0
    var totalHead = 0
    $('.header').each(function(index, obj) {
        if($(this).closest('tr').find('.headerInfo').text() != '0/0'){
            totalHead += parseInt($(this).text().slice($(this).text().indexOf('(')+1,-1))
        }
    });
    $('.header').each(function(index, obj) {
        var weight = $(this).text().slice($(this).text().indexOf('(')+1,-1)
        var points = $(this).closest('tr').find('.headerInfo').text()
        var val = eval(points)
        if (isNaN(val)){val = 0}
        gradeVal += (weight*100/totalHead)*val
    }); 
    if (isNaN(gradeVal)){gradeVal = 100}
    grade = 'A'
    var btn = 'success'
    if (gradeVal >= 79.5 && gradeVal < 89.5){btn = 'info', grade = 'B'}else if (gradeVal > 69.5 && gradeVal < 89.5){btn = 'primary', grade = 'C'}else if (gradeVal > 59.5 && gradeVal < 89.5){btn = 'warning', grade = 'D'}else if (gradeVal < 59.5){btn = 'danger', grade = 'E'}
    $('.btn-lg').removeClass().addClass('btn btn-lg btn-'+btn).text(grade+' - '+String(gradeVal.toFixed(1))+'%')
}
$(document).on('click', '#editGrades', function(){
    $(this).text('Add Grade');
    $(this).attr("id","addGrade");
    $(this).after("&nbsp;<button type=\"button\" class=\"btn btn-secondary\" id=\"undoBtn\">Undo Changes</button>");
    $(".gradeHeader").text("Keep grade?")
    $(".date").before("<td><button type=\"button\" class=\"btn btn-danger remove\">Remove Grade</button></td>")
    $(".date").remove()
    $('.header').each(function(index, obj) {
        headers.push($(this).text())
    });
    $('.type').each(function(index, obj) {
        $(this).before("<td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+$(this).text()+"</button>"+addDropdown($(this).text()));
    });
    $(".type").remove()
    $('.grade').each(function(index, obj) {
        //alert(parseInt($(this).text().slice(0, $(this).text().indexOf('/'))));
        var one = $(this).text().slice(0, $(this).text().indexOf('/'))
        var two = $(this).text().slice($(this).text().indexOf('/')+1)
        if(one == '' || isNaN(one)){one='0'}
        if(two == '0' || two ==''){two == '1'}
        $(this).before("<td style=\"width: 20%\"><form><div class=\"form-row\"><div class=\"col-sm\"><input class=\"form-control one\" type=\"number\" min=\"0\" step=\".5\" value="+one+"></div><div class=\"col-sm\"><input class=\"form-control two\" type=\"number\" min=\"1\" step=\"1\" value="+two+"></form></div></div></td>");
    });
    var doUpdate = false
    $('button').each(function(index, obj) {
        if($(this).is(":disabled") || $(this).hasClass("btn-secondary")){
            var one = $(this).closest("tr").find(".one").val()
            var two = $(this).closest("tr").find(".two").val()
            var doPercent = true
            var btn = 'success'
            var grade = 'A'
            if (two == 0){doPercent = false}else if (one/two >= .795 && one/two < .895){btn = 'info', grade = 'B'}else if (one/two > .695 && one/two < .895){btn = 'primary', grade = 'C'}else if (one/two > .595 && one/two < .895){btn = 'warning', grade = 'D'}else if (one/two < .595){btn = 'danger', grade = 'E'}
            doPercent?percent = String((one/two*100).toFixed(1))+'%':percent = '100%'
            $(this).closest("tr").find('.gradeLetter').text(grade+' - '+percent)
            $(this).closest("tr").find('.gradeLetter').prop("disabled", false).removeClass().addClass('btn btn-'+btn+' gradeLetter')
            doUpdate = true
        }
    });  
    if(doUpdate){updateGrades()}
    $(".grade").remove()
});
$(document).on('click', '#addGrade', function(){
    $("#gradeTable").prepend("<tr class=\"userAdded\"><td><button type=\"button\" class=\"btn btn-danger remove\">Remove Grade</button></td>\
    <td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+headers[0]+"</button>"+addDropdown(headers[0])+"</td>\
    <td>User Added Grade</td>\
    <td style=\"width: 20%\"><form><div class=\"form-row\"><div class=\"col-sm\"><input class=\"form-control one\" type=\"number\" min=\"0\" step=\".5\" value=\"0\"></div><div class=\"col-sm\"><input class=\"form-control two\" type=\"number\" min=\"1\" step=\"1\" value=\"1\"></form></div></div></td>\
    <td><button type=\"button\" class=\"btn btn-danger gradeLetter\"\">E - 0.0%</button></td></tr>");
    updateGrades()
});
$(document).on('click', '#undoBtn', function(){
    location.reload();
});
$(document).on('click', '.remove', function(){
    $(this).closest("tr").remove()
    updateGrades()
});
$(document).on('click', '.dropdown-menu a', function(){
    $(this).closest("td").find('button').text($(this).text())
    updateGrades()
});
$(document).on('change', '.col-sm input', function(){
    var one = $(this).closest("form").find(".one").val()
    var two = $(this).closest("form").find(".two").val()
    var doPercent = true
    var btn = 'success'
    var grade = 'A'
    if (two == 0){doPercent = false}else if (one/two >= .795 && one/two < .895){btn = 'info', grade = 'B'}else if (one/two > .695 && one/two < .895){btn = 'primary', grade = 'C'}else if (one/two > .595 && one/two < .895){btn = 'warning', grade = 'D'}else if (one/two < .595){btn = 'danger', grade = 'E'}
    doPercent?percent = String((one/two*100).toFixed(1))+'%':percent = '100%'
    $(this).closest("tr").find('.gradeLetter').text(grade+' - '+percent)
    $(this).closest("tr").find('.gradeLetter').prop("disabled", false).removeClass().addClass('btn btn-'+btn+' gradeLetter')
    updateGrades()
});