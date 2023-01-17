from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from IntelliLearnBackendAPI.modelserializers import McqSerializer
from rest_framework.response import Response
import rest_framework.request
from IntelliLearnBackendAPI.models import McqModel

# Create your views here.
def home(request):

    return HttpResponse("API IS UP!")

class McqsAPIView(APIView):

    def post(self, request):

        print()
        print()
        print("Data: ", request.data)
        print("request.query_params: ", request.query_params, end="\n\n")

        print("len Data: ", len(request.data))
        print("len request.query_params: ", len(request.query_params), end="\n\n")


        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data


        serializer = McqSerializer(data = data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=200)
 
        return Response(serializer.errors, status=400)


    def get(self, request):

        mcqs = McqModel.objects.all()

        if mcqs:

            serializer = McqSerializer(mcqs, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response("Error loading data!", status=400)

    def delete(self, request):

        id = request.query_params['question_ID']

        try:
            
            mcq = McqModel.objects.get(question_ID = id)

            if mcq:

                mcq.delete()
                data = {"response" : "MCQ deleted successfully!"}
                return Response(data, status=200)

        except McqModel.DoesNotExist:
        
            data = {"response" : "MCQ does not exist!"}
            return Response(data, status=400)


    # def get(self, request):

    #     data = request.data

    #     print("METHOD: ", request.method)
    #     #data = {'weight':6}

    #     print("REQUEST: ", request)
    #     print("DATA IS: ", str(data))
    #     serializer = McqSerializer(data = data)

    #     if serializer.is_valid():

    #         serializer.save()
    #         return Response(serializer.data, status=200)
 
    #     return Response(serializer.errors, status=400)