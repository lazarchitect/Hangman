#hangman.py in tkinter
from tkinter import * #for GUI tools
import urllib.request as req #for API access

####SOME NOTES:
#"UnScWord" refers to the UnderScore Word, the puzzle that is presented to the player.
#As the Player succeeds, more letters are revealed to them, but initially, all they see is underscores.

def window_die():# pretty simple, it exists so the button can be changed to this command after the game ends.
	root.destroy() #closes window

#The command behind the button at the end which fetches the definition of a word.
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
	global tries #the number of attempts the user has made so far.
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

tries = 0 #the number of attempts the user has made so far.

AG = StringVar() #AG stands for Already Guessed, keeping track of the user's previous moves.
AG.set("") #Initially empty, obviously

#the congratulatory image that appears when you win
winnerpic = PhotoImage(file = "(10)Winner.png")

#A series of horrific, gory stick figure lynchings. Each one contains more and more body parts. Barbaric.
#Updated to be more complete each time the user enters an incorrect letter.
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
	formatted_word = API_Read.decode("utf-8") #format it
	final_word = "" 
	for letter in formatted_word: #add spaces in between the letters
		final_word+=letter+" "
	word = final_word.lower()
except: 
	#This bloc will trigger if the API call failed or returned some bizarrely unworkable value.
	#A word will be chosen randomly from this preset list.
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
pic.grid(row=0,column=0,rowspan=2) #These "grid" function calls insert elements into the GUI at specific row-column cells.
				   #rowspan refers to an element being able to take up a longer width.
 
UserInput = StringVar()
textfield = Entry(root, textvariable=UserInput, width=len(UserInput.get()))#the textfield
textfield.focus_set() #So the user can tart typing into it and guessing right away
textfield.grid(row=2, column=0)

# Label(root, text="Word: ").grid(row=0, column=1)

UnScWord = StringVar() #the creation of the underscore word.
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
