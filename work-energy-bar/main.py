#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import qt_material
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from energy_bar import EnergyBarWindow

def main():
    app = QApplication(sys.argv)
    # 应用Qt Material主题
    qt_material.apply_stylesheet(app, theme='dark_blue.xml')
    
    # 获取图标文件的绝对路径
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cat.png')
    
    # 设置应用程序图标
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    
    window = EnergyBarWindow()
    # 设置窗口图标
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()