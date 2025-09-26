#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设置窗口模块
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTimeEdit, QPushButton
from PyQt5.QtCore import QTime
import datetime

class SettingsWindow(QDialog):
    """设置窗口类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('设置')
        self.setGeometry(200, 200, 300, 150)
        
        # 保存父窗口引用
        self.parent_window = parent
        
        # 初始化UI
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 下班时间设置
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)
        time_label = QLabel('下班时间:')
        time_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: "微软雅黑";
                font-size: 16px;
                font-weight: bold;
            }
        """)
        self.time_edit = QTimeEdit()
        self.time_edit.setMinimumHeight(35)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background-color: #333333;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                font-size: 14px;
                padding: 5px;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                background-color: #2196f3;
                border: none;
                width: 20px;
            }
        """)
        
        # 设置默认时间为18:00
        default_time = QTime(18, 0)
        self.time_edit.setTime(default_time)
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)
        layout.addLayout(time_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 确定按钮
        ok_button = QPushButton('确定')
        ok_button.clicked.connect(self.accept_settings)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet("""
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
        button_layout.addWidget(ok_button)
        
        # 取消按钮
        cancel_button = QPushButton('取消')
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(35)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 8px;
                font-family: "微软雅黑";
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def accept_settings(self):
        """接受设置"""
        # 获取设置的时间
        time = self.time_edit.time()
        off_work_time = datetime.time(hour=time.hour(), minute=time.minute(), second=time.second())
        
        # 更新父窗口的下班时间
        if self.parent_window:
            self.parent_window.off_work_time = off_work_time
        
        # 关闭设置窗口
        self.accept()