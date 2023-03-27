from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from IntelliLearnBackendAPI.modelserializers import McqSerializer
from IntelliLearnBackendAPI.modelserializers import StudentSerializer, ClassSerializer, TeacherSerializer
from rest_framework.response import Response
import rest_framework.request
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import StudentModel, classModel, TeacherModel

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


class StudentsAPIView(APIView):

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


        serializer = StudentSerializer(data = data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=200)
 
        return Response(serializer.errors, status=400)


    def get(self, request):

        students = StudentModel.objects.all()

        if students:

            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response("Error loading data!", status=400)

    def delete(self, request):

        id = request.query_params['student_ID']

        try:
            
            student = StudentModel.objects.get(student_ID = id)

            if student:

                student.delete()
                data = {"response" : "Student data deleted successfully!"}
                return Response(data, status=200)

        except StudentModel.DoesNotExist:
        
            data = {"response" : "Student does not exist!"}
            return Response(data, status=400)

class TeacherAPIView(APIView):

    def post(self, request):

        print()
        print()
        print("Posted Data: ", request.data)
        print("request.query_params: ", request.query_params, end="\n\n")

        print("len Data: ", len(request.data))
        print("len request.query_params: ", len(request.query_params), end="\n\n")


        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        serializer = TeacherSerializer(data = data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=200)
 
        return Response(serializer.errors, status=400)


    def get(self, request):

        teachers = TeacherModel.objects.all()

        if teachers:

            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response("Error loading data!", status=400)

    def delete(self, request):

        id = request.query_params['teacher_ID']

        try:
            
            teacher = TeacherModel.objects.get(teacher_ID = id)

            if teacher:

                teacher.delete()
                data = {"response" : "Teacher data deleted successfully!"}
                return Response(data, status=200)

        except TeacherModel.DoesNotExist:
        
            data = {"response" : "Teacher does not exist!"}
            return Response(data, status=400)

class TeacherLoginAPIView(APIView):

    def post(self, request):

        # print()
        # print()
        # print("Data: ", request.data)
        # print("request.query_params: ", request.query_params, end="\n\n")

        # print("len Data: ", len(request.data))
        # print("len request.query_params: ", len(request.query_params), end="\n\n")

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        email = data['email']
        password = data['password']

        try:
            teacher = TeacherModel.objects.get(email = email)

            try:
                teacher = TeacherModel.objects.get(email = email, password = password)
                serializer = TeacherSerializer(teacher, many=False)
                data = {"response" : "Success", "data": serializer.data}
                return Response(data, status=200)
        
            except:
                data = {"response" : "Failure", "reason" : "Incorrect password!"}
                return Response(data, status=400)


        except:
            data = {"response" : "Failure", "reason" : "Email not registered!"}
            return Response(data, status=400)

#class to add, remove, select, and update teacher teaching classes
class TeacherClassesAPIView(APIView):

    def get(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        teacher_ID = data['teacher_ID']

        try:
            classes = classModel.objects.filter(teacher_ID = teacher_ID)
        except:
            return Response("No Classes Exist", status=404)

        if classes:

            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data, status=200)
        
        else:
        
            return Response("Error loading data!", status=400)


class ClassesAPIView(APIView):

    def post(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        serializer = ClassSerializer(data = data)

        if serializer.is_valid():

            serializer.save() #stores the data in the database
            return Response(serializer.data, status=200)
 
        return Response(serializer.errors, status=400)


    def get(self, request):

        classes = classModel.objects.all()

        if classes:

            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response("Error loading data!", status=400)

    def delete(self, request):

        id = request.query_params['class_ID']

        try:
            
            classObj = classModel.objects.get(class_ID = id)

            if classObj:

                classObj.delete() #data deleted from database
                data = {"response" : "Class data deleted successfully!"}
                return Response(data, status=200)

        except classModel.DoesNotExist:
        
            data = {"response" : "Class does not exist!"}
            return Response(data, status=400)