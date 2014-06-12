
// called on every page
function main() {
    registerSideMenu();
    registerNotificationsCloseButton();

    $('[data-toggle="popover"]').popover({
        trigger:'hover',
        placement: 'left',
        html:true
    });

    $('[data-must-confirm]').on('click', function (e) {
        var confirmText = $(this).data('confirm-text') || "Êtes vous sûr de vouloir continuer ?";
        return confirm(confirmText.replace("---", '\r\n'));
    });

    $('[data-reset-form]').on('click', function (e) {
        e.preventDefault();
        var form_id = $(this).data('reset-form') || null;
        var form = null;
        if (form_id === null) {
            form = $($(this).parents('form')[0]);
        } else {
            form = $('#' + form_id);
        }

        form.find('input, select').parent().removeClass('changed');
        form[0].reset();
    });
}

function registerNotificationsCloseButton() {
    console.log("registerNotificationsCloseButton");

    $(".close-notif-button").on('click', function (e) {
        notif = $(this).parent();
        notif.remove();
        e.preventDefault();
    });

    $('#menu').find('.pure-button-disabled').each(function () {
        $(this).removeAttr('href');
    });
}


function registerReportBrowserFilter(entity_browser, new_path) {
    if (new_path === null || new_path === undefined) {
        new_path = "/data/<reportcls_slug>/<entity_slug>/<period_strid>";
        // var new_path = "/data/"+ reportcls_slug +"/"+ entity_slug +"/" + period_strid;
    }

    entity_browser.parentElem.find('button').on('click', function() {
        var reportcls_slug = $("#filter_reportcls").val();
        var period_strid = $("#filter_period").val();
        if (period_strid === null)
            period_strid = "";
        var entity_slug = entity_browser.getEntitySlug();
        console.log(entity_slug);
        // var new_path = "/data/"+ reportcls_slug +"/"+ entity_slug +"/" + period_strid;
        new_path = new_path.replace('<reportcls_slug>', reportcls_slug)
                           .replace('<entity_slug>', entity_slug)
                           .replace('<period_strid>', period_strid);
        window.location = new_path;
    });
}

function registerEntityPeriodsFilter(options) {
    // options.entity_browser
    // options.periodAID
    // options.periodBID
    // options.url_tmpl
    // options.single_period


    options.entity_browser.parentElem.find('button').on('click', function() {

        var perioda_strid = $('#' + options.periodAID).val();
        var periodb_strid = $('#' + options.periodBID).val();
        var period_str = "";
        if (perioda_strid === null && periodb_strid === null) {
            period_str = "";
        } else if (perioda_strid === null || perioda_strid === undefined) {
            period_str = periodb_strid + "_" + periodb_strid;
        } else if (periodb_strid === null || periodb_strid === undefined) {
            period_str = perioda_strid + "_" + perioda_strid;
        } else {
            period_str = perioda_strid + "_" + periodb_strid;
        }

        // single period
        if (options.single_period === true) {
            period_str = period_str.split("_")[0];
        }

        var entity_slug = options.entity_browser.getEntitySlug();

        var new_path = options.url_tmpl.replace('<entity>', entity_slug).replace('<period_str>', period_str);
        window.location = new_path;
    });
}

function emulate_click_on(jQElem) {
    var e = document.createEvent("MouseEvents");
    e.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0,
                     false, false, false, false, 0, null);
    try {
        jQElem[0].dispatchEvent(e);
    } catch (exception) {}
}