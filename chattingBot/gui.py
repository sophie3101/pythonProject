import tkinter as tk
from openAI_davinci_model import OpenAI

class GUI:
  def __init__(self):
   
    self.root = tk.Tk()
    # resize window frame
    self.root.geometry("750x250")

    # title of window frame
    self.root.title('OpenAI ChatBot StudyGuide')

    label = tk.Label(self.root, text="What do you want to learn?", font=('Arial', 12))
    label.pack(pady=10)

    # entry for user input
    self.entry = tk.Entry(self.root, width = 45, font = ('Arial', 12))
    self.entry.pack(padx=10, pady=10)

    # output
    self.output_label = tk.Label(self.root, text="",font = ('Arial', 12), wraplength=600, justify=tk.LEFT)
    self.output_label.pack(padx=10)

    button = tk.Button(self.root, text = "submit", command=self.clickSubmit)
    button.pack(pady=20)

    self.root.mainloop()
    
  def clickSubmit(self):
    # set output as loading... while waiting to get answer from OpenAI
    self.setOutput("loading...")
    self.root.update_idletasks()

    input = self.entry.get()
    openAI = OpenAI()
    response = openAI.getResponse(input)
    self.setOutput(response)

  def setOutput(self, response):
    self.output_label.config(text=response)

app = GUI()

