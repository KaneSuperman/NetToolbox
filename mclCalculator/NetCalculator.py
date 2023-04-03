import ipaddress
from tkinter import ttk, StringVar, Text
from PIL import Image, ImageTk

TITLE_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ('microsoft yahei', 10)

# images
img_Calculator = Image.open('./Images/IP_Calculator.ico')

# 定义图片尺寸
Calculator_image = img_Calculator.resize((60, 60), Image.ANTIALIAS)

class NetCalculator(ttk.Frame):
    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe

        self.Calculator_img = ImageTk.PhotoImage(Calculator_image)
        self.NetCalculator = ttk.Label(self, text='IP地址计算器',image=self.Calculator_img,
                                       compound='left', font=TITLE_FONT, foreground='#1296db')

        self.Input_IP = ttk.Label(
            self, text='输入IP地址/掩码：', compound='left', font=LABEL_FONT)
        self.IP_Mask = StringVar()
        self.IP_Mask_Entry = ttk.Entry(self, textvariable=self.IP_Mask)
        self.GO_Calculate = ttk.Button(
            self, text="计算", command=lambda: self.Calculate())
        self.view_title = ttk.Label(
            self, text="计算结果", compound='left', font=LABEL_FONT)
        self.clear_views = ttk.Button(
            self, text="清空计算结果", command=lambda: self.cleane_view())

        # 结果显示
        VERTICAL = "vertical"
        self.Calculate_res = Text(self, height=20, width=100, font=LABEL_FONT)
        self.Calculate_view = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.Calculate_res.yview)
        self.Calculate_res['yscrollcommand'] = self.Calculate_view.set
        ttk.Sizegrip().grid(column=2, row=4, sticky="se")

        # 布局
        self.NetCalculator.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Input_IP.grid(column=1, row=1, sticky="nwes", padx=5, pady=5)
        self.IP_Mask_Entry.grid(column=2, row=1, sticky="nwes", padx=5, pady=5)
        self.GO_Calculate.grid(column=5, row=1, sticky="nwes", padx=5, pady=5)
        self.view_title.grid(column=1, row=2, sticky="nwes", padx=5, pady=5)
        self.Calculate_view.grid(column=21, row=3, sticky="ns")
        self.Calculate_res.grid(
            column=1, row=3, sticky="nwes", columnspan=10, padx=5, pady=5)
        self.clear_views.grid(column=10, row=11, sticky="nwes",
                              columnspan=1, rowspan=1, padx=5, pady=5)

    def Calculate(self):
        ip_mask = self.IP_Mask.get().replace(" ", "")
        try:
            net = ipaddress.ip_network(ip_mask, strict=False)
            output_text="=======================================\n输入IP/掩码为<{}>算结果如下：\n".format(net)
            output_text += "IP版本号：{}\n".format(str(net.version))
            output_text += "是否是私有地址：{}\n".format(str(net.is_private))
            output_text += "网络号：{}\n".format(str(net.network_address))
            output_text += "前缀长度：{}\n".format(str(net.prefixlen))
            output_text += "子网掩码：{}\n".format(str(net.netmask))
            output_text += "反子网掩码：{}\n".format(str(net.hostmask))
            output_text += "IP地址总数：{}\n".format(str(net.num_addresses))
            output_text += "可用IP地址总数：{}\n".format(
                str(len([x for x in net.hosts()])))
            output_text += "起始可用IP地址：{}\n".format(
                str([x for x in net.hosts()][0]))
            output_text += "最后可用IP地址：{}\n".format(
                str([x for x in net.hosts()][-1]))
            output_text += "可用IP地址范围：{}\n".format(
                str([x for x in net.hosts()][0]) + ' ~ ' + str([x for x in net.hosts()][-1]))
            output_text += "广播地址：{}\n\n".format(str(net.broadcast_address))

        except ValueError:
            output_text = "您输入的<IP/掩码>格式有误，请检查！\n"

        self.Calculate_res.insert('end', output_text)
        self.Calculate_res.update()

    def cleane_view(self):
        self.Calculate_res.delete('1.0', 'end')


if __name__ == "__main__":
    app = NetCalculator()
    app.mainloop()
