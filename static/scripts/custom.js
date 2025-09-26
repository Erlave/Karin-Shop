



function addProductToOrder(productID) {
    const ProductCount = $('#product_count').val();

    $.get('/order/add-to-order?product_id=' + productID + '&count=' + ProductCount)
    .then(res => {
        Swal.fire({
            title: res.title || "اعلان",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if(result.isConfirmed && res.status ==='not_logged_in'){
                window.location.href='/account/login/'
            }
        });
    })
    .catch(err => {
        Swal.fire('خطا', 'ارتباط با سرور برقرار نشد!', 'error');
    });
}

