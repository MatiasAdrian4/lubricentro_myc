
$(".allownumericwithdecimal").on("keypress keyup blur",function (event) {
    $(this).val($(this).val().replace(/[^0-9\.]/g,''));
    if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
        event.preventDefault();
    }
});

$(".allownumericwithoutdecimal").on("keypress keyup blur",function (event) {    
    $(this).val($(this).val().replace(/[^\d].+/, ""));
    if ((event.which < 48 || event.which > 57)) {
      event.preventDefault();
    }
});

$(function(){
    
    // si el precio cambia
    $('.carrito-table tr td:nth-child(3) input').change(function() {
        $(this).addClass('prod-modified')
        var precio = this.value
        var cantidad = $('.carrito-table tr:has("td .prod-modified") td:nth-child(4) input').val()
        $('.carrito-table tr:has("td .prod-modified") td:nth-child(5) input').val((precio * cantidad).toFixed(2))
        $(this).removeClass('prod-modified')

        var total = 0;
        $('.carrito-table tr td:nth-child(5) input').each(function() {
            total += parseFloat(this.value)
        });
        $('.resumen-venta tr:nth-child(1) td:nth-child(2) input').val(total.toFixed(2))
    });

    // si la cantidad cambia
    $('.carrito-table tr td:nth-child(4) input').change(function() {
        $(this).addClass('prod-modified')
        var cantidad = this.value
        var precio = $('.carrito-table tr:has("td .prod-modified") td:nth-child(3) input').val()
        $('.carrito-table tr:has("td .prod-modified") td:nth-child(5) input').val((precio * cantidad).toFixed(2))
        $(this).removeClass('prod-modified')

        var total = 0;
        $('.carrito-table tr td:nth-child(5) input').each(function() {
            total += parseFloat(this.value)
        });
        $('.resumen-venta tr:nth-child(1) td:nth-child(2) input').val(total.toFixed(2))
    });

    $("#producto-modal .modal-body table tr:nth-child(4) td input, #producto-modal .modal-body table tr:nth-child(5) td input, #producto-modal .modal-body table tr:nth-child(6) td input, #producto-modal .modal-body table tr:nth-child(7) td input, #producto-modal .modal-body table tr:nth-child(8) td input, #producto-modal .modal-body table tr:nth-child(9) td input, #producto-modal .modal-body table tr:nth-child(10) td input, #producto-modal .modal-body table tr:nth-child(11) td input, #producto-modal .modal-body table tr:nth-child(12) td input").change(function() {
        var precio_costo = parseFloat($('#producto-modal .modal-body table tr:nth-child(4) td input').val());
        var desc1 = parseFloat($('#producto-modal .modal-body table tr:nth-child(5) td input').val());
        var desc2 = parseFloat($('#producto-modal .modal-body table tr:nth-child(6) td input').val());
        var desc3 = parseFloat($('#producto-modal .modal-body table tr:nth-child(7) td input').val());
        var desc4 = parseFloat($('#producto-modal .modal-body table tr:nth-child(8) td input').val());
        var flete = parseFloat($('#producto-modal .modal-body table tr:nth-child(9) td input').val());
        var ganancia = parseFloat($('#producto-modal .modal-body table tr:nth-child(10) td input').val());
        var iva = parseFloat($('#producto-modal .modal-body table tr:nth-child(11) td input').val());
        var agregado_cta_cte = parseFloat($('#producto-modal .modal-body table tr:nth-child(12) td input').val());
        
        var precio_total_con_descuentos = precio_costo * ((100 - desc1) / 100) * ((100 - desc2) / 100) * ((100 - desc3) / 100) * ((100 - desc4) / 100);
        var precio_total_con_ganancias = precio_total_con_descuentos * ((100 + flete) / 100) *  ((100 + ganancia) / 100) * ((100 + iva) / 100);
        var precio_total_con_ganancias_y_agregado = precio_total_con_ganancias * ((100 + agregado_cta_cte) / 100);

        $('#producto-modal .modal-body table tr:nth-child(13) td input').val(Math.floor(precio_total_con_ganancias).toFixed(2));
        $('#producto-modal .modal-body table tr:nth-child(14) td input').val(Math.floor(precio_total_con_ganancias_y_agregado).toFixed(2));
    });

});