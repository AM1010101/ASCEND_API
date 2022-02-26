# ASCEND_API
ASCEND_API


**Please refer to Documentation.pdf**

Installation
pip install -r requirements.txt

Main api code is in app.py

Tests are in test.py



    
## Endpoint 1
/device/user_name

GET returns basic info on all devices owned by <user_name>

>Example: 
    http://54.172.7.149:8080/device/andrew_merrin

## Endpoint 2
/device/full/id

GET returns full information about a device with <id>

>Example: 
    http://54.172.7.149:8080/device/full/1

## Endpoint 3
    
device/control/id #GET
    
device/control/id {updated_parameters: updated values} #PATCH
    
GET returns controlable infomration associated with <id>
    
PATCH updates and then returns updated controlable infomration associated with <id>
    
>Example
    http://54.172.7.149:8080/device/control/2


## Endpoint 4
    
device/control/id,timeframe,attribute,data_points
    
GET returns timeseries information about <attribute> for device with <id>
 
timeframe -> month, week, day, hour, minute
    
attribute -> temp, operating_hours, analogue_in, spool_position, pressure, flow_torque, uptime, cycles, issues

    
>Example
    http://54.172.7.149:8080/device/history/1,month,temp,10
    
    

![image](https://user-images.githubusercontent.com/78210129/155620634-f4b98146-7756-406f-b898-21dbe88195c4.png)
![image](https://user-images.githubusercontent.com/78210129/155620668-0d1f9ac1-a40b-4e8b-9fe6-d4a212a7946c.png)
![image](https://user-images.githubusercontent.com/78210129/155688173-d3204057-96a4-44de-8649-d73160a1507c.png)
![image](https://user-images.githubusercontent.com/78210129/155620979-07e4f846-c709-44ed-b525-22448c6001ae.png)
