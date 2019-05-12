"""
Run this file to generate the text files needed for autograding a 
python assignment.
"""

from Tkinter import*
import ttk
import tkMessageBox as messagebox

import pickle
import pyro

FILENAME = "state.pkl"


NBOOKS = []
NBOOKS2 = []
with open("function_class.py", "r") as f:
    
    FUNCTEMPLATE = f.readlines()
    f.close()

'''THIS CLASS IS COPIED AND EDITTED FROM 
https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close
buttons-to-tabs-in-tkinter-ttk-notebook '''
class Notebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, initialized, nbooks, stringVar, *args, **kwargs):
        self.nbooks = nbooks
        self.stringVar = stringVar
        if not initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")
        
        

        self.state(["!pressed"])
        self._active = None


        for i in range(self.index('end')):
            self.tab(i, text = self.stringVar + " " + str(i))
        self.nbooks.remove(self.nbooks[index])


    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])






#######MAIN WINDOW INTERFACE#########

        
class Main:
    def __init__(self):
        self.numQ = 1
        self.restored = False

        self.root= Tk()
        self.root.wm_protocol("WM_DELETE_WINDOW", self.save_state)
        self.root.geometry('1000x600')
        self.root.title("PAG")
        self.root.resizable(False,False)
        self.top_frame = Frame(self.root)
        self.top_frame.pack()

        self.bottom_frame = Canvas(self.root)
        self.bottom_frame.pack()
#        self.questions = NBOOKS
        self.nbooks = NBOOKS

        self.n = Notebook(False, NBOOKS, "Question", self.top_frame)        
        for i in range(self.numQ):                    
            f1 = ttk.Frame(self.n)
            self.n.add(f1, text='Question' + str(i))
            NBOOKS.append(MainFrame(self, f1))
            
        self.n.pack()
        
        BottomFrame(self,self.bottom_frame)
        self.root.after(1, self.restore)
        self.root.mainloop()

    
    def restore(self):
        if messagebox.askyesno("Restore", "Do you want to restore the latest saved version?"):
            try:
                f = open("state.pkl")
                state = pickle.load(f)
                self.nbooks.pop(0)
                self.n.forget(0)
                for i in range(len(state)):
                    f1 = ttk.Frame(self.n)
                    f2 = MainFrame(self, f1)
                    
                    f2.qText.insert(0, state[i]["Question"])
                    f2.fText.insert(0, state[i]["Function"])
                    f2.numCasesvar.set(state[i]["NumClasses"])
                    f2.timeoutVar.set(state[i]["timeout"])
                    f2.tkvar.set(state[i]["indexName"])
                    f2.refFunctionBody = state[i]["refFunc"]
                    f2.generateClasses(True, state[i]["classes"])
                        
                    self.nbooks.append(f2)
                    self.n.add(f1, text='Question' + str(i)) 
                    
                    
            except:
                NBOOKS = []
                f1 = ttk.Frame(self.n)
                NBOOKS.append(MainFrame(self, f1))
                self.n.add(f1, text='Question' + str(0))
                messagebox.showerror("Error", "Unable to load")



 
    def save_state(self):
        state = []
        if messagebox.askyesno("Save", "Do you want to save current state?"):
            try:
                for Q in NBOOKS:
                    d = dict()
                    d["Question"] = Q.qText.get()
                    d["Function"] = Q.fText.get()
                    d["NumClasses"] = len(Q.classes)
                    d["timeout"] = Q.timeoutW.get()
                    d["indexName"] = Q.tkvar.get() 
                    d["refFunc"] = Q.refFunctionBody
                    classes = dict()
                    for c in Q.classes:
                        classes["fail"] = c.failText.get()
                        classes["success"] = c.successText.get()
                        classes["points"] =  c.pointsW.get()
                        classes["cases"] =  c.casesW.get('1.0',END)
                    d["classes"] = classes
                    state.append(d)
                f  = open(FILENAME,'wb')
                pickle.dump(state, f)
                self.root.destroy()
            except:
                messagebox.showerror("Error", "Unable to save")
                self.root.destroy()
        else:
            self.root.destroy()
                
        
        
        

    
class MainFrame:
    def __init__(self,parent,cnv):
        self.parent = parent
#        self.num = self.parent.page
        self.classes = []
        
        self.stringsFrame = Frame(cnv)        
        self.stringsFrame.pack()
        self.refFunctionBody = None

        self.qName = Label(self.stringsFrame, text = "Quesion Name: ")
        self.fName = Label(self.stringsFrame, text = "Function Name: ")
        self.qText = Entry(self.stringsFrame)
        self.fText = Entry(self.stringsFrame)        
        self.qName.grid(row=0,column = 0, sticky = W)
        self.qText.grid(row=0, column = 1)
        self.fName.grid(row=0,column= 2)  
        self.fText.grid(row=0, column = 3)
        self.numCases = Label(self.stringsFrame, text = "Number of Test Classes: ")
        self.numCasesvar = StringVar(self.parent.root)
        self.numCasesW = Spinbox(self.stringsFrame,from_=1, to =20, textvariable = self.numCasesvar)
        self.numCasesB = Button(self.stringsFrame, command = self.generateClasses, text = "Generate Classes")
        self.numCases.grid(row=0,column=4)
        self.numCasesW.grid(row=0,column=5)
        self.numCasesB.grid(row=0,column=6)
        
        self.timeout = Label(self.stringsFrame, text = "Timeout in seconds: ")
        self.timeoutVar = StringVar(self.parent.root)
        self.timeoutW = Spinbox(self.stringsFrame,from_=0.1, to =10, textvariable = self.timeoutVar)
        self.timeout.grid(row=1,column = 1, sticky = W)
        self.timeoutW.grid(row=1,column= 2) 
        
        
        self.tkvar = StringVar(self.parent.root)
#        choices = [ 'Integer Comparison','Float Comparison','String Comparison']
        self.tkvar.set('Integer Comparison') # set the default option
        self.index = Label(self.stringsFrame, text = "Comparison Function: ")
        self.indexW = OptionMenu(self.stringsFrame, self.tkvar, 'Integer Comparison','Float Comparison','String Comparison')        
        self.index.grid(row=1,column = 3, sticky = W)
        self.indexW.grid(row=1,column= 4)   

        self.referenceF = Button(self.stringsFrame, text = "Reference Function", command = self.addRef)
        self.referenceF.grid(row = 1, column = 6)

        self.classFrames = Frame(cnv)
        self.classFrames.pack()
        
        
    def addRef(self):
        self.func = self.fText.get()
        if self.func =="":
            messagebox.showerror("Function Name", "Function name cannot be empty")
        elif re.search("\s", self.func):
            messagebox.showerror("Function Name", "Function name cannot have whitespace")
            
        else:
            f = open("function_class.py", "w")
            FUNCTEMPLATE[0] = "class " + self.func+":\n"
            FUNCTEMPLATE[25] = "        return lab1."+ self.func +"( int(raw_input()) )\n"
            f.writelines(FUNCTEMPLATE)
            f.close()
            self.ui_core = pyro.CoreUI(parent = self)    
            self.ui_core.mainloop()
#        pyro.run()


    def generateClasses(self, regenerate = False, classes = None):
        
        if self.classes == []:
            self.n = Notebook(True, self.classes, "Category", self.classFrames)        
            
            numClasses = self.numCasesW.get()
            try:
                numClasses = int(numClasses)
            except:
    #            spinBoxError()
                return
            for i in range(numClasses):
                
                f1 = ttk.Frame(self.n)
                f2 = TestClass(f1, i, self)
                if regenerate:
                    try:
                        f2.failText.insert(0, classes["fail"])
                        f2.successText.insert(0, classes["success"])
                        f2.pointsVar.set(classes["points"])
                        f2.casesW.insert('1.0', classes["cases"])
                    except:
                        print "none"
                        f2 = TestClass(f1, i, self)
                    
                self.classes.append(f2)
                self.n.add(f1, text='Category ' + str(i))
                
            self.n.pack()
        else:
            numClasses = self.numCasesW.get()
            try:
                numClasses = int(numClasses)
            except:
    #            spinBoxError()
                return     
            if numClasses <= len(self.classes):
                return
            
            for i in range(len(self.classes), numClasses):
                f1 = ttk.Frame(self.n)
                self.classes.append(TestClass(f1, i, self))
                self.n.add(f1, text='Category ' + str(i))
                

        
        



        
class TestClass:
    def __init__(self, frame, i, parent):  
        self.own = frame
        self.parent = parent
        self.own.grid(row = 0 , column = i)
        Label(self.own, text = "Category " + str(i)).pack()

        self.stringsFrame = Frame(self.own)
        self.stringsFrame.pack()

        self.failMessage = Label(self.stringsFrame, text = "Fail Message: ")
        self.successMessage = Label(self.stringsFrame, text = "Success Message: ")
        self.failText = Entry(self.stringsFrame, width = 70)
        self.successText = Entry(self.stringsFrame, width = 70)
        self.failMessage.grid(row=2, column = 0)
        self.successMessage.grid(row=3 ,column = 0)
        self.failText.grid(row=2, column=1)
        self.successText.grid(row = 3, column = 1)

        self.numsFrame = Frame(self.own)
        self.numsFrame.pack()
        
        self.points = Label(self.numsFrame, text = "Points Per Test Case: ")
        self.pointsVar = StringVar(self.parent.parent.root)
        self.pointsW = Spinbox(self.numsFrame,from_=0, to =10, textvariable = self.pointsVar)        
        self.points.grid(row=2,column = 0, sticky = W)
        self.pointsW.grid(row=2,column= 1)
        
        self.cases = Label(self.numsFrame, text = "Input Arguments: (each case should be on a separate line, and each argument should be space-separated)")
        self.casesW = Text(self.numsFrame, state=NORMAL, height = 15)        
        self.cases.grid(row=4,column = 0, sticky = W)
        self.casesW.grid(row=5,column= 0)        
        
class BottomFrame:
    def __init__(self,parent,cnv):
        self.parent = parent
        iButton = Button(cnv,text = "Instructions")
        iButton.grid(row=0,column=0,padx=5)
        qButton = Button(cnv, text = "Add Questions", command = self.addQuestions)
        qButton.grid(row = 0, column = 1, padx=5)
        nextButton= Button(cnv,text= "Generate", command = self.generate)
        nextButton.grid(row = 0,column = 2, padx = 5)
        
    def addQuestions(self):
        
        f1 = ttk.Frame(self.parent.n)
        NBOOKS.append(MainFrame(self.parent, f1))
        self.parent.numQ = len(NBOOKS) 
        i = self.parent.numQ-1
        self.parent.numQ+=1
        self.parent.n.add(f1, text='Question' + str(i))
        
    def generate(self):
        f = open("metadata.txt","w")
        functions = []
        names = []
        for Q in NBOOKS:
            if Q.refFunctionBody is None:
                messagebox.showerror("Error", "Please add reference function!")
                break
            Question = Q.qText.get()
            Function = Q.fText.get()
            names.append(Function)
            functions.append(Q.refFunctionBody)
            NumClasses = len(Q.classes)
            timeout = Q.timeoutW.get()
            indexName = Q.tkvar.get() 
            if indexName == "Float Comparison":
                index = 1
            else:
                index = 0
            f.write(Question+"\n")
            f.write(Function+"\n")
            f1 = open(Question+".txt", "w")
            f1.write(str(NumClasses)+" #this is the number of test classes \n")
            for c in Q.classes:
                f1.write("#NEW CATEGORY STARTS \n")
                fail = c.failText.get()
                success = c.successText.get()

                points = c.pointsW.get()
                cases = c.casesW.get('1.0',END).rstrip()
                ###credits below:
                numCases = str(len(cases.split("\n")))
                f1.write(fail+ " #this is the fail message \n")
                f1.write(success+ " #this is sucess fail message \n")
                f1.write(timeout+ " #this is the timeout \n")
                f1.write(str(index)+ " #this is the index \n")
                f1.write(points+ " #this is the points per case \n")
                f1.write(numCases+ " #this is the number of cases \n")
                f1.write(cases)
                
                
        f2 = open("function_generator.py","w")
        for funct in functions:
            f2.write(funct)
            
        src = open("source.py")
        srcLines = list(map(lambda x: x.rstrip('\0'), src.readlines()))
        for name in names:
            g = open(name + ".py", 'w')
            srcLines[1] = "from function_generator import " + name + " as s"
            g.writelines(srcLines)
            g.close()   

            
               
                             
                            
                
                
               
Main()



# =============================================================================
# CREDITS:
# https://stackoverflow.com/questions/4609382/getting-the-total-number-of-lines-in-a-tkinter-text-widget
# https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
# =============================================================================
