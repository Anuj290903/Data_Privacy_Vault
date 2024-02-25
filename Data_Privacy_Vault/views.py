from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ff3 import FF3Cipher
import random, string, json, os
from .models import myData, ID

# Encryption_Key="EF4359D8D580AA4F7F036D6F04FC6A94"
# Encryption_Key is stored in the environment variable

def display(request):
    return render(request, "display.html")

def generate_token(length=8):
    # Generate a token of the given length
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def tokenize(request):
    if request.method == 'POST':
        # Get the data from the POST request
        data = request.body.decode('utf-8')
        # Check if the data is empty
        if data == None:
            return HttpResponse("Data is empty", status=401)

        try:
            # Check if the data is in JSON format and convert to Python dictionary
            data = json.loads(data)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=402)

        # Get the data_id from the JSON data  
        if not data['id']:
            return HttpResponse("Data ID is missing", status=403)

        # Check if the data_id is already in the database
        if ID.objects.filter(data_id=data['id']).exists():
            return HttpResponse("Data ID already exists", status=404)
        # Create a new entry of the Data ID
        entry = ID(data_id=encrypt(data['id']))
        entry.save()
        # Tokenize the data
        data['data'] = tokenize_data(data['data'], entry)
        return JsonResponse(data, status=201)
    else:
        return HttpResponse("Only POST method is allowed", status=405)

def tokenize_data(data, dataId):
    for key in data:
        temp_token = generate_token()
        while myData.objects.filter(key=temp_token).exists():
            temp_token = generate_token()
        dict = myData(key=encrypt(temp_token), value=encrypt(data[key]), id=dataId, field=encrypt(key))    
        dict.save()
        data[key] = temp_token
    return data

def detokenize(request):
    if request.method == 'POST':
        # Get the data from the POST request
        data = request.body.decode('utf-8')
        # Check if the data is empty
        if data == None:
            return HttpResponse("Data is empty", status=401)

        try:
            # Check if the data is in JSON format and convert to Python dictionary
            data = json.loads(data)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=402)

        # Get the data_id from the JSON data  
        if not data['id']:
            return HttpResponse("Data ID is missing", status=403)

        # Check if the data_id is already in the database
        if not ID.objects.filter(data_id=encrypt(data['id'])).exists():
            return HttpResponse("Data ID does not exist", status=404)

        # Detokenize the data
        data['data'] = detokenize_data(data['data'], data['id'])
        return JsonResponse(data, status=201)
    else:
        return HttpResponse("Only POST method is allowed", status=405)

def detokenize_data(data, dataId):
    data_copy = data.copy()
    for key in data_copy:
        if myData.objects.filter(key=encrypt(data[key])).exists():
            entry = myData.objects.get(key=encrypt(data[key]))
            if decrypt(entry.id.data_id) == dataId and decrypt(entry.field) == key:
                data[key] = {'found' : True, 'value': decrypt(entry.value)}
            else: 
                data[key] = {'found' : False, 'value': ""}
        else:
            data[key] = {'found' : False, 'value': ""}
    return data

def encrypt(data):
    cipher = FF3Cipher(key = os.environ.get('ENCRYPTION_KEY'), tweak="D8E7920AFA330A73", radix=62)
    return cipher.encrypt(data)

def decrypt(data):
    cipher = FF3Cipher(key = os.environ.get('ENCRYPTION_KEY'), tweak="D8E7920AFA330A73", radix=62)
    return cipher.decrypt(data)