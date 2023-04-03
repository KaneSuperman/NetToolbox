from tkinter import Menu, Tk, messagebox, ttk

from IPScanning import NetScan, oneIPtest
from mclCalculator import NetCalculator


class NetToolbox(Tk):
    """
    MainApp
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        mainframe = ttk.Frame(self, padding=(3, 3, 12, 12),
                              borderwidth=2, relief='sunken')
        self.resizable(width=False, height=False)  # 禁止拉升窗口
        # self.iconbitmap("./Images/app_ico.ico")
        mainframe.grid(column=0, row=0, sticky="nwes")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.hig = []
        for i in range(0, 18):
            hi = mainframe.rowconfigure(i, weight=1)
            self.hig.append(hi)
        self.big = []
        for j in range(0, 25):
            tc = mainframe.columnconfigure(j, weight=1)
            self.big.append(tc)
        self.frames = {}
        for F in (LayoutPage, NetScan.NetScan, oneIPtest.oneIPtest, NetCalculator.NetCalculator):
            page_name = F.__name__
            frame = F(parent=mainframe, mainframe=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LayoutPage")
        self.show_frame("oneIPtest")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class LayoutPage(ttk.Frame):
    """
    初始界面
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.mainframe.title("NetToolbox")

        # 菜单栏
        self.mainframe.option_add('*tearOff', False)
        menubar = Menu(self.mainframe)
        self.mainframe['menu'] = menubar
        menu_tools = Menu(menubar)
        menu_help = Menu(menubar)
        menubar.add_cascade(menu=menu_tools, label='工具库(Tools)')
        menu_tools.add_command(label='IP地址测试(IP Test)',
                               command=lambda: mainframe.show_frame("oneIPtest"))
        menu_tools.add_command(label='网段扫描(Network scanning)',
                               command=lambda: mainframe.show_frame("NetScan"))
        menu_tools.add_command(label='IP地址计算器(IPCalculator)',
                               command=lambda: mainframe.show_frame("NetCalculator"))

        menubar.add_cascade(menu=menu_help, label='帮助(H)')
        menu_help.add_command(
            label='关于(About)', command=lambda: self.AboutPage())

    def AboutPage(self):
        messagebox.showinfo('网络测试',
                            """
        版本: 1.0
        提交：
        日期: 2023-04-20 11:30
        Python 3.11.2
        Pillow 9.4.0
        源码发布于: https://github.com/KaneSuperman/NetToolbox
        """
                            )


if __name__ == "__main__":
    app = NetToolbox()
    app.mainloop()
