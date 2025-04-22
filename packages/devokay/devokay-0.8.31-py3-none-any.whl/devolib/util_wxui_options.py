#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# CopyLeft 2023 W.H.J.
#
#

#
import wx
#

#
class wxSelect:
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		# List Text Show
		self.__list__ = []
		#
		# Data Saved
		self.__data__ = {}
		#
	#
	def Clear( self ):
		#
		super().Clear()
		#
		self.__list__ = []
		#
		self.__data__ = {}
		#
		return self
		#
	#
	def GetSelectList( self ):
		#
		return self.__data__
		#
	#
	def RemoveSelect( self , selectKeyList ):
		#
		if isinstance( selectKeyList , str ):
			selectKeyList = [ selectKeyList ]
		#
		for _key in selectKeyList:
			#
			if _key in self.__data__:
				#
				del self.__data__[_key]
				#
			#
		#
		return self.SetSelect( self.__data__ )
		#

	#
	def AppendSelect( self , selectData ):
		#
		if isinstance( selectData , list ):
			return self.AppendSelectList( selectData )
		#
		if isinstance( selectData , dict ):
			return self.AppendSelectDict( selectData )
		#
		raise Exception( f"Invalid Data Type: `{type(selectData)}` found but `dict` or `list` required." )
		#
	#
	def AppendSelectList( self , textList ):
		#
		return self.AppendSelectDict( { _text : _text for _text in textList } )
		#
	#
	def AppendSelectDict( self , dataDict ):
		#
		_appendList = list( dataDict.keys() )
		#
		for _key in _appendList:
			#
			# Already Exists
			if _key in self.__data__:
				raise Exception( f"Key Already In SelectList: {_key}" )
			#
		#
		self.__list__ += _appendList
		self.__data__.update( dataDict )
		#
		self.AppendItems( _appendList )
		#



	#
	def SetSelect( self , selectData ):
		#
		if isinstance( selectData , list ):
			return self.SetSelectList( selectData )
		#
		if isinstance( selectData , dict ):
			return self.SetSelectDict( selectData )
		#
		raise Exception( f"Invalid Data Type: `{type(selectData)}` found but `dict` or `list` required." )
		#
	#
	def SetSelectList( self , textList ):
		#
		return self.SetSelectDict( { _text : _text for _text in textList } )
		#
	#
	def SetSelectDict( self , dataDict ):
		#
		if not isinstance( dataDict , dict ):
			raise Exception( f"Invalid Data Type: `{type(dataDict)}` found but `dict` required." )
		#
		# 1. Clear Data
		self.Clear()
		#
		# 2. Set Data
		#
		self.__list__ = list( dataDict.keys() )
		#
		self.__data__ = dataDict
		#
		self.AppendItems( self.__list__ )
		#


#
class SelectList( wxSelect , wx.ComboBox ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		# 1. members
		#
		self.__now_select_value__  = None
		#
		self.__last_select_value__ = None
		#
		self.__on_select_change__  = False
		#
		self.__auto_select_first__ = False
		#

		#
		# 2. events
		#
		self.Bind( wx.EVT_COMBOBOX , self.__OnSelectChange__ , self )
		#
	#
	def GetText( self ):
		#
		return self.GetStringSelection()
		#
	#
	# Get Selected Value with String
	def GetValue( self ):
		#
		_key = self.GetText()
		if _key not in self.__data__:
			return None
		#
		return self.__data__[_key]
		#
	#
	#
	def IsChanged( self ):
		#
		if self.__on_select_change__ is True:
			return self.__last_select_value__ == self.__now_select_value__
		#
		return False
		#
	#
	def __OnSelectChange__( self , event ):
		#
		self.__on_select_change__ = True
		#
		self.__last_select_value__ = self.__now_select_value__
		#
		self.__now_select_value__  = self.GetValue()
		#
		event.Skip()
		#
	#



#
class MultiSelectList( wxSelect , wx.CheckListBox ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
	#