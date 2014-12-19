#MD5 Cracker (GUI Version)
#d3hydr8[at]gmail[dot]com
#http://www.darkc0de.com

from Tkinter import *
import tkFileDialog, md5

class Application(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widget()
	def create_widget(self):
		
		self.lbl = Label(self, text = "ENTER MD5: ")
		self.lbl.grid(row = 2, column = 0, sticky = E)
		
		self.pw_ent = Entry(self, width = 32)
		self.pw_ent.grid(row = 2, column = 1, sticky = E)
		
		self.submit_bttn = Button(self, text = "Choose Wordlist", command = self.loadwords)
		self.submit_bttn.grid(row = 5, column = 1, sticky = W)
		
		self.txtbox = Text(self, width = 55, height = 8, font=('Georgia', 8), bg = "#CCC", wrap = WORD)
		self.txtbox.grid(row = 7, column = 0, columnspan = 2, sticky = W)

		self.bttn1 = Button(self, text = "Crack", font=('courier', 10, 'bold'), command = self.crack)
		self.bttn1.grid(row = 9, columnspan = 2, sticky = "WE")
	
		self.clear = Button(self, text="Clear", font=('Georgia', 8), command = self.clear)
		self.clear.grid(row = 10, column = 1,sticky= E)
		
	def loadwords(self):
		global wordlist
		file = tkFileDialog.askopenfile(parent=root,mode='r',title='Choose a file')
		wordlist = file.readlines()
		self.txtbox.insert(END, "Loaded: "+str(len(wordlist))+" words")
		
	def crack(self):
		pw = self.pw_ent.get()
		if len(pw) == 32:
			self.txtbox.insert(END, "\nCracking: "+pw)
			for word in wordlist:
				hash = md5.new(word.replace("\n","")).hexdigest()
				if pw == hash:
					self.txtbox.insert(END, "\n\nCracked: "+word)
					break
			self.txtbox.insert(END, "\nComplete")
		else:
			self.txtbox.insert(END, "\nImproper MD5 Length: "+str(len(pw)))
			
	def clear(self):
		self.pw_ent.delete(0, END)
   		self.txtbox.delete(0.0, END)
		wordlist = []
		
root = Tk()
root.title("MD5 Cracker")
root.geometry("350x200")
app = Application(root)
root.mainloop()
