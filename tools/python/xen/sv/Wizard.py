from xen.sv.util import *
from xen.sv.HTMLBase import HTMLBase
from xen.xend import sxp

DEBUG = 1

class Wizard( HTMLBase ):

    def __init__( self, urlWriter, title, sheets ):
        HTMLBase.__init__( self )
        self.title = title
        self.sheets = sheets
        self.urlWriter = urlWriter
        
    def write_MENU( self, request ):
    	request.write( "<p class='small'><a href='%s'>%s</a></p>" % (self.urlWriter( '' ), self.title) ) 
    
    def write_BODY( self, request ):
        
   	request.write( "<table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td>" )
        request.write( "<p align='center'><u>%s</u></p></td></tr><tr><td>" % self.title )
        
        currSheet = getVar( 'sheet', request )
    
        if not currSheet is None:
            currSheet = int( currSheet )
        else:
            currSheet = 0
            
        op = getVar( 'op', request )
        
        if op == 'next':
            currSheet += 1
        elif op == 'prev':
             currSheet -= 1
             
        sheet = self.sheets[ currSheet ]( self.urlWriter )    
            
        sheet.parseForm( request )
        sheet.write_BODY( request )
        
        request.write( "</td></tr><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr>" )
        request.write( "<td width='80%'></td><td width='20%' align='center'><p align='center'>" )
	if currSheet > 0:
       	    request.write( "<img src='images/previous.png' onclick='doOp( \"prev\" )' onmouseover='update( \"wizText\", \"Previous\" )' onmouseout='update( \"wizText\", \"&nbsp;\" )'>&nbsp;" )
        if currSheet < ( len( self.sheets ) - 2 ):        
            request.write( "<img src='images/next.png' onclick='doOp( \"next\" )' onmouseover='update( \"wizText\", \"Next\" )' onmouseout='update( \"wizText\", \"&nbsp;\" )'>" )
        elif currSheet == ( len( self.sheets ) - 2 ):
            request.write( "<img src='images/finish.png' onclick='doOp( \"next\" )' onmouseover='update( \"wizText\", \"Finish\" )' onmouseout='update( \"wizText\", \"&nbsp;\" )'>" )
        request.write( "</p><p align='center'><span id='wizText'></span></p></td></tr></table>" )
        request.write( "</td></tr></table>" )
        
    def op_next( self, request ):
    	pass
        
    def op_prev( self, request ):
    	pass
        
    def op_finish( self, request ):
    	pass  
        
class Sheet( HTMLBase ):

    def __init__( self, urlWriter, title, location ):
        HTMLBase.__init__( self )
        self.urlWriter = urlWriter
        self.feilds = []
        self.title = title
        self.location = location
        self.passback = "()"
        
    def parseForm( self, request ):
    	do_not_parse = [ 'mod', 'op', 'sheet' ] 
    
    	passed_back = request.args
        
        temp_passback = passed_back.get( "passback" )
        
        if temp_passback is not None and len( temp_passback ) > 0:
            temp_passback = temp_passback[ len( temp_passback )-1 ]
        else:
            temp_passback = "( )"        
        
        last_passback = ssxp2hash( string2sxp( temp_passback ) ) #use special function - will work with no head on sxp
        
        if DEBUG: print last_passback
        
        try: 
            del passed_back[ 'passback' ]
        except:
            pass
        
        for (key, value) in passed_back.items():
            if key not in do_not_parse:
                last_passback[ key ] = value[ len( value ) - 1 ]
                
        self.passback = sxp2string( hash2sxp( last_passback ) ) #store the sxp
        
        if DEBUG: print self.passback
        
    def write_BODY( self, request ):
        
   	request.write( "<p>%s</p>" % self.title )
    
    	previous_values = sxp2hash( string2sxp( self.passback ) ) #get the hash for quick reference
        
        request.write( "<table width='100%' cellpadding='0' cellspacing='1' border='0'>" )
        
    	for (feild, control) in self.feilds:
            control.write_Control( request, previous_values.get( feild ) )
            
        request.write( "</table>" )
            
        request.write( "<input type='hidden' name='passback' value=\"%s\"></p>" % self.passback )
        request.write( "<input type='hidden' name='sheet' value='%s'></p>" % self.location )
        
    def addControl( self, control ):
    	self.feilds.append( [ control.getName(), control ] )
        
class SheetControl( HTMLBase ):

    def __init__( self ):
        HTMLBase.__init__( self )
        self.name = ""
        
    def write_Control( self, request, persistedValue ):
        request.write( "<tr colspan='2'><td>%s</td></tr>" % persistedValue )
        
    def validate( self ):
    	return True
        
    def getName( self ):
    	return self.name
        
    def setName( self, name ):
    	self.name = name
        
class InputControl( SheetControl ):

    def __init__( self, name, defaultValue, humanText):
        SheetControl.__init__( self )
        self.setName( name )
        
        self.defaultValue = defaultValue
        self.humanText = humanText
        
    def write_Control( self, request, persistedValue ):
    	if persistedValue is None:
            persistedValue = self.defaultValue
        
        request.write( "<tr><td width='50%%'><p>%s</p></td><td width='50%%'><input type='text' name='%s' value=\"%s\"></td></tr>" % (self.humanText, self.getName(), persistedValue) )

class TextControl( SheetControl ):

    def __init__( self, text ):
    	SheetControl.__init__( self )
        self.text = text
        
    def write_Control( self, request, persistedValue ):
    	request.write( "<tr><td colspan='2'><p>%s</p></td></tr>" % self.text )

class SmallTextControl( SheetControl ):

    def __init__( self, text ):
    	SheetControl.__init__( self )
        self.text = text
        
    def write_Control( self, request, persistedValue ):
    	request.write( "<tr><td colspan='2'><p class='small'>%s</p></tr></td>" % self.text )
        
                 
            
    
      
