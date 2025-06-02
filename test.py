import threading
import time
import os

def data_processor():
    """持续处理数据，从文件读取参数"""
    counter = 0
    param_file = "param.txt"
    
    # 初始化参数文件
    if not os.path.exists(param_file):
        with open(param_file, 'w') as f:
            f.write("1.0")
    
    while True:
        try:
            with open(param_file, 'r') as f:
                current_param = float(f.read().strip())
        except:
            current_param = 1.0
        
        # 处理数据
        result = counter * current_param
        print(f"处理数据: {counter} * {current_param} = {result}")
        counter += 1
        time.sleep(1)

# 启动处理线程
processor_thread = threading.Thread(target=data_processor, daemon=True)
processor_thread.start()

# 主线程处理参数修改
while True:
    try:
        new_param = float(input("输入新参数值: "))
        with open("param.txt", 'w') as f:
            f.write(str(new_param))
        print(f"参数已写入文件: {new_param}")
    except ValueError:
        print("请输入有效数字")