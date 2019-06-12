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

// Now the actual "complex" part begins, its not really complex, just kind or lengthy, this function updates all the grade category grades based on the info in the grade "body", so this is the grade calculator part
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
        // Now, iterate through all the headers in the html
        $('.header').each(function(index, obj) {
            // If it matches the current header, 
            if ($(this).text() == type){
                // Set the grade and the percent to what they should be, also add the proper button class, which is simply the color of the button 
                $(this).closest('tr').find('button').removeClass().text(grade+' - '+percent).addClass('btn btn-'+btn+' gradeLetter')
                alert()
                // Also, change the number in the "points" column to match the actual grade
                $(this).closest('tr').find('.headerInfo').text(String(colOne)+'/'+String(colTwo))
            }
        });  
    }
    // Call the function that updates the total grade, which is the overall class grade in the top right corner
    updateTotalGrade()
}

// As I said before, this is the function that updates the overall class grade
function updateTotalGrade(){
    // Define two variables, gradeVal and totalHead, they will be helpful in calculating the total grade in the class
    var gradeVal = 0,
        // Declare totalHead which will represent the weight of all the items in the class
        totalHead = 0
    // Iterate through all of the grade headers, the purpose of this loop is to get the total weight of all the categories
    $('.header').each(function(index, obj) {
        // As long as the grade isn't 0/0, we will do stuff with it
        if($(this).closest('tr').find('.headerInfo').text() != '0/0'){
            // This adds the weight of that assignment to the variable to keep track of it, the reason that we do this is because, for example, if you have no grades in the graded (90%) category and a 5/5 on a homework (10%) category, you wouldn't have a 10% in the class, you would have a 100%
            totalHead += parseInt($(this).text().slice($(this).text().indexOf('(')+1,-1))
        }
    });
    // Iterate through the headers once more, this time, we are going to do some more calculations and then we are done 
    $('.header').each(function(index, obj) {
        // Declare some more variables that will help us, wieght is the weight of the category
        var weight = $(this).text().slice($(this).text().indexOf('(')+1,-1),
            // Val is simply the points earned/points possible
            val = eval($(this).closest('tr').find('.headerInfo').text())
        // Quick check to see if the val is not a number, incase we are doing divison by 0 again
        if (isNaN(val)){val = 0}
        // Finally, add points according to weight to the total grade
        gradeVal += (weight*100/totalHead)*val
    }); 
    // Check if gradeVal is not a number, this would occur if all the grades are 0/0 meaning that totalHead remains as 0, causing divison by 0, if this occurs, just set the percentage to 100
    if (isNaN(gradeVal)){gradeVal = 100}
    // Create new helper varibales, set grades to A
    var grade = 'A',
        // Set the button value to green/success again, this is the same process that we did before
        btn = 'success'
    // So again, we have this one liner which determines the grade and color of the button, it is only slightly different since we are sure that there is no diviosn by 0
    if (gradeVal >= 79.5 && gradeVal < 89.5){btn = 'info', grade = 'B'}else if (gradeVal > 69.5 && gradeVal < 89.5){btn = 'primary', grade = 'C'}else if (gradeVal > 59.5 && gradeVal < 89.5){btn = 'warning', grade = 'D'}else if (gradeVal < 59.5){btn = 'danger', grade = 'E'}
    // Now we remove all the formatting classes on the button and then we make it a large button with the color and the text is the grade as well as the percent
    $('.btn-lg').removeClass().addClass('btn btn-lg btn-'+btn).text(grade+' - '+String(gradeVal.toFixed(1))+'%')
}

// If they change either of the input feilds for the grades, this is the part that changes the indvidual grades, the two functions above changed the overall class grade as well as the grades for each individual category
$(document).on('change', '.col-sm input', function(){
    // Create some helpful variables, this is the same process as before
    var one = $(this).closest("form").find(".one").val(),
        // Two again is the points possible
        two = $(this).closest("form").find(".two").val(),
        // The same as last time, a boolean to determine if we need to calculate the percent
        doPercent = true,
        // Defaults to success
        btn = 'success',
        // Default to a
        grade = 'A'
    // Again, we have the long line thing
    if (two == 0){doPercent = false}else if (one/two >= .795 && one/two < .895){btn = 'info', grade = 'B'}else if (one/two > .695 && one/two < .895){btn = 'primary', grade = 'C'}else if (one/two > .595 && one/two < .895){btn = 'warning', grade = 'D'}else if (one/two < .595){btn = 'danger', grade = 'E'}
    // Quick ternary operator
    doPercent?percent = String((one/two*100).toFixed(1))+'%':percent = '100%'
    // Change everything
    $(this).closest("tr").find('.gradeLetter').text(grade+' - '+percent).prop("disabled", false).removeClass().addClass('btn btn-'+btn+' gradeLetter')
    // Finally update the grades
    updateGrades()
});

// This is the part that allows users to edit their grades, this is run when the edit grades button is clicked
$(document).on('click', '#editGrades', function(){
    // Change the text of this button (this is the button that says edit grades) to be "Add Grade", also change the id, after this button, add an undo button
    $(this).text('Add Grade').attr("id","addGrade").after("&nbsp;<button type=\"button\" class=\"btn btn-secondary\" id=\"undoBtn\">Undo Changes</button>");
    // We also change the column that says "Due Date" to "Keep grade?"
    $(".gradeHeader").text("Keep grade?")
    // Place a button before all classes that are marked with date and then remove them, what this essentially does is that it replaces all the dates in the column with buttons that say romve grade
    $(".date").before("<td><button type=\"button\" class=\"btn btn-danger remove\">Remove Grade</button></td>").remove()
    // We iterate through all the headers agian
    $('.header').each(function(index, obj) {
        // Now we add all the header names to the headers list, this is because we only need to calculate the grades after someone changes them, so we are "paving the road" for the calculator here
        headers.push($(this).text())
    });
    // Iterate through all the things labeled with "type", we are doing the same replacing thing that we did before with dates in the date column, only we need a loop here because we want to keep the category of the assignment so we need a more "individualized" approach
    $('.type').each(function(index, obj) {
        // Before all of these, add the dropdowns which we populate as soon as we add, then we reomve the original thing
        $(this).before("<td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+$(this).text()+"</button>"+addDropdown()).remove()
    });
    // Now we iterate thorugh all the grades
    $('.grade').each(function(index, obj) {
        // Create variables which will be helpful later, one is equal to the points earned for a certain grade
        var one = $(this).text().slice(0, $(this).text().indexOf('/')),
            // Two is equal to the points possible for a certain grade
            two = $(this).text().slice($(this).text().indexOf('/')+1)
        // Check to see if the points possible are unentered or it is an x or z, therefore assign it the value of 0
        if(one == '' || isNaN(one)){one='0'}
        // Similarly, if two is blank or a 0, simply set it to 1 because we want to aviod divison of 0 even though we account for the user doing it anyway, since it's just good practice
        if(two == '0' || isNaN(two)){two == '1'}
        // Create the "number boxes" for the points earned and points possible and remove the old ones
        $(this).before("<td style=\"width: 20%\"><form><div class=\"form-row\"><div class=\"col-sm\"><input class=\"form-control one\" type=\"number\" min=\"0\" step=\".5\" value="+one+"></div><div class=\"col-sm\"><input class=\"form-control two\" type=\"number\" min=\"1\" step=\"1\" value="+two+"></form></div></div></td>").remove();
    });
    // Boolean that will be used later to determine if a grade update is needed
    var doUpdate = false
    // Iterate through each button
    $('button').each(function(index, obj) {
        // If the grade is disabled, meaning if the grade is unentered, an X or a Z
        if($(this).is(":disabled")){
            // We simply set the grade to 0, this allows the user to do whatever they want with it, if they wish to delete it or change it etc
            $(this).closest("tr").find('.gradeLetter').text('E - 0.0%').prop("disabled", false).removeClass().addClass('btn btn-danger gradeLetter')
            // Set do update to true since we changed some grades to 0's
            doUpdate = true
        }
    });  
    // If anything changed, we need to update the grades again
    if(doUpdate){updateGrades()}
});

// Some easy stuff at the end and then we are done

// Function that handles what happens when the add grade button is clicked
$(document).on('click', '#addGrade', function(){
    // Create a new row, and in that row we put the same stuff as what would be in all the other rows, set the points earned to 0 and the points possible to 1, set the description to user entered grade and also add the dropdown
    $("#gradeTable").prepend("<tr class=\"userAdded\"><td><button type=\"button\" class=\"btn btn-danger remove\">Remove Grade</button></td><td><button class=\"btn btn-secondary dropdown-toggle types\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+headers[0]+"</button>"+addDropdown()+"</td><td>User Added Grade</td><td style=\"width: 20%\"><form><div class=\"form-row\"><div class=\"col-sm\"><input class=\"form-control one\" type=\"number\" min=\"0\" step=\".5\" value=\"0\"></div><div class=\"col-sm\"><input class=\"form-control two\" type=\"number\" min=\"1\" step=\"1\" value=\"1\"></form></div></div></td><td><button type=\"button\" class=\"btn btn-danger gradeLetter\"\">E - 0.0%</button></td></tr>");
    updateGrades()
});

// If they click the undo button
$(document).on('click', '#undoBtn', function(){
    // This just reloads the page so everything will be back to normal
    location.reload();
});

// If they click the remove button for a grade
$(document).on('click', '.remove', function(){
    // Remove the grade
    $(this).closest("tr").remove()
    // Update the grades
    updateGrades()
});

// If they click any of the dropdown items for a grade
$(document).on('click', '.dropdown-menu a', function(){
    // Set the text of the dropdown to that value
    $(this).closest("td").find('button').text($(this).text())
    // Update the grades
    updateGrades()
});
