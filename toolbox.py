import tkinter as tk
from tkinter import font

import sys 
import os 
import io
import re

import numpy as np
import pandas as pd

from PIL import Image, ImageOps
from pdf2image import convert_from_path

from difflib import SequenceMatcher

from datetime import date
from datetime import time
from datetime import datetime



credential_path = 'E:\GCP\macbook-2c718e707810.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types




def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    l1 = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # A new block starts here
            l2 = []
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    #print(word_text)
                    l2.append(word_text)
            l1.append(l2)
    return(l1)



# Function that returns invoice amount
def amt(data1):
    list3=[]
    ##pattern
    pattern=re.compile('(\d?\d?\d\s\.\s\d\d)|(\d?\d?\d\s,\s\d{3}\s\.\s\d\d)|(\d?\d?\d\s,\s\d{3}\s,\s\d{3}\s\.\s\d\d)')
    amount=pattern.finditer(data1)
    y3=0
    for match in amount:
        #print(match.group(0))
        x=match.group(0)
        y=x.replace(' ','').replace(',','')
        z=float(y)
        list3.append(z)

    return(max(list3))



# Function to find list of available currencies
def currency(data1):
    list2=[];
    pattern=re.compile('(sgd)|(eur)|(usd)|(chf)|(inr)')
    currency=pattern.finditer(data1)
    for match in currency:
        list2.append(match.group(0))
    x2=np.array(list2)
    y2=np.unique(x2)
    a = y2.tolist()
    return(a)



# Function to find the reference number
def find_ref(data1):
    reference = re.compile(r'ref')
    matches = reference.finditer(data1)
    start = []
    group = []
    for match in matches:
        #print(match)
        start.append(match.start())
        group.append(match.group())
    r1 = start[0] + 3
    r2 = r1 + 20
    num = []
    for i in range(len(data1[r1: r2])):
        if(data1[r1+i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            num.append(data1[r1+i])
            if(len(num) == 10):
                break
    # Correction for characters misclassified
    for j in range(len(num)):
        if(num[j] in ['(', ')', '[', ']', '{', '}','|','!','/','l', 'i']):
            num[j] = 1

        if(num[j] in ['?', 'z']):
            num[j] = 2

        if(num[j] in ['s']):
            num[j] = 5

        if(num[j] in ['b']):
            num[j] = 6

        if(num[j] in ['q']):
            num[j] = 9

        if(num[j] in ['o', 'd']):
            num[j] = 0
    ref_no = 0
    for i in range(len(num)):
        ref_no = 10*ref_no + int(num[i])
    return(ref_no)



# Function that changes the format of date to a prescribed format that is easy to process
def changeformat(str1):
    str1=str1.lower()
    inputDate=str1
    dateFormat='%d-%b-%Y'
    date= datetime.strptime(inputDate, dateFormat)
    outPutDateFormat = "%Y,%m,%d"
    y=date.strftime(outPutDateFormat )
    listdate=[]
    listdate.append(date.strftime(outPutDateFormat )[0:4])
    listdate.append(date.strftime(outPutDateFormat )[5:7])
    listdate.append(date.strftime(outPutDateFormat )[8:10])
    listndate=[]
    listndate.append(int(listdate[0]))
    listndate.append(int(listdate[1]))
    listndate.append(int(listdate[2]))
    return listndate


def datestring(data1):
    listfinal=[]
    import re
    list1=[]
    pattern=re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\s*?)[\s./-](\s*?)([1-9]|0[1-9]|1[0-2])(\s*?)[\s./-](\s*)(([1-2][(0)|(9)]\d{2})|\d{2})|([1-3]?\d(\s*?)[\s./-]?(\s*?)(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2})|((jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?,?(\s*?)\d?\d(\s*?),?[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2})')
    pattern1=re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\s*?)[\s./-](\s*?)([1-9]|0[1-9]|1[0-2])(\s*?)[\s./-](\s*)(([1-2][(0)|(9)]\d{2})|\d{2})')
    pattern2=re.compile(r'[1-3]?\d(\s*?)[\s./-]?(\s*?)(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?(\s*?)[2]?[(0)|(9)]?\d{2}')
    pattern3=re.compile(r'(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?,?(\s*?)\d?\d(\s*?),?[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2}')

    matches=pattern.finditer(data1)
    matches1=pattern1.finditer(data1)
    matches2=pattern2.finditer(data1)
    matches3=pattern3.finditer(data1)
    #adding different date formats to different lists
    list10=[]
    list11=[]
    list12=[]
    for match in matches1:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace()
        list10.append(l)
    for match in matches2:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        list11.append(l)
    for match in matches3:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        list12.append(l)
    for match in matches:
        d=match.group(0)
        #print (d)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        #print(l)
        if l in list10:
            inputDate0 = l
            DateFormat0 = '%d-%m-%Y'
            date= datetime.strptime(inputDate0 , DateFormat0 )
            outPutDateFormat = "%d-%B-%Y"
            listfinal.append(date.strftime(outPutDateFormat ))
            #print(date)
        if l in list11:
            inputDate1 = l
            DateFormat1 = "%d-%b-%Y"
            date= datetime.strptime(inputDate1 , DateFormat1 )
            outPutDateFormat = "%d-%B-%Y"
            listfinal.append(date.strftime(outPutDateFormat ))
            #print(date)
        if l in list12:
            inputDate2 =l
            DateFormat2 = "%b-%d-%Y"
            date= datetime.strptime(inputDate2 , DateFormat2 )
            outPutDateFormat = "%d-%B-%Y"
            listfinal.append(date.strftime(outPutDateFormat ))
            #print(date)
    #print(listfinal)
    
    return listfinal



# Function that takes in input a string and return three dates(Invoice, settlement and Stamp)
def givedates(data1):
    listfinal=[]
    import re
    list1=[]
    pattern=re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\s*?)[\s./-](\s*?)([1-9]|0[1-9]|1[0-2])(\s*?)[\s./-](\s*)(([1-2][(0)|(9)]\d{2})|\d{2})|([1-3]?\d(\s*?)[\s./-]?(\s*?)(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2})|((jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?,?(\s*?)\d?\d(\s*?),?[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2})')
    pattern1=re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\s*?)[\s./-](\s*?)([1-9]|0[1-9]|1[0-2])(\s*?)[\s./-](\s*)(([1-2][(0)|(9)]\d{2})|\d{2})')
    pattern2=re.compile(r'[1-3]?\d(\s*?)[\s./-]?(\s*?)(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?(\s*?)[2]?[(0)|(9)]?\d{2}')
    pattern3=re.compile(r'(jan|feb|mar|apr|may|june?|jul|aug|sep|oct|nov|dec)(\s*?)[\s./-]?,?(\s*?)\d?\d(\s*?),?[\s./-]?(\s*?)[1-2]?[(0)|(9)]?\d{2}')

    matches=pattern.finditer(data1)
    matches1=pattern1.finditer(data1)
    matches2=pattern2.finditer(data1)
    matches3=pattern3.finditer(data1)
    #adding different date formats to different lists
    list10=[]
    list11=[]
    list12=[]
    for match in matches1:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace()
        list10.append(l)
    for match in matches2:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        list11.append(l)
    for match in matches3:
        d=match.group(0)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        list12.append(l)
    for match in matches:
        d=match.group(0)
        #print (d)
        l=d.replace(' ','-').replace('.','-').replace('/','-').replace(',','-').replace('--','-').replace('--','-').replace('june','jun').replace('march','mar').replace('july','jul')
        #print(l)
        if l in list10:
            inputDate0 = l
            DateFormat0 = '%d-%m-%Y'
            date= datetime.strptime(inputDate0 , DateFormat0 )
            outPutDateFormat = "%Y,%m,%d"
            listfinal.append(date.strftime(outPutDateFormat )[0:4])
            listfinal.append(date.strftime(outPutDateFormat )[5:7])
            listfinal.append(date.strftime(outPutDateFormat )[8:10])
            #print(date)
        if l in list11:
            inputDate1 = l
            DateFormat1 = "%d-%b-%Y"
            date= datetime.strptime(inputDate1 , DateFormat1 )
            outPutDateFormat = "%Y,%m,%d"
            listfinal.append(date.strftime(outPutDateFormat )[0:4])
            listfinal.append(date.strftime(outPutDateFormat )[5:7])
            listfinal.append(date.strftime(outPutDateFormat )[8:10])
            #print(date)
        if l in list12:
            inputDate2 =l
            DateFormat2 = "%b-%d-%Y"
            date= datetime.strptime(inputDate2 , DateFormat2 )
            outPutDateFormat = "%Y,%m,%d"
            listfinal.append(date.strftime(outPutDateFormat )[0:4])
            listfinal.append(date.strftime(outPutDateFormat )[5:7])
            listfinal.append(date.strftime(outPutDateFormat )[8:10])
            #print(date)
    #print(listfinal)
    invoice=[]
    invoice.append(int(listfinal[0]))
    invoice.append(int(listfinal[1]))
    invoice.append(int(listfinal[2]))
    settlement=[]
    settlement.append(int(listfinal[3]))
    settlement.append(int(listfinal[4]))
    settlement.append(int(listfinal[5]))
    if len(listfinal)>6 :
        stamp=[]
        stamp.append(int(listfinal[-3]))
        stamp.append(int(listfinal[-2]))
        stamp.append(int(listfinal[-1]))
            
    listnew=[];
    listnew.append(invoice)
    listnew.append(settlement)
    if len(listfinal)>6 :
        listnew.append(stamp)
    return listnew
    

# Function that returns list of possible organisation names
def organisation(data):
    org_name = []
    for i in range(len(data)):
        lol = data[i]
        for f in range(len(lol)):
            dub = (" ".join(lol[f])).lower()

            reference = re.compile(r'(ltd|limited)')
            matches = reference.finditer(dub)

            start = []
            group = []
            for match in matches:
                start.append(match.start())
                group.append(match.group())

                if not start:
                    break

                ending = start[0] + len(group[0])
                firm_name = dub[0: ending]
                org_name.append(firm_name)
                break

    sub = []
    some_list = ['ltd', 'limited', 'pvtltd', 'pvt ltd', 'pvtlimited', 'pvt limited', 'privateltd',
                 'private ltd', 'privatelimited', 'private', 'limited', 'pvt', 'private']
    val_j = 0
    for i in range(len(org_name)-1):
        for j in range(i+1, len(org_name)):
            string1 = org_name[i]
            string2 = org_name[j]
            match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))

            ms = (string1[match.a: match.a + match.size]).strip(' ')
            if(ms.split(" ")[-1] in some_list):

                if(ms not in sub):
                    if(ms in some_list):
                        ()
                    else:
                        sub.append(ms)
    return(sub)