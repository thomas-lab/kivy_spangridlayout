#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout, GridLayoutException
from kivy.properties import NumericProperty, BooleanProperty, DictProperty, \
    BoundedNumericProperty, ReferenceListProperty, VariableListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

class SGridLayoutException(GridLayoutException):
    '''Exception for errors if the grid layout manipulation fails.
    '''
    pass

class SGridLayoutCell(Widget):
    row = NumericProperty(0)
    col = NumericProperty(0)
    swidth = NumericProperty(1)
    sheight = NumericProperty(1)
    index = NumericProperty(0)
    def __call__(self, **kwargs):
        super(SGridLayoutCell, self).__init__(**kwargs)

    def add_widget(self, widget, row=0, col=0, width=1, height=1):
        self.swidth = width
        self.sheight = height
        self.row = row
        self.col = col
        self.widget = widget
        self.bind(pos=widget.setter('pos'))
        if self.swidth == 1:
            self.bind(width=widget.setter('width'))
        else:
            widget.width = self.width * self.swidth
        if self.sheight == 1:
            self.bind(height=widget.setter('height'))
        else:
            widget.height = self.height * self.sheight
        Clock.schedule_once(self.post_init, 0)

    def post_init(self, dt):
        widget = self.widget
        if len(self.children) > 0:
            self.remove_widget(self.children[0])
        super(SGridLayoutCell, self).add_widget(widget)
        Clock.schedule_once(self.post_init2, 0)

    def post_init2(self, dt):
        if len(self.children) == 0:
            return
        if self.swidth > 1:
            self.children[0].width = self.width * self.swidth
        if self.sheight > 1:
            self.children[0].height = self.height * self.sheight



class SGridLayout(GridLayout):
    def __init__(self, *args, **kwargs):
        super(SGridLayout, self).__init__(**kwargs)
        print kwargs
        self.init_done = False

    def add_widget(self, widget, index=0):
        super(SGridLayout, self).add_widget(widget, index)

    def set_widget(self, widget, row=0, col=0, width=1, height=1):
        if not self.init_done:
            self.init()
        index = self.rows * self.cols - (self.cols * row + col) -1
        self.children[index].add_widget(widget, row, col, width, height)

    def do_layout(self, *largs):
        if not self.init_done:
            self.init()
        super(SGridLayout, self).do_layout(*largs)

    def init(self):
        if not self.init_done:
            if self.cols is None or self.rows is None:
               raise SGridLayoutException('cols or rows missing')
            for i in range(self.cols * self.rows):
                t = SGridLayoutCell()
                super(SGridLayout, self).add_widget(t)
            self.init_done = True

    def get_widget(self, row, col):
        index = self.rows * self.cols - (self.cols * row + col) -1
        return self.children[index].children[0]

    def remove_widget(self, row, col):
        index = self.rows * self.cols - (self.cols * row + col) -1
        print row, col, index
        w = self.children[index]
        w.remove_widget(w.children[0])

    def remove_widgets(self,row, col, width, height):
        for i in range(width):
            for j in range(height):
                self.remove_widget(row - i, col + j)

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.button import Button

    class TestApp(App):
        def build(self):
            sg = SGridLayout(rows = 4, cols=5)
            self.sg = sg
            for i in range(sg.rows):
                for j in range(sg.cols):
                    t = SGridLayoutCell()
                 #   t.add_widget(Label(text='L%i' % i))
                    sg.set_widget(t, i, j)
                    sg.set_widget(Button(text='bb %i' % (i * sg.cols + j,)), i, j)
            Clock.schedule_once(self.post_init, 0)
            return sg
        def post_init(self, dt):
            self.sg.remove_widgets(2, 1, 2, 2)
            bt = Button(text='bb')
            self.sg.set_widget(bt, 2, 1, 2, 2)
            print self.sg.get_widget(1, 0).text

    TestApp().run()
    #t.add_widget()
