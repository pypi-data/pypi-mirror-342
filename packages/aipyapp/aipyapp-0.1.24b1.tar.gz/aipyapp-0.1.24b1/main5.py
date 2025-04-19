import wx
import wx.html2
import os

class ChatRoomFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, title="Markdown 聊天室", size=(800, 600))
        
        # 创建面板和垂直布局
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 创建 WebView
        self.webview = wx.html2.WebView.New(panel)
        vbox.Add(self.webview, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # 创建水平布局用于输入区域
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # 创建文本输入框
        self.message_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox.Add(self.message_input, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=10)
        
        # 创建发送按钮
        send_button = wx.Button(panel, label="发送")
        send_button.Bind(wx.EVT_BUTTON, self.on_send)
        hbox.Add(send_button, proportion=0, flag=wx.EXPAND)
        
        # 添加输入区域到主布局
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # 设置面板布局
        panel.SetSizer(vbox)
        
        # 加载 HTML 内容
        self.init_html()
        
        # 展示窗口
        self.Centre()
        self.Show()
    
    def init_html(self):
        """初始化 WebView 的 HTML 内容"""
        # 读取外部 HTML 文件
        html_file_path = "chat-ui.html"
        
        # 检查文件是否存在
        if os.path.exists(html_file_path):
            # 从文件加载 HTML
            self.webview.LoadURL(f"file://{os.path.abspath(html_file_path)}")
        else:
            # 文件不存在，显示错误消息
            error_html = """
            <!DOCTYPE html>
            <html>
            <body>
                <h1>错误：找不到UI文件</h1>
                <p>请确保 chat-ui.html 文件位于应用程序的同一目录中。</p>
            </body>
            </html>
            """
            self.webview.SetPage(error_html, "")
    
    def on_send(self, event):
        """发送消息事件处理"""
        message = self.message_input.GetValue()
        if message.strip():
            # 执行 JavaScript 添加消息
            js_code = f'appendMessage("🧑", "我", {repr(message)});'
            self.webview.RunScript(js_code)
            
            # 清空输入框
            self.message_input.SetValue("")
            
            # 模拟回复
            self.simulate_reply(message)
    
    def simulate_reply(self, received_msg):
        """模拟回复消息"""
        # 这里可以实现实际的聊天逻辑
        # 作为示例，我们简单地回复相同的消息，但添加一些 Markdown 格式
        reply = f"我收到了你的消息。这是你发送的内容：\n\n> {received_msg}\n\n"
        
        # 添加一些 Markdown 示例
        if "代码" in received_msg.lower():
            reply += "这是一个代码示例：\n```python\ndef example():\n    return 'Hello, Markdown!'\n```"
        elif "列表" in received_msg.lower():
            reply += "这是一个列表示例：\n- 项目 1\n- 项目 2\n- 项目 3"
        elif "表格" in received_msg.lower():
            reply += "这是一个表格示例：\n\n| 标题 1 | 标题 2 |\n| ------ | ------ |\n| 内容 1 | 内容 2 |\n| 内容 3 | 内容 4 |"
        
        # 执行 JavaScript 添加回复消息
        js_code = f'appendMessage("🤖", "机器人", {repr(reply)});'
        wx.CallLater(1000, lambda: self.webview.RunScript(js_code))
        
        # 演示连续消息功能，在第一条消息后再发送第二条消息
        if "连续" in received_msg.lower() or "多条" in received_msg.lower():
            second_reply = "这是同一用户的连续消息，会自动合并显示！\n\n以下是一个示例图表：\n```mermaid\ngraph TD\nA[开始] --> B[处理消息]\nB --> C{是否同一用户?}\nC -->|是| D[合并消息]\nC -->|否| E[新建消息]\n```"
            js_code = f'appendMessage("🤖", "机器人", {repr(second_reply)});'
            wx.CallLater(2500, lambda: self.webview.RunScript(js_code))

if __name__ == "__main__":
    app = wx.App()
    frame = ChatRoomFrame()
    app.MainLoop()
