import ipaddress
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("IP 地址计算器")
        self.master.geometry("400x400")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self, text="IP 地址", font=("Helvetica", 14))
        self.ip_label.pack(side="top", fill="x", padx=20, pady=20)

        self.ip_entry = tk.Entry(self, font=("Helvetica", 12))
        self.ip_entry.pack(side="top", fill="x", padx=20, pady=20)

        self.mask_label = tk.Label(self, text="子网掩码", font=("Helvetica", 14))
        self.mask_label.pack(side="top", fill="x", padx=20, pady=20)

        self.mask_entry = tk.Entry(self, font=("Helvetica", 12))
        self.mask_entry.pack(side="top", fill="x", padx=20, pady=20)

        self.calc_button = tk.Button(self, text="计算", width=10, height=2, font=("Helvetica", 12), bg="#58D3F7", fg="white", command=self.calculate)
        self.calc_button.pack(side="left", padx=20, pady=20)

        self.quit_button = tk.Button(self, text="退出", width=10, height=2, font=("Helvetica", 12), bg="#FF0000", fg="white", command=self.master.destroy)
        self.quit_button.pack(side="left", padx=20, pady=20)

        self.result_label = tk.Label(self, text="计算结果", font=("Helvetica", 14))
        self.result_label.pack(side="top", fill="x", padx=20, pady=20)

        self.result_text = tk.Text(self, font=("Helvetica", 12), height=10, state=tk.DISABLED)
        self.result_text.pack(side="top", fill="both", expand=True, padx=20, pady=20)

    def calculate(self):
        ip_str = self.ip_entry.get().strip()
        mask_str = self.mask_entry.get().strip()
        if ip_str and mask_str:
            try:
                ip = ipaddress.IPv4Address(ip_str)
                mask = ipaddress.IPv4Address(mask_str)
                net = ipaddress.IPv4Network(ip_str + "/" + mask_str, False)
                output_text = "网络地址：{}\n".format(net.network_address)
                output_text += "广播地址：{}\n".format(net.broadcast_address)
                output_text += "可用 IP 地址数量：{}\n".format(net.num_addresses - 2)
                output_text += "IP 地址类型：{}\n".format("私有" if net.is_private else "公共")
            except Exception as e:
                output_text = "计算错误：{}".format(e)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, output_text)
            self.result_text.config(state=tk.DISABLED)
        else:
            self.result
root = tk.Tk()
app = Application(master=root)
app.mainloop()