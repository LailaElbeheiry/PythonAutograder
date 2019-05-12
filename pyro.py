#!/usr/bin/env python
 
 
###THIS MODULE IS COPIED AND EDITTED FROM: https://github.com/JamesStallings/pyro
 
import os
import io
import sys
import code
import re
 
try:
    # Python 3
    import tkinter
    from tkinter import font, ttk, scrolledtext, _tkinter

except ImportError:
    # Python 2
    import Tkinter as tkinter
    import ttk
    import tkFont as font
    import ScrolledText as scrolledtext
import tkMessageBox as messagebox

from pygments.lexers.python import PythonLexer


from pygments.styles import get_style_by_name
 
 
class CoreUI(object):
    """
        CoreUI is the editor object, derived from class 'object'. It's instantiation initilizer requires the
        ubiquitous declaration of the 'self' reference implied at call time, as well as a handle to
        the lexer to be used for text decoration.
    """
    def __init__(self, lexer = PythonLexer(), parent = None):
        self.sourcestamp = {}
        self.filestamp = {}
        self.uiopts = []
        self.lexer = lexer
        self.lastRegexp = ""
        self.markedLine = 0
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.uiconfig()
        self.root.bind("<Key>", self.event_key)
        self.root.bind('<Control-KeyPress-q>', self.close)
        self.text.bind('<Return>', self.autoindent)
        self.text.bind('<Tab>', self.tab2spaces4)
        self.create_tags()
        self.text.edit_modified(False)
        self.bootstrap = [self.recolorize]

        self.filename = "function_class.py"
        self.parent = parent
        
            

        if not os.access(self.filename,os.R_OK):
            os.system("touch " + self.filename)

        with open(self.filename, "r") as f:
            if self.parent.refFunctionBody is not None:
                self.loadfile(self.parent.refFunctionBody)
            else:
                self.loadfile(f.read())

            
    def uiconfig(self):
        """ 
            this method sets up the main window and two text widgets (the editor widget, and a 
            text entry widget for the commandline).
        """
        self.uiopts = {"height": "60",
                        "width": "132",
                        "cursor": "xterm",
                        "bg": "white",
                        "fg": "#FFAC00",
                        "insertbackground": "#FFD310",
                        "insertborderwidth": "1",
                        "insertwidth": "3",
                        "exportselection": True,
                        "undo": True,
                        "selectbackground": "#E0000E",
                        "inactiveselectbackground": "#E0E0E0"
                       }
        self.text = scrolledtext.ScrolledText(master=self.root, **self.uiopts)
        self.text.vbar.configure(
            width = "3m",
            activebackground = "#FFD310",
            borderwidth = "0",
            background = "#68606E",
            highlightthickness = "0",
            highlightcolor = "#00062A",
            highlightbackground = "#00062A",
            troughcolor = "#20264A",
            relief = "flat")    
        self.text.grid(column = 0, row = 0, sticky = ('nsew'))
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 0)

    def destroy_window(self):
        """
            this method safely closes the window
        """
        self.close()
        


    def autoindent(self, event):
        """
            this method implements the callback for the Return Key in the editor widget.
            arguments: the tkinter event object with which the callback is associated
        """
        indentation = ""
        lineindex = self.text.index("insert").split(".")[0]
        linetext = self.text.get(lineindex+".0", lineindex+".end")
        
        for character in linetext:
            if character in [" ","\t"]:
                indentation += character
            else:
                break
                
        self.text.insert(self.text.index("insert"), "\n"+indentation)
        return "break"


    def tab2spaces4(self, event):
        """
            this method implements the callback for the indentation key (Tab Key) in the
            editor widget. 
            arguments: the tkinter event object with which the callback is associated
        """
        self.text.insert(self.text.index("insert"), "    ")
        return "break"


    def loadfile(self, text):
        """
            this method implements loading a file into the editor.
            arguments: the scrollable text object into which the text is to be loaded
        """
        if text:
            self.text.insert(tkinter.INSERT, text)
            self.text.tag_remove(tkinter.SEL, '1.0', tkinter.END)
            self.text.see(tkinter.INSERT)
 

    def event_key(self, event):
        """
            this method traps the keyboard events. anything that needs doing when a key is pressed is done here.
            arguments: the associated event object
        """
        keycode = event.keycode
        char = event.char
        self.recolorize()
#        self.updatetitlebar()
 

    def event_write(self, event):
        """
            the callback method for the root window 'ctrl+w' event (write the file to disk)
            arguments: the associated event object.
        """
        with open(self.filename, "w") as filedescriptor:
            filedescriptor.write(self.text.get("1.0", tkinter.END)[:-1])
            
        filedescriptor.close()
        
        self.text.edit_modified(False)
        self.root.title("Pyro: File Written.")
 
 
#    def event_mouse(self, event):
#        """
#            this method traps the mouse events. anything that needs doing when a mouse
#            operation occurs is done here.
#            arguments: the associated event object
#        """
#        self.updatetitlebar()
#        #self.recolorize()
        
        
    def close(self, event=None):
        """
            this event callback method implements the Quit operation (ctrl+q). In a perfect 
            world, it will check on whether the file is saved and warn the user accordingly
            a graceful way out.
            arguments: the associated event argument. However, unlike the other event 
            callbacks in the code, this one may be called without an associated event object
            as it will discard everything.
        """
        self.parent.refFunctionBody = self.text.get("1.0",  tkinter.END)[:-1]
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):

            self.root.destroy()
        
            
#        with open(self.filename, "w") as filedescriptor:
#            filedescriptor.write(self.text.get("1.0", tkinter.END)[:-1])
#            
#        filedescriptor.close()
        
#        try:
##            c =  code.compile_command(self.filename)
#            f = open(self.filename)
#            script = f.readlines()
#            s = ''.join(script)
##            
##            ind = s.rindex("def")
##            
##            s1 = s[:ind]
##            s2 = s[ind:]
#            
#            print s
##            print code.compile_command(s)
#
#        except:
#            print "failed"
#        


    # ---------------------------------------------------------------------------------------
 
    def mainloop(self):
        """
            the classical tkinter event driver loop invocation, after running through any 
            startup tasks
        """
            
        for task in self.bootstrap:
            task()

        self.root.mainloop()

 
    def create_tags(self):
        """
            thmethod creates the tags associated with each distinct style element of the 
            source code 'dressing'
        """
        bold_font = font.Font(self.text, self.text.cget("font"))
        bold_font.configure(weight=font.BOLD)
        italic_font = font.Font(self.text, self.text.cget("font"))
        italic_font.configure(slant=font.ITALIC)
        bold_italic_font = font.Font(self.text, self.text.cget("font"))
        bold_italic_font.configure(weight=font.BOLD, slant=font.ITALIC)
        style = get_style_by_name('default')
        
        for ttype, ndef in style:
            tag_font = None
        
            if ndef['bold'] and ndef['italic']:
                tag_font = bold_italic_font
            elif ndef['bold']:
                tag_font = bold_font
            elif ndef['italic']:
                tag_font = italic_font
 
            if ndef['color']:
                foreground = "#%s" % ndef['color'] 
            else:
                foreground = None
#            tag_font = ("Helvetica", 15)                 
            self.text.tag_configure(str(ttype), foreground=foreground, font=tag_font) 
            
 
    def recolorize(self):
        """
            this method colors and styles the prepared tags
        """
        code = self.text.get("1.0", "end-1c")
        tokensource = self.lexer.get_tokens(code)
        start_line=1
        start_index = 0
        end_line=1
        end_index = 0
        
        for ttype, value in tokensource:
            if "\n" in value:
                end_line += value.count("\n")
                end_index = len(value.rsplit("\n",1)[1])
            else:
                end_index += len(value)
 
            if value not in (" ", "\n"):
                index1 = "%s.%s" % (start_line, start_index)
                index2 = "%s.%s" % (end_line, end_index)
 
                for tagname in self.text.tag_names(index1): # FIXME
                    self.text.tag_remove(tagname, index1, index2)
 
                self.text.tag_add(str(ttype), index1, index2)
 
            start_line = end_line
            start_index = end_index
 
 

def run():    
    ui_core = CoreUI(lexer = PythonLexer())    # default (no extension) lexer is python
    ui_core.mainloop()
