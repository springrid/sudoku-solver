$('form[name="sudoku-form"] input:reset').click(function () {
    $("input, select, textarea")
        .not("input[type=checkbox], input[type=radio], input[type=button], input[type=submit]")
        .val("");
    $("input[type=checkbox], input[type=radio]").prop("checked", false);
});
