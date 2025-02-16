import random
import math

class Circle():
    def __init__(self,x,y):
        
        self.id=0
        self.radius=10
        self.x=x
        self.y=y
        self.vx=random.uniform(-2,2) #生成随机浮点数
        self.vy=random.uniform(-2,2)
        self.selected=False
        
        # 属性
        self.name='aaa'
        self.tags=[]
        self.categories=[]
        self.connections = []
        
    def update(self, circles, offset_x, offset_y, center_force=0.5, attraction_force=0.01, repulsion_force=200.0, rest_length=100):
        """
        更新 Circle 位置：
        - 图谱向心力：指向 offset_x, offset_y
        - 连接吸引力（Hooke 定律）：距离越远，吸引力越强
        - 全局排斥力（库仑定律）：距离越近，斥力越强
        """
        ax, ay = 0, 0  # 初始化加速度

        # 1. 计算向心力
        dx = offset_x - self.x
        dy = offset_y - self.y
        dist_sq = dx ** 2 + dy ** 2
        dist = math.sqrt(dist_sq) if dist_sq > 0 else 1  # 避免除以 0

        ax += center_force * dx / dist
        ay += center_force * dy / dist

        for circle in circles:
            if circle is self:
                continue

            dx = circle.x - self.x
            dy = circle.y - self.y
            dist_sq = dx ** 2 + dy ** 2
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 1  # 避免除以 0

            # 2. 计算连接吸引力 (Hooke's Law: F_attr = k * (dist - rest_length))
            if circle in self.connections:
                spring_force = attraction_force * (dist - rest_length)
                ax += spring_force * dx / dist
                ay += spring_force * dy / dist

            # 3. 计算全局排斥力 (Coulomb's Law: F_rep ∝ 1 / r)
            if dist < rest_length * 2:  # 避免过远的影响
                repulsion = repulsion_force / (dist_sq + 1e-6)  # 避免除以 0
                ax -= repulsion * dx / dist
                ay -= repulsion * dy / dist

        # 计算速度
        self.vx += ax
        self.vy += ay

        # 添加阻尼（防止无限加速）
        self.vx *= 0.9
        self.vy *= 0.9

        # 更新位置
        self.x += self.vx
        self.y += self.vy
        
    def toggle_connection(self, other):        
        """添加/移除与另一个 Circle 的连接"""
        if other in self.connections:
            self.connections.remove(other)
        else:
            self.connections.append(other)