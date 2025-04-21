import tkinter as tk
from tkinter import messagebox
from update import open_update_window  # 导入更新窗口的函数

class TermsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("条款和条件")
        self.master.geometry("800x600")

        # 创建说明文本
        self.terms_text = tk.Text(self.master, wrap=tk.WORD)
        self.terms_text.insert(tk.END, "软件使用免责条款\n\n"
                                       "1. 接受条款\n"
                                       "   使用本软件即表示您同意遵守本免责条款。如果您不同意这些条款，请勿使用本软件。\n\n"
                                       "2. 软件用途\n"
                                       "   本软件仅供学习使用，请勿用于商业用途。您同意不将软件用于任何非法活动或违反当地法律法规的行为。\n\n"
                                       "3. 风险自负\n"
                                       "   使用本软件的所有风险由您自行承担。开发者不对因使用本软件而导致的任何直接、间接、偶然、特殊或后果性损害承担责任，包括但不限于数据丢失、利润损失或其他经济损失。\n\n"
                                       "4. 软件提供和维护\n"
                                       "   本软件以“现状”提供，不保证其功能、性能或适用性。开发者不承诺对软件进行维护、更新或修复。\n\n"
                                       "5. 知识产权\n"
                                       "   本软件及其所有内容、功能和特性（包括但不限于所有信息、软件、文本、显示、图形、音频、视频和设计）均为开发者或其许可方的财产，受版权、商标和其他知识产权法律保护。\n\n"
                                       "6. 条款的修改\n"
                                       "   开发者保留随时修改本免责条款的权利。修改后的条款将会在软件中发布，并自发布之日起生效。\n\n"
                                       "7. 法律适用\n"
                                       "   本免责条款适用中华人民共和国法律。如因本条款引起的争议，双方应友好协商解决；协商不成的，任何一方可向开发者所在地人民法院提起诉讼。\n\n"
                                       "8. 联系方式\n"
                                           "   如您对本免责条款有任何疑问，请联系开发者：[QQ:283044916]")
        self.terms_text.config(state=tk.DISABLED)  # 禁止编辑
        self.terms_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # 创建按钮框架
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        # 创建同意按钮
        self.agree_button = tk.Button(button_frame, text="同意", command=self.agree)
        self.agree_button.pack(side=tk.LEFT, padx=10)

        # 创建拒绝按钮
        self.reject_button = tk.Button(button_frame, text="拒绝", command=self.reject)
        self.reject_button.pack(side=tk.LEFT, padx=10)

        # 创建更新按钮
        self.update_button = tk.Button(button_frame, text="检查更新", command=open_update_window)
        self.update_button.pack(side=tk.LEFT, padx=10)

    def agree(self):
        """同意按钮的处理逻辑"""
        messagebox.showinfo("信息", "感谢您同意条款，正在进入主界面...")
        self.master.destroy()  # 关闭条款窗口
        self.open_main_app()  # 调用主应用

    def reject(self):
        """拒绝按钮的处理逻辑"""
        messagebox.showwarning("警告", "您必须同意条款才能使用本软件。")
        self.master.quit()  # 退出程序

    def open_main_app(self):
        """打开主应用程序的逻辑"""
        import main_app  # 假设主应用程序在 main_app.py 中
        main_app.run()  # 运行主应用程序

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TermsWindow(root)
#     root.mainloop()