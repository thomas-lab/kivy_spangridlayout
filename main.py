#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.button import Button


class MainApp(App):
    def add(self, gd, x, y, w, h):
        print gd, x.text, y.text, w.text, h.text
        x = int(x.text)
        y = int(y.text)
        w = int(w.text)
        h = int(h.text)
        gd.set_widget(Button(text='B %i %i' % (x, y)), x, y, w, h)
        gd.do_layout()

MainApp().run()
