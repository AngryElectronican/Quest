from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Kvest
import playsound
import threading
import os

quests={'Kvest1':[0,0,0,0,0,0],
        'Kvest2':[0,0,0,0,0,0],
        'Kvest3':[0,0,0,0,0,0],
        'Kvest4':[0,0,0,0,0,0],
        'Kvest5':[0,0,0,0,0,0],
}
QUESTS_NUM=5
ENIGMAS_NUM=6
def play(name,zagadka):
    PATH_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(PATH_ROOT)
    KVEST_DIR=PATH_ROOT+'/static/sound/'+name+'/'
    file_list=os.listdir(KVEST_DIR)
    
    for media in filter(lambda x: x.startswith(zagadka), file_list):
        neded_file=media.encode('cp1251') 

    playsound.playsound(KVEST_DIR+neded_file.decode('cp1251'),True)

def calc_status(quest_status,ESP_status):
    if(ESP_status==-1):
        return quest_status
    else:
        return ESP_status

def request(request):               # Запрос от ЕСП
    if request.method=="GET":
        quest_name=request.GET["name"]
        zagadka=int(request.GET["zagadka"])-1
        status=int(request.GET["status"])
        #quest=Kvest.objects.get(name=quest_name)
        data=[]
        quests[quest_name][zagadka]=calc_status(quests[quest_name][zagadka],status)
        data.append(quests[quest_name][zagadka])
        if (status==2):
            th=threading.Thread(target=play,args=(quest_name,request.GET["zagadka"],))
            th.start()
        print("quest_name={} zagadka={} status={}".format(quest_name,zagadka+1,status))
        return JsonResponse({quest_name:data})

def status_to_text(status):
    text=["Не активно","В работе","Завершено"]
    if(status==0):              #проверка начальных состояний
        return text[0]
    elif(status==1):
        return text[1]
    else:
        return text[2]

def interface(request):

#########################################################################################
#################################### AJAX ###############################################
#########################################################################################
    if request.is_ajax():                   # по аяксу
        print(request.POST)
        data_ajax=[]

        if ('start' in request.POST):
            for i in range(QUESTS_NUM):
                for j in range(ENIGMAS_NUM):
                    quests['Kvest'+str(i+1)][j]=1

        elif ('hard_reset' in request.POST):
            for i in range(QUESTS_NUM):
                for j in range(ENIGMAS_NUM):
                    quests['Kvest'+str(i+1)][j]=0


        for i in range(QUESTS_NUM):# по кнопкам "Завершить"
            for j in range(ENIGMAS_NUM):
                if('z'+str(i+1)+str(j+1) in request.POST):
                    print('z'+str(i+1)+str(j+1))
                    quests['Kvest'+str(i+1)][j]=2
                    th=threading.Thread(target=play,args=("Kvest"+str(i+1),str(j+1)))
                    th.start()

        for i in range(QUESTS_NUM):# по кнопкам "Перезагрузить"
           for j in range(ENIGMAS_NUM):
                if('r'+str(i+1)+str(j+1) in request.POST):
                    print('r'+str(i+1)+str(j+1))
                    quests['Kvest'+str(i+1)][j]=1
        
        for i in range(QUESTS_NUM):
            data_ajax.append(quests['Kvest'+str(i+1)])

        print(data_ajax)
        #print("is ajax")
        return HttpResponse(data_ajax)
#########################################################################################
#################################### GET REQUEST ########################################
#########################################################################################
    elif request.method=="GET":             # при переходе на страницу
        print(os.environ)
        print(os.path.exists("/static/jquery-3.3.1.js"))

        status_all=[]
        colour_all=[]

        for i in range(QUESTS_NUM):
            status_i=[]
            colour_i=[]
            
            for j in range(ENIGMAS_NUM):
                status_i.append(quests['Kvest'+str(i+1)][j])
                if quests['Kvest'+str(i+1)][j]==0:
                    colour_i.append("rgb(192,192,192)")
                elif quests['Kvest'+str(i+1)][j]==1:
                    colour_i.append("rgb(23,102,255)")
                elif quests['Kvest'+str(i+1)][j]==2:
                    colour_i.append("rgb(114,242,36)")

            status_all.append(status_i)
            colour_all.append(colour_i)

        return render(request,"str.html",{
            "status1":status_all[0],"colour1":colour_all[0],
            "status2":status_all[1],"colour2":colour_all[1],
            "status3":status_all[2],"colour3":colour_all[2],
            "status4":status_all[3],"colour4":colour_all[3],
            "status5":status_all[4],"colour5":colour_all[4],
        })
#########################################################################################
#################################### POST_REQUEST #######################################
#########################################################################################
'''    elif request.method=='POST':            # по кнопкам

        if ('start' in request.POST):
            for i in range(6):
                for j in range(6):
                    quests['Kvest'+str(i+1)][j]=1

        elif ('hard_reset' in request.POST):
            for i in range(6):
                for j in range(6):
                    quests['Kvest'+str(i+1)][j]=0


        for i in range(6):# по кнопкам "Завершить"
            for j in range(6):
                if('z'+str(i+1)+str(j+1) in request.POST):
                    print('z'+str(i+1)+str(j+1))
                    quests['Kvest'+str(i+1)][j]=2
                    th=threading.Thread(target=play,args=("tink.mp3",))
                    th.start()

        for i in range(6):# по кнопкам "Перезагрузить"
           for j in range(6):
                if('r'+str(i+1)+str(j+1) in request.POST):
                    print('r'+str(i+1)+str(j+1))
                    quests['Kvest'+str(i+1)][j]=1

        #for i in range(6):
        #    quests[i].save()

        status_all=[]
        colour_all=[]

        for i in range(6):
            status_i=[]
            colour_i=[]
            
            for j in range(6):
                status_i.append(quests['Kvest'+str(i+1)][j])
                if quests['Kvest'+str(i+1)][j]==0:
                    colour_i.append("rgb(192,192,192)")
                elif quests['Kvest'+str(i+1)][j]==1:
                    colour_i.append("rgb(23,102,255)")
                elif quests['Kvest'+str(i+1)][j]==2:
                    colour_i.append("rgb(114,242,36)")

            status_all.append(status_i)
            colour_all.append(colour_i)

        return render(request,"str.html",{
            "status1":status_all[0],"colour1":colour_all[0],
            "status2":status_all[1],"colour2":colour_all[1],
            "status3":status_all[2],"colour3":colour_all[2],
            "status4":status_all[3],"colour4":colour_all[3],
            "status5":status_all[4],"colour5":colour_all[4],
            "status6":status_all[5],"colour6":colour_all[5],
        })
# Create your views here.
'''