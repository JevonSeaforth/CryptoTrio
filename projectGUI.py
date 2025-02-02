import tkinter as tk
from tkinter import messagebox
import sys
import dsa
import dhkey
import rsa

# Run this program to use GUI
# The GUI formats the terminal output in a more readable way
# and allows for execution of each algorithm

# control execution of DSA
def executeDSA():
    try:
        # clear the text area 
        clearTextArea() 
        # then run the code for dsa
        dsa.runDSA()
    # handles any exception thrown
    except Exception as e:
        messagebox.showerror(f"Error: {str(e)} occurred")

# control execution of RSA
def executeRSA():
    try:
        # clear the text area
        clearTextArea()
        # then run the code for dsa
        rsa.runRSA()
    # handles any exception thrown
    except Exception as e:
        messagebox.showerror(f"Error: {str(e)} occurred")

# control execution of DH
def executeDH():
    try:
        # clear the text area
        clearTextArea()
        # then run the code for dsa
        dhkey.runDH()
    # handles any exception thrown
    except Exception as e:
        messagebox.showerror(f"Error: {str(e)} occurred")

# function clears text area
def clearTextArea():
    textArea.delete(1.0, tk.END)

# Application window 
root = tk.Tk()
root.state('zoomed')
root.title("CryptoTrio project") 

root.configure(bg="#2E2E2E")

# create the frame for the buttons
frameA = tk.Frame(root, background="#333333")
frameA.pack(side='bottom', fill=None)

# create widget to display terminal output
textArea = tk.Text(root, font=("Arial", 20), bg="#1E1E1E", fg="white", insertbackground='white', borderwidth=2, relief='flat')
textArea.pack(expand=True, fill=tk.BOTH) 

# add title to text area 
textArea.insert(tk.END, "Welcome to the CryptoTrio project - Please select an algorithm to run.\n\n") 

# Class responsible for writing to text area widget 
class writeToTextArea:
    # Constructor initializes instance of TextRedirector
    def __init__(self, widget):
        self.widget = widget
    
    # writes/prints output to widget
    def write(self, message):
        self.widget.insert(tk.END, message)

# capture output stream and display in text area 
sys.stdout = writeToTextArea(textArea)
# capture error stream and display in text area 
sys.stderr = writeToTextArea(textArea)

# Button styling 
buttonStyle = {
    'bg': '#555555',  
    'fg': 'white',   
    'activebackground': '#555555', 
    'activeforeground': 'white',    
    'relief': 'flat',  
    'font': ('Arial', 14),
    'borderwidth': 1, 
}

# frame for buttons to arrange them horizontally
buttonFrame = tk.Frame(root, background="#333333")
buttonFrame.pack(pady=20)

# button that runs dsa program
dsaButton = tk.Button(buttonFrame, text="Run DSA", command=executeDSA, **buttonStyle)
dsaButton.pack(side='left', padx=10)

# button that runs rsa program
rsaButton = tk.Button(buttonFrame, text="Run RSA", command=executeRSA, **buttonStyle)
rsaButton.pack(side='left', padx=10)

# button that runs key exchange program
keyExchangeButton = tk.Button(buttonFrame, text="Run Key Exchange", command=executeDH, **buttonStyle)
keyExchangeButton.pack(side='left', padx=10)

# event loop
root.mainloop()
