/*// Compressed MD5 js Hash algorithm
var hexcase=0,b64pad="";function b64_md5(r){return rstr2b64(rstr_md5(str2rstr_utf8(r)))}function hex_hmac_md5(r,d){return rstr2hex(rstr_hmac_md5(str2rstr_utf8(r),str2rstr_utf8(d)))}function rstr_md5(r){return binl2rstr(binl_md5(rstr2binl(r),8*r.length))}function rstr_hmac_md5(r,d){var _=rstr2binl(r);16<_.length&&(_=binl_md5(_,8*r.length));for(var m=Array(16),t=Array(16),n=0;n<16;n++)m[n]=909522486^_[n],t[n]=1549556828^_[n];var f=binl_md5(m.concat(rstr2binl(d)),512+8*d.length);return binl2rstr(binl_md5(t.concat(f),640))}function rstr2hex(r){for(var d,_=hexcase?"0123456789ABCDEF":"0123456789abcdef",m="",t=0;t<r.length;t++)d=r.charCodeAt(t),m+=_.charAt(d>>>4&15)+_.charAt(15&d);return m}function rstr2b64(r){for(var d="",_=r.length,m=0;m<_;m+=3)for(var t=r.charCodeAt(m)<<16|(m+1<_?r.charCodeAt(m+1)<<8:0)|(m+2<_?r.charCodeAt(m+2):0),n=0;n<4;n++)8*m+6*n>8*r.length?d+=b64pad:d+="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(t>>>6*(3-n)&63);return d}function str2rstr_utf8(r){for(var d,_,m="",t=-1;++t<r.length;)d=r.charCodeAt(t),_=t+1<r.length?r.charCodeAt(t+1):0,55296<=d&&d<=56319&&56320<=_&&_<=57343&&(d=65536+((1023&d)<<10)+(1023&_),t++),d<=127?m+=String.fromCharCode(d):d<=2047?m+=String.fromCharCode(192|d>>>6&31,128|63&d):d<=65535?m+=String.fromCharCode(224|d>>>12&15,128|d>>>6&63,128|63&d):d<=2097151&&(m+=String.fromCharCode(240|d>>>18&7,128|d>>>12&63,128|d>>>6&63,128|63&d));return m}function rstr2binl(r){for(var d=Array(r.length>>2),_=0;_<d.length;_++)d[_]=0;for(_=0;_<8*r.length;_+=8)d[_>>5]|=(255&r.charCodeAt(_/8))<<_%32;return d}function binl2rstr(r){for(var d="",_=0;_<32*r.length;_+=8)d+=String.fromCharCode(r[_>>5]>>>_%32&255);return d}function binl_md5(r,d){r[d>>5]|=128<<d%32,r[14+(d+64>>>9<<4)]=d;for(var _=1732584193,m=-271733879,t=-1732584194,n=271733878,f=0;f<r.length;f+=16){var h=_,i=m,a=t,e=n;m=md5_ii(m=md5_ii(m=md5_ii(m=md5_ii(m=md5_hh(m=md5_hh(m=md5_hh(m=md5_hh(m=md5_gg(m=md5_gg(m=md5_gg(m=md5_gg(m=md5_ff(m=md5_ff(m=md5_ff(m=md5_ff(m,t=md5_ff(t,n=md5_ff(n,_=md5_ff(_,m,t,n,r[f+0],7,-680876936),m,t,r[f+1],12,-389564586),_,m,r[f+2],17,606105819),n,_,r[f+3],22,-1044525330),t=md5_ff(t,n=md5_ff(n,_=md5_ff(_,m,t,n,r[f+4],7,-176418897),m,t,r[f+5],12,1200080426),_,m,r[f+6],17,-1473231341),n,_,r[f+7],22,-45705983),t=md5_ff(t,n=md5_ff(n,_=md5_ff(_,m,t,n,r[f+8],7,1770035416),m,t,r[f+9],12,-1958414417),_,m,r[f+10],17,-42063),n,_,r[f+11],22,-1990404162),t=md5_ff(t,n=md5_ff(n,_=md5_ff(_,m,t,n,r[f+12],7,1804603682),m,t,r[f+13],12,-40341101),_,m,r[f+14],17,-1502002290),n,_,r[f+15],22,1236535329),t=md5_gg(t,n=md5_gg(n,_=md5_gg(_,m,t,n,r[f+1],5,-165796510),m,t,r[f+6],9,-1069501632),_,m,r[f+11],14,643717713),n,_,r[f+0],20,-373897302),t=md5_gg(t,n=md5_gg(n,_=md5_gg(_,m,t,n,r[f+5],5,-701558691),m,t,r[f+10],9,38016083),_,m,r[f+15],14,-660478335),n,_,r[f+4],20,-405537848),t=md5_gg(t,n=md5_gg(n,_=md5_gg(_,m,t,n,r[f+9],5,568446438),m,t,r[f+14],9,-1019803690),_,m,r[f+3],14,-187363961),n,_,r[f+8],20,1163531501),t=md5_gg(t,n=md5_gg(n,_=md5_gg(_,m,t,n,r[f+13],5,-1444681467),m,t,r[f+2],9,-51403784),_,m,r[f+7],14,1735328473),n,_,r[f+12],20,-1926607734),t=md5_hh(t,n=md5_hh(n,_=md5_hh(_,m,t,n,r[f+5],4,-378558),m,t,r[f+8],11,-2022574463),_,m,r[f+11],16,1839030562),n,_,r[f+14],23,-35309556),t=md5_hh(t,n=md5_hh(n,_=md5_hh(_,m,t,n,r[f+1],4,-1530992060),m,t,r[f+4],11,1272893353),_,m,r[f+7],16,-155497632),n,_,r[f+10],23,-1094730640),t=md5_hh(t,n=md5_hh(n,_=md5_hh(_,m,t,n,r[f+13],4,681279174),m,t,r[f+0],11,-358537222),_,m,r[f+3],16,-722521979),n,_,r[f+6],23,76029189),t=md5_hh(t,n=md5_hh(n,_=md5_hh(_,m,t,n,r[f+9],4,-640364487),m,t,r[f+12],11,-421815835),_,m,r[f+15],16,530742520),n,_,r[f+2],23,-995338651),t=md5_ii(t,n=md5_ii(n,_=md5_ii(_,m,t,n,r[f+0],6,-198630844),m,t,r[f+7],10,1126891415),_,m,r[f+14],15,-1416354905),n,_,r[f+5],21,-57434055),t=md5_ii(t,n=md5_ii(n,_=md5_ii(_,m,t,n,r[f+12],6,1700485571),m,t,r[f+3],10,-1894986606),_,m,r[f+10],15,-1051523),n,_,r[f+1],21,-2054922799),t=md5_ii(t,n=md5_ii(n,_=md5_ii(_,m,t,n,r[f+8],6,1873313359),m,t,r[f+15],10,-30611744),_,m,r[f+6],15,-1560198380),n,_,r[f+13],21,1309151649),t=md5_ii(t,n=md5_ii(n,_=md5_ii(_,m,t,n,r[f+4],6,-145523070),m,t,r[f+11],10,-1120210379),_,m,r[f+2],15,718787259),n,_,r[f+9],21,-343485551),_=safe_add(_,h),m=safe_add(m,i),t=safe_add(t,a),n=safe_add(n,e)}return Array(_,m,t,n)}function md5_cmn(r,d,_,m,t,n){return safe_add(bit_rol(safe_add(safe_add(d,r),safe_add(m,n)),t),_)}function md5_ff(r,d,_,m,t,n,f){return md5_cmn(d&_|~d&m,r,d,t,n,f)}function md5_gg(r,d,_,m,t,n,f){return md5_cmn(d&m|_&~m,r,d,t,n,f)}function md5_hh(r,d,_,m,t,n,f){return md5_cmn(d^_^m,r,d,t,n,f)}function md5_ii(r,d,_,m,t,n,f){return md5_cmn(_^(d|~m),r,d,t,n,f)}function safe_add(r,d){var _=(65535&r)+(65535&d);return(r>>16)+(d>>16)+(_>>16)<<16|65535&_}function bit_rol(r,d){return r<<d|r>>>32-d}
// Gets form values 'pw' and 'dpw' and puts them in hidden feilds
function getPCASAuth(){
    var pskey = document.getElementById('inputPskey').value
    var originalpw = document.getElementById('inputOpriginalpw').value
    document.getElementById('inputPskey').value = hex_hmac_md5(pskey, b64_md5(originalpw)) //PW
    document.getElementById('inputOpriginalpw').value = hex_hmac_md5(pskey, originalpw.toLowerCase()) //DBPW
    }
*/
var overlay = jQuery('<div id="overlay"> </div>');
$("#submit").click(function() {
    $("div").show();
    sessionStorage.setItem('selected', 'grades-color')
});
$( document ).ready(function() {
    setInterval(function(){
        if (document.title == 'MyMCPS++ - Login'){
            document.getElementById("about-color").classList.remove('active');
            document.getElementById("grades-color").classList.remove('active');
            document.getElementById("contact-color").classList.remove('active');
        }
        else if (document.title == 'MyMCPS++ - Grades'){
            document.getElementById("about-color").classList.remove('active');
            document.getElementById("grades-color").classList.add('active');
            document.getElementById("contact-color").classList.remove('active');
        }
    }, 100);
    if (sessionStorage.getItem('selected') != null){
        if (sessionStorage.getItem('selected') == 'grades-color'){
            document.getElementById("grades-color").classList.add('active');
            document.getElementById("about-color").classList.remove('active');
            document.getElementById("contact-color").classList.remove('active');
        }
        else if (sessionStorage.getItem('selected') == 'contact-color'){
            document.getElementById("contact-color").classList.add('active');
            document.getElementById("grades-color").classList.remove('active');
            document.getElementById("about-color").classList.remove('active');
        }
        else{
            document.getElementById("about-color").classList.add('active');
            document.getElementById("grades-color").classList.remove('active');
            document.getElementById("contact-color").classList.remove('active');
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

/*
    alert('Toggle clicked')
    if ($(this).closest("td").find('div').text()){
        $(this).closest("td").find('div').remove()
        $(this).after(addDropdown($(this).text()))
    }
    else {
        $(this).after(addDropdown($(this).text()))
    }
});*/
