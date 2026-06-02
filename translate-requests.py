import base64
import ctypes
import threading
import time
import tkinter as tk
from io import BytesIO
from tkinter import messagebox
from PIL import ImageGrab
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass
zck=tk.Tk()
y=zck.maxsize()
w,h=y
zck.geometry(f'1200x130+{int(w/4)}+{int(h/3)}')
zck.title('本地文字实时翻译',)
zck.resizable(False,False)
zck.configure(bg='#ACD2F7')
zck.attributes('-alpha',1)
zck.attributes('-topmost',True)
zck.protocol("WM_DELETE_WINDOW", lambda :zck.destroy())
indexlist=[]
kg=1
def func1():
    if kg==1:
        fck = tk.Tk()
        fck.attributes("-fullscreen", True)  # 全屏
        fck.attributes("-alpha", 0.3)  # 窗口透明度（0.0到1.0之间）
        fck.attributes("-topmost", True)  # 窗口置顶
        fck.configure(bg='black')  # 窗口背景色（配合透明度形成遮罩）
        fck.overrideredirect(True)
        canvas = tk.Canvas(fck, cursor="cross", bg='black', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        # 用于存储起始坐标和矩形框对象的变量
        start_x, start_y = None, None
        rect = None
        def on_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            # 创建一个矩形框（初始时宽高为0）
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='skyblue', width=4)
            # 3. 定义鼠标拖动事件（实时更新矩形的大小）
        def on_drag(event):
            nonlocal rect
            if rect:
                # 将矩形的右下角坐标更新为当前鼠标的位置
                canvas.coords(rect, start_x, start_y, event.x, event.y)
            # 4. 定义鼠标释放事件（获取最终坐标，并关闭窗口）
        def on_release(event):
            global indexlist
            nonlocal start_x, start_y, rect
            end_x, end_y = event.x, event.y
            # 确保坐标顺序正确（左上角到右下角）
            x1, y1 = min(start_x, end_x), min(start_y, end_y)
            x2, y2 = max(start_x, end_x), max(start_y, end_y)
            indexlist = [x1, y1, x2, y2]
            if x2 - x1 >= 32 and y2 - y1 >= 32:
                indexlist = [x1, y1, x2, y2]
                if indexlist and len(indexlist) == 4:
                    text4.set('已设置翻译区域\n(点击重新设置)')
                else:
                    text4.set('设置翻译区域\n(按Esc退出操作)')
            else:
                messagebox.showwarning('警告', '请勿选择过小的区域(长度和宽度均需超过32px)')
            # 销毁全屏遮罩窗口
            fck.destroy()
            # 打印出最终选中的区域坐标
            # 5. 将鼠标事件绑定到画布上
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        # 可选：绑定 ESC 键，按下后取消选择并退出
        fck.bind("<Escape>", lambda e: fck.destroy())
        # 6. 进入主事件循环，等待用户操作
        fck.mainloop()
    else:
        messagebox.showwarning('警告','运行期间请勿修改翻译区域')
def func2():
    global kg
    if kg==1:
        kg=0
        if indexlist and len(indexlist)==4:
            text1.set('运行状态:正常')
            text3.set('正在翻译中')
            text2.set('翻译已启动,请耐心等待...')
            thread1 = threading.Thread(target=func3)
            thread1.start()
        else:
            text3.set('启动翻译')
            text2.set('等待启动翻译')
            messagebox.showwarning('警告','请先手动设置翻译区域')
    else:
        kg=1
        text3.set('启动翻译')
        text2.set('等待启动翻译')
def func3():
    llm = ChatOllama(
        model="adelnazmy2002/Qwen3-VL-4B-Instruct:Q4_K_M",
        temperature=0
    )
    region = (indexlist[0], indexlist[1], indexlist[2], indexlist[3])
    while kg==0:
        try:
            time.sleep(1)
            screenshot = ImageGrab.grab(bbox=region)
            buffered = BytesIO()
            screenshot.save(buffered, format="PNG")  # 以 PNG 格式存入缓冲区
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            messages = [
            HumanMessage(
            content=[
                {"type": "text", "text": "请以最快速度识别图片区域中的所有文字，并翻译成流畅的中文拼接成字符串返回"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{img_base64}",  # 加上前缀告诉模型这是Base64图片
                },
            ]
        )
    ]
            result = llm.invoke(messages)
            text2.set(result.content)
        except Exception as e:
            text1.set('运行状态:异常')
            messagebox.showerror('错误','请尝试重新启动')
            break
#常量相关
text1=tk.StringVar(value='运行状态:正常')
text2=tk.StringVar(value='等待启动翻译(注:翻译字数超出不显示)')
text3=tk.StringVar(value='启动翻译')
text4=tk.StringVar(value='设置翻译区域\n(按Esc退出操作)')
#组件相关
tk.Button(zck,fg='black',bg='white',textvariable=text4,font=('仿宋',10),command=func1).place(x=20,y=15)
tk.Button(zck,fg='black',bg='white',textvariable=text3,font=('华文行楷',10),command=func2,width=15).place(x=1057,y=5)
tk.Label(zck,fg='black',bg='white',textvariable=text1,font=('仿宋',12)).place(x=20,y=85)
tk.Label(zck,fg='black',bg='white',text='翻译内容:',font=('仿宋',12)).place(x=180,y=10)
tk.Label(zck,fg='black',bg='white',textvariable=text2,font=('仿宋',12),width=100,height=4,anchor='nw',justify='left',wraplength=1000).place(x=180,y=40)
zck.mainloop()