from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json 
from .models import CartItem
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# add a decorator to the dispatch method which will set the csrf_exempt to true: this tells the method no need for csrf token
@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):
# define the post method for yout api
#writes the incoming request body into a dictionary and create a CartItem object, persisting it in the database
    def post(self,request):
        #decoded and parsed with the json module
        data = json.loads(request.body.decode("utf-8"))
        product_data = {
            'product_name': data.get('product_name'),
            'product_price': data.get('product_price'),
            'product_quantity': data.get('product_quantity'),
        }
        #persisted a cartitem to the db
        cart_item = CartItem.objects.create(**product_data)
        data = {
            "message": f"Item has been added to Cart with id: {cart_item.id}"
        }
        return JsonResponse(data, status=201)

    def get(self, request):
        try:
            items_count = CartItem.objects.count()
            items = CartItem.objects.all()

            items_data = []
            for item in items:
                items_data.append({
                    'product_name': item.product_name,
                    'product_price': item.product_price,
                    'product_quantity': item.product_quantity,
                })

            resp = {
                'data': items_data,
                'count': items_count,
            }

            return JsonResponse(resp, status=200)  

        except CartItem.NoSuchElementException:
            resp = {
                'message': f'Item does not exist'
            }
            return JsonResponse(resp, status=400) 

@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):
    def get(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)

            items_data = {
                'product_name': item.product_name,
                'product_price': item.product_price,
                'product_quantity': item.product_quantity,
            }

            resp = {
                'data': items_data,
            }

            return JsonResponse(resp, status=200)  

        except CartItem.DoesNotExist:
            resp = {
                'message': f'Item does not exist'
            }
            return JsonResponse(resp, status=404)  

    def patch(self, request, pk):
        try:
            data = json.loads(request.body.decode("utf-8"))
            item = CartItem.objects.get(id=pk)
            item.product_quantity = data['product_quantity']
            item.save()

            data = {
                'message': f'Item {pk} has been updated'
            }

            return JsonResponse(data, status=201)
        except CartItem.DoesNotExist:
            data = {
                'message': f'Item does not exist'
            }
            return JsonResponse(data, status=404) 
    def delete(self, request, pk):
        item = CartItem.objects.get(id=pk)
        item.delete()

        data = {
            'message': f'Item {pk} has been deleted'
        }

        return JsonResponse(data)