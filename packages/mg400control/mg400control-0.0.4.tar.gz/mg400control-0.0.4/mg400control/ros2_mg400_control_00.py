import sys
import rclpy
from rclpy.node import Node

from mg400_msgs.msg import *

from mg400_msgs.srv import *
from rclpy.executors import ExternalShutdownException


from rclpy.action import ActionClient
from mg400_msgs.action import *
from mg400_msgs.action import *

import math
import time

# def main(args=None):
#     enable()

######service

def emergency_stop(args=None):
    rclpy.init(args=args)
    node = Node('emergency_stop')
    emergency_stop_client = node.create_client(EmergencyStop, '/mg400/emergency_stop')

    if not emergency_stop_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('emergency_stop service not available, waiting again...')
        return False

    request = EmergencyStop.Request()
    future = emergency_stop_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        if response is None:
            node.get_logger().error('Received no response from emergency_stop service.')
            return False
        node.get_logger().info(f"emergency_stop response: {response}")
        return response
        # return True
    except Exception as e:
        node.get_logger().error(f"emergency_stop service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()

def clear_error(args=None):
    rclpy.init(args=args)
    node = Node('clear_error')
    clear_error_client = node.create_client(ClearError, '/mg400/clear_error')

    if not clear_error_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('clear_error service not available, waiting again...')
        return False

    request = ClearError.Request()
    future = clear_error_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        if response is None:
            node.get_logger().error('Received no response from clear_error service.')
            return False
        node.get_logger().info(f"Clear error response: {response}")
        return response
        # return True
    except Exception as e:
        node.get_logger().error(f"Clear error service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()




def enable_robot(args=None):
    rclpy.init(args=args)
    # node = Node('enable_robot_client')
    #Node('Node_name)
    node = Node('enable_robot_client')
    #add_two_ints = node.create_client(servicetype, 'service name')
    client = node.create_client(EnableRobot, '/mg400/enable_robot')

    while not client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('service not available, waiting again...')

    req = EnableRobot.Request()
    future = client.call_async(req)

    rclpy.spin_until_future_complete(node, future)
    try:
        response = future.result()
        if response is None:
            node.get_logger().error('Received no response from enable_robot service.')
            return False
        node.get_logger().info(f"Enable robot response: {response}")
        return response
    except Exception as e:
        node.get_logger().error(f"Service call failed: {e}")

    finally:
        node.destroy_node()
        rclpy.shutdown()


def disable_robot():
    rclpy.init()
    node = Node('disable_robot_client')
    disable_robot_client = node.create_client(DisableRobot, '/mg400/disable_robot')

    if not disable_robot_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('disable_robot service not available, waiting again...')
        return False

    request = DisableRobot.Request()
    future = disable_robot_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()

        if response is None:
            node.get_logger().error('Received no response from disable_robot service.')
            return False
        node.get_logger().info(f"Disable robot response: {response}")

        return response
        # return True
    except Exception as e:
        node.get_logger().error(f"Disable robot service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()



def speed_factor(ratio):
    rclpy.init()

    node = Node('mg400_speed_factor_client')
    service_name = '/mg400/speed_factor'

    # Create a service client using the node's create_client method
    service_client = node.create_client(SpeedFactor, service_name)

    if not service_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('service not available, waiting again...')
        return False

    request = SpeedFactor.Request()
    request.ratio = ratio

    future = service_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()

        if response is None:
            node.get_logger().error('Received no response from speed_factor service.')
            return False
        node.get_logger().info(f"Set speed response: {response}")
        return response
    
        # return True
    except Exception as e:
        node.get_logger().error(f"Service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()

def do(index, status):
    rclpy.init()

    node = Node('mg400_do_client')
    do_client = Node.create_client(node,DO, '/mg400/do')

    if not do_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('do_execute service not available, waiting again...')
        return False

    request = DO.Request()
    request.index = DOIndex()  # Create an instance of ToolDOIndex
    request.index.index = index  # Set the value of the index
    request.status= DOStatus() 
    request.status.status = status

    future = do_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
 
    try:
        response = future.result()

        if response is None:
            node.get_logger().error('Received no response from d0 service.')
            return False
        node.get_logger().info(f"Tool DO Execute service response: {response}")
        return response
    except Exception as e:
        node.get_logger().error(f"Tool DO Execute service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()


def di(index):
    rclpy.init()

    node = Node('tool_di_execute_client')
    di_client = Node.create_client(node,DI, '/mg400/di')

    if not di_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('di_execute service not available, waiting again...')
        return False

    request = DI.Request()
    request.index = DIIndex()  # Create an instance of ToolDOIndex
    request.index.index = index  # Set the value of the index
    

    future = di_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
 
    try:
        response = future.result()

        if response is None:
            node.get_logger().error('Received no response from di service.')
            return False
        
        node.get_logger().info(f"Tool DI Execute service response: {response}")
        return response
    except Exception as e:
        node.get_logger().error(f"Tool DI Execute service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()






def tool_do_execute(index,status):
    rclpy.init()

    node = Node('mg400_tool_do_execute_client')
    service_name = '/mg400/tool_do_execute'

    # Create a service client using the node's create_client method
    service_client = node.create_client(ToolDOExecute, service_name)

    if not service_client.wait_for_service(timeout_sec=5.0):
        node.get_logger().info('service not available, waiting again...')
        return False

    request = ToolDOExecute.Request()
    request.index = index
    request.status = status

    future = service_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        if response is None:
            node.get_logger().error('Received no response from tool_do_execute service.')
            return False

        node.get_logger().info(f"Set DO response: {response}")
        return response  # Return the response object instead of True
        # return True
    except Exception as e:
        node.get_logger().error(f"Service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()


def get_pose():
    rclpy.init()
    node = Node('get_pose')
    get_pose_client = node.create_client(GetPose, '/mg400/get_pose')
    if not get_pose_client.wait_for_service(timeout_sec=10.0):
        node.get_logger().info('get_pose service not available, waiting again...')
        return False

    request = GetPose.Request()
    future = get_pose_client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()

        if response is None:
            node.get_logger().error('Received no response from get_pose service.')
            return False
    
        node.get_logger().info(f"get_pose response: {response}")

          # Log specific poses for confirmation
        node.get_logger().info(f"pose1 = {response.pose1}")
        node.get_logger().info(f"pose2 = {response.pose2}")
        node.get_logger().info(f"pose3 = {response.pose3}")
        node.get_logger().info(f"pose4 = {response.pose4}")
        node.get_logger().info(f"pose5 = {response.pose5}")
        node.get_logger().info(f"pose6 = {response.pose6}")



        # Return the entire response object containing pose1, pose2, etc.
        return response  # Return the response object instead of True
    
    except Exception as e:
        node.get_logger().error(f"get_pose service call failed: {e}")
        return False

    finally:
        node.destroy_node()
        rclpy.shutdown()

    
def Mov_J(position_x, position_y, position_z, r):
    rclpy.init()
    node = Node('mg400_controller')
    
    mov_j_action_client = ActionClient(node, MovJ, 'mg400/mov_j')

    if not mov_j_action_client.wait_for_server(timeout_sec=10.0):
        node.get_logger().info('MovL action server not available, waiting...')
        return False

    # Convert rotation degree to quaternion for orientation
    orientation_z, orientation_w = degree_to_quaternion_z_w(r)

    # Create and populate the goal message
    goal_msg = MovJ.Goal()
    goal_msg.pose.header.frame_id = 'mg400_end_effector_flange'

    # goal_msg.pose.header.frame_id = 'mg400_origin_link'
    goal_msg.pose.pose.position.x = position_x
    goal_msg.pose.pose.position.y = position_y
    goal_msg.pose.pose.position.z = position_z
    goal_msg.pose.pose.orientation.z = orientation_z
    goal_msg.pose.pose.orientation.w = orientation_w

    # Send goal and wait for the result
    future = mov_j_action_client.send_goal_async(goal_msg)
    rclpy.spin_until_future_complete(node, future)
    
    try:
        response = future.result()
        
        if not response.accepted:
            node.get_logger().error('MovJ action was not accepted')
            return False
        
        # Wait for the result (blocking until movement is complete)
        result_future = response.get_result_async()
        rclpy.spin_until_future_complete(node, result_future)
        
        result = result_future.result()
        node.get_logger().info(f"MovJ action completed: {result}")
        
        return result
        
    except Exception as e:
        node.get_logger().error(f"Action call failed: {e}")
        return False
    
    finally:
        # Ensure the node is destroyed and rclpy is shut down
        node.destroy_node()
        rclpy.shutdown()




def Mov_L(position_x, position_y, position_z, r):
    rclpy.init()
    node = Node('mg400_controller')
    
    mov_l_action_client = ActionClient(node, MovL, '/mg400/mov_l')

    if not mov_l_action_client.wait_for_server(timeout_sec=10.0):
        node.get_logger().info('MovL action server not available, waiting...')
        return False

    # Convert rotation degree to quaternion for orientation
    orientation_z, orientation_w = degree_to_quaternion_z_w(r)

    # Create and populate the goal message
    goal_msg = MovL.Goal()
    goal_msg.pose.header.frame_id = 'mg400_origin_link'
    goal_msg.pose.pose.position.x = position_x
    goal_msg.pose.pose.position.y = position_y
    goal_msg.pose.pose.position.z = position_z
    goal_msg.pose.pose.orientation.z = orientation_z
    goal_msg.pose.pose.orientation.w = orientation_w

    # Send goal and wait for the result
    future = mov_l_action_client.send_goal_async(goal_msg)
    rclpy.spin_until_future_complete(node, future)
    
    try:
        response = future.result()
        
        if not response.accepted:
            node.get_logger().error('MovL action was not accepted')
            return False
        
        # Wait for the result (blocking until movement is complete)
        result_future = response.get_result_async()
        rclpy.spin_until_future_complete(node, result_future)
        
        result = result_future.result()
        node.get_logger().info(f"MovL action completed: {result}")
        # time.sleep(0.5)
        return result
        
    except Exception as e:
        node.get_logger().error(f"Action call failed: {e}")
        return False
    
    finally:
        # Ensure the node is destroyed and rclpy is shut down
        node.destroy_node()
        rclpy.shutdown()
#######################


def degree_to_quaternion_z_w(degree):
    # Convert the angle from degrees to radians
    theta_rad = math.radians(degree)
    
    # Compute the quaternion components for a Z-axis rotation
    z = math.sin(theta_rad / 2)
    w = math.cos(theta_rad / 2)
    
    return z, w

# # Example usage
# r = 100.345  # Roll angle in degrees
# z, w = degree_to_quaternion_z_w(r)
# print(f"For r = {r} degrees, quaternion components are z = {z}, w = {w}")



# if __name__ == '__main__':
#     main()




################

# if __name__ == '__main__':
#     main()









# if __name__ == '__main__':
#     result = do(1, 0)  # Replace 1 and 0 with your desired values

#     if result:
#         print("Tool DO Execute service call successful")
#         print("Result:", result)
#     else:
#         print("Tool DO Execute service call failed")