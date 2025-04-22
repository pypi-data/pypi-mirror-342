#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx
from devolib.util_wxui_options import *
from devolib.util_wxui_grid import *


class JussSportUIFrame(wx.Frame):
    def __init__(self, *args, **kwds):
		
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		
        wx.Frame.__init__(self, *args, **kwds)
		
        self.SetTitle(u"Omni Helper App")
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 800))
        self.Center()

        panel = wx.Panel(self)
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        outer_sizer.AddStretchSpacer(1)  # 弹性空间，可以将sample panel 推到底部

        ###################################### sample panel
        self.sample_panel = wx.Panel(panel)
        self.sample_panel.SetBackgroundColour(wx.Colour(200, 200, 255))

        self.sample_panel.SetMinSize((-1, 200))
        # outer_sizer.Add(self.sample_panel, flag=wx.ALL, border=40)
        outer_sizer.Add(self.sample_panel, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=40)

        self.sample_panel_box = wx.StaticBox(self.sample_panel, label="Sample Panel")
        self.sample_panel_sizer = wx.StaticBoxSizer(self.sample_panel_box, wx.VERTICAL)
        self.sample_panel_sizer.Add((20, 10), 0, 0, 0)
	
        ###################################### input
        input_div_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sample_panel_sizer.Add(input_div_sizer, 0, wx.EXPAND, 0)

        input_div_sizer.Add((20, 20), 0, 0, 0)

        labelAuth = wx.StaticText(self.sample_panel, wx.ID_ANY, u"Input: ")
        input_div_sizer.Add(labelAuth, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        ###################################### button
        self.button = wx.Button(self.sample_panel, wx.ID_ANY, u"Button")
        input_div_sizer.Add(self.button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

        input_div_sizer.Add((20, 20), 0, 0, 0)

        self.sample_panel_sizer.Add((20, 10), 0, 0, 0)

        

        ###################################### Select
        select_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sample_panel_sizer.Add(select_sizer, 0, wx.EXPAND, 0)

        select_sizer.Add((20, 20), 0, 0, 0)

        labelStadiumList = wx.StaticText(self.sample_panel, wx.ID_ANY, u"Select: ")
        select_sizer.Add(labelStadiumList, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.select = SelectList(self.sample_panel, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.select.SetMinSize((300, 23))
        select_sizer.Add(self.select, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sample_panel_sizer.Add((20, 10), 0, 0, 0)

        ###################################### grid
        sizerGrid = wx.BoxSizer(wx.HORIZONTAL)
        self.sample_panel_sizer.Add(sizerGrid, 0, wx.EXPAND, 0)

        sizerGrid.Add((20, 20), 0, 0, 0)

        labelGroundBlock = wx.StaticText(self.sample_panel, wx.ID_ANY, u"Grid: ")
        sizerGrid.Add(labelGroundBlock, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.matrixGroundTime = NamedCheckMatrix(self.sample_panel, wx.ID_ANY)
        sizerGrid.Add(self.matrixGroundTime, 1, wx.EXPAND, 0)

        self.sample_panel_sizer.Add((20, 10), 0, 0, 0)

        ###################################### spin
        spin_div_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sample_panel_sizer.Add(spin_div_sizer, 0, wx.EXPAND, 0)

        spin_div_sizer.Add((20, 20), 0, 0, 0)

        spin_div_title = wx.StaticText(self.sample_panel, wx.ID_ANY, u"Spin: ")
        spin_div_sizer.Add(spin_div_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.spin_div_spin = wx.SpinCtrl(self.sample_panel, wx.ID_ANY, "500", min=0, max=5000)
        spin_div_sizer.Add(self.spin_div_spin, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        ###################################### container
        self.sample_panel.SetSizer(self.sample_panel_sizer)
        panel.SetSizer(outer_sizer)

        self.Layout()

        ###################################### Action handler
        self.Bind(wx.EVT_BUTTON, self.onButtonClicked, self.button)
        self.Bind(wx.EVT_COMBOBOX, self.onListSelected, self.select)
        # self.Bind(wx.EVT_COMBOBOX, self.onSportVenuesChange, self.selectSportVenuesList)
        # self.Bind(wx.EVT_COMBOBOX, self.onVenuesDateChange, self.selectVenuesDateList)
        # self.Bind(wx.EVT_BUTTON, self.onClickAddOrder, self.buttonAddOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickRemoveOrder, self.buttonRemoveOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickEmptyOrder, self.buttonEmptyOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickTestOrder, self.buttonTestOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickManualOrder, self.buttonManualOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickFastOrder, self.buttonFastOrder)
        # self.Bind(wx.EVT_BUTTON, self.onClickStopFastOrder, self.buttonFastOrderStop)
        self.Bind(wx.EVT_CLOSE, self.onClose, self)

    def onButtonClicked(self, event):
        print("onButtonClicked")
        event.Skip()

    def onListSelected(self, event):
        print("onListSelected")
        event.Skip()

    def onClose(self, event):
        print("onClose")
        event.Skip()

class ApplicationUI(wx.App):
	def OnInit(self):
		self.JussSportUI = JussSportUIFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.JussSportUI)
		self.JussSportUI.Show()
		return True

if __name__ == "__main__":
	app = ApplicationUI(0)
	app.MainLoop()
