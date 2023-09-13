from PythonMagick import Image as PImage
from PIL import Image as img
from PIL import ImageTk
from tkinter import *
from datetime import date
import tkinter.font as tkfont
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from os.path import exists
from os.path import abspath
from os.path import join as Pjoin
import sys

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = abspath('.')
    return Pjoin(base_path, relative_path)
example_image = get_resource_path(Pjoin("./resources","dfimage.jpg"))


window_width = 600
window_height = window_width*2//3
margin = window_height//20
button_width = 7
button_color = "#4fcde7"
text_color = "#4fcde7"
window_color = "#bae7ee"


# 图片读取
def get_image( filename, width, height):
    try:
        im = img.open(filename).resize((width, height))
    except:
        return None
    else:
        return ImageTk.PhotoImage(im)


class Transform(object):
    # 界面初始化
    def __init__(self):
        # 窗口对象
        self.window = Tk()
        # 窗口标题
        self.window.title("图像转ico图标工具")
        # 设置窗口背景
        self.window.config(background=window_color)
        # 设置窗口大小
        self.window.geometry("{:d}x{:d}+450+240".format(window_width+margin*2,window_height+margin*4))
        # 设置窗口不可改变大小
        self.window.resizable(False,False)
        # 设置字体
        self.Font = tkfont.Font(family='Fixdsys', size=15, weight=tkfont.BOLD)
        self.output_Font = tkfont.Font(family='Fixdsys', size=15, weight=tkfont.NORMAL)
        # 其他组件设置
        self.interface()

    # 界面组件
    def interface(self):
        # ico尺寸选择
        self.size_selection = {}
        # 输入变量
        self.entry_path = StringVar(value="")# 输入图片路径
        self.output_path = StringVar(value="输出路径默认为当前位置")# 输出图片路径
        self.image=get_image(example_image,width=window_width//2,height=window_height*2//3)# 预览路径
        self.selection = 0
        self.filetype=[("jpg格式","jpeg;*.jpg;*.jpe;*.jfif"),("png格式","*.png"),("gif格式","*.gif"),("bmp格式","*.bmp"),("heic格式","*.heic"),("tif格式","*.tif;*.tiff"),("webp格式","*.webp")]
        # 界面布置

        # 输入部分框架
        frame_in = Frame(self.window,height=window_height/6,width=window_width,bg=window_color)
        frame_in.grid(row=0,padx=margin,pady=margin)
        frame_in.grid_propagate(0)
        # 输入部分组件
        self.select_in_btn = Button(frame_in,text="选择输入图片",font=self.Font,height=1,width=button_width*3,bg=button_color,command=self.select_entry_path)
        self.input_path = Entry(frame_in,textvariable = self.entry_path,width=button_width*4,font=self.Font,bg=text_color,bd=5,state="disabled",relief="flat")
        self.select_in_btn.grid(row=0,column=0,columnspan=1,padx=10,pady=10)
        self.input_path.grid(row=0,column=1,columnspan=5,padx=10,pady=0)
        

        # 预览部分框架
        frame_prev = Frame(self.window,width=window_width,height=window_height*2//3,bg=window_color)
        frame_prev.grid(row=1,padx=margin,pady=0)
        frame_prev.grid_propagate(0)
        # 预览部分组件
        # 选择尺寸
        values=["16x16","24x24","32x32","48x48","64x64","128x128"]
        self.select_size = Combobox(frame_prev,values=values,font=self.Font,width=button_width*3,height=3)
        self.select_size.current(5)
        # 选择输出位置
        self.select_out_btn = Button(frame_prev,text = "选择输出位置",font=self.Font,width = button_width*3, height = 1,bg=button_color,command=self.select_output_path)
        self.out_path = Entry(frame_prev,textvariable = self.output_path,width=button_width*3,font=self.Font,bg=text_color,bd=5,state="disabled",relief="flat")
        # 开始转换
        self.trans_btn = Button(frame_prev,text="开始转换",font=self.Font,width = button_width*3, height = 1,bg=button_color,command=self.transform_pic)
        # 图片预览
        self.preview = Label(frame_prev,width=window_width//2,height=window_height*2//3,image = self.image)
        
        self.select_out_btn.grid(row=0,column=0,padx=10,pady=0,ipadx=0,ipady=0)
        self.out_path.grid(row=1,column=0,padx=10,pady=0,ipadx=0,ipady=0)
        self.select_size.grid(row=2,column=0,padx=10,pady=0,ipadx=0,ipady=0)
        self.trans_btn.grid(row=3,column=0,padx=10,pady=0,ipadx=0,ipady=0)
        self.preview.grid(row=0,column=1,rowspan=4,columnspan=1,padx=10,pady=10)


        # 退出部分框架
        frame_quit = Frame(self.window,width=window_width,height=window_height//6,bg=window_color)
        frame_quit.grid(row=2,padx=margin,pady=margin)
        frame_quit.grid_propagate(0)
        # 退出部分组件
        self.quit_button=Button(frame_quit,text="退出",font=self.Font,width = button_width, height = 1,bg=button_color,command=self.quit_window)
        self.current_time = Label(frame_quit,text="当前日期: {}".format(date.today()),font=self.Font,width=button_width*6,height=1,bg=text_color,bd=5)
        self.quit_button.grid(row=0,column=1,columnspan=5,padx=10,pady=10)
        self.current_time.grid(row=0,column=0,columnspan=1,padx=10,pady=0)

    def select_entry_path(self):
        file_input_path = filedialog.askopenfilename(filetypes=self.filetype)
        if file_input_path == "":
            messagebox.showerror(title = "输入路径出错", message = "请选择正确的图片！！")
            return
            #先判斷Entry輸入值是否為空值

        self.entry_path.set(file_input_path)
        self.image=get_image(file_input_path,width=window_width//2,height=window_height*2//3)
        self.preview.config(image=self.image)
    
    # 选择输出路径
    def select_output_path(self):
        file_output_path = filedialog.askdirectory()
        # 不选择直接退出默认会保存在当前文件夹
        if len(file_output_path)!=0:
            self.output_path.set(file_output_path)
    
    # 转换图片
    def transform_pic(self):
        # 写入存储
        def write_to_file(filepath,image):
            if exists(filepath):
                    option = messagebox.askquestion(title="文件已存在",message="是否覆盖源文件夹中的文件")
                    
                    if option=="yes":
                        image.write(filepath)
                        return True
                    else:
                        return False
            else:
                image_file.write(filepath)
                return True
            
        entryvalue = self.entry_path.get()
        if entryvalue=="":
            messagebox.showerror(title = "Error", message = "请选择正确的图片！！")
        else:
            filename = entryvalue.rsplit("/",1)[1].rsplit(".",1)[0]# 得到不带后缀的文件名
            try:
                image_file = PImage(entryvalue)
            except:
                messagebox.showerror(title = "Error", message = "抱歉,打开图片错误,可能是不支持的图片类型.")
                self.entry_path.set("")

            else:
                image_file.sample(self.select_size.get())
                success=False
                if self.output_path.get()=="输出路径默认为当前位置":
                    success = write_to_file("./"+filename+".ico",image_file)
                else:
                    success =  write_to_file(self.output_path.get()+"/"+filename+".ico",image_file)
                if success:
                    messagebox.showinfo(title = "注意", message = "图片转换完成！！")
                else:
                    messagebox.showinfo(title = "注意", message = "图片转换失败！！")
                
 
    
    # 退出删除窗口
    def quit_window(self):
        self.window.destroy()
    
    # 每次处理成功清除预览
    

if __name__=="__main__":
    a = Transform()
    a.window.mainloop()