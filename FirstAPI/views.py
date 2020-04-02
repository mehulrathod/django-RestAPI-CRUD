from django.shortcuts import render
from django.http import HttpResponse

# IMPORTANT imports
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports Models
from .models import Person
from .serializer import PersonSerializers

# Imports for list API's
from rest_framework import generics

# Imports for Rest API filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Imports for Pagination in Rest Api
from rest_framework.pagination import LimitOffsetPagination

''' list API's which is basically similar to the get requests'''


class PersonViewPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3


class PersonView(generics.ListAPIView):
    """
    GET
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    # Filter logic and for that we have a filter backends which is nothing but a tuples.
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'Name')  # It's for filter button
    search_fields = ('id', 'Name')  # It's for Search button
    pagination_class = PersonViewPagination


class PersonCreateListApi(generics.CreateAPIView):
    serializer_class = PersonSerializers

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get("Name", None)
            age = request.data.get("Age", None)
            birthday = request.data.get("Birthday", None)
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({
                "Message": "Failed"
            })


class PersonViewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    lookup_field = 'id'
    serializer_class = PersonSerializers

    def delete(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)  # if id is not found then it returns None and we use get() bucz its dict.
            response = super().delete(request, *args, **kwargs)

            if response.status_code == 204:
                from django.core.cache import cache
                cache.delete("{}".format(id))
                return response
        except Exception as e:
            return Response({
                "Message": "Failed"
            })

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)

            if response.status_code == 200:
                mydata = response.data

                from django.core.cache import cache
                cache.set("ID: {}".format(mydata.get('id', None)), {
                    'Name': mydata["Name"],
                    'Age': mydata["Age"],
                    'Birthday': mydata["Birthday"]
                })
                return response
        except Exception as e:
            return Response({
                "Message": "Failed"
            })


'''
    Generic data view is generally a static data view where the data is static,
    which was basically a server added data by statically
    in simple terms that data which doesn't come from the database are called GenericDataView / StaticData 
'''
# In order to create a GenericApiView you should have a Serializer
from .serializer import DummySerializer


class PersonDummyViews(generics.GenericAPIView):
    serializer_class = DummySerializer

    def get(self, request):
        message = {
            'mydictdata': "Some Data"
        }

        serializer = DummySerializer({
            'data': message
        })

        return Response(serializer.data)


''' 
    this is the API's for the post and get by using serializer
    this API is for the normal use not for the complex data
'''
# class PersonView(APIView):
#
#     def get(self, request):
#         data = Person.objects.all()
#         serializer = PersonSerializers(data, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         try:
#             serializer = PersonSerializers(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' this is the API's for the post, get and put by using functions for clearing concepts about API's in django'''
# data = ["Mehul"]
#
#
# # API's/FUNCTION for Get request
# class Youtube(APIView):
#     # constructor
#     # def __init__(self):
#     #     self.data = ["Mehul"]  # list of data
#
#     def get(self, requests, format=None):
#         # return Response({"Message": "Get Works"})
#         # return Response({"Message": self.data})  # we are adding data
#         return Response({"Message": data})
#
#     # API's/FUNCTION for POST requests
#     def post(self, requests, format=None):
#         Mydata = requests.data  # this is a dictionary
#         Name = Mydata.get("Name", None)  # so we can extract the data and if data not found then return None.
#         data.append(Name)
#         # self.data.append(Name)  # one's we get data then append the Name init.
#         # print("Data Received : {}".format(data))
#
#         return Response({
#             'Response': 200,
#             'Data': Name,
#             'Message': 'Item was Added to DataBase'
#
#             # "Message": data
#         })
#
#     # API's/FUNCTION for PUT requests
#     def put(self, requests, format=None):
#         Mydata = requests.data
#         return Response(
#             {"Response": "PUT WORKS"}
#         )

# def index(request):
#     return HttpResponse("<h1>Hello World</h1>")
