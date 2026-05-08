## multi class classification using a MLP (fully connected )

one hot encoding 
output layer has n nodes 
n-> numberof classes 
sigmoid on each unit returning probability

we need summation of all nodes to be 1
as all of them represents prob

Perform softmax over the outputs / logits 


[o1 o2 o3] -------->  [p1 p2 p3]
            softmax


### how does softmax works ?

### how to decide what class is the answer?
[0.3 0.3 0.4]
a   b    c

c is the answer


we can skip softmax...
and directly say the answer.. if we take argmax matrix O 
l(y,y^) -> y= groud truth
        y^ -> prediction


## backprop (maybe)
 ### how to compute the gradients?
 ### propagate backwords 
 univariate chain rule 
 basic chain rule from calc
 z=wx + b 
 y = sigmoid(z)
 L= .5 (y-t)^2
 we would find gradients respect to w and b
 :(
    backprop started . i am lost .
