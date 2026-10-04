import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)  #认祖归宗，让node_name子类被Node承认，获取相应的能力
        self.get_logger().info(f'{node_name},start!')
        self.novels_queue_ = Queue()  #创建队列
        self.novel_publisher_ = self.create_publisher(String,'novel',10)
        self.create_timer(5,self.timer_callback)


    def timer_callback(self):
        #self.novel_publisher_.publish()   实现间隔5s的连续发布
        if self.novels_queue_.qsize()>0:
            line = self.novels_queue_.get()
            msg = String()
            msg.data = line
            self.novel_publisher_.publish(msg)
            self.get_logger().info(f'发表了:{msg}')
            pass
    

    def download(self,url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f'下载{url},{len(text)}')
        for line in text.splitlines():
            self.novels_queue_.put(line)
        #text.splitlines()   分割函数
        #response.text
        



def main():
    rclpy.init()
    node = NovelPubNode('novel_pub')
    node.download('http://0.0.0.0:8000/novel1.txt')
    rclpy.spin(node)  #类似于哨兵站岗，持续监听 ROS 的事件信号，来了事件自动执行回调
    rclpy.shutdown()