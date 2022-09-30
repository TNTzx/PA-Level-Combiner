import json
from decimal import Decimal

import threading as thr

import widgets as wg
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msg

#import my_sanity as sanity
#import projectstatus as project
# while project.working():
#     if sanity.state == 0:
#         sanity.takebreak(min=30)
#         sanity.state = 1
#     sanity.state -= 0.01




#define stuff
main = tk.Tk()

wg.padx = 5
wg.pady = 5

wg.font = "Inconsolata"
wg.fontsizemult = 15

version = "20.4.4 (Normal Branch)"

levels = []
levelamount = 2
output = ""

final = {}

# widget specific
instructionsbutton_text = str("""
Instructions:
1. Convert all levels to the level format version """ + version + """.
   This can be done by simply saving the levels in this version of Project Arrhythmia.
2. Select levels to the list.
3. Save output level.
4. Choose the items you want to combine using the "Advanced" button.
   If unchecked, the output will only get the attribute from the first level
   (for example, if \"markers\" is unchecked, only the markers
   from the first level would be copied to the second).
4. Press the combine button!

Make sure you've done the following:
- Have all the themes in both levels in your themes folder.
- Delete objects on the second level that you don't want to be duplicated.
- Both levels must have the same music.
""")

creditstext = """
Project and UI by @TNTz#7964.
Combining script by @Rin Chiropteran#2065.
JSON level format by @Xenon1345#6650.
"""

advanced_checkboxes = []
advanced_names = [
    "Beatmap Objects",
    "BG Objects",
    "Event Keyframes",
    "Checkpoints",
    "Markers",
    "Prefabs"
]
advanced_values = []

combining = ""
advanced_selectedtext = tk.Canvas()

#functions
#adds level to list
def askforlevel():
    selected = list(fd.askopenfilenames(title="Select level/s to add:", filetypes = (("Project Arrhythmia Level", "*.lsb"),("All Files", "*.*"))))
    for i in selected:
        level_list.call.insert("end", i)

#removes level from list
def removelevel():
    levelselect = level_list.call.curselection()
    plural = ""
    if len(levelselect) == 0:
        msg.showerror("Error! D:", "You didn't select any levels! Please select on at least one level to delete.")
        return

    if not len(levelselect) == 1:
        plural = "s"
    answer = msg.askquestion("Confirm", "Are you sure you want to remove the selected level" + plural + "? \n")

    levelselect = reversed(list(levelselect))

    if answer == "yes":
        for i in levelselect:
            level_list.call.delete(i)

#asks for output level
def askforoutput():
    output_entry.call.delete("1.0")
    output_entry.call.insert("1.0", fd.asksaveasfilename(title="Save level to:", initialfile='level.lsb', filetypes = (("Project Arrhythmia Level", "*.lsb"),("All Files", "*.*"))))


#loads levels
def loading(x):
    with open(x, encoding="utf-8") as input_file:
        return json.load(input_file)

def loadingmult(list):
    var = []
    for i in list:
        var.append(loading(i))
    return var


def extract(object, path):
    for key in path:
        object = object.get(key, {})
    return object

def identify(object):
    if "id" in object:
        return object["id"]
    if "t" in object:
        # assuming that markers/keyframes with <0.01 difference in time are the same
        return str(round(Decimal(object["t"]), 2))
    return str(object)

def merge(levels, *path):
    id_to_object = {}
    for array in [extract(level, path) for level in levels]:
        if not array:
            continue
        for object in array:
            id_to_object[identify(object)] = object
    return list(id_to_object.values())

def getlistoflevels():
    return list(level_list.call.get(0, "end"))

#show confirm
def confirm():
    if len(getlistoflevels()) == 0:
        msg.showerror("Error! D:", "No levels selected! Please select the levels using the \"Add Level\" button.")
        return
    if len(getlistoflevels()) == 1:
        msg.showerror("Error! D:", "Please select more than one level.")
        return

    if str(output_entry.call.get("1.0", "end")) == "\n":
        msg.showerror("Error! D:", "Please select an output level using the \"Browse\" button.")
        return

    x = msg.askquestion("Confirm", "Are you sure you want to combine these levels? \n")
    if x == "yes":
        global output
        output = str(output_entry.call.get("1.0", "end")).replace("\n", "")
        try:
            combinelevels()
            msg.showinfo("Combined!", "Finished! :D")
        except Exception as y:
            msg.showerror("Error! D:", y)


#combine levels
def combinelevels():
    levelsloaded = getlistoflevels()
    levels = []

    for i in levelsloaded:
        levels.append(loading(i))

    markers = []
    prefabs = []
    prefab_objects = []
    themes = []
    checkpoints = []
    beatmap_objects = []
    bg_objects = []

    events = {}
    for level in levels:
        for event in level["events"]:
            events[event] = []

    if (advanced_values[4].get()):
        markers = merge(levels, "ed", "markers")
    if (advanced_values[5].get()):
        prefabs = merge(levels, "prefabs")
        prefab_objects = merge(levels, "prefab_objects")
    if (advanced_values[3].get()):
        checkpoints = merge(levels, "checkpoints")
    if (advanced_values[0].get()):
        beatmap_objects = merge(levels, "beatmap_objects")
    if (advanced_values[1].get()):
        bg_objects = merge(levels, "bg_objects")

    if (advanced_values[2].get()):
        themes = merge(levels, "themes")
        for event in events.keys():
            # sort event keyframes by time to prevent bugs
            events[event] = sorted(merge(levels, "events", event), key=identify)

    final = {
        "ed":{
            "timeline_pos":"0",
            "markers": markers
        },
        "level_data":{
            "level_version": "20.4.4",
            "background_color": "0",
            "follow_player": "False",
            "show_intro": "False"
        },
        "prefabs": prefabs,
        "prefab_objects": prefab_objects,
        "themes": themes,
        "checkpoints": checkpoints,
        "beatmap_objects": beatmap_objects,
        "bg_objects": bg_objects,
        "events": events,
    }

    final = json.dumps(final, ensure_ascii=False, separators=(',', ':')).encode('utf8')

    # final write
    with open(output, "wb") as output_level:
        output_level.write(final)

#show instructions
def openIns():
    toplevel_ins = tk.Toplevel(main)
    toplevel_ins.configure(bg="white")

    def OK():
        toplevel_ins.destroy()

    instructions = wg.widgets(type="label", root=toplevel_ins, text=instructionsbutton_text, justify="left", columnspan=2)
    okbutton = wg.widgets(type="button", root=toplevel_ins, row=1, column=1, text="Got it!", command=OK)


#show "advanced" text
def openAdv():
    global advanced_checkboxes, advanced_names, advanced_values, combining

    def OK():
        toplevel.call.destroy()

    toplevel = wg.widgets(type="toplevel", root=main)

    advanced_checkboxes.clear()
    label = wg.widgets(type="label", root=toplevel.call, text="Combine the following:", justify="left", sticky="w", wraplength=220)

    for x in range(len(advanced_names)):
        y = wg.widgets(type="checkbutton", root=toplevel.call, row=x+1, columnspan=2, text=advanced_names[x], variable=advanced_values[x], sticky="w")
        advanced_checkboxes.append(y.call)

    advanced_ok = wg.widgets(type="button", root=toplevel.call, command=OK, row=len(advanced_names) + 1, column=1, sticky="w", text="Confirm")
    main.wait_window(toplevel.call)
    combining = ", ".join([advanced_names[i] for i in range(len(advanced_values)) if advanced_values[i].get()])
    showAdvText()

def showAdvText():
    global combining, advanced_selectedtext
    combiningfinal = str("Selected: " + combining)
    try:
        advanced_selectedtext.call.destroy()
    except:
        pass
    advanced_selectedtext = wg.widgets(type="label", root=frame_insadv.call, row=1, column=1, columnspan=2, text=combiningfinal, justify="left", fontsize=0.9, wraplength=250)
    main.geometry("1200x700")

#show stats
def callShowStats(type):
    lists = []
    if type == "listoflevels":
        if len(level_list.call.curselection()) == 0:
            msg.showerror("Error! D:", "No levels selected! Please select the levels you'd want to see the statistics of.")
            return
        for i in level_list.call.curselection():
            lists.append(level_list.call.get(i))
    elif type == "output":
        if len(getlistoflevels()) == 0:
            msg.showerror("Error! D:", "You don't have levels in the list to combine! Please add levels using the \"Add Levels\" button.")
            return
        lists = getlistoflevels()
    showStats(lists)

def showStats(file):

    stats_dfc_bias = -1
    stats_dfc_state = tk.IntVar()

    objects = statsReturn(file, 0, "Objects", "beatmap_objects")
    prefab_objects = statsReturn(file, 0, "Prefab objects", "prefab_objects")
    bg_objects = statsReturn(file, 0, "BG objects", "bg_objects")
    markers = statsReturn(file, 0, "Markers", "ed", "markers")
    checkpoints = statsReturn(file, stats_dfc_bias, "Checkpoints", "checkpoints")

    stats_window = wg.widgets(type="toplevel")

    def updateStats(element):
        nonlocal stats_dfc_bias, checkpoints
        if element == "dfc":
            checkpoints = statsReturn(file, -1 if stats_dfc_state.get() == 0 else 0, "Checkpoints", "checkpoints")
        
        stats_text = str(objects + prefab_objects + bg_objects + markers + checkpoints)
        stats_label = wg.widgets(type="label", root=stats_window.call, text=stats_text)

    updateStats("")
    
    #dfc means display first checkpoint
    stats_dfc = wg.widgets(type="checkbutton", root=stats_window.call, row=1, text="Include starting checkpoint", variable=stats_dfc_state, command=lambda: updateStats("dfc"))

def statsReturn(file, bias, string, *key):
    return str(string + ": " + str(len(merge(loadingmult(file), *key)) + bias) + "\n")



#intialize ui
main.title("PA Level Combiner")
main.configure(bg="white")

main_width = 1200
main_height = 600
def getcenter(dimension):
    if dimension == "width":
        return str(round((main.winfo_screenwidth() / 2) - main_width / 2))
    elif dimension == "height":
        return str(round((main.winfo_screenheight() / 2) - main_height / 2))

main.geometry("1200x600+" + getcenter("width") + "+" + getcenter("height"))

wg.rowcolumnconfig(main, [1, 1, 1, 1, 1], [10, 1])

#create frames
frame_title = wg.widgets(type="labelframe", root=main, row=0, columnspan=2, rowweight=[3, 1], text="Title")

frame_level = wg.widgets(type="labelframe", root=main, row=1, rowweight=[1, 1], columnweight=[100, 1, 50], text="Levels Select")
frame_level_column2 = wg.widgets(type="frame", root=frame_level.call, column=2, rowspan=2, rowweight=[1, 1, 1], highlightthickness=0)

frame_output = wg.widgets(type="labelframe", root=main, row=1, column=1, rowweight=[1, 1, 1], columnweight=[100, 1, 50], text="Output Select")

frame_insadvcomb = wg.widgets(type="frame", root=main, row=2, columnspan=2, columnweight=[1, 1], highlightthickness=0)
frame_insadv = wg.widgets(type="labelframe", root=frame_insadvcomb.call, columnweight=[1, 1], text="Instructions and Advanced")
frame_combine = wg.widgets(type="labelframe", root=frame_insadvcomb.call, column=1, text="Combine")
frame_credits = wg.widgets(type="labelframe", root=main, row=3, columnspan=2, text="Credits")


#create wg.widgets
title = wg.widgets(type="label", root=frame_title.call, text="PA Level Combiner", fontsize=3)
title_sub = wg.widgets(type="label", root=frame_title.call, row=1, text="for PA Version: " + version)

level_list = wg.widgets(type="listbox", root=frame_level.call, fontsize=0.8, selectmode="multiple")
level_scrollv = wg.widgets(type="scrollbar", root=frame_level.call, attach=level_list.call, orient="v", column=1, rowspan=2)
level_scrollh = wg.widgets(type="scrollbar", root=frame_level.call, attach=level_list.call, orient="h", row=1)
level_add = wg.widgets(type="button", root=frame_level_column2.call, text="Add levels", command=askforlevel)
level_remove = wg.widgets(type="button", root=frame_level_column2.call, row=1, text="Remove levels", command=removelevel)
level_stats = wg.widgets(type="button", root=frame_level_column2.call, row=2, text="Check statistics for\nselected levels", command= lambda: callShowStats("listoflevels"))

output_label = wg.widgets(type="label", root=frame_output.call, columnspan=3, text="Output level:")
output_entry = wg.widgets(type="text", root=frame_output.call, row=1, column=0, width=20, height=1)
output_scrollh = wg.widgets(type="scrollbar", root=frame_output.call, row=1, column=1, attach=output_entry.call, orient="v")
output_browse = wg.widgets(type="button", root=frame_output.call, row=1, column=2, text="Browse", command=askforoutput)
output_stats = wg.widgets(type="button", root=frame_output.call, row=2, columnspan=3, text="Check statistics for combined level", command= lambda: callShowStats("output"))

combinebutton = wg.widgets(type="button", root=frame_combine.call, text="Combine levels!", command=confirm)

instructionsbutton = wg.widgets(type="button", root=frame_insadv.call, rowspan=2, text="Open Instructions", command=openIns)

advanced_button = wg.widgets(type="button", root=frame_insadv.call, column=1, text="Advanced", command=openAdv)
for x in range(len(advanced_names)):
    advanced_values.append(tk.IntVar())
    advanced_values[x].set(1)

credits = wg.widgets(type="label", root=frame_credits.call, text=creditstext, fontsize=0.9)

#display ui
main.mainloop()