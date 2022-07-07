from django.shortcuts import render,redirect
from .models import PaymentGateway, Invoice, InvoiceDetail
from product_module.models import CartItem, Product
from datetime import date, datetime
from django.db import transaction
from django.urls import reverse
# Create your views here.
def confirmpayment(request):
    if request.method == "POST":
        token = request.POST.get("token")
        amount = request.POST.get("amount")
        product_id=request.POST.get("id")
        quantity=request.POST.get("qty")
        # clean up
        token = token.strip()
        amount = float(amount)
        try:
            with transaction.atomic():
                # open an atomic transaction, i.e. all successful or none
                make_payment(token, amount)
                maintain_invoice(request, token, amount)
                request.session["message"] = "Payment successful."

        except Exception as e:
            request.session["message"] = str(e)
            return redirect(reverse('error_page'))
        else:
            if product_id:
            # retrieve product data
                product = Product.objects.get(id=product_id)
                try:
            # get cart item and increase quantity
                    cart_item = CartItem.objects.get(user=request.user, product=product)
                    cart_item.quantity = int(quantity)
                    cart_item.entered_on = datetime.now()
                except CartItem.DoesNotExist:
        # initialize cart item
                    cart_item = CartItem(
                    user=request.user,
                    product=product,
                    quantity=int(quantity),entered_on = datetime.now(),
                )
        # save to database
                cart_item.save()
            # retrieve the cart items for the user from db
            cart_items = CartItem.objects.filter(user=request.user)
            # calculate total
            total = 0
            for item in cart_items:
                total += item.product.price * item.quantity
            # return view
            context = {'cart_items': cart_items,
            'total': total,
            }
            return redirect(reverse('success_page'), context)

def make_payment(token, amount):
    try:
        payment_gateway = PaymentGateway.objects.get(token=token)
    except:
        raise Exception(f"Invalid token '{token}'")
        # Check if available amount is sufficient for payment
    if payment_gateway.balance < amount:
        raise Exception("Insufficient balance")
    # check for expiry date
    if payment_gateway.expiry_date < date.today():
        raise Exception("Token has expired")
    # deduct amount and save
    payment_gateway.balance -= amount
    payment_gateway.save()

def maintain_invoice(request, token, amount):
    # retrieve cart items
    cart_items = CartItem.objects.filter(user=request.user)
    # save invoice
    invoice = Invoice(
    user = request.user,
    token = token,
    total_amount = amount,
    payment_date = datetime.now()
    )
    invoice.save()
    # save invoice detail
    for cart_item in cart_items:
        invoice_detail = InvoiceDetail(
            invoice = invoice,
            product = cart_item.product,
            quantity = cart_item.quantity,
            sub_amount = cart_item.quantity * cart_item.product.price
        )
        invoice_detail.save()
    # adjust product quantity and clear cart
    for cart_item in cart_items:
    # reduce quantity from Product
        product = Product.objects.get(id=cart_item.product.id)
        if product.quantity < cart_item.quantity:
            raise Exception(f"Insufficient quantity {cart_item.quantity} for {product.name}")
        product.quantity -= cart_item.quantity
        product.save()
    # clear cart for the user
        cart_item.delete()