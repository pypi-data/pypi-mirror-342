CatBit包可以帮助您将小猫板接入您的Python程序

示例：
```python
from catbit import CatBit
async def main():
    cb = CatBit()
    def key_handler(keys):
        print('按键状态：', keys)
    cb.setKeyEvent(key_handler)
    await cb.connect()
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已终止")
```
## 运行结果
```
> python test.py
正在搜索设备...
发现小猫板: CODEMAO_catbit_####
设备地址: C0:##:##:##:##:CE
准备连接...
连接成功!
正在监听设备数据...
按键状态： {'up': False, 'down': False, 'left': False, 'right': False, 'p0': False, 'p1': False, 'p2': True, 'p3': False, 'p4': False}
......