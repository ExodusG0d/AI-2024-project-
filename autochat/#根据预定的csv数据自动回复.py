import os
import pandas as pd
from uiautomation import WindowControl
import time
from pynput import keyboard

# 获取当前工作目录
print(os.getcwd())

# 绑定微信主窗口
wx = WindowControl(Name='微信', searchDepth=1)   
wx.SwitchToThisWindow()

# 寻找会话控件绑定
hw = wx.ListControl(Name='会话')

# 通过pd读取数据
df = pd.read_csv('c:/Users/13801/Desktop/python/孙非/回复数据.csv', encoding='utf-8')
print(df)

conversations = hw.GetChildren()
jilu_num = 0

# 找到孙非的会话并点击
for conversation in conversations:
    if conversation.Name == '蔡佳豪':
        conversation.Click(simulateMove=False)
        break

# 获取初始消息列表长度
message_list = wx.ListControl(Name='消息').GetChildren()
jilu_num = len(message_list)

# 已处理的消息集合
processed_messages = set()

# 定义停止标志
stop_flag = False

# 监听键盘事件
def on_press(key):
    global stop_flag
    try:
        if key.char == 'q':  # 按下 'q' 键停止程序
            print("停止程序...")
            stop_flag = True
            return False  # 停止监听
    except AttributeError:
        pass

# 启动键盘监听
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 主循环
while not stop_flag:
    try:
        # 重新获取最新的消息列表
        message_list = wx.ListControl(Name='消息').GetChildren()
        
        # 记录当前消息数量
        current_jilu_num = len(message_list)
        
        # 打印当前消息列表长度
        print(f"当前消息列表长度：{current_jilu_num}")
        
        # 打印消息列表中的每条消息的 Name 属性
        for i, message in enumerate(message_list):
            print(f"消息 {i + 1}: {message.Name}")

        # 检查是否有新消息
        new_messages = []
        for i in range(jilu_num, current_jilu_num):
            msg_text = message_list[i].Name
            
            # 检查是否已处理过这条消息
            if msg_text not in processed_messages:
                new_messages.append((i, msg_text))
                processed_messages.add(msg_text)
        
        if new_messages:
            print(f"有{len(new_messages)}条新消息：")
            
            for i, msg_text in new_messages:
                print(f"正在回复第{i+1}条消息")
                # 处理每一条消息
                # 判断关键字
                msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in msg_text else None, axis=1)
                
                # 返回的结果是一个包含处理结果的Series对象，msg和列表差不多
                print(f"匹配到的回复内容：{msg}")
                
                # 过滤掉 None 值
                valid_msg = msg.dropna().tolist()
                
                # 能够匹配到数据时
                if valid_msg:
                    # 将数据输入
                    # 替换换行符号
                    wx.SendKeys(valid_msg[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
                    # 发送消息，回车键
                    wx.SendKeys('{Enter}', waitTime=1)
                    print(f"回复内容是 {valid_msg[0]}")
                else:
                    # 如果没有有效回复内容，则发送默认回复
                    wx.SendKeys('不知道你在说什么', waitTime=0)
                    wx.SendKeys('{Enter}', waitTime=0)
            
            # 更新已记录的消息数量
            jilu_num = current_jilu_num
            print(f"现在一共有{jilu_num}条消息")
        else:
            print("没有新消息")
        
        # 等待一段时间再检查
        time.sleep(1)  # 防止CPU占用过高
        
    except Exception as e:
        print(f"发生错误：{e}")
        break

# 等待键盘监听结束
listener.join()