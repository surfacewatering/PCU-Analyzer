from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Cookie, Depends
from starlette.responses import RedirectResponse, Response
import csv
from fastapi import FastAPI, File, UploadFile
import pandas as pd
from matplotlib import pyplot as plt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def check(request: Request, file: UploadFile = File(...),file2:UploadFile=File(...)):
    try:
        db = pd.read_csv(file.file)
        fields=[]
        rows=[]

        cnt=1
        for i in range(len(list(db.Entry))):
            rows.append([cnt,list(db.Lane)[i],list(db.Type)[i],list(db.Entry)[i],list(db.Exit)[i],list(db.Time)[i]])
            cnt+=1

        speed=[]

        for i in rows:
            speed.append((62*18)/(5*float(i[5])))

        entryflow = [0 for i in range(87)]
        exitflow = [0 for i in range(87)]
        totaltime = [0 for i in range(87)]

        smallcarNO = [0 for i in range(87)]
        bigcarNO = [0 for i in range(87)]
        twowheelerNO = [0 for i in range(87)]
        lcvNO = [0 for i in range(87)]
        busNO = [0 for i in range(87)]
        singleaxleNO = [0 for i in range(87)]
        multiaxleNO = [0 for i in range(87)]

        smallcarSPEED = [0 for i in range(87)]
        bigcarSPEED = [0 for i in range(87)]
        twowheelerSPEED = [0 for i in range(87)]
        lcvSPEED = [0 for i in range(87)]
        busSPEED = [0 for i in range(87)]
        singleaxleSPEED = [0 for i in range(87)]
        multiaxleSPEED = [0 for i in range(87)]

        for i in rows:
            entry=int(float(i[3])//300)
            exit=int(float(i[4])//300)
            time=float(i[5])
            entryflow[entry]+=1
            exitflow[exit]+=1
            totaltime[exit]+=time

            if(i[2]==1):
                smallcarNO[exit]+=1
            elif(i[2]==2):
                bigcarNO[exit]+=1
            elif(i[2]==3):
                twowheelerNO[exit]+=1
            elif(i[2]==4):
                lcvNO[exit]+=1
            elif(i[2]==5):
                busNO[exit]+=1
            elif(i[2]==6):
                singleaxleNO[exit]+=1
            else:
                multiaxleNO[exit]+=1

            if(i[2]==1):
                smallcarSPEED[exit]+=speed[int(i[0])-1]
            elif(i[2]==2):
                bigcarSPEED[exit]+=speed[int(i[0])-1]
            elif(i[2]==3):
                twowheelerSPEED[exit]+=speed[int(i[0])-1]
            elif(i[2]==4):
                lcvSPEED[exit]+=speed[int(i[0])-1]
            elif(i[2]==5):
                busSPEED[exit]+=speed[int(i[0])-1]
            elif(i[2]==6):
                singleaxleSPEED[exit]+=speed[int(i[0])-1]
            else:
                multiaxleSPEED[exit]+=speed[int(i[0])-1]

        averagetime=[]
        sms=[]

        for i in range(87):
            averagetime.append(totaltime[i]/exitflow[i])
            sms.append((62/averagetime[i])*3.6)


        smallcarAvSPEED = [(0 if smallcarNO[i]==0 else smallcarSPEED[i]/smallcarNO[i]) for i in range(87)]
        bigcarAvSPEED = [(0 if bigcarNO[i]==0 else bigcarSPEED[i]/bigcarNO[i]) for i in range(87)]
        twowheelerAvSPEED = [(0 if twowheelerNO[i]==0 else twowheelerSPEED[i]/twowheelerNO[i]) for i in range(87)]
        lcvAvSPEED = [(0 if lcvNO[i]==0 else lcvSPEED[i]/lcvNO[i]) for i in range(87)]
        busAvSPEED = [(0 if busNO[i]==0 else busSPEED[i]/busNO[i]) for i in range(87)]
        singleaxleAvSPEED = [(0 if singleaxleNO[i]==0 else singleaxleSPEED[i]/singleaxleNO[i]) for i in range(87)]
        multiaxleAvSPEED = [(0 if multiaxleNO[i]==0 else multiaxleSPEED[i]/multiaxleNO[i]) for i in range(87)]
        
        area={
            
        }

        db1 = pd.read_csv(file2.file)

        for i in range(len(list(db1.Type))):
            area[list(db1.Vehicle)[i]]=float(list(db1.Area)[i])

        smallcarIndiPCU = [(0 if smallcarAvSPEED[i]==0 else (smallcarAvSPEED[i]/smallcarAvSPEED[i])/(area['smallcar']/area['smallcar'])) for i in range(87)]
        bigcarIndiPCU = [(0 if bigcarAvSPEED[i]==0 else (smallcarAvSPEED[i]/bigcarAvSPEED[i])/(area['smallcar']/area['bigcar'])) for i in range(87)]
        twowheelerIndiPCU = [(0 if twowheelerAvSPEED[i]==0 else (smallcarAvSPEED[i]/twowheelerAvSPEED[i])/(area['smallcar']/area['twowheeler'])) for i in range(87)]
        lcvIndiPCU = [(0 if lcvAvSPEED[i]==0 else (smallcarAvSPEED[i]/lcvAvSPEED[i])/(area['smallcar']/area['lcv'])) for i in range(87)]
        busIndiPCU = [(0 if busAvSPEED[i]==0 else (smallcarAvSPEED[i]/busAvSPEED[i])/(area['smallcar']/area['bus'])) for i in range(87)]
        singleaxleIndiPCU = [(0 if singleaxleAvSPEED[i]==0 else (smallcarAvSPEED[i]/singleaxleAvSPEED[i])/(area['smallcar']/area['singleaxle'])) for i in range(87)]
        multiaxleIndiPCU = [(0 if multiaxleAvSPEED[i]==0 else (smallcarAvSPEED[i]/multiaxleAvSPEED[i])/(area['smallcar']/area['multiaxle'])) for i in range(87)]

        PCUper5min=[]

        for i in range(87):
            PCUper5min.append(  smallcarIndiPCU[i]*smallcarNO[i]+
                                bigcarIndiPCU[i]*bigcarNO[i]+
                                twowheelerIndiPCU[i]*twowheelerNO[i]+
                                lcvIndiPCU[i]*lcvNO[i]+
                                busIndiPCU[i]*busNO[i]+
                                singleaxleIndiPCU[i]*singleaxleNO[i]+
                                multiaxleIndiPCU[i]*multiaxleNO[i])

        PCUperHr=[PCUper5min[i]*12 for i in range(87)]
        FLOWinVehperHr=[exitflow[i]*60 for i in range(87)]
        Density=[PCUperHr[i]/sms[i] for i in range(87)]

        FinalValues = [[str(PCUper5min[i]), str(PCUperHr[i]), str(sms[i]), str(Density[i]), str(FLOWinVehperHr[i]), 300+300*i] for i in range(87)]
        OutputFields = ['PCU/5min', 'Total PCU/Hr', 'SMS', 'Density', 'Flow in Veh/hr', 'Time Interval']
        OutputFile='output.csv'

        with open(OutputFile, 'w', newline='') as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow(OutputFields)
            csvwriter.writerows(FinalValues)
        
        def q(k):
            return 150*k-(150*k*k)/300

        x = [i for i in range(300)]
        plt.xlabel("Density in veh/km")
        plt.ylabel("Flow in veh/hr")
        plt.plot(x, [q(k) for k in x], color='red')
        plt.scatter(Density, FLOWinVehperHr, color='blue')
        plt.savefig("static/q-k.png")

        print("200 OK")
        return templates.TemplateResponse("index.html", {"request": request, "result": FinalValues})
    except:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
