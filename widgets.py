import tkinter as tk

main = ""
font = "Arial"

padx = 0
pady = 0

fontsizemult = 15

def fontsizefunc(x):
    return int(x * fontsizemult)

def rowcolumnconfig(obj, rowweight, columnweight):
    for i in range(len(rowweight)):
        obj.rowconfigure(i, weight=rowweight[i])
    for i in range(len(columnweight)):
        obj.columnconfigure(i, weight=columnweight[i])

class widgets():
    def __init__(self,
        type="label", root=main, #main

        #grid attributes
        row=0, column=0, #set coordinates
        rowspan=1, columnspan=1, #set span
        rowweight=[1], columnweight=[1], #set weights for frames, canvas, and toplevel
        width=0, height=0,
        sticky="NSEW", #set sticky
        anchor="nw", #set anchor

        #text style attributes
        text="", #set text
        fontstyle=font, fontsize=1, justify="center", wraplength=10000, #set text format
        bg="white", highlightbackground="black", highlightthickness=1, #set styles

        #widget specific attributes
        command="", variable="", #set commands and variables
        orient="", attach="", #set scrollbar attributes
        selectmode="single"): #set listbox attributes

        fontstyle = font #apparently the attributes were dumb so i just went to do this

        if type == "label":
            self.call = tk.Label(root, text=text, font=(fontstyle, fontsizefunc(fontsize)), justify=justify, wraplength=wraplength, bg=bg)
        elif type == "entry":
            self.call = tk.Entry(root, font=(fontstyle, fontsizefunc(fontsize)))
        elif type == "button":
            self.call = tk.Button(root, text=text, font=(fontstyle, fontsizefunc(fontsize)), command=command, bg=bg)
        elif type == "checkbutton":
            self.call = tk.Checkbutton(root, text=text, font=(fontstyle, fontsizefunc(fontsize)), command=command, variable=variable, onvalue=1, offvalue=0, bg=bg)
        elif type == "listbox":
            self.call = tk.Listbox(root, font=(fontstyle, fontsizefunc(fontsize)), bg=bg, selectmode=selectmode)
        elif type == "text":
            self.call = tk.Text(root, font=(fontstyle, fontsizefunc(fontsize)), bg=bg, width=width, height=height)

        elif type == "scrollbar":
            self.call = tk.Scrollbar(root, orient=orient)
            if orient == "v":
                attach.config(yscrollcommand=self.call.set)
                self.call.config(command=attach.yview)
            else:
                attach.config(xscrollcommand=self.call.set)
                self.call.config(command=attach.xview)

        elif type == "frame":
            self.call = tk.Frame(root, highlightbackground=highlightbackground, highlightthickness=highlightthickness, bg=bg)
            rowcolumnconfig(self.call, rowweight, columnweight)
        elif type == "labelframe":
            self.call = tk.LabelFrame(root, text=text, labelanchor=anchor, bg=bg)
            rowcolumnconfig(self.call, rowweight, columnweight)
        elif type == "toplevel":
            self.call = tk.Toplevel(root)
            self.call.configure(bg=bg)
            rowcolumnconfig(self.call, rowweight, columnweight)
        elif type == "canvas":
            self.call = tk.Canvas(root, width=1, height=1, bg=bg)
            rowcolumnconfig(self.call, rowweight, columnweight)

        if not type == "toplevel":
            self.call.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)