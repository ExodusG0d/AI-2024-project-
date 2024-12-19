import os
import pandas as pd
from uiautomation import WindowControl, ListControl, SendKeys
import time
from pynput import keyboard

# 从CSV文件中加载会话关键词和回复内容
df = pd.read_csv('c:/Users/13801/Desktop/python/孙非/回复数据.csv', encoding='utf-8')

# 绑定微信主窗口
try:
    wx = WindowControl(Name='微信', searchDepth=1)
    wx.SwitchToThisWindow()
except Exception as e:
    print("找不到微信窗口：", e)
    exit()

# 寻找会话列表控件
try:
    conversation_list = wx.ListControl(Name='会话')
except Exception as e:
    print("找不到会话列表控件：", e)
    exit()

# 查找并点击 "蔡佳豪" 的会话
conversations = conversation_list.GetChildren()
for conversation in conversations:
    if conversation.Name == '段家龙':
        conversation.Click(simulateMove=False)
        break
else:
    print("找不到会话蔡佳豪")
    exit()

# 获取初始的消息数量，作为基准点
initial_message_count = len(wx.ListControl(Name='消息').GetChildren())
print(f"初始消息数量：{initial_message_count}")

# 初始化已处理消息集合和停止标志
processed_messages = set()
stop_flag = False

# 使用 'q' 键停止程序
def on_press(key):
    global stop_flag
    try:
        if key.char == 'q':  
            print("停止程序...")
            stop_flag = True
            return False
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# 主循环
while not stop_flag:
    try:
        # 获取最新消息列表
        message_list = wx.ListControl(Name='消息').GetChildren()
        current_message_count = len(message_list)
        
        # 只处理超过初始消息数量的新增消息
        new_messages = []
        for i in range(initial_message_count, current_message_count):
            msg_control = message_list[i]
            msg_text = msg_control.Name  # 获取消息文本
            
            # 调试输出：查看消息控件的属性
            print(f"调试消息控件属性: {dir(msg_control)}")
            print(f"消息文本内容: {msg_text}")

            # 假设可以通过检查msg_text或其他属性来区分消息来源
            # 仅处理对方消息（假设对方消息不包含特定关键词）
            if "我发出的消息标识" not in msg_text:  # 请用实际标识替换
                if msg_text not in processed_messages:
                    new_messages.append((i, msg_text))
                    processed_messages.add(msg_text)

        if new_messages:
            print(f"检测到 {len(new_messages)} 条新消息：")

            for i, msg_text in new_messages:
                print(f"正在处理消息 {i + 1}: {msg_text}")
                
                # 根据关键词寻找匹配的回复
                matched_responses = df[df['关键词'].apply(lambda keyword: keyword.strip() in msg_text)]
                
                if not matched_responses.empty:
                    reply_text = matched_responses.iloc[0]['回复内容'].replace('{br}', '{Shift}{Enter}')
                else:
                    reply_text = "不知道你在说什么"

                # 发送回复
                SendKeys(reply_text)
                SendKeys('{Enter}', waitTime=0.5)
                print(f"发送回复：{reply_text}")

        else:
            print("没有新消息")
        
        time.sleep(1)

    except Exception as e:
        print(f"发生错误：{e}")
        break

listener.join()