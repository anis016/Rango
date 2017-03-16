/**
 * Created by anis on 3/16/17.
 */
console.log("hello world");
$(document).ready(function() {
    console.log("hello world");
    $(".nav a").on("click", function(){
        console.log('Hello !')
        $(".nav").find(".active").removeClass("active");
        $(this).parent().addClass("active");
    });
});