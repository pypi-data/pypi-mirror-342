#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import json

try:
	from .omni_api_gmt import *
except:
	from omni_api_gmt import *

try:
	from .omni_helper_ui import *
except:
	from omni_helper_ui import *


import wx
from wx.lib.embeddedimage import PyEmbeddedImage


class JussSportItem:
	def __init__( self , item ):
		self.__item__ = item
		self.__date__ = None
	#
	def GetData( self ):
		return self.__item__
	#
	#
	def GetDate( self ):
		#
		if self.__date__ is None:
			#
			_date = time.strftime( "%m-%d" , time.localtime( self.GetItemData('startTime') // 1000 ) )
			_date = _date.split('-')
			#
			self.__date__ = f"{_date[0]}月{_date[1]}日"
			#
		#
		return self.__date__
		#
	#
	def GetTimeBlock( self ):
		#
		_startBlock = time.strftime( "%H:%M" , time.localtime( self.GetItemData('startTime') // 1000 ) )
		_endBlock   = time.strftime( "%H:%M" , time.localtime( self.GetItemData('endTime') // 1000 ) )
		#
		return f"[{_startBlock}-{_endBlock}]"
		#
	#
	def GetGroundName( self ):
		#
		return f"{self.GetItemData('groundId')}-{self.GetItemData('groundName')}"
		#
	#
	def GetOrderKey( self ):
		#
		return f"{self.GetGroundName()}@{self.GetTimeBlock()}@{self.GetDate()}"
		#

	#
	def IsOrderable( self ):
		#
		return self.GetStatus() == 1 and self.IsPriceValid()
		#
	#
	def IsSold( self ):
		#
		return self.GetStatus() == 0
		#
	#
	def IsPriceValid( self ):
		#
		return self.GetPrice() > 0
		#
	#
	def IsCheckable( self ):
		#
		return self.IsOrderable()
		#
	#

	#
	def GetItemData( self , key , default = None ):
		#
		if key not in self.__item__:
			return default
		#
		return self.__item__[key]
		#
	#
	def GetStatus( self ):
		#
		return self.GetItemData('status')
		#
	#
	def GetPrice( self ):
		#
		return self.GetItemData('price')
		#
	#
	def GetColor( self ):
		#
		if self.IsSold():
			return wx.LIGHT_GREY
		#
		if not self.IsPriceValid():
			return wx.LIGHT_GREY
		#
		return None
		#
	#
	def GetText( self ):
		if self.IsSold():
			return '售罄'
		if self.IsOrderable():
			return self.GetPrice()
		if not self.IsPriceValid():
			return '不可预订'
		return None
		
class ApplicationWindow(ApplicationUI):
	#
	def __init__(self, *args, **kwds):
		super().__init__( *args, **kwds )

		self.SetIcon( self.GetFrameIcon() )
		# 场馆表
		self.dataStadiumDict = {}
		#
		# 运动项目表
		self.dataSportDict = {}
		#
		# 场馆运动场地表
		self.dataStadiumSportVenuesDict = {}
		#
		# 场地表
		self.dataGroundListDict = {}
		#
		# 已在订单内的Item订单
		self.dataOrderItemDict = {}
		#
		# 任务执行
		self.fastOrderRunning  = False
		#
		# 运行锁
		self.Lock = threading.Lock()

	def ResizeWindow( self ):
		self.batchToolSizer.Fit(self)
		self.Layout()

	def LockItem( self ):
		[ _item.Disable() for _item in self.lockListChain ]

	def UnlockItem( self ):
		[ _item.Enable() for _item in self.lockListChain ]

	def _________():
		pass
	#----------------------------------------------------------
	def GetFrameIcon( self ):
		return PyEmbeddedImage(b'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K//teyv/7Xkp/++MR//97uP//efa//nBnv/5wZ7/+cGe//nBnv/5wZ7/+cCe//nAnv/5wJ3W9ZNY6PWUWP/1lFj/9ZRX//WTV//1k1f/9pRX/+uKSv/2387/+tS6/+58Lv/teyz/7Xss/+17LP/teyz/7Xss/+17LP/teyz/7Xss/+17LP/teyz/7nwu//nQtP/+8+z/+sWk//nCn//5wp//+cKf//nCn//5wp//+cGf//nBn+n1lVn79ZVZ//WVWf/1lVn/9ZRZ//aVWf/xjk//4YA8//ns4f/4yqv/7nss/+58Lv/ufC3/7nwu/+58Lv/ufC3/7nwt/+58Lf/ufC3/7nwt/+58Lv/ueir/9reN//748//6yav/+cKg//nDof/5w6H/+cOh//nCof/5wqD/+cKg/PWVW/v1llv/9ZZb//WVWv/1lVr/9pVa/+d+N//ceTD/+uzi//jKq//uey3/7nwv/+58L//ufC//7nwv/+58L//ufC//7nwv/+58L//ufC//7nwv/+56K//2uI7//vj0//rKrP/5w6L/+cSi//nEov/5xKL/+cOi//nDov/5w6L79Zdc6PWXXP/2l1z/9Zdc//aXXf/wjU7/3G8f/9txI//2383/+ta9/+9+Mv/vfTD/730w/+99MP/vfTD/730w/+99MP/vfTD/730w/+99MP/vfTD/734y//nSt//+8+3/+seo//nEpP/5xKT/+cWk//nEpP/5xKT/+cSk//nEo+j2mF7W9phe//aYXv/2mF7/9ZZb/+R7Mv/aaxj/2msZ/+++mf/98Of/8ZBP/+98L//vfjH/734x/+9+Mf/vfjH/734x/+9+Mf/vfjH/734x/+98L//xkE///e/m//3p3f/5xqb/+sal//rGpv/5xaX/+cWl//nFpf/5xaX/+cWl1vaZX6P2mV//9plf//aZYP/ui0n/3W4c/9xsGf/bahb/5JBS//328P/4xKL/734z/+9+Mv/vfjP/734z/+9+Mv/vfjL/734y/+9+Mv/vfjL/734z//fBnf//+/r/+9W+//rGpv/6x6f/+san//nGp//6xqf/+san//rGpv/6xqaz9pphZfaaYfr2mmH/9JZb/+N4K//dbBj/3W0Z/91sGf/dbx3/8L2Y//738//2tIj/8H81//B9Mv/wfzT/8H80//B/NP/wfzT/8H4y//B/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').GetIcon()
	#
	def showErrorMessage( self , message ):
		wx.MessageBox( message, '错误', wx.OK | wx.ICON_ERROR)

	#
	def showMessage( self , message ):
		wx.MessageBox( message, '提示', wx.OK | wx.ICON_INFORMATION )

	#----------------------------------------------------------
	def getAuthorization( self ):
		#
		_string = self.authorizationBearer.GetValue().strip()
		_string = _string.split(' ')[-1]
		#
		return _string
		#
	#
	def _________():
		pass
	#
	'''
	{
		"week": "今天",
		"date": 1698508800000,
		"dateStr": "10月29日"
	}
	'''
	#
	def _________():
		pass
	#
	# 封装获取 CellItem
	#
	def getMatrixCellItem( self , item ):
		#
		_item = JussSportItem( item )
		#
		_cell = CheckedMatrixCell()
		_cell.SetCellData( _item )
		_cell.SetCellText( _item.GetText() )
		_cell.SetBgColor( _item.GetColor() )
		#
		if _item.IsCheckable():
			_cell.SetCheckable()
		#
		return _cell
		#
	#
	def getTimeBlock( self , blockItem ):
		#
		_startBlock = time.strftime( "%H:%M" , time.localtime( blockItem['startTime'] // 1000 ) )
		_endBlock   = time.strftime( "%H:%M" , time.localtime( blockItem['endTime'] // 1000 ) )
		#
		return f"{_startBlock}-{_endBlock}"
		#
	#
	def getGroundName( self , blockItem ):
		#
		return f"{blockItem['groundId']}-{blockItem['groundName']}"
		#
	#
	# 获取场地列表
	#
	def fetchVenuesGroundMatrix( self , venuesId , sportType , skuId , startTime ):
		#
		_blockData = JussSportApi.getBlockGround( venuesId , sportType , skuId , startTime )
		#
		#_matrixList = []
		#
		_matrixData = {}
		#
		for _model in _blockData['modelList']:
			#
			# 1. Rows (Time Block)
			_row = self.getTimeBlock( _model )
			#
			if _row not in _matrixData:
				_matrixData[_row] = {}
			#
			# 2. Cols ( Ground Name )
			#
			#_rowList = []
			#
			for _item in _model['blockModel']:
				#
				_item['name'] = _item['groundName']
				_item['startTime'] = _model['startTime']
				_item['endTime']   = _model['endTime']
				_item['chosen']    = False
				#
				_col = self.getGroundName( _item )
				#
				_matrixData[_row][_col] = self.getMatrixCellItem( _item )
				#
				#
				#_rowList.append( _item )
				#
			#
			#_matrixList.append( _rowList )
			#
		#
		#return _matrixList
		#
		return _matrixData

	#
	# 显示场馆列表: 必须同步数据
	#
	def showStadiumList( self ):
		#
		self.selectStadiumList.SetSelect( self.dataStadiumDict )
		#
	#
	# 获取选定的【场馆】信息
	#
	def getSelectedStadium( self ):
		#
		return self.selectStadiumList.GetValue()
		#
	#
	def _________():
		pass
	#
	# 获取【场馆内】的所有运动项目及对应场地列表
	#
	def getStadiumSportList( self , stadiumId ):
		#
		if stadiumId not in self.dataStadiumSportVenuesDict:
			return None
		#
		return self.dataStadiumSportVenuesDict[stadiumId]
		#
	#
	# 显示【场馆内】的运动项目
	#
	def showStadiumSportList( self ):
		#
		_stadiumItem = self.getSelectedStadium()
		if _stadiumItem is None:
			return self.showErrorMessage( f"你需要选定一个场馆！" )
		#
		_stadiumSportList = self.getStadiumSportList( _stadiumItem['id'] )
		if _stadiumSportList is None:
			return self.showErrorMessage( f"指定场馆【{_stadiumItem['id']}-{_stadiumItem['name']}】有误，请检查数据！" )
		#
		# self.selectSportList.SetSelect( _stadiumSportList )
		#
	#
	# 获取选定的【运动项目】信息
	#
	def getSelectedSport( self ):
		pass
		#
		# return self.selectSportList.GetValue()
		#
	#
	def _________():
		pass
	#
	#
	# 显示【运动项目】的场地列表
	#
	def showStadiumSportVenuesList( self ):
		#
		_sportItem = self.getSelectedSport()
		if _sportItem is None:
			return self.showErrorMessage( f"请选择指定【运动项目】！" )
		#
		#
		_venuesList = _sportItem['venuesList']
		#
		#
		# 1. Sort By VenuesId
		_venuesDict = { _item['venuesId'] : _item for _item in _venuesList }
		#
		_venuesKeys = list(_venuesDict.keys() )
		_venuesKeys.sort()
		#
		# 2. Pack Value
		_venuesData = { f"{_venuesDict[_key]['venuesId']}-{_venuesDict[_key]['venuesTitle']}" : _venuesDict[_key] for _key in _venuesKeys }
		#
		# 3. Set Select
		self.selectSportVenuesList.SetSelect( _venuesData )
		#
	#
	# 获取选定的【运动场地】信息
	#
	def getSelectedSportVenues( self ):
		#
		return self.selectSportVenuesList.GetValue()
		#
	#
	def _________():
		pass
	#
	# 人工获取在往后一天的时间
	def getNextDate( self , startTime ):
		#
		_nextTime = startTime + 60 * 60 * 24 * 1000
		#
		_date = time.strftime( "%m-%d" , time.localtime( _nextTime // 1000 ) )
		_date = _date.split('-')
		_nextDate = f"*{_date[0]}月{_date[1]}日"
		#
		return { _nextDate : { 'date' : _nextTime , 'dateStr' : _nextDate , 'week' : '人工' } }
		#
	#
	# 显示【运动场地】的抢订日期列表
	#
	def showVenuesDateList( self ):
		#
		_venues = self.getSelectedSportVenues()
		if _venues is None:
			return self.showErrorMessage( f"请选择指定【运动场地】！" )
		#
		_blockDateList = JussSportApi.getBlockDate( _venues['venuesId'] )
		#
		_dateData = { _item['dateStr'] : _item for _item in _blockDateList }
		#
		_dateData.update( self.getNextDate( max( [ _item['date'] for _item in _blockDateList ] ) ) )
		#
		self.selectVenuesDateList.SetSelect( _dateData )
		#
	#
	# 获取选定的【抢订日期】信息
	#
	def getSelectedVenuesDate( self ):
		#
		return self.selectVenuesDateList.GetValue()

	def syncStadiumList( self ):
		#
		# 1. Sync Data with Server
		self.dataStadiumDict = { f"{_item['id']}-{_item['name']}" : _item for _item in JussSportApi.getStadiumList() }
		#
		# 2. Show Platform List
		#
	#
	# 同步运动场地表
	#
	def syncVenuesSportData( self ):
		pass
	def syncData( self ):
		pass
	def onClickGetData(self, event):
		pass

	def clearSubSelection( self , event = None ):
		_eventObject = None
		#
		_startClear = False
		if event is None:
			_startClear = True
		else:
			_eventObject = event.GetEventObject()
		#
		for _selectObject in self.checkListChain:
			#
			if _startClear is True:
				_selectObject.Clear()
				continue
			#
			if _eventObject == _selectObject:
				_startClear = True
			#
		#
		#
		self.ResizeWindow()


	def fastOrder( self , venuesId , itemList ):
		pass

	def tryFastOrder( self , selectList , sleepTime = 0 ):
		pass

class ApplicationMain(wx.App):
	def OnInit(self):
		self.window = ApplicationWindow(None, wx.ID_ANY, "")

		self.SetTopWindow(self.window)
		self.uiHandler.Show()

		return True

if __name__ == "__main__":
	app = ApplicationMain(0)
	app.MainLoop()
