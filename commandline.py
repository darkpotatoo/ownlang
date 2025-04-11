import tkinter as tk; input = "";
def updateInput(event):
	current_line = text.get("end-1l linestart", "end-1l lineend")
	global input
	if current_line.startswith("$ "):
		input = current_line[2:]
	else:
		input = current_line
	handleInput(input)
	text.insert(tk.END, "\n$ ")
	text.see(tk.END)
	return "break"
def preventBackspace(event):
	if text.index(tk.INSERT).split(".")[1] == "2":
		return "break"
root = tk.Tk()
root.title("Thing.terminal")
root.configure(bg="black")
text = tk.Text(root, bg="black", fg="white", insertbackground="white", font=("Menlo", 12), wrap="none", borderwidth=0)
text.pack(fill=tk.BOTH, expand=True)
text.insert(tk.END, "$ ")
text.bind("<Return>", updateInput)
text.bind("<BackSpace>", preventBackspace)
text.focus()
def outputLine(text_to_send=""):
	text.insert(tk.END, "\n")
	text.see(tk.END)
	text.insert(tk.END, text_to_send)
	text.see(tk.END)
def handleInput(line):
	if "help" in line:
		if len(line.split(" ")) == 1:
			outputLine("-=-=- Help Menu -=-=-")
			outputLine()
			outputLine("Run 'help <command>' for help with a specific command.")
			outputLine("Commands available:")
			outputLine("\thelp\n\trun <file>\n\tbuild <file>")
		elif line.split(" ")[1] == "run":
			outputLine("-=- Help for `run` -=-")
			outputLine()
			outputLine("run <file>")
			outputLine("<file>: Script file name to execute")
		elif line.split(" ")[1] == "build":
			outputLine("-=- Help for `build` -=-")
			outputLine()
			outputLine("build <file>")
			outputLine("<file>: Script file name to check for errors")
	if line.split(" ")[0] == "run" and line.split(" ")[1]:
		from parser import run
		run(line.split(" ")[1])

	try:
		if line.split(" ")[0] == "build" and line.split(" ")[1]:
			from parser import run
			run(line.split(" ")[1], False)
	except:
		outputLine("Expected <file> argument")
root.mainloop()