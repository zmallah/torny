window.addEventListener("load", function (evt) {
    var submit = $("#inpSbmt");
    var pass1 = $("#inpPass");
    var pass2 = $("#inpPass2");
    var warn = $("#passWarn");
    var form = $("form");

    form.on("submit", function (evt) {
        if (pass1.val() != pass2.val()) {
            warn.removeClass("warn-nodisp");
            warn.addClass("warn-disp");
            evt.preventDefault();
        }
    });
});
