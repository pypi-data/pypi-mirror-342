'''
easy_qmainwindow.py
简化版的QMainWindow类，提供了更简单的API来创建和管理窗口控件。
Simplified version of QMainWindow class, provides a simpler API to create and manage window widgets.
'''

__all__ = ['EasyMainWindow']
from qtpy.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, 
                           QTextEdit, QCheckBox, QRadioButton, QSpinBox)

from typing import TypeVar, Callable
T = TypeVar('T', bound=QWidget)

class EasyMainWindow(QMainWindow):
    def __init__(self, title="Easy Window", show_full_screen=False, width=800, height=600):
        super().__init__()
        self.setWindowTitle(title)
        if show_full_screen:
            self.showFullScreen()
        else:
            self.resize(width, height)
        # 主中心部件和布局  The main central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 存储所有控件的字典  The dictionary to store all widgets
        self.widgets: dict[str, list[T|list[float]]] = {}
        
        # 当前窗口尺寸  The current window size
        self.window_width = width
        self.window_height = height

        #存储所有GUI显示控件  The dictionary to store all GUI display widgets
        self.all_GUI: dict[str, tuple[str]] = {}

        # 连接窗口大小改变事件  The event when the window size changes
        self.resizeEvent = self.on_resize


    def update_widget_positions(self):
        # 获取窗口的宽度和高度  Get the width and height of the window
        window_width = self.width()
        window_height = self.height()
        for i in self.widgets:
            x = int(self.widgets[i][1][0] * window_width -
                    self.widgets[i][0].width() / 2)
            y = int(self.widgets[i][1][1] * window_height -
                    self.widgets[i][0].height() / 2)
            self.widgets[i][0].move(x, y)


    def on_resize(self, event):
        # 窗口大小改变时更新子QWidget的位置  Update the position of the child QWidget when the window size changes
        super().resizeEvent(event)
        self.update_widget_positions()       


    def update_relx_and_rely(self, name: str, relx: float, rely: float):
        #更新指定控件的relx与rely  Update the relx and rely of the specified widget
        if name not in self.widgets:
            raise ValueError(f"no such a widget: '{name}'")
        self.widgets[name][1][0] = relx
        self.widgets[name][1][1] = rely
        self.update_widget_positions()


    def true_x_y_to_relx_rely(self, name: str, x: int=0, y: int=0):
        #指定控件的准确xy换算成relx与rely  Convert the exact xy of the specified widget to relx and rely
        window_width = self.width()
        window_height = self.height()
        if name not in self.widgets:
            raise ValueError(f"no such a widget: '{name}'")
        self.widgets[name][0].move(x, y)
        self.widgets[name][1][0] = (x + self.widgets[name][0].width() / 2)/window_width
        self.widgets[name][1][1] = (x + self.widgets[name][0].height() / 2)/window_height
            

    def add_widget(self, widget_type: type[T], name: str, relx: float=0, rely: float=0, **kwargs):
        """添加控件到窗口  Add a widget to the window
        
        Args:
            widget_type: 控件类型类  The class of the widget type
            name: 控件名称(作为字典键)  The name of the widget (as the dictionary key)
            relx: 相对x位置(0-1)  Relative x position (0-1)
            rely: 相对y位置(0-1)  Relative y position (0-1)
            kwargs: 传递给控件的其他参数  Other parameters passed to the widget
        """
        if name in self.widgets:
            raise ValueError(f"Widget with name '{name}' already exists")
            
        widget = widget_type(parent=self.central_widget, **kwargs)
        self.widgets[name] = [widget, [relx, rely]]
        
        # 计算绝对位置      Calculate the absolute position
        x = int(relx * self.window_width)
        y = int(rely * self.window_height)
        
        widget.move(x, y)
        self.update_widget_positions()
        return widget
    

    def add_GUI(self, name, *args):
        #添加GUI显示控件  Add GUI display widgets
        if name in self.all_GUI:
            raise ValueError(f"GUI with name '{name}' already exists")
        for i in args:
            if not isinstance(i, str):
                raise TypeError(f"the name of the widget must be 'str'")
            if i not in self.widgets:
                raise ValueError(f"no such a widget: '{i}'")
        self.all_GUI[name] = args


    def show_GUI(self, name: str):
        #显示指定的GUI控件  Show the specified GUI widgets
        if name not in self.all_GUI:
            raise ValueError(f"no such a GUI: '{name}'")
        for i in self.widgets:
            if i in self.all_GUI[name]:
                self.widgets[i][0].show()
            else:
                self.widgets[i][0].hide()


    def add_button(self, name, text, relx=0, rely=0, width=None, height=None, connect_func=None):
        """添加按钮  Add a button"""
        btn = self.add_widget(QPushButton, name, relx, rely)
        btn.setText(text)
        
        if width:
            btn.setFixedWidth(width)
        if height:
            btn.setFixedHeight(height)
            
        if connect_func:
            btn.clicked.connect(connect_func)
            
        return btn

    def add_combobox(self, name, items=None, relx=0, rely=0, width=None, height=None, connect_func=None):
        """添加下拉框  Add a combobox"""
        combo = self.add_widget(QComboBox, name, relx, rely)
        
        if items:
            combo.addItems(items)
            
        if width:
            combo.setFixedWidth(width)
        if height:
            combo.setFixedHeight(height)
            
        if connect_func:
            combo.currentIndexChanged.connect(connect_func)
            
        return combo

    def add_label(self, name, text="", relx=0, rely=0, width=None, height=None):
        """添加标签  Add a label"""
        label = self.add_widget(QLabel, name, relx, rely)
        label.setText(text)
        
        if width:
            label.setFixedWidth(width)
        if height:
            label.setFixedHeight(height)
            
        return label

    def add_lineedit(self, name, text="", relx=0, rely=0, width=None, height=None, connect_func: Callable[[], None]=None):
        """添加单行文本框  Add a line edit"""
        line_edit = self.add_widget(QLineEdit, name, relx, rely)
        line_edit.setText(text)
        
        if width:
            line_edit.setFixedWidth(width)
        if height:
            line_edit.setFixedHeight(height)
            
        if connect_func:
            line_edit.textChanged.connect(connect_func)
            
        return line_edit

    def add_textedit(self, name, text="", relx=0, rely=0, width=None, height=None):
        """添加多行文本框  Add a text edit"""
        text_edit = self.add_widget(QTextEdit, name, relx, rely)
        text_edit.setText(text)
        
        if width:
            text_edit.setFixedWidth(width)
        if height:
            text_edit.setFixedHeight(height)
            
        return text_edit

    def add_checkbox(self, name, text="", relx=0, rely=0, connect_func: Callable[[], None]=None):
        """添加复选框  Add a checkbox"""
        checkbox = self.add_widget(QCheckBox, name, relx, rely)
        checkbox.setText(text)
        
        if connect_func:
            checkbox.stateChanged.connect(connect_func)
            
        return checkbox

    def add_radiobutton(self, name, text="", relx=0, rely=0, connect_func: Callable[[], None]=None):
        """添加单选按钮  Add a radio button"""
        radio = self.add_widget(QRadioButton, name, relx, rely)
        radio.setText(text)
        
        if connect_func:
            radio.toggled.connect(connect_func)
            
        return radio

    def add_spinbox(self, name, value=0, min_val=0, max_val=100, relx=0, rely=0, connect_func: Callable[[], None]=None):
        """添加整数微调框  Add a spin box"""
        spin = self.add_widget(QSpinBox, name, relx, rely)
        spin.setValue(value)
        spin.setMinimum(min_val)
        spin.setMaximum(max_val)
        if connect_func:
            spin.valueChanged.connect(connect_func)
        return spin
