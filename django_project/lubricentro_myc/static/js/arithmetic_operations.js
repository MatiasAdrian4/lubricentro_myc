
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

function actualizar_total() {
    console.log(1)
}

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

});