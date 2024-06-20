performance_test_msgs/PerformanceHeader header

int32 sec
uint32 nanosec
string frame_id

uint32 height 480
uint32 width 640

sensor_msgs/PointField[4] fields # x, y, z, rgb

bool    is_bigendian false
uint32  point_step 32
uint32  row_step 20480
uint8[9830400] data # row_step*height

bool is_dense true