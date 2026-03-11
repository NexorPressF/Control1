#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class DistanceSensor(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        
        # Параметры
        self.distance = 3.0  # начальное расстояние
        self.change_rate = 0.2  # изменение за 0.2 сек
        self.min_distance = 0.5
        self.max_distance = 3.0
        self.current_linear_x = 0.0
        
        # Publisher для /distance
        self.publisher = self.create_publisher(Float32, '/distance', 10)
        
        # Subscriber для /cmd_vel
        self.subscriber = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_vel_callback, 
            10
        )
        
        # Таймер для публикации с частотой 5 Hz (0.2 сек)
        self.timer = self.create_timer(0.2, self.timer_callback)
        
        self.get_logger().info("Distance sensor started. Initial distance: 3.0m")
    
    def cmd_vel_callback(self, msg):
        """Обновление текущей скорости робота"""
        self.current_linear_x = msg.linear.x
        self.get_logger().debug(f'Received cmd_vel.linear.x = {self.current_linear_x}', throttle_duration_sec=1.0)
    
    def timer_callback(self):
        """Обновление расстояния и публикация (каждые 0.2 сек)"""
        
        # Логика изменения расстояния в зависимости от скорости
        if abs(self.current_linear_x) < 0.001:  # робот стоит (учитываем погрешность float)
            self.distance = 3.0
            self.get_logger().debug('Robot is stationary, distance set to 3.0m')
        
        elif self.current_linear_x > 0:  # движение вперед
            self.distance = max(
                self.min_distance, 
                self.distance - self.change_rate
            )
            self.get_logger().debug(f'Moving forward, distance decreased to {self.distance:.2f}m')
        
        elif self.current_linear_x < 0:  # движение назад
            self.distance = min(
                self.max_distance, 
                self.distance + self.change_rate
            )
            self.get_logger().debug(f'Moving backward, distance increased to {self.distance:.2f}m')
        
        # Публикация текущего расстояния
        msg = Float32()
        msg.data = self.distance
        self.publisher.publish(msg)
        
        # Логирование при достижении граничных значений
        if self.distance <= self.min_distance + 0.01:
            self.get_logger().info(f'WARNING: Distance reached minimum: {self.distance:.2f}m')
        elif self.distance >= self.max_distance - 0.01:
            self.get_logger().info(f'Distance reached maximum: {self.distance:.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Distance sensor stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()