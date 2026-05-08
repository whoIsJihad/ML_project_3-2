### Premise 
many devices share one meduim
### Goal    
avoid two people talking at once

### Two main strategies:
-Static allocation
-Dynamic allocation

### Static allocation
each device is given a fixed piece of channel permanently
it might be 
- one frequence( like FM station)
- one time slot in a repeating frame
- one code (CDMA)

#### PRO:    
- 1. No Collision Possible (scheduled, exclusive)
- 2. Simple to reason about
#### Cons:
-  Inefficient Use of Resources
    - Idle devices hold channel capacity
    - Wasted capacity when no data to send
-  Hard to scale with bursty traffic
### Pure ALOHA
- Rule: send whenever you have data. Dont wait. Dont listen.
#### If collision happens :
- both senders dont get ack
- each waits a random time
- then tries again
#### Why random wait?
- prevents repeat collision among same nodes
- if they both backoff at the same time and for the same period, then they will collide forever 

#### There is another issue. 
For transmitting a single packet that takes t time, we need dead silence for atleast 2*t in the entire network. cause overlapping for even a small amount can cause a lot of data loss

### Slotted ALOHA
By forcing everyone to start sending at discrete start intervals , 
we can remove the overlapping issues easily.

- In pure ALOHA , frames could overlap by 10 , 20, 32 , 99 percent .
- In slotted ALOHA , frames could overlap either 100 percent or 0 percent
- Vulnearble period in pure ALOHA is 2*t 
- Vulnerable period in slotted ALOHA is t

### CSMA ( carrier sense multiple access )
It is a bit different than ALOHA. In the sense that in ALOHA we dont wait for anything to complete. When the sender has data to send , it justs sends it. It doesnt wait. If someone was already sending the data , collision happens.
In CSMA, senders act like gentleman. It first listens if someone else was already sending  or not. If someone was already sending,it stops and waits .
