#! /usr/bin/env python3

# The following base code was found here at:
# https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/

# Author of base starting code :
# - Addison Sears-Collins
# - https://automaticaddison.com

# The addition of face detection was added
# Author of modified code addition:
# - David Metcalf
# - no web site.



# A basic ROS 2 program for publishing real-time streaming 
# video from your built-in webcam then apply face detection 
# to that incoming video.


# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
 
class ImagePublisher(Node):
	#Create an ImagePublisher class, which is a subclass of the Node class.
	def __init__(self):
		#Class constructor to set up the node
			
		# Initiate the Node class's constructor and give it a name
		super().__init__('image_publisher')
			
		# Create the publisher. This publisher will publish an Image
		# to the video_frames topic. The queue size is 10 messages.
		topic_name = 'video_frames'
		self.publisher_ = self.create_publisher(Image,topic_name, 10)
			
		# We will publish a message every 0.1 seconds
		timer_period = 0.1  # seconds
			
		# Create the timer
		self.timer = self.create_timer(timer_period, self.timer_callback)
			
		# Create a VideoCapture object
		# The argument '0' gets the default webcam.
		self.cap = cv2.VideoCapture(0)
		
		self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 
		self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml') 
		self.profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
			
		# Used to convert between ROS and OpenCV images
		self.br = CvBridge()
			
	def timer_callback(self):
		#Callback function.
		#This function gets called every 0.1 seconds.
		
		# Capture frame-by-frame
		# This method returns True/False as well
		# as the video frame.
		ret, img = self.cap.read()
		
		if ret == True:
			# If an image can be captured, then apply cv2 
			# face end eye detection. Then Publish the image.
			# The 'cv2_to_imgmsg' method converts an OpenCV
			# image to a ROS 2 image message
			
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			profile = self.profile_cascade.detectMultiScale(gray, 1.3, 5)
			for (x, y, w, h) in profile:
				cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
				
			#Detect the presence of eyes.
			#Colours are defined as 3 values of (blue,green,red) eg (255, 0, 0 ) = blue
			
			faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
			for (x, y, w, h) in faces:
				cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
				self.get_logger().info("Found: Face at [X: "+str(x)+"] [Y: "+str(y)+"]")# Print out to user.
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = img[y:y+h, x:x+w]
				eyes = self.eye_cascade.detectMultiScale(roi_gray)
				
				for (ex, ey, ew, eh) in eyes:
					#cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
					#rectangle(image, start_point, end_point, color, thickness)
					#circle(image, center_coordinates, radius, color, thickness)
				
					ecx =int(ex+(ew/2)+x)
					ecy =int(ey+(eh/2)+y)
					#cv2.circle(img, (ecx, ecy), (2), (0, 0, 255), 5) # Toggle me to view
					cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2) # Toggle me to view
					#self.get_logger().info("eye height: "+str(eh)+" eye width: "+str(ew))# Print out to user.
					#self.get_logger().info("eye center x: "+str(ecx)+" eye center y: "+str(ecy))# Print out to user.
					self.get_logger().info("Found: Eye at [X: "+str(x)+"] [Y: "+str(y)+"]")# Print out to user.
				
		self.publisher_.publish(self.br.cv2_to_imgmsg(img))
				
		# Display the message on the console
		self.get_logger().info('Publishing video frame')
			
def main(args=None):
	# Initialize the rclpy library
	rclpy.init(args=args)
			
	# Create the node
	image_publisher = ImagePublisher()
			
	# Spin the node so the callback function is called.
	rclpy.spin(image_publisher)
			
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	image_publisher.destroy_node()
			
	# Shutdown the ROS client library for Python
	rclpy.shutdown()
  
if __name__ == '__main__':
	main()
