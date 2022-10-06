from django.shortcuts import render
from .models import *
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
# @api_view(['POST'])
# def Register(request):
#     try:
#         username = request.data['username']
#         password = request.data['password']
#         usrs = User.objects.create(username=username, password=password)
#         token = Token.objects.create(user=usrs)
#         data = {
#             'username': username,
#             'user_id': usrs.id,
#             'token': token.key,
#         }
#         return Response(data)
#     except Exception as err:
#         return Response({"error": f'{err}'})
@api_view(['POST'])
def Register(request):
    try:
        username = request.data['username']
        password = request.data['password']
        users = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=users)
        data = {
            'username': username,
            'user_id': users.id,
            'token': token.key,
        }
        return Response(data)
    except Exception as err:
        return Response({'error': f'{err}'})

@api_view(['POST'])
def login_view(request):
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            usrs = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                status = 200
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'status': status,
                    'username': username,
                    'user_id': usrs.id,
                    'token': token.key,
                }
            else:
                status = 403
                message = 'Username yoki parol xato!'
                data = {
                    'status': status,
                    'message': message,
                }
        except User.DoesNotExist:
            status = 404
            message = 'Bunday foydalanuvchi mavjud emas!'
            data = {
                'status': status,
                'message': message,
            }
        return Response(data)
    except Exception as er:
        return Response({"error": f'{er}'})



class GetMenyu(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.type == 1:
            product = Food.objects.filter(available=True)
            food = []
            for i in product:

                data = {

                   'name': i.name,
                   'image': i.image.url,
                   'bio': i.description,
                   'price': i.price
                }
                food.append(data)
                return Response(food)


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_menu(request):
#     user = request.user
#     if user.type == 1:
#         product = Food.objects.filter(available=True)
#         food = []
#         for i in product:
#             data = {
#                 'name': i.name,
#                 'image': i.image.url,
#                 'bio': i.description,
#                 'price': i.price
#             }
#             food.append(data)
#     return Response(food)



class GetAll(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.type == 1:
            product = []
            price = 0
            order = Order.objects.get(id=pk)
            for i in order.order.all():
                hello = {
                    'name': i.food.name,
                    'image': i.food.image.url,
                    'bio': i.food.description,
                    'price': i.food.price,
                    'quantity': i.quantity,
                }
                product.append(hello)
                price += i.food.price * i.quantity
            data = {
                'price': price,
                'product': product,
            }
            return Response(data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
# @api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_all(request, pk):
#     user = request.user
#     if user.type == 2:
#         product = []
#         price = 0
#         order = Order.objects.get(id=pk)
#         for i in order.order.all():
#             hello = {
#                 'name': i.food.name,
#                 'image': i.food.image.url,
#                 'bio': i.food.description,
#                 'price': i.food.price,
#                 'quantity': i.quantity,
#             }
#             product.append(hello)
#             price += i.food.price * i.quantity
#             data = {
#                 'price': price,
#                 'product': product,
#
#             }
#     return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def OrderItemcreate(request):
    user = request.user
    if user.type == 1:
        food = request.POST.get('food')
        quantity = request.POST.get('quantity')
        order = OrderItem.objects.create(food_id=food, quantity=quantity)
        return Response(OrderItemSerializer(order).data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Ordercreated(request):
    user = request.user
    item = request.POST.getlist('item')
    table = request.POST.get('table')
    order = Order.objects.create(table_id=int(table), user=user)
    for i in item:
        order.order.add(OrderItem.objects.get(id=int(i)))
    return Response(OrderSerializer(order).data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delete(request, pk):
    user = request.user
    if user.type == 2:
        table = Table.objects.get(id=pk)
        number = table.number
        for i in Order.objects.all():
            idlar = i.id
            if i.table.number == number:
                order = Order.objects.get(id=idlar)
                order.delete()
            else:
                pass
        table.busyness = 1
        table.save()
        return Response('ok')
    else:
        return Response('sen ochirmesan')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Update(request, pk):
    user = request.user
    table = request.POST.get('table')
    date = request.POST.get('date')
    orderitem = request.POST.get('order')
    order = Order.objects.get(id=pk)
    if user.type == 1:
        order.table = table
        order.date = date
        order.save()
        return Response(OrderSerializer(order).data)




