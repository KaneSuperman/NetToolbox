import sys

from PyQt5.QtWidgets import QApplication

from MainWindowLogic import WidgetLogic
from Network import NetworkLogic
import Style.qss_rc  # 导入资源


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_qss(style):
        """读取QSS样式表的方法"""
        with open(style, "r") as f:
            return f.read()


class MainWindow(WidgetLogic, NetworkLogic):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.link_signal.connect(self.link_signal_handler)
        self.disconnect_signal.connect(self.disconnect_signal_handler)
        self.send_signal.connect(self.send_signal_handler)
        self.tcp_signal_write_msg.connect(self.msg_write)
        self.tcp_signal_write_info.connect(self.info_write)
        self.udp_signal_write_msg.connect(self.msg_write)
        self.udp_signal_write_info.connect(self.info_write)
        self.signal_write_msg.connect(self.msg_write)

    def link_signal_handler(self, signal) -> None:
        """
        连接信号分用的槽函数
        """
        link_type, target_ip, port = signal
        if link_type == self.ServerTCP:
            self.tcp_server_start(port)
        elif link_type == self.ClientTCP:
            self.tcp_client_start(target_ip, port)
        elif link_type == self.ServerUDP:
            self.udp_server_start(port)
        elif link_type == self.ClientUDP:
            self.udp_client_start(target_ip, port)
        elif link_type == self.WebServer:
            self.web_server_start(port)

    def disconnect_signal_handler(self) -> None:
        """断开连接的槽函数"""
        if self.link_flag == self.ServerTCP or self.link_flag == self.ClientTCP:
            self.tcp_close()
        elif self.link_flag == self.ServerUDP or self.link_flag == self.ClientUDP:
            self.udp_close()
        elif self.link_flag == self.WebServer:
            self.web_close()

    def send_signal_handler(self, msg: str) -> None:
        """发送按钮的槽函数"""
        if self.link_flag == self.ServerTCP or self.link_flag == self.ClientTCP:
            self.tcp_send(msg)
            self.SendCounter += 1
        elif self.link_flag == self.ClientUDP:
            self.udp_send(msg)
            self.SendCounter += 1
        self.counter_signal.emit(self.SendCounter, self.ReceiveCounter)

    def closeEvent(self, event) -> None:
        """
        重写closeEvent方法，实现MainWindow窗体关闭时执行一些代码
        :param event: close()触发的事件
        """
        self.disconnect_signal_handler()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    styleFile = "./Style/qss/flat_white.qss"

    qssStyle = CommonHelper.read_qss(styleFile)
    window.setStyleSheet(qssStyle)
    window.show()
    sys.exit(app.exec_())
