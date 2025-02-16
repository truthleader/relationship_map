import wx
import random
import math
from InfoPanel import InfoPanel
from Circle import Circle

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="简单窗口", size=(1400, 700))

        self.panel=wx.Panel(self)
        
        self.offset_sx=0 # 窗口偏移量x
        self.offset_sy=0 # 窗口偏移量y
        
        width,height = super().GetSize()
    
        # 全局变量
        ## 让 (0,0) 对应到窗口中心
        self.offset_sx = width / 4
        self.offset_sy = height / 4
        self.center_force=0.5
        self.attraction_force=0.01
        self.repulsion_force=200.0
        self.rest_length=100
        
        self.is_dragging=False
        self.last_mouse_x=0
        self.last_mouse_y=0 
        
        self.is_shift_down = False
        self.manager=None # 是否有侧边栏
        
        self.scale=1.0   
        self.last_selected=None
        self.clicked_circle = []
        
        # Menu
        filemenu1= wx.Menu()
        filemenu2= wx.Menu()
        menuBar = wx.MenuBar()
        
        self.CreateStatusBar()
        
        my_exit_id = wx.NewIdRef()

        self.circles = []
        
        # ID ref
        ID_1=wx.NewIdRef()
        ID_2=wx.NewIdRef()
        
        self.opr_num1 = filemenu1.AppendRadioItem(ID_1, "新建",)
        self.opr_num2 = filemenu1.AppendRadioItem(ID_1, "选中")
        self.opr_num3 = filemenu1.AppendRadioItem(ID_1, "画线")
        self.opr_num4 = filemenu1.AppendRadioItem(ID_1, "4")
        self.opr_num5 = filemenu2.AppendRadioItem(ID_2, "放大缩小")
        self.opr_num6 = filemenu2.AppendRadioItem(ID_2, "移动")
        menuBar.Append(filemenu1,"&一指")
        menuBar.Append(filemenu2,"&两指")
        self.SetMenuBar(menuBar)
        
        # event binding
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.panel.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.panel.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update, self.timer)
        self.timer.Start(2)  # 每16ms更新一次（约60FPS）
        
        self.Bind(wx.EVT_MENU, self.on_exit, id=my_exit_id)
        
        self.Show()
    
    def on_exit(self, event):
        self.Close()
        
    def on_click(self, event):
        if self.opr_num1.IsChecked():
            pos = event.GetPosition()
            self.circles.append(Circle(pos.x-self.offset_sx,pos.y-self.offset_sy))
            self.last_selected=self.circles[-1]
            self.last_selected.selected=True
            self.clicked_circle=[]
            self.clicked_circle.append(self.last_selected)
        elif self.opr_num2.IsChecked():
            pos = event.GetPosition()
            pos = (pos.x / self.scale, pos.y / self.scale)  # 考虑缩放
            for circle in self.circles:
                dist = math.sqrt((circle.x+self.offset_sx - pos[0]) ** 2 + (circle.y+self.offset_sy - pos[1]) ** 2)
                if dist <= circle.radius:  # 假设圆圈半径为10
                    self.last_selected=circle
                    break
                self.last_selected=None

            if self.last_selected:
                self.last_selected.selected=True
                if self.is_shift_down:
                    self.clicked_circle.append(self.last_selected)
                elif self.last_selected:
                    self.clicked_circle = []
                    self.clicked_circle.append(self.last_selected)
                else:
                    # 取消其他圆圈的选中状态
                    self.clicked_circle=[] 
            else:
                if not self.is_shift_down:
                    # 点击空白区域时，取消所有选中状态
                    for circle in self.circles:
                        circle.selected = False
                    self.last_selected = None    
                    self.clicked_circle=[] 
            for circle in self.circles:
                circle.selected=False
            for circle in self.clicked_circle:
                circle.selected=True
                    

            self.panel.Refresh()
        
        elif self.opr_num3.IsChecked():
            pos = event.GetPosition()
            pos = (pos.x / self.scale, pos.y / self.scale)  # 考虑缩放
            last_selected=None
            for circle in self.circles:
                dist = math.sqrt((circle.x+self.offset_sx - pos[0]) ** 2 + (circle.y+self.offset_sy - pos[1]) ** 2)
                if dist <= 10:  # 假设圆圈半径为10
                    last_selected=circle
                    break
                last_selected=None
            
            if last_selected is not None:
                for circle in self.clicked_circle:
                    circle.toggle_connection(last_selected)
            
            self.panel.Refresh()
            

    def on_mouse_wheel(self,event):
        if self.opr_num5.IsChecked():
            rotation = event.GetWheelRotation()
            if rotation > 0:
                self.scale *= 1.1  # 放大
            else:
                self.scale /= 1.1  # 缩小
            self.Refresh()  # 触发重绘
        
        elif self.opr_num6.IsChecked():
            rotation = event.GetWheelRotation()
            axis = event.GetWheelAxis()
            
            if axis==wx.MOUSE_WHEEL_VERTICAL:
                self.offset_sy+=rotation
            else:
                self.offset_sx-=rotation
            

    def on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_SHIFT:
            self.is_shift_down = True
        event.Skip()

    def on_key_up(self, event):
        if event.GetKeyCode() == wx.WXK_SHIFT:
            self.is_shift_down = False
        event.Skip()
        
        
    def draw_arrow(self, dc, start, end):
        """绘制带箭头的线"""
        if not start or not end :
            return

        # 画主线
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 255), width=2))  # 蓝色箭头
        
        x=end[0]-start[0]
        y=end[1]-start[1]
        dist=math.sqrt(x**2+y**2)
        
        if dist==0:
            return
        
        delta_x=10*(x/dist)
        delta_y=10*(y/dist)
        start_x=start[0]+delta_x
        start_y=start[1]+delta_y
        end_x=end[0]-delta_x
        end_y=end[1]-delta_y
        
        dc.DrawLine(int(start_x), int(start_y), int(end_x), int(end_y))

        # 计算箭头方向
        angle = math.atan2(y, x)
        arrow_size = 10

        # 计算箭头的两个侧翼点
        right_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
        right_y = end_y - arrow_size * math.sin(angle - math.pi / 6)
        left_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
        left_y = end_y - arrow_size * math.sin(angle + math.pi / 6)

        # 画箭头
        dc.DrawLine(int(end_x), int(end_y), int(left_x), int(left_y))
        dc.DrawLine(int(end_x), int(end_y), int(right_x), int(right_y))
    
    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()
        dc.SetUserScale(self.scale, self.scale)
        
        for circle in self.circles:
            for connected in circle.connections:
                self.draw_arrow(dc, (circle.x+self.offset_sx, circle.y+self.offset_sy), (connected.x+self.offset_sx, connected.y+self.offset_sy))
        
        for circle in self.circles:
            if circle.selected:
                dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
                dc.SetPen(wx.Pen(wx.Colour(128, 0, 128), width=3))  # 紫色光环
            else:
                dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), width=1))  # 默认边框
            dc.DrawCircle(int(circle.x+self.offset_sx), int(circle.y+self.offset_sy), circle.radius)  # 圆半径为10
            
            text_x = int(circle.x + self.offset_sx - dc.GetTextExtent(circle.name)[0] / 2)
            text_y = int(circle.y + self.offset_sy + 15)  # 圆的底部下方一些
            dc.DrawText(circle.name, text_x, text_y)
        
        

    def on_update(self, event):
        for circle in self.circles:
            circle.update(self.circles,self.offset_sx,self.offset_sy,self.center_force,self.attraction_force,self.repulsion_force,self.rest_length)
        self.panel.Refresh() # 会产生事件EVT_PAINT
        
        if self.clicked_circle and self.manager==None:
            self.manager=wx.aui.AuiManager(self) 
            self.info_panel = InfoPanel(self, self.last_selected)
            self.info_pane = self.manager.AddPane(
                self.info_panel,
                wx.aui.AuiPaneInfo().Right().Caption("Circle 信息").CloseButton(True).BestSize(300, 200)
            )

            self.manager.Update()  # 更新 UI
        elif self.manager and self.clicked_circle is None:
            
            self.manager.UnInit()
            self.manager=None
            event.skip
        
            
        
        
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
