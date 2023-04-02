from tkinter import Tk, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import Image

from NetworkScanning import NetScan, SetMainPage

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


class Network_Test(Tk):
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
        # self.geometry("600x300")
        self.frames = {}
        for F in (SetMainPage.StartPage, NetScan.Network_scan):
            page_name = F.__name__
            frame = F(parent=mainframe, mainframe=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Network_Test()
    app.mainloop()
