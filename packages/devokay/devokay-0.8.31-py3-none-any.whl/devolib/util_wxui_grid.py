# -*- coding: utf-8 -*-
# python3

import wx
import wx.grid


'''

		col-1	col-2	col-3	col-4

row-1    aa		  bb	  cc	  dd

row-2	 xx		  yy   ...

{
	'row-1' : {
		'col-1' : aa,
		'col-2' : bb,
		'col-3' : cc,
	}
}

aa , bb , cc , dd , xx , yy , ......:
{
	'value'   : True/False/String...
	'data'    : $dataItem,

	'bgcolor' : True,
	'readonly': False,
}





'''
#
def _________MatrixCell_________():
	pass
#
class MatrixCell( wx.grid.GridCellAttr ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		self.SetAlignment( wx.ALIGN_CENTRE , wx.ALIGN_CENTRE )
		#
		self.__text__ = None
		#
		self.__data__ = None
		#
		self.__bool__ = True
		#
	#
	def SetCellText( self , text ):
		#
		self.__text__ = text
		#
		return self
		#
	#
	def GetCellText( self ):
		#
		return f"{self.__text__}"
		#
	#

	#
	def SetCellData( self , data ):
		#
		self.__data__  = data
		#
		return self
		#
	#
	def GetCellData( self ):
		#
		return self.__data__
		#
	#



	#
	def SetBgColor( self , color ):
		#
		if color is not None:
			self.SetBackgroundColour( color )
		#
		return self
		#
	#
	def SetReadOnly( self ):
		#
		super().SetReadOnly( True )
		#
		return self
		#


#
class CheckedMatrixCell( MatrixCell ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		self.SetReadOnly()
		#
		self.__checkable__ = False
		#
		self.__checked__   = False
		#
	#
	def GetCellText( self ):
		#
		if not self.IsCheckable():
			return super().GetCellText()
		#
		if self.IsChecked():
			return f"[√]{super().GetCellText()}"
		#
		else:
			return f"[ ]{super().GetCellText()}"
		#
	#
	def IsChecked( self ):
		#
		return self.__checked__
		#
	#
	def ToggleCheckbox( self ):
		#
		if not self.IsCheckable():
			return self
		#
		self.__checked__ = not self.__checked__
		#
		return self
		#
	#
	def UnCheck( self ):
		#
		self.__checked__ = False
		#
	#
	def SetCheckable( self ):
		#
		self.__checkable__ = True
		#
		return self
		#
	#
	def IsCheckable( self ):
		#
		return self.__checkable__
		#
	#






#
def _________Matrix_________():
	pass
#
class wxMatrix( wx.grid.Grid ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		# Rows
		self.__rows__ = []
		#
		# Cols
		self.__cols__ = []
		#
		# Data Saved
		self.__matrix__ = None
		#
	#
	def Clear( self ):
		#
		if self.GetNumberRows() > 0:
			try:
				self.DeleteRows( pos = 0 , numRows = self.GetNumberRows() )
			except Exception as e:
				print( e )
				pass
		#
		if self.GetNumberCols() > 0:
			try:
				self.DeleteCols( pos = 0 , numCols = self.GetNumberCols() )
			except Exception as e:
				print( e )
				pass
		#
		return self
		#
	#
	def ReadOnlyStringMatrixCell( self ):
		#
		_attr = wx.grid.GridCellAttr()
		#
		_attr.SetRenderer( wx.grid.GridCellStringRenderer() )
		_attr.SetReadOnly()
		#
		return _attr
		#

	#
	def ParseMatrixData( self , matrixData , rowList = [] , colList = [] ):
		#
		if isinstance( matrixData , dict ):
			#
			return self.ParseNamedMatrixData( matrixData , rowList , colList )
			#
		#
		if isinstance( matrixData , list ):
			#
			return self.ParseListMatrixData( matrixData , rowList , colList )
			#
		#
		raise Exception( f"Invalid Matrix Data: {type(matrixData)}" )
		#

	#
	def ParseNamedMatrixData( self , matrixData , rowList = [] , colList = [] ):
		#
		print( 'ParseNamedMatrixData()')
		#
		# 1. Row List
		_rowList = list( matrixData.keys() )
		#
		# 2. Col List
		_colDict = {}
		for _row , _colData in matrixData.items():
			#
			for _col in _colData.keys():
				_colDict[_col] = _col
			#
		#
		_colList = list(_colDict.keys() )
		#
		# 3. Fix Matrix Data
		for _row , _colData in matrixData.items():
			#
			for _col in _colList:
				#
				if _col not in matrixData[_row]:
					matrixData[_row][_col] = None
				#
			#
		#
		self.__rows__   = _rowList
		self.__cols__   = _colList
		self.__matrix__ = matrixData
		#
		return ( self.__rows__ , self.__cols__ , self.__matrix__ )
		#

	#
	def ExtendList( self , listData , toLength , padding ):
		#
		if len(listData) < toLength:
			return listData + padding * ( toLength - len(listData) )
		#
		return listData
		#

	#
	def ParseListMatrixData( self , matrixData , rowList = [] , colList = [] ):
		#
		print( 'ParseListMatrixData()')
		#
		# 1. Rows
		#
		_rowList   = self.ExtendList( rowList , len(matrixData) , [''] )
		#
		matrixData = self.ExtendList( matrixData , len(_rowList) , [ [] ] )
		#

		#
		# 2. Cols
		#
		_colList = self.ExtendList( colList , max( [ len(_row) for _row in matrixData ] ) , [''] )
		#
		_colLength = len(_colList)
		#
		self.__rows__   = _rowList
		self.__cols__   = _colList
		self.__matrix__ = [ self.ExtendList( _row , _colLength , [None] ) for _row in matrixData ]
		#
		return ( self.__rows__ , self.__cols__ , self.__matrix__ )
		#


	#
	def SetMatrix( self , matrixData , rowList = [] , colList = [] ):
		#
		print( 'SetMatrix()')
		#
		_rowList , _colList , _matrixData = self.ParseMatrixData( matrixData )
		#
		# 1. Clear
		self.Clear()
		#
		# 2. Adjust Grid
		self.SetRows( _rowList )
		self.SetCols( _colList )
		#
		# 3. Set Attr According to Data
		#
		for _rowIdx , _rowName in enumerate( self.__rows__ ):
			#
			for _colIdx , _colName in enumerate( self.__cols__ ):
				#
				#_val = self.GetMatrixCell( _rowName , _colName )
				#
				#print( _rowIdx , _rowName , _colIdx , _colName )
				#
				_cell = self.GetMatrixCell( _rowIdx , _colIdx )
				#
				print( _rowIdx , _colIdx , _cell )
				#
				if isinstance( _cell , MatrixCell ):
					#
					self.SetAttr( _rowIdx , _colIdx , _cell )
					self.SetCellValue( _rowIdx , _colIdx , _cell.GetCellText() )
					#
					continue
					#
				#
				raise Exception( f"Cell Not Valid: {_cell}" )
				#
			#
		#



	#
	def SetRows( self , rowList ):
		#
		_adjust = len(rowList) - self.GetNumberRows()
		#
		# 1. Adjust Size
		if _adjust > 0:
			#
			self.AppendRows( _adjust )
			#
		elif _adjust < 0:
			#
			self.DeleteRows( numRows = abs(_adjust) )
			#
		#
		# 2. Set Labels
		for _idx in range( len(rowList) ):
			#
			self.SetRowLabelValue( _idx , rowList[_idx] )
			#
		#
		return self
		#
	#
	def SetCols( self , colList ):
		#
		_adjust = len(colList) - self.GetNumberCols()
		#
		# 1. Adjust Size
		if _adjust > 0:
			#
			self.AppendCols( _adjust )
			#
		elif _adjust < 0:
			#
			self.DeleteCols( numCols = abs(_adjust) )
			#
		#
		# 2. Set Labels
		for _idx in range( len(colList) ):
			#
			self.SetColLabelValue( _idx , colList[_idx] )
			#
		#
		return self
		#
	#
	def GetMatrixCell( self , row , col ):
		#
		if isinstance( self.__matrix__ , dict ):
			#
			if isinstance( row , int ):
				row = self.__rows__[row]
			#
			if isinstance( col , int ):
				col = self.__cols__[col]
			#
		#
		return self.__matrix__[row][col]
		#
#

#
# Use Name as Row & Col Indexes
#
class NamedCheckMatrix( wxMatrix ):
	#
	def __init__( self , *args , **kwargs ):
		#
		super().__init__( *args , **kwargs )
		#
		# List Text Show
		self.__list__ = []
		#
		# Data Saved
		self.__matrix__ = {}
		#
		self.CreateGrid( 0 , 0 )
		#
		#
		# Looks Like Disable Selection
		#self.SetSelectionBackground( self.GetDefaultCellBackgroundColour() )
		#self.SetSelectionForeground( self.GetDefaultCellTextColour() )
		#
		#
		self.Bind( wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK , self.__OnMouseLeftClick__ , self )
		#
		# Cell Select
		self.Bind( wx.grid.EVT_GRID_CMD_RANGE_SELECT , self.__OnCellSelect__ , self )
		#self.Bind( wx.grid.EVT_GRID_CMD_SELECT_CELL , self.__OnCellSelect__ , self )
		#
	#
	def __OnCellSelect__( self , event ):
		#
		print( 'OnCellSelect()' )
		#
		if event.Selecting():
			self.ClearSelection()
		#
	#
	def __OnMouseLeftClick__( self , event ):
		#
		print( '\n\n\n\nOnMouseLeftClick' )
		#
		_row = event.GetRow()
		_col = event.GetCol()
		#
		# Get Cell
		#
		_cell = self.GetMatrixCell( _row , _col )
		#
		print( _cell.GetCellText() )
		#
		if not isinstance( _cell , CheckedMatrixCell ):
			#
			self.ClearSelection()
			#
			return
			#
		#
		_cell.ToggleCheckbox()
		#
		self.SetCellValue( _row , _col , _cell.GetCellText() )
		#
		self.ClearSelection()
		#
		event.Skip()
		#
	#
	#
	def UnCheckAll( self ):
		#
		for _rowIdx , _rowName in enumerate( self.__rows__ ):
			#
			for _colIdx , _colName in enumerate( self.__cols__ ):
				#
				_cell = self.GetMatrixCell( _rowIdx , _colIdx )
				#
				if isinstance( _cell , CheckedMatrixCell ) and _cell.IsChecked():
					#
					_cell.UnCheck()
					#
					self.SetCellValue( _rowIdx , _colIdx , _cell.GetCellText() )
					#
					continue
					#
				#
			#
		#
	#
	def GetCheckedList( self ):
		#
		_checkedList = []
		#
		for _rowIdx , _rowName in enumerate( self.__rows__ ):
			#
			for _colIdx , _colName in enumerate( self.__cols__ ):
				#
				_cell = self.GetMatrixCell( _rowIdx , _colIdx )
				#
				if isinstance( _cell , CheckedMatrixCell ) and _cell.IsChecked():
					#
					_checkedList.append( _cell.GetCellData() )
					#
					continue
					#
			#
		#
		return _checkedList
		#