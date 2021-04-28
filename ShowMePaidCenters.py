import time
import json
from plyer import notification
import requests
import sys
from datetime import datetime


#298 Kollam
#300 Pathanamthitta 
#301 Alappuzha
#307 Ernakulam
#304 Kottayam
#296 Thiruvananthapuram

#Change the following
distcode = '304'
dateforvaccine = '29-04-2021'
pincode0 = 686501 #685582
pincode1 = 686630 #686540 #685582
#pincode2 = 686001 #685582

never_get_me_blocked_timer = 15
jsonurl =  "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+distcode+"&date="+dateforvaccine

def saveMeSomeTimeLoop():
        print ( "fetching...")
        while True:
                time.sleep(never_get_me_blocked_timer)
                responseJson = requests.get(jsonurl)
                if responseJson.status_code != 200:
                        print ("API MISBEHAVING")
                else:
                        responseJson = json.loads(responseJson.text)
                        if( len(responseJson['centers']) == 0 ):
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S, %d/%m/%Y")
                                print("No centers for Kottayam, polled at ", current_time)
                                saveMeSomeTimeLoop()
                                break
                        else :
                            for center in responseJson['centers']:
                                    #(center['pincode'] >= pincode0 and center['pincode'] <= pincode1) and )  :
                                    if ( center['fee_type'] == 'Paid') :
                                            file1 = open("report18To45.txt", "a")  # append mode
                                            now = datetime.now()
                                            current_time = now.strftime("%H:%M:%S, %d/%m/%Y")
                                            print("{center} with pincode {pincode} which is {paid} available at {time}\n DETAILS:".format(center = center['name'], pincode = center['pincode'], time = current_time, paid = center['fee_type']))
                                            # Append-adds at last
                                            file1.write("{center} with pincode {pincode} which is {paid} available at {time}\n DETAILS:".format(center = center['name'], pincode = center['pincode'], time = current_time, paid = center['fee_type']))
                                            for session in center['sessions']:
                                                    file1.write("     {date} has {count} seats. \n".format(date = session['date'], count = session['available_capacity']))
                                            file1.close()
                                            notification.notify(
                                            title = "Paid {center} is Available!".format(center = center['name']),
                                            message = "{pincode} pincode at Kottayam!".format(pincode = center['pincode']),
                                            timeout  = 50
                                            )
                                    else :
                                            file1 = open("report18To45Kak.txt", "a")
                                            now = datetime.now()
                                            current_time = now.strftime("%H:%M:%S, %d/%m/%Y")
                                            print("No paid centers for Kottayam, polled at ", current_time)
                                            # Append-adds at last
                                            file1.write("{center} with {pincode} which is {paid} at {time}\n".format(center = center['name'], pincode = center['pincode'], time = current_time,paid = center['fee_type']))
                                            for session in center['sessions']:
                                                    file1.write("     {date} has {count} seats. \n".format(date = session['date'], count = session['available_capacity']))
                                            file1.close()
                                            #saveMeSomeTimeLoop()
saveMeSomeTimeLoop()
