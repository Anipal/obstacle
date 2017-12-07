#!/usr/bin/env python

import sys
import rospy
import math
from gazebo_msgs.srv import *
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

def x_t(xb,xr):
	return xb-xr

def y_t(yb,yr):
	return yb-yr

def process(a,c,y):
    rospy.wait_for_service('gazebo/get_model_state')
    try:
        ob = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)	
	rospy.init_node('getModelState_and_move', anonymous=True)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
	rate = rospy.Rate(10000000)
	

	resp1 = ob(a, y)
	orientation_q = resp1.pose.orientation
       	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
       	(roll, pitch, init_yaw) = euler_from_quaternion (orientation_list)

	resp3 = ob(c, y)
	current_yaw=init_yaw


	# to turn randomly
	"""
	for tt in range(1000):
		resp1 = ob(a, y)
		orientation_q = resp1.pose.orientation
       		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
          	(roll, pitch, current_yaw) = euler_from_quaternion (orientation_list)
		print "yaw -"+str(current_yaw)
		o=Twist()
		o.linear.x=0.0
       		o.linear.y=0
       		o.linear.z=0
       		o.angular.x=0
       		o.angular.y=0
       		o.angular.z=0.2
  		pub.publish(o)
		rate.sleep()
	
	
	for x in range(50):	
		o=Twist()	
		pub.publish(o)
		rate.sleep()
	"""
	"""
	while (math.fabs(current_yaw)> 0.1):
		resp1 = ob(a, y)
		orientation_q = resp1.pose.orientation
       		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
          	(roll, pitch, current_yaw) = euler_from_quaternion (orientation_list)
		print "curretn yaw -"+str(current_yaw)
		o=Twist()
		o.linear.x=0.0
       		o.linear.y=0
       		o.linear.z=0
       		o.angular.x=0
       		o.angular.y=0
       		o.angular.z=0.01*math.fabs(current_yaw)
  		pub.publish(o)
		rate.sleep()

	for x in range(100):	
		o=Twist()	
		pub.publish(o)
		rate.sleep()

	"""
	xt=x_t(resp3.pose.position.x,resp1.pose.position.x)
	yt=y_t(resp3.pose.position.y,resp1.pose.position.y)

	print xt
	print yt
	
	#sys.exit(1)
	angl=math.atan(yt/xt)

	resp1 = ob(a, y)
	orientation_q = resp1.pose.orientation
       	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
       	(roll, pitch, current_yaw) = euler_from_quaternion (orientation_list)
	# current yaw taken

	final_yaw = current_yaw + angl
	#print "angl - " + str(angl)
	#a_diff=angl-yaw
	#print "current yaw - " + str(current_yaw)
	#print "final yaw - " + str(final_yaw)
	#sys.exit(1)
	while (math.fabs(final_yaw-current_yaw)> 0.01):
		resp1 = ob(a, y)
		orientation_q = resp1.pose.orientation
       		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
          	(roll, pitch, current_yaw) = euler_from_quaternion (orientation_list)
		#print "yaw diff - " + str(current_yaw-final_yaw)
	        #print "angl - " + str(angl)
		#a_diff=angl-yaw
		print "final yaw - " + str(final_yaw)
		print "curretn yaw -"+str(current_yaw)
		o=Twist()
       		o.angular.z=0.05*(final_yaw-current_yaw)
  		pub.publish(o)
		rate.sleep()
	print "Out" 
	"""for x in range(100):	
		o=Twist()	
		pub.publish(o)
		rate.sleep() """

	while pose_diff(resp1,resp3):
		resp1 = ob(a, y)
		#print resp1.pose.position.x
		#ex=resp3.pose.position.x-resp1.pose.position.x
		#ey=resp3.pose.position.y-resp1.pose.position.y
    		o=Twist()
		o.linear.x=0.2#*ex
    		pub.publish(o)		
		rate.sleep()

	o=Twist()	
	pub.publish(o)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def pose_diff(aa,bb):
	if math.fabs(aa.pose.position.x-bb.pose.position.x) < 0.2 and math.fabs(aa.pose.position.y-bb.pose.position.y) < 0.2:
		 return False
	else:
  		 return True



if __name__ == "__main__":
    a='mybot'
    c='cylinder'
    y='world'
    process(a,c,y)
    
