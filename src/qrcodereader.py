#!/usr/bin/env python

# This node will perform a search pattern
# 
# Author : Ananthakrishnan U S

import roslib
# ardrone_tutorials has a good ardrone classs for controlling drone. load_manifest import that python module
#roslib.load_manifest("ardrone_control")

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import String
from visualization_msgs.msg import Marker
#from drone_controller import BasicDroneController
import time
from sensor_msgs.msg import Image
from sys import argv
import zbar
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy
import Image as Image2
from rospy.numpy_msg import numpy_msg
from qrcode_zbar.msg import qrcode

def image_callback(msg):
	cv_image = bridge.imgmsg_to_cv2(msg, "mono8")
		
	pil = Image2.fromarray(cv_image)

	width, height = pil.size
	raw = pil.tobytes()
	images = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(images)

	# extract results
	for symbol in images:
		# do something useful with results
		#print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		data = qrcode()
		data.qrcode = symbol.data
		data.header.stamp = rospy.Time.now()
		pub1.publish(data)

	# clean up
	del(images)


if __name__ == '__main__':
	#rospy.init_node('qrcode_reader', anonymous=True)
	#
	rospy.init_node('image_listener')


	scanner = zbar.ImageScanner()
	bridge = CvBridge()	

	# configure the reader
	scanner.parse_config('enable')

	# Define your image topic
	image_topic = "/ardrone/image_raw"
	
	# Set up your subscriber and define its callback
	rospy.Subscriber(image_topic, Image, image_callback)
	pub1 = rospy.Publisher('/qr_code', qrcode, queue_size=10)
	# Spin until ctrl + c
	
	rospy.spin()
	


