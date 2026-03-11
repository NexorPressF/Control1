#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        
        # Параметры
        self.battery_level = 100.0
        self.discharge_rate = 1.0  # % в секунду
        self.last_log_threshold = 100  # для логирования каждых 10%
        
        # Publisher
        self.publisher = self.create_publisher(Float32, '/battery_level', 10)
        
        # Таймер на 1 Hz
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.get_logger().info("Battery node started. Initial level: 100.0%")
    
    def timer_callback(self):
        # Обновляем уровень батареи
        if self.battery_level > 0.0:
            self.battery_level = max(0.0, self.battery_level - self.discharge_rate)
        
        # Публикуем текущий уровень
        msg = Float32()
        msg.data = self.battery_level
        self.publisher.publish(msg)
        
        # Логирование при снижении на каждые 10%
        current_int = int(self.battery_level)
        
        # Проверяем, пересекли ли мы порог в 10% (90, 80, 70...)
        if current_int < self.last_log_threshold and current_int % 10 == 0:
            self.get_logger().info(f'Battery: {current_int}%')
            self.last_log_threshold = current_int
        
        # Для отладки (можно закомментировать)
        # self.get_logger().debug(f'Current battery: {self.battery_level:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Battery node stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()