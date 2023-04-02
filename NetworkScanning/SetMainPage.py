import datetime
import platform
import subprocess
from tkinter import Listbox, Menu, StringVar, messagebox, ttk
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


class StartPage(ttk.Frame):
    """
    初始界面
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.mainframe.title("网络测试(NetworkTest)")

        # 菜单栏
        self.mainframe.option_add('*tearOff', FALSE)
        menubar = Menu(self.mainframe)
        self.mainframe['menu'] = menubar
        menu_tools = Menu(menubar)
        menu_help = Menu(menubar)
        menubar.add_cascade(menu=menu_tools, label='工具库(Tools)')
        menubar.add_cascade(menu=menu_help, label='帮助(H)')
        menu_tools.add_command(label='IP地址测试(IP Test)',
                               command=lambda: mainframe.show_frame("StartPage"))
        menu_help.add_command(
            label='关于(About)', command=lambda: self.About_view())
        menu_tools.add_command(label='网段扫描(Network scanning)',
                               command=lambda: mainframe.show_frame("Network_scan"))

        # 单个地址测试
        self.one_IPtest_img = ImageTk.PhotoImage(one_IPtest_image)
        self.IPtest = ttk.Label(self, text='IP地址测试',
                                image=self.one_IPtest_img, compound='left', font=TITLE_FONT, foreground='#1296db')

        self.Ip_start = ttk.Label(self, text='输入地址：', compound='left')
        self.one_iptest = StringVar()
        self.one_Ip_Entry = ttk.Entry(self, textvariable=self.one_iptest)
        self.one_scanning = ttk.Button(
            self, text="测试", command=lambda: self.One_IPtest())

        self.clear_views = ttk.Button(
            self, text="清空", command=lambda: self.cleane_view())

        self.Stop_test = ttk.Button(
            self, text="停止", command=lambda: self.Stop_Popen())

        self.choie_N = ttk.Label(self, text="选择测试次数：", compound='left')
        self.view_title = ttk.Label(self, text="测试结果", compound='left')

        # stop_popen
        self.stop_IPtest = StringVar()
        self.stop_IPtest.set('1')

        # 选择ping次数
        self.count_IPtest = StringVar()
        self.country_one = ttk.Combobox(self, textvariable=self.count_IPtest)
        self.country_one.bind('<< ComboboxSelected >>', function)
        self.country_one['values'] = ('2', '4', '10', '100', '∞')
        self.count_IPtest.set('4')

        # 结果显示
        VERTICAL = "vertical"
        self.Scanning_one = Listbox(self, height=20, width=100)
        self.ScanViews_one = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.Scanning_one.yview)
        self.Scanning_one['yscrollcommand'] = self.ScanViews_one.set
        ttk.Sizegrip().grid(column=2, row=4, sticky="se")

        # 布局
        self.IPtest.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Ip_start.grid(column=1, row=1, sticky="nwes", padx=5, pady=5)
        self.one_Ip_Entry.grid(column=2, row=1, sticky="nwes", padx=5, pady=5)
        self.choie_N.grid(column=3, row=1, sticky="nwes", padx=5, pady=5)
        self.country_one.grid(column=4, row=1, sticky="nwes", padx=5, pady=5)
        self.one_scanning.grid(column=5, row=1, sticky="nwes", padx=5, pady=5)
        self.view_title.grid(column=1, row=2, sticky="nwes", padx=5, pady=5)
        self.ScanViews_one.grid(column=21, row=3, sticky="ns")
        self.Scanning_one.grid(
            column=1, row=3, sticky="nwes", columnspan=10, padx=5, pady=5)
        self.Stop_test.grid(column=1, row=11, sticky="nwes",
                            columnspan=1, rowspan=1, padx=5, pady=5)
        self.clear_views.grid(column=10, row=11, sticky="nwes",
                              columnspan=1, rowspan=1, padx=5, pady=5)

    # 开始ping测试
    def One_IPtest(self):
        """
        获取IP，开始Ping测试，结果实时输出到窗口
        """
        one_ip = self.one_iptest.get()  # 获取IP
        count_testnum = self.count_IPtest.get()  # 获取测试次数
        self.stop_IPtest.set('1')
        if (platform.system() == 'Windows'):       # Windows系统
            if count_testnum == '∞':
                add_num = "ping -t -w 600 "
            else:
                add_num = "ping -n {0} -w 600 ".format(count_testnum)
            cmd = add_num+"{0}".format(one_ip)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            while p.poll() is None:
                control = self.stop_IPtest.get()
                if control == '0':
                    cmd_close = "taskkill /t /f /pid {0}".format(p.pid)
                    subprocess.Popen(cmd_close, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, shell=True)
                    break
                else:
                    line = p.stdout.readline().strip().decode('gbk')
                    if line:
                        Time_Print = str(datetime.datetime.now())
                        Test_Print = Time_Print+'：'+line
                        self.Scanning_one.insert('end', Test_Print)
                        self.Scanning_one.update()
            for i in range(5):
                line = p.stdout.readline().strip().decode('gbk')
                Time_Print = str(datetime.datetime.now())
                if line:
                    Test_Print = Time_Print+'：'+line
                else:
                    Test_Print = line
                self.Scanning_one.insert('end', Test_Print)
                self.Scanning_one.update()
        elif (platform.system() == 'Linux'):  # Linux系统
            if count_testnum == '∞':
                add_num = "ping -w 10 "
            else:
                add_num = "ping -c {0} -w {0} ".format(count_testnum)
            cmd = add_num+"{0}".format(one_ip)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            while p.poll() is None:
                control = self.stop_IPtest.get()
                if control == '0':
                    cmd_close = "pkill -9 {0}".format(p.pid)
                    subprocess.Popen(cmd_close, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, shell=True)
                    break
                else:
                    line = p.stdout.readline().strip().decode('utf-8')
                    if line:
                        Time_Print = str(datetime.datetime.now())
                        Test_Print = Time_Print+'：'+line
                        self.Scanning_one.insert('end', Test_Print)
                        self.Scanning_one.update()
            for i in range(5):
                line = p.stdout.readline().strip().decode('utf-8')
                Time_Print = str(datetime.datetime.now())
                if line:
                    Test_Print = Time_Print+'：'+line
                else:
                    Test_Print = line
                self.Scanning_one.insert('end', Test_Print)
                self.Scanning_one.update()
        else:
            messagebox.showinfo('不支持该操作系统！')

    def cleane_view(self):
        self.Scanning_one.delete('0', 'end')

    def Stop_Popen(self):
        self.stop_IPtest.set('0')

    def About_view(self):
        messagebox.showinfo('网络测试', """    版本: 0.2
    日期: 2019-02-05 11:30
    Python: 3.7.0
    源码发布于: https://github.com/ErickQian/NetworkScanning
    """)


if __name__ == "__main__":
    app = StartPage()
    app.mainloop()
