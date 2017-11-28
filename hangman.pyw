#hangman.py in tkinter
from tkinter import * #for GUI tools
import urllib.request as req #for API access

def window_die():# pretty simple, it exists so the button can be changed to this command after the game ends.
	root.destroy() #closes window

def definitionButton():
	import webbrowser
	webbrowser.open("http://dictionary.reference.com/browse/"+formatted_word+"?s=t")
	
def replaceAll(letter,theWord):	#replace all characters in UnScWord at indices of the given letter with the letter.
	for qw in range(len(theWord)):
		if(theWord[qw]==letter):
			UnScWord.set(UnScWord.get()[0:qw]+letter+UnScWord.get()[1+qw:])	

def callback(event):#for key presses
	update()
	
def update():#what happens when you press the button.
	global tries
	global UnScWord
	guess = UserInput.get().lower()

	if(len(guess)!=1 or not guess.isalpha()):#bad input
		result.set("Not a letter.")

	elif(guess in AG.get() or guess in UnScWord.get()):#twas a repeat guess
		result.set("Already Guessed")

	elif(guess in word):#they were right
		result.set("correct")
		replaceAll(guess,word)#iterate through the underscores, replacing any correct one with the letter
		if("_" not in UnScWord.get()):#are they done?
			result.set("You win!")	
			Button(root, text="Click Here for definition",command = definitionButton).grid()
			pic.config(image = winnerpic)
			textfield.destroy()
			enterButton.config(command=window_die, text="Close")
			# repeatButton = Button(root, text="Play Again", command = killButton)
			# repeatButton.grid()

	else:#they were wrong
		result.set("wrong")
		tries+=1
		pic.config(image=imglist[tries]) #add another body part
		AG.set(AG.get()+guess) #add the wrong guess to Already Guessed
		
		if(tries>5): #GAME OVER. ONLY 6 TRIES
			Button(root, text="Click Here for definition",command = definitionButton).grid()
			textfield.destroy() #no more input
			UnScWord.set(word) #reveal the answer
			enterButton.config(command=window_die, text="Close") #button now closes window
			result.set("You died.")
			# repeatButton = Button(root, text="Try Again", command = killButton)
			# repeatButton.grid()
	UserInput.set("")#after everything else, empty the text field.		
##################################################
#necessary variables
root = Tk()
root.bind("<Return>", callback)

tries = 0

AG = StringVar()
AG.set("")

winnerpic = PhotoImage(file = "(10)Winner.png")

imglist = [
PhotoImage(file = "(0)Nothing.png"), 
PhotoImage(file = "(1)Head.png"),
PhotoImage(file = "(2)Body.png"),
PhotoImage(file = "(3)1 Arm.png"),
PhotoImage(file = "(4)2 Arms.png"),
PhotoImage(file = "(5)1 leg.png"),
PhotoImage(file = "(6)Dead.png")
]
try:
	API_Read = str(req.urlopen("http://setgetgo.com/randomword/get.php").read()) #get a random word from the API
	formatted_word = API_Read[2:len(API_Read)-5] #format it
	final_word = "" 
	for letter in formatted_word: #add spaces in between the letters
		final_word+=letter+" "
	word = final_word.lower()
except:
	words = ["courtyard", "lamppost", "establishment", "fumigate", "accumulate", "larynx", "particle", "bagpipe", "jugular", "aluminum","pentecostal"]
	from random import choice
	formatted_word = choice(words)
	final_word = "" 
	for letter in formatted_word: #add spaces in between the letters
		final_word+=letter+" "
	word = final_word.lower()

##################################################
#window elements
root.title("Hangman")


pic = Label(root, image=imglist[tries])#the picture
pic.grid(row=0,column=0,rowspan=2)
 
UserInput = StringVar()
textfield = Entry(root, textvariable=UserInput, width=len(UserInput.get()))#the textfield
textfield.focus_set()
textfield.grid(row=2, column=0)

# Label(root, text="Word: ").grid(row=0, column=1)

UnScWord = StringVar()
for eachLetter in range(int(len(word)/2)):
	UnScWord.set(UnScWord.get()+"_ ")
Label(root, textvariable = UnScWord, font = (40)).grid(row=1, column=1)#the word in underscores. guessing correctly should reveal it.
# Label(root,text="("+str(int(len(word)/2))+" Letters Long)").grid(row=2,column=1)

Label(root, text="Already Guessed: ").grid(row=3,column=1)
Label(root,textvariable=AG).grid(row=4,column=1)#the already guessed string list

enterButton = Button(root, text="<Enter>", command=update)
enterButton.grid(row=3, column=0)#the button

result=StringVar()
output = Label(root, textvariable=result).grid(row=4,column=0) # alert label

root.mainloop()
