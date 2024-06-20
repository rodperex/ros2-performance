performance_test_msgs/PerformanceHeader header

# This message contains an uncompressed image
# (0, 0) is at top-left corner of image

int32 sec
uint32 nanosec
string frame_id "camera_frame"
                        
uint32 height 480
uint32 width 640

string encoding "bgr8"

uint8 is_bigendian 0
uint32 step 1920
uint8[921600] data # step*height