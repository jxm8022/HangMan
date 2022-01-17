from numpy import random
import tkinter as tk
from PIL import Image, ImageTk
import time

def getRandomWord():
    print("getting random word")
    f = open('wordlist.txt', 'r')
    counter = 0
    word = ""
    rnd = random.randint(1,numberOfWords())
    while counter != rnd:
        word = f.readline().strip('\n')
        counter += 1
    f.close()
    print("random word is: ", word)
    return word

def numberOfWords():
    f = open('wordlist.txt', 'r')
    counter = 0
    line = f.readline()
    while line:
        counter += 1
        line = f.readline().strip('\n')
    f.close()
    return counter

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Loading...")
        img = ImageTk.PhotoImage(Image.open("images/splash.png").resize((500,500), Image.ANTIALIAS))
        background = tk.Label(self)
        background.image = img
        background.configure(image=img)
        background.pack()
        self.update()

class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)
        self.title("HangMan")
        self.geometry("600x650")

        time.sleep(3)

        splash.destroy()

        self.deiconify()

        self.HANGMAN_PICS = {
            0: "images/template0.png",
            1: "images/template1.png",
            2: "images/template2.png",
            3: "images/template3.png",
            4: "images/template4.png",
            5: "images/template5.png",
            6: "images/template6.png",
        }

        self.tries = 0

        img = ImageTk.PhotoImage(Image.open(self.HANGMAN_PICS[self.tries]).resize((400,400)))#, Image.ANTIALIAS))

        self.man = tk.Label(self) # CHANGE IMAGE
        self.man.image = img
        self.man.configure(image=img)
        self.man.pack(pady=30)

        self.ans = getRandomWord()
        self.placeholder = (" _ " * len(self.ans)).split()
        self.word = tk.Label(self, text=self.placeholder)
        self.word.pack(pady=10, padx=10)

        self.used = []
        self.guessed = tk.Label(self, text=self.used)
        self.guessed.pack(pady=10, padx=10)

        group = tk.Frame(self)

        self.guess = tk.StringVar()
        self.text = tk.Entry(group,textvariable=self.guess, width=10)
        self.text.grid(row=0, column=0)

        button = tk.Button(group, text="submit",
            command=lambda: self.checkLetter())
        self.bind("<Return>", (lambda event: self.checkLetter()))
        button.grid(row=0, column=1)

        group.pack(pady=10, padx=10)

        self.notif = tk.Label(self)
        self.notif.pack(pady=10, padx=10)

    def checkLetter(self):
        guess = self.guess.get()
        if len(self.guess.get()) == 1:
            print("checking letter: ", guess)
            if guess in self.used:
                self.notif.config(text=guess+" has already been used.")
                self.text.delete(0, 'end')
            else:
                self.used.append(self.guess.get())
                if guess in self.ans:
                    self.notif.config(text="Noice!")
                    self.updateWord(guess)
                else:
                    self.notif.config(text="Sorry!")
                    self.changeMan()
            self.guessed.config(text=self.used)
        else:
            self.notif.config(text=guess+" is not a letter.")

    def changeMan(self):
        print("changing man")
        self.text.delete(0, 'end')
        self.tries += 1
        if self.tries == len(self.HANGMAN_PICS)-1:
            self.notif.config(text="You lose! - "+self.ans)
            self.newGame()
        else:
            img = ImageTk.PhotoImage(Image.open(self.HANGMAN_PICS[self.tries]).resize((400,400)))#, Image.ANTIALIAS))
            self.man.image = img
            self.man.config(image=img)
        
    def updateWord(self, guess):
        print("updating word")
        self.text.delete(0, 'end')
        counter = 0
        for x in self.ans:
            if x == guess:
                self.placeholder[counter] = guess
            counter += 1
        self.word.config(text=self.placeholder)
        if '_' not in self.placeholder:
            self.notif.config(text="Congratulations, you win!")
            self.newGame()

    def newGame(self):
        print("new game")
        self.tries = 0
        img = ImageTk.PhotoImage(Image.open(self.HANGMAN_PICS[self.tries]).resize((400,400)))#, Image.ANTIALIAS))
        self.man.image = img
        self.man.config(image=img)
        self.ans = getRandomWord()
        self.placeholder = (" _ " * len(self.ans)).split()
        self.word.config(text=self.placeholder)
        self.used = []
        self.guessed.config(text=self.used)

if __name__ == "__main__":
    app = Game()
    app.mainloop()