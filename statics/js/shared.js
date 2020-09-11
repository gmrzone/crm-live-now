var nav_open_button = document.querySelector(".mobile-nav-open-button")
var backdrop = document.querySelector(".back-model2")
var navigation = document.querySelector(".main-nav")
var nav_close_button = document.querySelector(".close-button")
var nav_open_button_hover = document.querySelectorAll(".mobile-nav-open-button_items")

nav_open_button.onmouseover = change_color
nav_open_button.onmouseout = change_to_white

        // Event Listenors
        nav_open_button.addEventListener('click', open_nav)
        backdrop.addEventListener('click', close_nav)
        nav_close_button.addEventListener('click', close_nav)


        // Functions
        function open_nav(){
            navigation.style.width = "60vw"
            backdrop.style.display = "block";
        }
        function close_nav(){
            navigation.style.width = "0vw";
            backdrop.style.display = "none";
        }

        function change_color(){
            nav_open_button_hover[0].style.background = "#03c9a8";
            nav_open_button_hover[1].style.background = "#03c9a8";
            nav_open_button_hover[2].style.background = "#03c9a8";
        }
        function change_to_white(){
            nav_open_button_hover[0].style.background = "white";
            nav_open_button_hover[1].style.background = "white";
            nav_open_button_hover[2].style.background = "white";
        }