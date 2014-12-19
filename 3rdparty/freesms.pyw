#Send Free SMS (GUI Version)
#d3hydr8[at]gmail[dot]com
#http://www.darkc0de.com

from Tkinter import *
import urllib, urllib2

class Application(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widget()
	def create_widget(self):
		
		self.lbl = Label(self, text = "From: (hello@abc.com)")
		self.lbl.grid(row = 0, column = 0)
		
		self.addr = Entry(self, width = 32, bg = "#888")
		self.addr.grid(row = 0, column = 1, sticky = W)
	
		self.lbl = Label(self, text = "Number: ")
		self.lbl.grid(row = 3, column = 0)
		
		self.num = Entry(self, width = 3, bg = "#888")
		self.num.grid(row = 3, column = 1, sticky = W)
		self.num1 = Entry(self, width = 3, bg = "#888")
		self.num1.grid(row = 3, column = 1, padx=35,pady=1, sticky = W)
		self.num2 = Entry(self, width = 4, bg = "#888")
		self.num2.grid(row = 3, column = 1, padx=70,pady=1, sticky = W)

		self.lbl = Label(self, text = "Message: (120 Max) ")
		self.lbl.grid(row = 6, column = 0)
		
		self.mess = Entry(self, width = 45, bg = "#888")
		self.mess.grid(row = 6, column = 1, sticky = W)
		
		self.txtbox = Text(self, width = 60, height = 4, relief = "sunken", font=('Georgia', 8, 'bold'), bg = "#888")
		self.txtbox.grid(row = 8, column = 0, columnspan = 2, sticky = W)

		self.bttn1 = Button(self, text = "Send", relief = "raised", font=('courier', 10, 'bold'), fg = "#1569C7", bg = "#18181C", command = self.send)
		self.bttn1.grid(row = 9, columnspan = 2, sticky = "WE")
	
		self.clear = Button(self, text="Clear", font=('Georgia', 8), command = self.clear)
		self.clear.grid(row = 10, column = 1,sticky= E)
		
	def send(self):
		a = self.addr.get()
		n = self.num.get()
		n1 = self.num1.get()
		n2 = self.num2.get()
		m = self.mess.get() 
		host = "http://www.txtdrop.com/" 

		if len(m) > 120:
			self.txtbox.insert(END, "\nMessage Length Over (Max: 120 characters)")
			self.mess.delete(0, END)
		elif len(n) != 3 or len(n1) != 3 or len(n2) != 4:
			self.txtbox.insert(END, "\nMisformed Number")
			self.num.delete(0, END)
			self.num1.delete(0, END)
			self.num2.delete(0, END)
		else:
			login_form_seq = [ 
     				('emailfrom',a), 
				('npa',n), 
				('exchange',n1), 
				('number',n2), 
				('body',m), 
				('submitted','1'), 
				('submit','Send')] 
			login_form_data = urllib.urlencode(login_form_seq) 
			opener = urllib2.build_opener() 
			try: 
				opener.addheaders = [('User-agent', 'Mozilla/5.0')] 
				opener.open(host, login_form_data) 
				self.txtbox.insert(END, "FROM: "+a)
				self.txtbox.insert(END, "\nNUMBER: "+n+"-"+n1+"-"+n2)
				self.txtbox.insert(END, "\nMessage: "+m)
				self.txtbox.insert(END, "\nMessage Sent!!!")
			except(urllib2.URLError), msg: 
				self.txtbox.insert(END, "\nMessage Failed") 

	def clear(self):
		self.addr.delete(0, END)
		self.num.delete(0, END)
		self.num1.delete(0, END)
		self.num2.delete(0, END)
		self.mess.delete(0, END)
   		self.txtbox.delete(0.0, END)
		
root = Tk()
root.title("Send Free SMS")
root.geometry("500x225")
root.config(background="#18181C")
app = Application(root)
root.mainloop()

