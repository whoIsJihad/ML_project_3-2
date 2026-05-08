message wqueing temlemetry transporit
\lightwieght mesaging protocol d3esigned for 
low bandwidth
usntable snetworiks 
low poer devices s
small memory requiremnets 
perfect for IOT
a lot less overhead 
lightweight and efficient
control / monitoring er jonno concise message 
hightly scalable
low power consumption
jara publish kortce and jara subscribe kortce tara connected na

Limitation
MQTT broker single piont of failure 
broker jodi nosto hoye jay -> system gone.
why it existes?
imagein 10000 sensors 
low batter
tinym microcontrollers 
asnc
publish / subscribe based 

mqtt architecture uses a broker based publish subscribe model 
there are three components 
publicsh 
broker
subscriber 


a device publishes a message to a topic 
the borker receivers it
anyone subscribed to that topic receives it

the publisher and the subscriber doesnt know each other 
this decoupling is poiewrful

example
esp32 sends temperature 
mobile app reads temperature
 

esp32 -> publish -> topic: home/livingroom/temp
broker -> forwards 
mobile app -> subscribed to home/livingromm/temp gets the data 
do direct communication between esp32 and mobiel 

core concepts 

topic: 
a hierarchical string
 
 it is like a routing label
 QOS
 quality of service

mqtt supports 3 reliability levels 

qos     guarantee
0       NO guarantee
1       might duplicate
2       guaranteed delivery


QoS
how sure you want to be that the message arrives 
thats it


QoS 0
jst send it
no confirmation
no retry
fire and forget

if it gets lost -> gone


Qos 1
make sure it arrives at least once 
broker sends acknowledge 
if no ack -> sender retries 