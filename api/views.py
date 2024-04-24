from django.shortcuts import render
from rest_framework.decorators import api_view
import cv2 
from django.core.files.base import ContentFile
import numpy as np
import tempfile
from rest_framework.response import Response
from .helpers import *
import time
@api_view(["POST"])
def gettrans(request):

    video_file = request.FILES['video']

    # Create a temporary file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    filepath = temp.name
    
    # Write the uploaded video file to the temporary file
    for chunk in video_file.chunks():
        temp.write(chunk)
    temp.close()
    vidObj = cv2.VideoCapture(filepath)
    count = 0
    # checks whether frames were extracted 
    success = 1
    while success: 
  
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
        # Saves the frames with frame-count 
        if(count%10 == 0):
            cv2.imwrite("data/frame%d.jpg" % count, image) 
  
        count += 1
    time.sleep(10)
    s = gettextfromvideo()
    translate = generativetranslate(s)
    return Response({"message":translate})
# Create your views here.