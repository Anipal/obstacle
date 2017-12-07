#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates


def callback(data):
   	rospy.loginfo("I heard\n"+ str(data.name[1])+str(data.name[2]))
    	#rospy.loginfo("\n"+ str(data.twist[1]))
    	rospy.loginfo("\n"+ str(data.pose[3].position.x))
	X = ModelStates()
	X=data
	
	talker(X)

	
	

def talker(X):
    temp = X
    f=1
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    o=Twist()
    rate = rospy.Rate(5) # 10hz
    for x in range(100) :
	 t = temp.pose[1].position.x-temp.pose[2].position.x
	 print(X.pose[1].position.x)
	 
	 print(X.pose[2].position.x)
	 print(t)
	 if t <0:
	    t=t*-1
   	 o.linear.x=0.2
         o.linear.y=0
         o.linear.z=0
         o.angular.x=0
         o.angular.y=0
         o.angular.z=0
    	 pub.publish(o)
	 f=0
	 print("f is"+ str(f))
	 rate.sleep()
    

       
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber("gazebo/model_states", ModelStates, callback)
    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.spin()

if __name__ == '__main__':
    listener()


