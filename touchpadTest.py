import wx

def log_event(event, event_name):
    """通用事件处理函数，打印事件名称和相关信息"""
    print(f"{event_name} - Position: {event.GetPosition()}, KeyCode: {getattr(event, 'GetKeyCode', lambda: None)()}")
    event.Skip()

class TouchpadTestFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Mac 触控板事件测试", size=(500, 400))
        panel = wx.Panel(self)
        panel.Bind(wx.EVT_LEFT_DOWN, lambda e: log_event(e, "EVT_LEFT_DOWN"))
        panel.Bind(wx.EVT_LEFT_UP, lambda e: log_event(e, "EVT_LEFT_UP"))
        panel.Bind(wx.EVT_MIDDLE_DOWN, lambda e: log_event(e, "EVT_MIDDLE_DOWN"))
        panel.Bind(wx.EVT_MIDDLE_UP, lambda e: log_event(e, "EVT_MIDDLE_UP"))
        panel.Bind(wx.EVT_RIGHT_DOWN, lambda e: log_event(e, "EVT_RIGHT_DOWN"))
        panel.Bind(wx.EVT_RIGHT_UP, lambda e: log_event(e, "EVT_RIGHT_UP"))
        panel.Bind(wx.EVT_MOTION, lambda e: log_event(e, "EVT_MOTION"))
        panel.Bind(wx.EVT_LEFT_DCLICK, lambda e: log_event(e, "EVT_LEFT_DCLICK"))
        panel.Bind(wx.EVT_MIDDLE_DCLICK, lambda e: log_event(e, "EVT_MIDDLE_DCLICK"))
        panel.Bind(wx.EVT_RIGHT_DCLICK, lambda e: log_event(e, "EVT_RIGHT_DCLICK"))
        panel.Bind(wx.EVT_LEAVE_WINDOW, lambda e: log_event(e, "EVT_LEAVE_WINDOW"))
        panel.Bind(wx.EVT_ENTER_WINDOW, lambda e: log_event(e, "EVT_ENTER_WINDOW"))
        panel.Bind(wx.EVT_MOUSEWHEEL, lambda e: log_event(e, "EVT_MOUSEWHEEL"))
        panel.Bind(wx.EVT_MOUSE_AUX1_DOWN, lambda e: log_event(e, "EVT_MOUSE_AUX1_DOWN"))
        panel.Bind(wx.EVT_MOUSE_AUX1_UP, lambda e: log_event(e, "EVT_MOUSE_AUX1_UP"))
        panel.Bind(wx.EVT_MOUSE_AUX1_DCLICK, lambda e: log_event(e, "EVT_MOUSE_AUX1_DCLICK"))
        panel.Bind(wx.EVT_MOUSE_AUX2_DOWN, lambda e: log_event(e, "EVT_MOUSE_AUX2_DOWN"))
        panel.Bind(wx.EVT_MOUSE_AUX2_UP, lambda e: log_event(e, "EVT_MOUSE_AUX2_UP"))
        panel.Bind(wx.EVT_MOUSE_AUX2_DCLICK, lambda e: log_event(e, "EVT_MOUSE_AUX2_DCLICK"))
        panel.Bind(wx.EVT_GESTURE_PAN, lambda e: log_event(e, "EVT_GESTURE_PAN"))
        panel.Bind(wx.EVT_GESTURE_ZOOM, lambda e: log_event(e, "EVT_GESTURE_ZOOM"))
        panel.Bind(wx.EVT_GESTURE_ROTATE, lambda e: log_event(e, "EVT_GESTURE_ROTATE"))
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = TouchpadTestFrame()
    app.MainLoop()
