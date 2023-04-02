from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from IntelliLearnBackendAPI.modelserializers import McqSerializer
from IntelliLearnBackendAPI.modelserializers import StudentSerializer, ClassSerializer, TeacherSerializer, MarksSerializer, TeacherAttendanceSerializer
from rest_framework.response import Response
import rest_framework.request
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import StudentModel, classModel, TeacherModel, MarksModel
from IntelliLearnBackendAPI.models import TeacherAttendance

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


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

#API to answer questions using bert
#takes question and context as input
class QuestionAnswering(APIView):

    def post(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        question = data['question']
        #context = data['context']

        context = '''
            Physics is a branch of Science that 
            deals with matter, energy and their 
            relationship.
            Some main branches of Physics 
            are mechanics, heat, sound, light 
            (optics), electricity and magnetism, 
            nuclear physics and quantum 
            physics.
            Physics plays an important role in 
            our daily life. For example, 
            electricity is widely used 
            everywhere, domestic appliances, 
            office equipments, machines used 
            in industry, means of transport and 
            communication etc. work on the 
            basic laws and principles of 
            Physics.
            A measurable quantity is called a 
            physical quantity.
            Base quantities are defined 
            independently. Seven quantities 
            are selected as base quantities. 
            These are length, time, mass, 
            electric current, temperature, 
            intensity of light and the amount of 
            a substance
        '''

        input_ids = tokenizer.encode(question, context)
        print (f'We have about {len(input_ids)} tokens generated')

        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        print(" ")
        print('Some examples of token-input_id pairs:')

        for i, (token,inp_id) in enumerate(zip(tokens,input_ids)):
            
            print(token,":",inp_id)
        sep_idx = tokens.index('[SEP]')

        # we will provide including [SEP] token which seperates question from context and 1 for rest.
        token_type_ids = [0 for i in range(sep_idx+1)] + [1 for i in range(sep_idx+1,len(tokens))]
        print(token_type_ids)

        # Run our example through the model.
        out = model(torch.tensor([input_ids]), # The tokens representing our input text.
                        token_type_ids=torch.tensor([token_type_ids]))

        start_logits,end_logits = out['start_logits'],out['end_logits']
        # Find the tokens with the highest `start` and `end` scores.
        answer_start = torch.argmax(start_logits)
        answer_end = torch.argmax(end_logits)

        ans = ' '.join(tokens[answer_start:answer_end + 1])
        print('Predicted answer:', ans)

        if len(ans) < 1:

            ans = "Oops! I got confused.."

        return Response(ans, status=200)

    # #another version for longer text
    # def get(self, request):

    #     if len(request.query_params) > 0:
    #         data = request.query_params
    #     elif len(request.data) > 0:
    #         data = request.data

    #     question = data['question']
    #     context = data['context']


    #     return Response(ans, status=200)


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
        
#API to get marks by evaluation for a whole class
#inputs: {class_level, section, subject, evaluationType}
class MarksByEvaluationType(APIView):

    def get(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        class_level = data['class_level']
        section = data['section']
        subject = data['subject']
        evaluationType = data['evaluationType']

        try:
            forClass = classModel.objects.get(class_level = class_level, section = section, subject = subject)

            if forClass: 

                try:
                    marks = MarksModel.objects.filter(class_ID = forClass.class_ID, evaluationType = evaluationType)

                    if marks:
                        serializer = MarksSerializer(marks, many=True)
                        return Response(serializer.data, status=200)

                    else:
                        return Response("Marks for requested class not available", status=404)

                except:
                    return Response("Marks for requested class not available", status=404)
            else:
                return Response("No data exists!", status=404)
        except:
            return Response("No Such Class Found", status=404)

# Mark and Retrieve teacher attendance
class TeacherAttendanceView(APIView):

    def get(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        teacher_id = data['teacher'] #retrieve attendance by email

        teacher = TeacherModel.objects.get(teacher_ID=teacher_id)

        try:
            attendance = TeacherAttendance.objects.filter(teacher = teacher)

        except:

            return Response("No attendance record!", status=404)

        
        serializer = TeacherAttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):

        if len(request.query_params) > 0:
            data = request.query_params
        elif len(request.data) > 0:
            data = request.data

        serializer = TeacherAttendanceSerializer(data = data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=200)
 
        return Response(serializer.errors, status=400)

