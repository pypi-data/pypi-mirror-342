import os
import tkinter as tk
from tkinter import messagebox
from pyupdater.client import Client

class UpdateWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("检查更新")
        self.master.geometry("400x400")

        # 更新说明框
        self.info_label = tk.Label(self.master, text="欢迎使用更新程序！\n\n"
                                                     "本程序将检查是否有新版本可用，并提供下载链接。\n"
                                                     "请确保您的网络连接正常。\n\n"
                                                     "点击“检查更新”按钮开始。", justify=tk.LEFT)
        self.info_label.pack(pady=10, padx=10)

        # 更新信息文本框
        self.update_text = tk.Text(self.master, wrap=tk.WORD, height=10)
        self.update_text.config(state=tk.DISABLED)  # 禁止编辑
        self.update_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # 创建检查更新按钮
        self.check_update_button = tk.Button(self.master, text="检查更新", command=self.check_for_update)
        self.check_update_button.pack(pady=10)

        # 创建关闭按钮
        self.close_button = tk.Button(self.master, text="关闭", command=self.master.destroy)
        self.close_button.pack(pady=10)

    def check_for_update(self):
        """检查更新的函数"""
        client = Client('YourAppName', 'YourAppVersion')  # 替换为你的应用名称和版本

        try:
            client.refresh()

            if client.is_update_available():
                latest_version = client.get_latest_version()
                download_url = client.get_update_url()

                self.update_text.config(state=tk.NORMAL)
                self.update_text.delete(1.0, tk.END)  # 清空文本框
                self.update_text.insert(tk.END, f"发现新版本: {latest_version}\n\n")
                self.update_text.insert(tk.END, "正在下载更新...\n")
                self.update_text.config(state=tk.DISABLED)

                # 下载并应用更新
                client.download_update()
                messagebox.showinfo("更新", "下载完成，正在应用更新...")
                self.apply_update()
            else:
                self.update_text.config(state=tk.NORMAL)
                self.update_text.delete(1.0, tk.END)  # 清空文本框
                self.update_text.insert(tk.END, "您已经是最新版本。")
                self.update_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("错误", f"检查更新时发生错误: {e}")

    def apply_update(self):
        """应用更新"""
        try:
            # 关闭当前应用程序
            messagebox.showinfo("更新", "应用程序将关闭以完成更新。")
            self.master.destroy()  # 关闭窗口

            # 重新启动应用程序
            os.startfile("your_software.exe")  # 启动新版本

        except Exception as e:
            messagebox.showerror("错误", f"更新失败: {e}")

def open_update_window():
    """打开更新窗口的函数"""
    update_window = tk.Toplevel()
    UpdateWindow(update_window)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UpdateWindow(root)
#     root.mainloop()