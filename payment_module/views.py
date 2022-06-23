from django.shortcuts import render

# Create your views here.
@login_required(login_url="/admin/login")
def cart(request):
        # get request data
        product_id = request.GET.get("id")
        quantity = request.GET.get("qty")
        
        if product_id:
            # retrieve product data
            product = Product.objects.get(id=product_id)
           
            try:
                # get cart item and increase quantity
                cart_item = CartItem.objects.get(user=request.user, product=product)
                cart_item.quantity += int(quantity)
                cart_item.entered_on = datetime.now()
            
            except CartItem.DoesNotExist:
                # initialize cart item
                cart_item = CartItem(
                    user=request.user,
                    product=product,
                    quantity=int(quantity),
                    entered_on = datetime.now(),
                    )
                
                # save to database
                cart_item.save()
            
        cart_items = CartItem.objects.filter(user=request.user)

        total = 0
        for item in cart_items:
                total += item.product.price * item.quantity

            # return view
        context = {
                'cart_items': cart_items,
                'total': total,
            }
        return render(request, "cart.html", context)

def removecart(request, id):
    try:
        # get cart item and increase quantity
            product = Product.objects.get(id=id)
            cart_item = CartItem.objects.get(user=request.user, product=product)
            cart_item.delete()

    except CartItem.DoesNotExist:
            pass

    # redirect to cart
    return redirect(cart)

def success_page(request):
    message = request.session["message"]
    return render(request, "success.html", {"message": message})

def error_page(request):
    message = request.session["message"]
    return render(request, "error.html", {"message": message})