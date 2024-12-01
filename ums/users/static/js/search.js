$(document).ready(function () {
    console.log("El archivo search.js se ha cargado correctamente");
// FUNCION PARA BUSCAR USUARIOS POR NOMBRE, APELLIDO O NOMBRE DE USUARIO
    $("#search-input").on("input", function () {
        let query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: "/search-users/",
                method: "GET",
                data: { query: query },
                success: function (data) {
                    let results = $("#search-results");
                    results.empty();
                    if (data.length > 0) {
                        data.forEach(user => {
                            results.append(`<div class="user-result">${user.username} - ${user.first_name} ${user.last_name}</div>`);
                        });
                    } else {
                        results.append("<div class='no-results'>No se encontraron usuarios.</div>");
                    }
                },
                error: function () {
                    console.error("Error al buscar usuarios.");
                }
            });
        } else {
            $("#search-results").empty();
        }
    });
});
