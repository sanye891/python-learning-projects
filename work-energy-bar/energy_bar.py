#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
能量条窗口模块
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import QTimer, Qt, QTime, QPoint
from PyQt5.QtGui import QFont
import datetime
from settings import SettingsWindow
from data_manager import DataManager

class EnergyBarWindow(QMainWindow):
    """能量条主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('打工人能量条')
        self.setGeometry(100, 100, 450, 350)
        
        # 移除窗口边框和标题栏按钮
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # 默认下班时间 18:00
        self.off_work_time = datetime.time(18, 0, 0)
        
        # 下班提醒已触发标志
        self.off_work_reminded = False
        
        # 初始化数据管理器
        self.data_manager = DataManager()
        
        # 初始化UI
        self.init_ui()
        
        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        
        # 初始化显示
        self.update_time()
        
        # 鼠标拖拽相关变量
        self.drag_position = QPoint()
    
    def init_ui(self):
        """初始化界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)
        
        # 顶部区域 - 标题栏（用于移动窗口）
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #222222; border-radius: 8px;")
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 0, 10, 0)
        title_bar.setLayout(title_bar_layout)
        
        # 标题
        title_label = QLabel('打工人能量条')
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: "微软雅黑";
                font-size: 18px;
                font-weight: bold;
            }
        """)
        title_bar_layout.addWidget(title_label)
        
        # 当前时间显示
        self.current_time_label = QLabel()
        self.current_time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.current_time_label.setStyleSheet("""
            QLabel {
                color: #bbbbbb;
                font-family: "微软雅黑";
                font-size: 14px;
            }
        """)
        title_bar_layout.addWidget(self.current_time_label)
        
        main_layout.addWidget(title_bar)
        
        # 中间区域 - 能量条和剩余时间
        # 能量条
        self.energy_bar = QProgressBar()
        self.energy_bar.setMinimum(0)
        self.energy_bar.setMaximum(100)
        self.energy_bar.setValue(0)
        self.energy_bar.setTextVisible(True)
        self.energy_bar.setFixedHeight(30)
        # 设置能量条样式
        self.energy_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 15px;
                text-align: center;
                background-color: #222222;
            }
            
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                                                  stop: 0 #42a5f5, stop: 1 #2196f3);
                border-radius: 13px;
                margin: 2px;
            }
        """)
        main_layout.addWidget(self.energy_bar)
        
        # 剩余时间显示
        self.remaining_time_label = QLabel()
        self.remaining_time_label.setAlignment(Qt.AlignCenter)
        self.remaining_time_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: "微软雅黑";
                font-size: 20px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.remaining_time_label)
        
        # 底部区域 - 功能按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)
        
        # 设置按钮
        settings_button = QPushButton('设置')
        settings_button.clicked.connect(self.open_settings)
        settings_button.setFixedHeight(35)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 8px;
                font-family: "微软雅黑";
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        bottom_layout.addWidget(settings_button)
        
        # 重置按钮
        reset_button = QPushButton('重置')
        reset_button.clicked.connect(self.reset_timer)
        reset_button.setFixedHeight(35)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border-radius: 8px;
                font-family: "微软雅黑";
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QPushButton:pressed {
                background-color: #1b5e20;
            }
        """)
        bottom_layout.addWidget(reset_button)
        
        # 最小化按钮
        minimize_button = QPushButton('最小化')
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.setFixedHeight(35)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 8px;
                font-family: "微软雅黑";
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #e65100;
            }
        """)
        bottom_layout.addWidget(minimize_button)
        
        main_layout.addLayout(bottom_layout)
        
        # 趣味语录展示区
        self.quote_label = QLabel('今天也要元气满满哦！')
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setWordWrap(True)
        self.quote_label.setFixedHeight(70)
        # 设置语录样式
        self.quote_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                background-color: #333333;
                border-radius: 8px;
                padding: 15px;
                font-family: "微软雅黑";
                font-size: 14px;
                font-style: italic;
            }
        """)
        main_layout.addWidget(self.quote_label)
        
        # 语录更新定时器
        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.update_quote)
        self.quote_timer.start(3600000)  # 每小时更新一次
        
        # 初始化语录
        self.quotes = [
            "今天也要元气满满哦！",
            "摸鱼一时爽，一直摸鱼一直爽！",
            "工作再忙，也要记得喝水！",
            "下班倒计时，冲鸭！",
            "今天的你，比昨天更优秀！",
            "代码写得好，下班回家早！",
            "努力工作，快乐生活！",
            "一杯咖啡，一份代码，一份好心情！"
        ]
        self.current_quote_index = 0
    
    def update_time(self):
        """更新时间显示"""
        # 获取当前时间
        now = datetime.datetime.now()
        current_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        self.current_time_label.setText(current_time_str)
        
        # 计算进度
        progress = self.calculate_progress(now)
        self.energy_bar.setValue(int(progress))
        self.energy_bar.setFormat(f'能量积累: {int(progress)}%')
        
        # 计算剩余时间
        remaining_time_str = self.calculate_remaining_time(now)
        self.remaining_time_label.setText(f'距离下班还有: {remaining_time_str}')
        
        # 检查是否到达下班时间
        self.check_off_work_time(now)
    
    def check_off_work_time(self, now):
        """检查是否到达下班时间"""
        # 获取今天的下班时间
        off_work_datetime = now.replace(hour=self.off_work_time.hour, 
                                       minute=self.off_work_time.minute, 
                                       second=self.off_work_time.second, 
                                       microsecond=0)
        
        # 如果当前时间已经超过下班时间且还未提醒
        if now >= off_work_datetime and not self.off_work_reminded:
            self.off_work_reminded = True
            self.show_off_work_reminder()
    
    def update_quote(self):
        """更新语录"""
        self.current_quote_index = (self.current_quote_index + 1) % len(self.quotes)
        self.quote_label.setText(self.quotes[self.current_quote_index])
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = SettingsWindow(self)
        # 设置当前下班时间

        current_time = QTime(self.off_work_time.hour, self.off_work_time.minute, self.off_work_time.second)
        settings_window.time_edit.setTime(current_time)
        
        # 显示设置窗口
        settings_window.exec_()
    
    def show_off_work_reminder(self):
        """显示下班提醒"""
        # 简单的弹窗提醒
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('下班提醒')
        msg_box.setText('下班时间到！辛苦工作一天了，该休息啦！')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
        
        # 记录下班时间
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        self.data_manager.record_off_work_time(date_str, time_str)
    
    def reset_timer(self):
        """重置计时器"""
        self.off_work_reminded = False
        self.update_time()
    
    def calculate_progress(self, now):
        """计算能量进度"""
        # 获取今天的工作开始时间(假设为9:00)
        work_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # 获取今天的下班时间
        off_work_datetime = now.replace(hour=self.off_work_time.hour, 
                                       minute=self.off_work_time.minute, 
                                       second=self.off_work_time.second, 
                                       microsecond=0)
        
        # 如果当前时间已经超过下班时间，则进度为100%
        if now >= off_work_datetime:
            return 100.0
        
        # 如果当前时间早于工作开始时间，则进度为0%
        if now <= work_start:
            return 0.0
        
        # 计算进度百分比
        total_work_seconds = (off_work_datetime - work_start).total_seconds()
        worked_seconds = (now - work_start).total_seconds()
        
        progress = (worked_seconds / total_work_seconds) * 100
        return max(0.0, min(100.0, progress))
    
    def calculate_remaining_time(self, now):
        """计算剩余时间"""
        # 获取今天的下班时间
        off_work_datetime = now.replace(hour=self.off_work_time.hour, 
                                       minute=self.off_work_time.minute, 
                                       second=self.off_work_time.second, 
                                       microsecond=0)
        
        # 如果当前时间已经超过下班时间
        if now >= off_work_datetime:
            return '下班时间到！'
        
        # 计算剩余时间
        remaining = off_work_datetime - now
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f'{hours:02d}时{minutes:02d}分{seconds:02d}秒'
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()