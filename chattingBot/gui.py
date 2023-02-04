import tkinter as tk
from tkinter import ttk
from openAI_davinci_model import OpenAI

class GUI:
  def __init__(self, root):
  
    self.root = root

    # resize window frame
    self.root.geometry("750x250")
    tk.Frame(self.root)

    # title of window frame
    self.root.title('OpenAI ChatBot StudyGuide')

    # input frame
    self.inputFrame = ttk.Frame(self.root)
    self.inputFrame.pack(fill="x")

    # input title
    label = ttk.Label(self.inputFrame, text="What do you want to learn?", font=('Arial', 12))
    label.pack(pady=5)

    # entry for user input
    self.userInput = ttk.Entry(self.inputFrame, font = ('Arial', 12))
    self.userInput.pack(fill="x")

    # button
    buttonsFrame = tk.Frame(self.root)
    buttonsFrame.pack(pady=10)

    button = ttk.Button(buttonsFrame, text = "submit", command=self.clickSubmit)
    button.pack(side="left")

    button = ttk.Button(buttonsFrame, text = "clear", command=self.reset)
    button.pack(side="left")

    # output
    # scrollbar
    resultFrame = tk.Frame(self.root)
    resultFrame.pack(fill="both", expand=True)

    self.scrollbar = ttk.Scrollbar(resultFrame)
    self.scrollbar.pack(side="right", fill="y")

    self.output = tk.Text(resultFrame, wrap="word")
    self.output.pack(side="left", fill="both", expand=True)

    self.scrollbar.config(command=self.output.yview)
    self.output.config(yscrollcommand=self.scrollbar.set)
    
  
  def reset(self):
    self.userInput.delete(0, 'end')
    self.output.delete("1.0", tk.END)
    
  def clickSubmit(self):
    # set output as loading... while waiting to get answer from OpenAI
    self.setOutput("loading...")
    self.root.update_idletasks()

    input = self.userInput.get()
    openAI = OpenAI()
    response = openAI.getResponse(input)
    self.setOutput(response)

  def setOutput(self, response):
    self.output.delete("1.0", tk.END)
    self.output.insert(tk.END, response)

root = tk.Tk()
app = GUI(root)
root.mainloop()
