from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request, product_slug):
    #product_id = request.POST.get("product_id")

    product = Products.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
         "includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
         "message": "Товар добавлен в корзину",
         "cart_items_html": cart_items_html,
     }

    return redirect(request.META['HTTP_REFERER'])


def cart_change(request, product_slug):
    #cart_id = request.POST.get("cart_id")
    #quantity = request.POST.get("quantity")
    cart = Cart.objects.get(slug=product_slug)
    #cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity
    user_cart = get_user_carts(request)
    context = {"carts": user_cart}
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["orders"] = True
    cart_items_html = render_to_string(
        'includes/included_cart.html', {'carts': cart}, request=request)
    response_data = {
        'message': 'Количество изменено',
        'cart_items_html': cart_items_html,
        'quantity': updated_quantity,
    }
    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, cart_id):
    #cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["orders"] = True

    cart_items_html = render_to_string(
        "includes/included_cart.html", context, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return redirect(request.META['HTTP_REFERER'])


# // Теперь + - количества товара
#     // Обработчик события для уменьшения значения
#     $(document).on("click", ".decrement", function () {
#         // Берем ссылку на контроллер django из атрибута data-cart-change-url
#         var url = $(this).data("cart-change-url");
#         // Берем id корзины из атрибута data-cart-id
#         var cartID = $(this).data("cart-id");
#         // Ищем ближайшеий input с количеством
#         var $input = $(this).closest('.input-group').find('.number');
#         // Берем значение количества товара
#         var currentValue = parseInt($input.val());
#         // Если количества больше одного, то только тогда делаем -1
#         if (currentValue > 1) {
#             $input.val(currentValue - 1);
#             // Запускаем функцию определенную ниже
#             // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
#             updateCart(cartID, currentValue - 1, -1, url);
#         }
#     });
#
#     // Обработчик события для увеличения значения
#     $(document).on("click", ".increment", function () {
#         // Берем ссылку на контроллер django из атрибута data-cart-change-url
#         var url = $(this).data("cart-change-url");
#         // Берем id корзины из атрибута data-cart-id
#         var cartID = $(this).data("cart-id");
#         // Ищем ближайшеий input с количеством
#         var $input = $(this).closest('.input-group').find('.number');
#         // Берем значение количества товара
#         var currentValue = parseInt($input.val());
#
#         $input.val(currentValue + 1);
#
#         // Запускаем функцию определенную ниже
#         // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
#         updateCart(cartID, currentValue + 1, 1, url);
#     });
#
#     function updateCart(cartID, quantity, change, url) {
#         $.ajax({
#             type: "POST",
#             url: url,
#             data: {
#                 cart_id: cartID,
#                 quantity: quantity,
#                 csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
#             },
#
#             success: function (data) {
#                 // Сообщение
#                 successMessage.html(data.message);
#                 successMessage.fadeIn(400);
#                 // Через 7сек убираем сообщение
#                 setTimeout(function () {
#                     successMessage.fadeOut(400);
#                 }, 7000);
#
#                 // Изменяем количество товаров в корзине
#                 var goodsInCartCount = $("#goods-in-cart-count");
#                 var cartCount = parseInt(goodsInCartCount.text() || 0);
#                 cartCount += change;
#                 goodsInCartCount.text(cartCount);
#
#                 // Меняем содержимое корзины
#                 var cartItemsContainer = $("#cart-items-container");
#                 cartItemsContainer.html(data.cart_items_html);
#
#             },
#             error: function (data) {
#                 console.log("Ошибка при добавлении товара в корзину");
#             },
#         });
#     }