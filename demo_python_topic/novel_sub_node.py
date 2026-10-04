import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time


class NovelPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)  #认祖归宗，让node_name子类被Node承认，获取相应的能力
        self.get_logger().info(f'{node_name},start!')
        self.novels_queue_ = Queue()
        self.novel_subscriber_ = self.create_subscription(String,'novel',self.novel_callback,10)
        self.speech_thread_ = threading.Thread(target=self.speaker_thread) 
        self.speech_thread_.start()

    def novel_callback(self,msg):
        self.novels_queue_.put(msg.data)

    def speaker_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'

        while rclpy.ok():  #检测当前ROS上下文是否ok 
            if self.novels_queue_.qsize()>0:
                text = self.novels_queue_.get()
                self.get_logger().info(f'朗读内容：{text}')
                speaker.say(text) #说话
                speaker.wait()   #等它说完
            else:
                #当前线程休眠
                time.sleep(1)

def main():
    rclpy.init()
    node = NovelPubNode('novel_sub')
    rclpy.spin(node)  #类似于哨兵站岗，持续监听 ROS 的事件信号，来了事件自动执行回调
    rclpy.shutdown()