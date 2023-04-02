import platform
import re
import subprocess
import threading
from tkinter import StringVar, messagebox, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import Image, ImageTk

TITLE_FONT = ("Helvetica", 16, "bold")
FALSE = False
function = 'function'


# images
img_IPtest = Image.open('./Images/IPtest_img.png')
img_ALL_IPimg = Image.open('./Images/ALL_IP_img.png')
img_go = Image.open('./Images/go_img.png')
img_one_IPtes = Image.open('./Images/one_IPtest_img.png')

# 定义图片尺寸
IPtest_image = img_IPtest.resize((60, 60), Image.ANTIALIAS)
ALL_IPimg_image = img_ALL_IPimg.resize((60, 60), Image.ANTIALIAS)
one_IPtest_image = img_one_IPtes.resize((60, 60), Image.ANTIALIAS)

go_image = img_go.resize((25, 25), Image.ANTIALIAS)


class Network_scan(ttk.Frame):
    """
    网段扫描工具
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.IPtest_img = ImageTk.PhotoImage(IPtest_image)
        self.IPtest = ttk.Label(self, text='地址段扫描',
                                image=self.IPtest_img, compound='left', font=TITLE_FONT, foreground='#1296db')

        self.Ip_start = ttk.Label(self, text='开始地址：', compound='left')
        self.Ip_end = ttk.Label(self, text='结束地址：', compound='left')
        self.var = StringVar()
        self.Ip_Entry_s = ttk.Entry(self)
        self.Ip_Entry_e = ttk.Entry(self, textvariable=self.var)

        self.get_end_IP = ttk.Button(
            self, text="自动", command=lambda: self.set_end_ip())
        self.Do_scanning = ttk.Button(
            self, text="开始扫描", command=lambda: self.start_ping())
        self.choie_num = ttk.Label(self, text="选择测试次数：", compound='left')

        # 选择ping次数
        self.countryvar = StringVar()
        self.country = ttk.Combobox(self, textvariable=self.countryvar)
        self.country.bind('<< ComboboxSelected >>', function)
        self.country['values'] = ('2', '4', '5')
        self.countryvar.set('3')
        # 网段地址图标
        self.list_index = 0
        self.label_list = []
        for i in range(1, 17):
            for j in range(9, 25):
                self.label = ttk.Label(
                    self, text=self.list_index, background="#CBCBCB")
                self.list_index += 1
                self.label.grid(column=j, row=i, sticky="nwes", padx=5, pady=5)
                self.label_list.append(self.label)

        # 界面布局
        self.IPtest.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Ip_Entry_s.grid(column=0, row=2, sticky="nwes", padx=5, pady=5)
        self.Ip_start.grid(column=0, row=1, sticky="nwes", padx=5, pady=5)
        self.Ip_end.grid(column=0, row=3, sticky="nwes", padx=5, pady=5)
        self.get_end_IP.grid(column=1, row=4, sticky="nwes", padx=5, pady=5)
        self.Ip_Entry_e.grid(column=0, row=4, sticky="nwes", padx=5, pady=5)
        self.choie_num.grid(column=0, row=5, sticky="nwes", padx=5, pady=5)
        self.country.grid(column=0, row=6, sticky="nwes", padx=5, pady=5)
        self.Do_scanning.grid(column=0, row=7, sticky="nwes", padx=5, pady=5)

    def set_end_ip(self):
        """
        填写起始地址后，默认填写结束地址为同网段最后一个地址
        """
        startip = self.Ip_Entry_s.get()
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        m = re.match(pattern, startip)      # 检查IP地址是否合法
        if m:
            startip = startip.split('.')
            startip[3] = '255'
            endip = '.'.join(startip)
            endip = self.var.set(endip)
        else:
            messagebox.showinfo(message='IP地址错误！\n地址只能为一个网段的IP，请检查你的输入！')

    def start_ping(self):
        """
        启动多线程
        """
        # 检测截至IP
        endip = self.var.get()
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        m = re.match(pattern, endip)      # 检查IP地址是否合法
        if m:
            end_ip_test = True
        else:
            end_ip_test = False
            messagebox.showinfo(message='IP地址错误！\n 详细信息：\nIP格式错误，请检查你的输入！')

        # 开始测试
        self.reset_ui()
        startip = self.Ip_Entry_s.get().split('.')
        endip = self.var.get().split('.')
        tmp_ip = startip
        if int(startip[3]) <= int(endip[3]) and end_ip_test:
            pthread_list = []
            for i in range(int(startip[3]), int(endip[3]) + 1):
                tmp_ip[3] = str(i)
                ip = '.'.join(tmp_ip)
                pthread_list.append(threading.Thread(
                    target=self.get_ping_result, args=(ip,)))
            for item in pthread_list:
                item.setDaemon(True)
                item.start()
        elif end_ip_test and int(startip[3]) > int(endip[3]):
            messagebox.showinfo(
                message='IP地址错误！\n详细信息：\n结束地址需要大于开始地址，请检查你的输入！')

    def get_ping_result(self, ip):
        """
        检查对应的IP是否被占用
        """
        if(platform.system() == 'Windows'):       # Windows系统
            num = self.countryvar.get()
            commands = "ping -n {0} -w 600".format(num)
            cmd_str = commands+" {0}".format(ip)
            DETACHED_PROCESS = 0x00000008   # 不创建cmd窗口
            try:
                subprocess.run(cmd_str, creationflags=DETACHED_PROCESS,
                               check=True)  # 仅用于windows系统
            except subprocess.CalledProcessError as err:
                self.set_ui(False, ip)
            else:
                self.set_ui(True, ip)
        elif(platform.system() == 'Linux'):  # Linux系统
            num = self.countryvar.get()
            commands = "ping -c {0} -w 4 -W 600".format(num)
            cmd_str = commands+" {0}".format(ip)
            DETACHED_PROCESS = 0x00000008   # 不创建cmd窗口
            try:
                subprocess.run(cmd_str, shell=True,
                               check=True)  # 仅用于Linux系统
            except subprocess.CalledProcessError as err:
                self.set_ui(False, ip)
            else:
                self.set_ui(True, ip)
        else:
            messagebox.showinfo('不支持该操作系统！')

    def reset_ui(self):
        """
        初始化窗口IP窗格为灰色背景
        """
        for item in self.label_list:
            item['background'] = "#CBCBCB"

    def set_ui(self, result, ip):
        """
        设置窗口颜色
        result：线程ping的结果
        ip：为对应的IP地址
        """
        index = int(ip.split('.')[3])
        if result:
            self.label_list[index]['background'] = "#55AA7F"  # 设置背景为绿色
        else:
            self.label_list[index]['background'] = "#FF8E77"   # 设置背景为红色


if __name__ == "__main__":
    app = Network_scan()
    app.mainloop()
