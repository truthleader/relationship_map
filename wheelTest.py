import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Mouse Wheel Event Info", size=(400, 300))
        
        panel = wx.Panel(self)
        self.label = wx.StaticText(panel, label="Scroll to see details", pos=(20, 20))
        
        # 绑定鼠标滚轮事件
        panel.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        rotation = event.GetWheelRotation()  # 滚轮滚动的原始值
        delta = event.GetWheelDelta()  # 系统定义的滚动刻度
        axis = event.GetWheelAxis()  # 获取滚动轴（水平/垂直）
        lines_per_action = event.GetLinesPerAction()  # 每次滚动多少行
        cols_per_action = event.GetColumnsPerAction()  # 每次滚动多少列

        direction = "Up" if rotation > 0 else "Down"
        axis_text = "Vertical" if axis == wx.MOUSE_WHEEL_VERTICAL else "Horizontal"

        info = (f"Wheel Rotation: {rotation}\n"
                f"Wheel Delta: {delta}\n"
                f"Scroll Direction: {direction}\n"
                f"Wheel Axis: {axis_text}\n"
                f"Lines per Action: {lines_per_action}\n"
                f"Columns per Action: {cols_per_action}")

        self.label.SetLabel(info)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

app = MyApp()
app.MainLoop()
