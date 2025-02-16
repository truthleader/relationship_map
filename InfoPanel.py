import wx
import wx.aui
from Circle import Circle

class MainFrame(wx.Frame):
    """主窗体"""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


        self.circles = [Circle(1,1)]  # 创建一个 Circle 实例
        self.manager = wx.aui.AuiManager(self)  # AUI 管理器

        # 主面板
        self.panel=wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        
        # 创建可调整大小的面板
        self.info_panel = InfoPanel(self, self.circles[0])
        self.info_pane = self.manager.AddPane(
            self.info_panel,
            wx.aui.AuiPaneInfo().Right().Caption("Circle 信息").CloseButton(True).BestSize(300, 200)
        )

        self.manager.Update()  # 更新 UI
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        """确保关闭时释放 AUI 资源"""
        self.manager.UnInit()
        event.Skip()
        
    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()
        
        for circle in self.circles:
            for connected in circle.connections:
                self.draw_arrow(dc, (circle.x, circle.y), (connected.x, connected.y))
        
        for circle in self.circles:
            dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), width=1))  # 默认边框
            dc.DrawCircle(int(circle.x), int(circle.y), circle.radius)  # 圆半径为10
            
            text_x = int(circle.x - dc.GetTextExtent(circle.name)[0] / 2)
            text_y = int(circle.y + 15)  # 圆的底部下方一些
            dc.DrawText(circle.name, text_x, text_y)

class InfoPanel(wx.Panel):
    """显示和修改 Circle 信息的面板"""
    def __init__(self, parent, circle):
        super().__init__(parent)
        self.circle = circle

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 名称
        vbox.Add(wx.StaticText(self, label="名称:"), flag=wx.LEFT | wx.TOP, border=5)
        self.name_ctrl = wx.TextCtrl(self, value=circle.name)
        vbox.Add(self.name_ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        # 半径
        vbox.Add(wx.StaticText(self, label="半径:"), flag=wx.LEFT | wx.TOP, border=5)
        self.radius_ctrl = wx.TextCtrl(self, value=str(circle.radius))
        vbox.Add(self.radius_ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        # 按钮
        self.save_btn = wx.Button(self, label="保存")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(self.save_btn, flag=wx.ALL | wx.CENTER, border=10)

        self.SetSizer(vbox)

    def on_save(self, event):
        """保存修改"""
        self.circle.name = self.name_ctrl.GetValue()
        self.circle.radius = int(self.radius_ctrl.GetValue())
        wx.MessageBox("信息已更新！", "提示", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, title="可伸缩边框栏示例", size=(600, 400))
    frame.Show()
    app.MainLoop()
