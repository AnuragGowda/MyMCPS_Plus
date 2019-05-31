// The easy stuff first 

// When the submit button is clicked
$("#submit").click(function() {
    // Show divs, in this case, it is an overlay div we care about that will be shown, created in the html
    $("div").show();
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

// When the page loads the following function runs
$( document ).ready(function() {
    // First, clear all of the highlighted headers
    clearAll();
    // If the title of the current page is the grade one
    if (document.title == 'MyMCPS++ - Grades'){
        // Add the active trait to the corresponding header
        document.getElementById("grades-color").classList.add('active');
    }
    // However if its the about page,
    else if (document.title == 'MyMCPS++ - About Page'){
        // Add the active attribute to the corresponding header
        document.getElementById("about-color").classList.add('active');
    }
    // And finally if we are on the contact page,
    else if (document.title == 'MyMCPS++ - Contact Page'){
        // Make the corresopning header active
        document.getElementById("contact-color").classList.add('active');
    }
});


// The more complex part begins here, all of this stuff is actually used during the gradePage part of the website, so it includes the "grade caluclator" part and other stuff


// Create a global list called headers, this is useful when showing the more specific grade info, this stuff is still easy but has to do with the harder stuff so I put it under this category
var headers = [];
// Create a function called addDropdown that will fill in the content of the dropdowns
function addDropdown(){
    // Create the dropdown that we will use later
    var dropdown = '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">';
    // Iterate through all the headers
    for (var i = 0; i < headers.length; i++) {
        // For each header, add a dropdown item in the dropdown with the name of the header
        dropdown+="<a class=\"dropdown-item\">"+headers[i]+"</a>";
    }
    // Now we add the ending portion to the dropdown and return it
    return dropdown+"</div></td>"
}

// Now the actual "complex" part begins, its not really complex, just kind or lengthy, this function updates all the grades based on the info in the grade "body", so this is the grade calculator part
function updateGrades(){
    // Iterate through all of the headers on the page
    for (var i = 0; i < headers.length; i++) {
        // Set the variable type to the header, simply set the type variable to the header name
        type = headers[i]
        // Intitalize a bunch of variables that will be useful for this process, set colOne to 0, this col will be points earned
        var colOne = 0,
            // Set col2 to 0, this col represents the points possible
            colTwo = 0
            // A variable set to a boolean, will decide if we will need to calculate the percent later
            doPercent = true
            // Bootstrap button class, set it to success, we may change it later, in bootstrap, the success class is green, so buttons are set to green unless changed
            btn = 'success'
            // Since we set the button to green, we also set the grade to an A since an A corresponds with the greeen button in our app
            grade = 'A'
        // Iterate through all of the classes that have the "types", what this is doing is it is iterating through all of the dropdowns and looking for this special keyword we put in
        $('.types').each(function(index, obj) {
            // If the text is the same as the header, meaning that if it is in the same grade category, so what we are doing here is that this nested loop is going through the grade body and then looking for a header that matches what the outer loop is currently on, so its looking for grades that are in the current category
            if ($(this).text() == type){
                // Add the float of the points earned for that assignment to the colOne variable
                colOne += parseFloat($(this).closest('tr').find('.one').val())
                // And add the float of the points possible to the coltwo variable
                colTwo += parseFloat($(this).closest('tr').find('.two').val())
            }
        });
        // Now we change a lot of variables, I wrote this like this because this peice of code is very simple and it wastes space writing it "neatly" so I just crammed it into one line
        // Anyway, what this line does is it sets the variables for the grade and the button color variables according to the percent the grade would be, keep in mind, we first check to see if colTwo equals 0 to aviod divison by 0 errors 
        if (colTwo == 0){doPercent = false}else if (colOne/colTwo >= .795 && colOne/colTwo < .895){btn = 'info', grade = 'B'}else if (colOne/colTwo > .695 && colOne/colTwo < .895){btn = 'primary', grade = 'C'}else if (colOne/colTwo > .595 && colOne/colTwo < .895){btn = 'warning', grade = 'D'}else if (colOne/colTwo < .595){btn = 'danger', grade = 'E'}
        // Just a quick ternary operator to condense simple code into fewer lines, what this code does is, simply put assign percent to the percent of the grade, if doPercent is false, meaning if colTwo equals 0, we assign it 100%
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
        $(this).before("<td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+$(this).text()+"</button>"+addDropdown());
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
    <td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+headers[0]+"</button>"+addDropdown()+"</td>\
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