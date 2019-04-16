from Tkinter import*
from PIL import Image, ImageTk
import ttk
import tkMessageBox as messagebox
import re



#######MAIN WINDOW INTERFACE#########

class Welcome:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1000x600')
        self.root.title("PAG")
        self.root.resizable(False,False)
        self.root.configure(background='#888888')
        self.bg = '#e9e9e9'
        self.font = ("Helvetica", 12)                            
        self.main_cnv = Canvas(self.root, bg = "#e9e9e9", width = 1000, height = 600)
        self.main_cnv.pack()        
        x = 50
        self.main_cnv.create_text(500,150, text = "Welcome to PAG!", font = ("Bucket O Blood",x), fill = "#0e969e")                                  
        self.main_cnv.create_text(500,300, text = "PAG", font = ("Bucket O Blood",x-20), fill = "#0e969e", tag = "pag", activefill = "#4a64e8")
        self.main_cnv.tag_bind("pag", '<ButtonRelease-1>', lambda e: self.popup(Toplevel(),self.root))                                                              
        self.root.mainloop()
        

    #open the fractals window
    def popup(self,wnd, parent):
        self.wnd = wnd
        self.parent = parent
        self.wnd.geometry('300x100')
        self.wnd.title("!")
        label = Label(self.wnd, text = "Please enter the number of questions to proceed.")
        label.pack()
        self.box = Spinbox(self.wnd,from_=1, to =30)
        self.box.pack()
        ok = Button(self.wnd, text = "Proceed", command = self.proceed )
        ok.pack()
        self.wnd.resizable(False,False)
        
    def proceed(self):
        numQ = int(self.box.get())
        self.wnd.destroy()
        self.parent.destroy()
        Main(numQ)
        
        
class Main:
    def __init__(self, numQ):
        self.numQ = numQ


        self.root= Tk()
        self.root.geometry('1000x600')
        self.root.title("PAG")
        self.root.resizable(False,False)
        self.top_frame = Frame(self.root)
        self.top_frame.pack()

        self.bottom_frame = Canvas(self.root)
        self.bottom_frame.pack()
        self.questions = []
#        for i in range(numQ):
#            self.questions.append(None)
        self.n = ttk.Notebook(self.top_frame)        
        for i in range(self.numQ):                    
            f1 = ttk.Frame(self.n)
            self.questions.append(MainFrame(self, f1))
            self.n.add(f1, text='Question' + str(i))
            
        self.n.pack()
        

        
#        TopFrame(self, self.top_frame)
#        MainFrame(self, self.main_frame)
        BottomFrame(self,self.bottom_frame)
        
        self.root.mainloop()
 
#class TopFrame:
#    def __init__(self,parent,cnv):
#        self.pageLabel = Label(cnv,text = str(parent.page) + "/" + str(parent.numQ), font = ("Bucket O Blood",18))
#        self.pageLabel.pack()

    
class MainFrame:
    def __init__(self,parent,cnv):
        self.parent = parent
#        self.num = self.parent.page
        self.classes = []
        
        self.stringsFrame = Frame(cnv)        
        self.stringsFrame.pack()

        self.qName = Label(self.stringsFrame, text = "Quesion Name: ")
        self.fName = Label(self.stringsFrame, text = "Function Name: ")
        self.qText = Entry(self.stringsFrame)
        self.fText = Entry(self.stringsFrame)        
        self.qName.grid(row=0,column = 0, sticky = W)
        self.qText.grid(row=0, column = 1)
        self.fName.grid(row=0,column= 2)  
        self.fText.grid(row=0, column = 3)
        self.numCases = Label(self.stringsFrame, text = "Number of Test Classes: ")
        self.numCasesW = Spinbox(self.stringsFrame,from_=1, to =20)
        self.numCasesB = Button(self.stringsFrame, command = self.generateClasses, text = "Generate Classes")
        self.numCases.grid(row=0,column=4)
        self.numCasesW.grid(row=0,column=5)
        self.numCasesB.grid(row=0,column=6)
       

        self.classFrames = Frame(cnv)
        self.classFrames.pack()


    def generateClasses(self):
        
        for widget in self.classFrames.winfo_children():
            widget.destroy()      
        n = ttk.Notebook(self.classFrames)        
        
        numClasses = self.numCasesW.get()
        try:
            numClasses = int(numClasses)
        except:
#            spinBoxError()
            return
        for i in range(numClasses):
            
            f1 = ttk.Frame(n)
            self.classes.append(TestClass(f1, i))
            n.add(f1, text='Category' + str(i))
            
        n.pack()

#        self.scrollbar = Scrollbar(self.classFrames, orient = HORIZONTAL)
#        self.scrollbar.grid(row = 1, columnspan = 1, sticky = W+E)




        
class TestClass:
    def __init__(self, parent, i):     
        self.own = parent
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

        self.timeout = Label(self.numsFrame, text = "Timeout in seconds: ")
        self.timeoutW = Spinbox(self.numsFrame,from_=0.1, to =10)
        self.timeout.grid(row=0,column = 0, sticky = W)
        self.timeoutW.grid(row=0,column= 1) 
        
        self.index = Label(self.numsFrame, text = "Index of Comparison Function: ")
        self.indexW = Spinbox(self.numsFrame,from_=0, to =10)        
        self.index.grid(row=1,column = 0, sticky = W)
        self.indexW.grid(row=1,column= 1)
        
        self.points = Label(self.numsFrame, text = "Points Per Test Case: ")
        self.pointsW = Spinbox(self.numsFrame,from_=0, to =10)        
        self.points.grid(row=2,column = 0, sticky = W)
        self.pointsW.grid(row=2,column= 1)
        
        self.numCases = Label(self.numsFrame, text = "Number of Test Cases: ")
        self.numCasesW = Spinbox(self.numsFrame,from_=0, to =10)        
        self.numCases.grid(row=3,column = 0, sticky = W)
        self.numCasesW.grid(row=3,column= 1)  
        
        self.cases = Label(self.numsFrame, text = "Input Arguments: (each case should be on a separate line, and each argument should be separated by a vertical bar: | <shift+backslash>")
        self.casesW = Text(self.numsFrame, state=NORMAL, height = 15)        
        self.cases.grid(row=4,column = 0, sticky = W)
        self.casesW.grid(row=5,column= 0)        
        
class BottomFrame:
    def __init__(self,parent,cnv):
        self.parent = parent
        qButton = Button(cnv, text = "Add Questions", command = self.addQuestions)
        qButton.grid(row = 0, column = 1, padx=5)
        nextButton= Button(cnv,text= "Generate", command = self.generate)
        nextButton.grid(row = 0,column = 2, padx = 5)
        
    def addQuestions(self):
        f1 = ttk.Frame(self.parent.n)
        MainFrame(self.parent, f1)
        i = self.parent.numQ
        self.parent.numQ+=1
        self.parent.n.add(f1, text='Question' + str(i))
        
    def generate(self):
        f = open("metadata.txt","w")
#        try:
        for Q in self.parent.questions:
            Question = Q.qText.get()
            Function = Q.fText.get()
            NumClasses = len(Q.classes)
            f.write(Question+"\n")
            f.write(Function+"\n")
            f1 = open(Question+".txt", "w")
            f1.write(str(NumClasses)+" #this is the number of test classes \n")
            for c in Q.classes:
                f1.write("#NEW CATEGORY STARTS \n")
                fail = c.failText.get()
                success = c.successText.get()
                timeout = c.timeoutW.get()
                index = c.indexW.get()
                points = c.pointsW.get()
                numCases = c.numCasesW.get()
                cases = c.casesW.get('1.0',END)
                f1.write(fail+ " #this is the fail message \n")
                f1.write(success+ " #this is sucess fail message \n")
                f1.write(timeout+ " #this is the timeout \n")
                f1.write(index+ " #this is the index \n")
                f1.write(points+ " #this is the points per case \n")
                f1.write(numCases+ " #this is the number of cases \n")
                f1.write(cases)
                
#        except:
#            print "error"
#            return
                             
                            
                
                
               
application = Welcome()