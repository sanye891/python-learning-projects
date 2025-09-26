#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据管理模块
"""

import json
import os
import datetime

class DataManager:
    """数据管理类"""
    
    def __init__(self, data_file='work_data.json'):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def record_off_work_time(self, date, off_work_time):
        """记录下班时间"""
        if 'off_work_times' not in self.data:
            self.data['off_work_times'] = {}
        
        self.data['off_work_times'][date] = off_work_time
        return self.save_data()
    
    def get_off_work_time(self, date):
        """获取指定日期的下班时间"""
        if 'off_work_times' in self.data and date in self.data['off_work_times']:
            return self.data['off_work_times'][date]
        return None
    
    def get_all_off_work_times(self):
        """获取所有下班时间记录"""
        if 'off_work_times' in self.data:
            return self.data['off_work_times']
        return {}