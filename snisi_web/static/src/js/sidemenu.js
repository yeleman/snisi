
function registerSideMenu() {

    var layout = $('#layout');
    var menu = $('#menu');
    var menuLink = $('#menuLink');
    var active = 'active';
    var popover = null;

    if ($('body').hasClass('dashboard')) {

        if (menuLink.css('display') !== 'none') {
            popover = menuLink.popover({
                content:"Cliquez-ici pour le menu",
                placement: "right",
                trigger: "click",

            }).popover('toggle');
        }
    }

    menuLink.on('click', function (e){
        e.preventDefault();

        if (popover !== null) {
            popover.popover('destroy');
        }
        layout.toggleClass(active);
        menu.toggleClass(active);
        menuLink.toggleClass(active);
    });
}
