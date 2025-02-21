import random
import time
import pygame
import hashlib

botNames = ["BOT Noah", "BOT Emma", "BOT Liam", "BOT Olivia", "BOT  William", "BOT Ava", "BOT Mason", "BOT Sophia",
            "BOT James", "BOT Isabella", "BOT Ben", "BOT Mia", "BOT Jacob", "BOT Charlotte", "BOT Michael",
            "BOT Abigail", "BOT Elijah", "BOT Emily", "BOT Ethan", "BOT Sylvia", "BOT Alex", "BOT Amelia", "BOT Ollie",
            "BOT Evelyn", "BOT Daniel", "BOT Elizabeth", "BOT Lucas", "BOT Sofia", "BOT Matthew", "BOT Madison",
            "BOT Aden", "BOT Avery", "BOT Jack", "BOT Ella", "BOT Logan", "BOT Scarlett", "BOT Toby", "BOT Grace",
            "BOT Joe", "BOT Chloe"]  # Array of Bot usernames to be assigned when initialising bots


class Button:
    # Create an instance of button
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):

        buttonPressed = False
        # Take position of mouse
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            # Check if player has clicked on button
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                buttonPressed = True

            # Check if player has not clicked on the button
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        window.blit(self.image, (self.rect.x, self.rect.y))

        return buttonPressed


class Player:
    def __init__(self, given_name):  # Constructor procedure to create a new object
        self.Name = given_name  # Assigns object the attribute name given by user
        self.Hand = []  # Assigns object the attribute hand
        self.Type = "Player"

    def getHand(self):
        return self.Hand  # Returns the object's attribute hand back to the program

    def setHand(self, new_hand):
        for i in range(len(new_hand)):
            if (new_hand[i][0] == "Red" or new_hand[i][0] == "Blue" or new_hand[i][0] == "Yellow"
                    or new_hand[i][0] == "Green" or new_hand[i][0] == "Wild"):  # Validates the inputted colour
                if (("0" <= new_hand[i][1] <= "9") or new_hand[i][1] == "+2" or new_hand[i][1] == "+4"
                        or new_hand[i][1] == "+0" or new_hand[i][1] == "Block"
                        or new_hand[i][1] == "Skip"):  # Validates the inputted number
                    self.Hand = new_hand  # Edits the object's attribute hand
                else:
                    print("Invalid value entered.")
            else:
                print("Invalid colour entered.")

    def draw_cards(self, temp_deck, temp_dpointer):  # Behaviour that allows the object to draw cards from the deck
        drawn_card, temp_deck, temp_dpointer = pop(temp_deck, temp_dpointer)  # Calls for the pop function to return
        # the top card of the deck stack
        self.Hand.append(drawn_card)  # Appends the drawn card to the object's attribute hand
        return temp_deck, temp_dpointer

    def play_cards(self, temp_pile, temp_pile_pointer, temp_reversed_order, temp_card_index):
        # Behaviour that allows the object to play a card that is in their hand

        """
        # Used before GUI was implemented to get the card a player would like to play
        temp_card = []
        playc_cont = False
        while not playc_cont:  # While loop used to validate the player's inputted colour
            temp_colour = input("What is the colour of the card you would like to play?"
                                " (Blue/Red/Yellow/Green/Wild): ").title()
            if (temp_colour == "Blue" or temp_colour == "Red" or temp_colour == "Yellow" or temp_colour == "Green"
                    or temp_colour == "Wild"):
                playc_cont = True
                temp_card.append(temp_colour)
                if temp_colour == "Wild":
                    playc_cont = False
                    while not playc_cont:  # While loop used to validate the player's inputted colour
                        wild_colour = input("What would you like the colour of your Wild card to be?"
                                            " (Blue/Red/Yellow/Green): ").title()
                        if (wild_colour == "Blue" or wild_colour == "Red" or wild_colour == "Yellow" or
                                wild_colour == "Green"):
                            playc_cont = True

                        else:
                            print("Invalid Colour.")
            else:
                print("Invalid Colour.")
        playc_cont = False
        while not playc_cont:  # While loop used to validate the player's inputted Value
            temp_value = str(input("What is the value of the card you would like to play?"
                                   " (0-9/+0/+2/+4/Block/Reverse): ").title())
            if (("0" <= temp_value <= "9") or temp_value == "+0" or temp_value == "+2" or
                    temp_value == "+4" or temp_value == "Block" or temp_value == "Reverse"):
                playc_cont = True
                temp_card.append(temp_value)
            else:
                print("Invalid Value.")
        temp_hand = self.Hand

        playc_count = 0
        playc_found = False
        while playc_count < len(temp_hand) and not playc_found:  # Linear search to search if the inputted card
            # can be found in the player's hand
            if temp_hand[playc_count] == temp_card:
                playc_found = True
            else:
                playc_count += 1

        if not playc_found:
            print("You do not have this card!")
            return temp_pile, temp_pile_pointer, False, False, False, False, temp_reversed_order
            """
        validPlayedCard = validCard(self.Hand[temp_card_index], temp_pile, temp_pile_pointer)

        if not validPlayedCard:
            errorOutput("Not valid card")
            return temp_pile, temp_pile_pointer, False, False, False, False, temp_reversed_order
        else:
            if self.Hand[temp_card_index][0] == "Wild":
                # Get the colour of the wild card
                self.Hand[temp_card_index][0] = getWildColour(self.Hand[temp_card_index][1])
                if self.Hand[temp_card_index][1] == "+4":
                    temp_pile.append(self.Hand[temp_card_index])
                    del self.Hand[temp_card_index]
                    return temp_pile, (temp_pile_pointer + 1), True, False, True, False, temp_reversed_order
                    # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder
            if self.Hand[temp_card_index][1] == "+2":
                temp_pile.append(self.Hand[temp_card_index])
                del self.Hand[temp_card_index]
                return temp_pile, (temp_pile_pointer + 1), True, True, False, False, temp_reversed_order
            # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder
            if self.Hand[temp_card_index][1] == "Block":
                temp_pile.append(self.Hand[temp_card_index])
                del self.Hand[temp_card_index]
                return temp_pile, (temp_pile_pointer + 1), True, False, False, True, temp_reversed_order
                # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder
            if self.Hand[temp_card_index][1] == "Reverse":
                temp_pile.append(self.Hand[temp_card_index])
                del self.Hand[temp_card_index]
                if not temp_reversed_order:
                    return temp_pile, (temp_pile_pointer + 1), True, False, False, False, True
                    # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder
                else:
                    return temp_pile, (temp_pile_pointer + 1), True, False, False, False, False
                    # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder
            temp_pile.append(self.Hand[temp_card_index])
            del self.Hand[temp_card_index]
            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, temp_reversed_order
            # Returning Pile, pilePointer, inputCont, drawTwo, drawFour,Blocked, reversedOrder

    def callUno(self):
        if len(self.Hand) == 2:
            drawText((self.Name + " has called UNO!"), 427, 250)
            pygame.display.update()
            time.sleep(3)
            return True
        else:
            return False

    def sortHand(self):  # Sorts the player object's hand
        n = len(self.Hand)
        swapped = True
        while n > 0 and swapped:
            swapped = False
            for i in range(n - 1):
                if self.Hand[i] > self.Hand[i + 1]:
                    temp = self.Hand[i]
                    self.Hand[i] = self.Hand[i + 1]
                    self.Hand[i + 1] = temp
                    swapped = True

    def getAnalysis(self, temp_pile, temp_pile_pointer, temp_called_uno):

        global run
        cont = False
        continueImage = pygame.image.load('PNGs/Continue.png').convert_alpha()

        continueButton = Button(480, 500, continueImage, 1)

        # Simulates the Hard bot's process to determine the best way to play cards.
        validPlayableCard = False
        # If the user has only 2 cards left, analysis will recommend they call uno.
        if len(self.Hand) == 2 and not temp_called_uno:
            bestMove = "Call_Uno"
        else:
            for i in range(len(self.Hand)):
                temp_card = self.Hand[i]
                validPlayableCard = validCard(temp_card, temp_pile, temp_pile_pointer)
                # Checks if there is a 'special' card in hand, then checks if there is a card that can be played at all.
                if validPlayableCard:
                    if temp_card[0] == "Wild":
                        tempRandom = random.randint(1, 4)
                        if tempRandom == 1:
                            temp_card = ["Red"]
                        if tempRandom == 2:
                            temp_card = ["Blue"]
                        if tempRandom == 3:
                            temp_card = ["Green"]
                        if tempRandom == 4:
                            temp_card = ["Yellow"]
                        if self.Hand[i] == "+4":
                            temp_card.append("+4")
                        else:
                            temp_card.append("+0")
                        bestMove = temp_card
                        break
                    if temp_card[1] == "+2" or temp_card[1] == "Block" or temp_card[1] == "Reverse":
                        bestMove = temp_card
                        break
                if i == (len(self.Hand) - 1):
                    for count in range(len(self.Hand)):
                        temp_card = self.Hand[count]
                        validPlayableCard = validCard(temp_card, temp_pile, temp_pile_pointer)
                        if validPlayableCard:
                            bestMove = temp_card
                            break
            # If no available card, choose to draw
            if not validPlayableCard:
                bestMove = "Draw"

        # Simulates the Normal bot's process to determine the best way to play cards.
        validPlayableCard = False
        # If the user has only 2 cards left, analysis will recommend they call uno.
        if len(self.Hand) == 2 and not temp_called_uno:
            averageMove = "Call_Uno"
        else:
            # Checks if the user has a playable card in their hand.
            for i in range(len(self.Hand)):
                temp_card = self.Hand[i]
                validPlayableCard = validCard(temp_card, temp_pile, temp_pile_pointer)
                if validPlayableCard:
                    if temp_card[0] == "Wild":
                        tempRandom = random.randint(1, 4)
                        if tempRandom == 1:
                            temp_card = ["Red"]
                        if tempRandom == 2:
                            temp_card = ["Blue"]
                        if tempRandom == 3:
                            temp_card = ["Green"]
                        if tempRandom == 4:
                            temp_card = ["Yellow"]
                        if self.Hand[i] == "+4":
                            temp_card.append("+4")
                        else:
                            temp_card.append("+0")
                    averageMove = temp_card
                    break
            # If no available card, choose to draw
            if not validPlayableCard:
                averageMove = "Draw"

        # Simulates the Easy bot's process to determine the best way to play cards.
        validPlayableCard = False
        # If tempRandom is 1, and the user has only 2 cards left, analysis will recommend they call uno.
        # This is used to force the accuracy of the easy recommendation to decrease
        tempRandom = random.randint(1, 2)
        if tempRandom == 1 and len(self.Hand) == 2 and not temp_called_uno:
            worstMove = "Call_Uno"
        else:
            tempRandom = random.randint(1, 7)
            if tempRandom < 7:
                # Checks if the user has a playable card in their hand.
                for i in range(len(self.Hand)):
                    temp_card = self.Hand[i]
                    validPlayableCard = validCard(temp_card, temp_pile, temp_pile_pointer)
                    if validPlayableCard:
                        if temp_card[0] == "Wild":
                            tempRandom = random.randint(1, 4)
                            if tempRandom == 1:
                                temp_card = ["Red"]
                            if tempRandom == 2:
                                temp_card = ["Blue"]
                            if tempRandom == 3:
                                temp_card = ["Green"]
                            if tempRandom == 4:
                                temp_card = ["Yellow"]
                            if self.Hand[i][1] == "+4":
                                temp_card.append("+4")
                            else:
                                temp_card.append("+0")
                        worstMove = temp_card
                        break
                # If no available card, choose to draw
                if not validPlayableCard:
                    worstMove = "Draw"
            # If tempRandom is equal to 7, the bot will recommend to draw.
            # This is used to force the accuracy of the easy recommendation to decrease
            else:
                worstMove = "Draw"

        # Output all calculated moves.
        # While loop to refresh the page consistently, also allowing the pygame window to be closed
        while run and not cont:
            window.fill((186, 40, 0))

            '''
            # Used before GUI was implemented
            print("The best move is: " + str(bestMove) + "\nThe average move is: "
              + str(averageMove) + "\nThe worst move is: " + str(worstMove))
            '''

            drawText(("The best move is: " + str(bestMove)), 150, 150)
            drawText(("The average move is: " + str(averageMove)), 150, 280)
            drawText(("The worst move is: " + str(worstMove)), 150, 410)

            if continueButton.draw():
                time.sleep(1)
                cont = True

            for tempAction in pygame.event.get():
                if tempAction.type == pygame.QUIT:
                    run = False

            pygame.display.update()


class Bot(Player):
    def __init__(self, given_difficulty):  # constructor procedure for Bot class
        tempNamePointer = random.randint(0, (len(botNames) - 1))
        given_name = botNames[tempNamePointer]
        del botNames[tempNamePointer]
        super().__init__(given_name)
        self.Hand = []
        self.Type = "Bot"
        self.Difficulty = given_difficulty

    def play_cards(self, temp_pile, temp_pile_pointer, temp_reversed_order):
        if self.Difficulty == "Easy" or self.Difficulty == "Normal":  # actions a bot with difficulty set to normal or
            # easy will follow when it plays a card
            for i in range(len(self.Hand)):
                validPlayedCard = validCard(self.Hand[i], temp_pile, temp_pile_pointer)
                if validPlayedCard:
                    temp_card = self.Hand[i]
                    del self.Hand[i]
                    if temp_card[0] == "Wild":
                        tempRandom = random.randint(1, 4)
                        if tempRandom == 1:
                            temp_card[0] = "Red"
                        if tempRandom == 2:
                            temp_card[0] = "Blue"
                        if tempRandom == 3:
                            temp_card[0] = "Green"
                        if tempRandom == 4:
                            temp_card[0] = "Yellow"
                        if temp_card[1] == "+4":
                            temp_pile.append(temp_card)
                            return temp_pile, (temp_pile_pointer + 1), True, False, True, False, temp_reversed_order
                    if temp_card[1] == "+2":
                        temp_pile.append(temp_card)
                        return temp_pile, (temp_pile_pointer + 1), True, True, False, False, temp_reversed_order
                    if temp_card[1] == "Block":
                        temp_pile.append(temp_card)
                        return temp_pile, (temp_pile_pointer + 1), True, False, False, True, temp_reversed_order
                    if temp_card[1] == "Reverse":
                        temp_pile.append(temp_card)
                        if not temp_reversed_order:
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, True
                        else:
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, False
                    temp_pile.append(temp_card)
                    return temp_pile, (temp_pile_pointer + 1), True, False, False, False, temp_reversed_order
            return temp_pile, temp_pile_pointer, False, False, False, False, temp_reversed_order

        if self.Difficulty == "Hard":  # actions a bot with difficulty set to Hard will follow when it plays a card,
            # allowing it to attempt to play a special card before any other.
            for i in range(len(self.Hand)):
                validPlayedCard = validCard(self.Hand[i], temp_pile, temp_pile_pointer)
                if validPlayedCard:
                    temp_card = self.Hand[i]
                    if temp_card[0] == "Wild":
                        tempRandom = random.randint(1, 4)
                        if tempRandom == 1:
                            temp_card[0] = "Red"
                        if tempRandom == 2:
                            temp_card[0] = "Blue"
                        if tempRandom == 3:
                            temp_card[0] = "Green"
                        if tempRandom == 4:
                            temp_card[0] = "Yellow"
                        if temp_card[1] == "+4":
                            del self.Hand[i]
                            temp_pile.append(temp_card)
                            return temp_pile, (temp_pile_pointer + 1), True, False, True, False, temp_reversed_order
                        if temp_card[1] == "+0":
                            del self.Hand[i]
                            temp_pile.append(temp_card)
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, temp_reversed_order
                    if temp_card[1] == "+2":
                        del self.Hand[i]
                        temp_pile.append(temp_card)
                        return temp_pile, (temp_pile_pointer + 1), True, True, False, False, temp_reversed_order
                    if temp_card[1] == "Block":
                        del self.Hand[i]
                        temp_pile.append(temp_card)
                        return temp_pile, (temp_pile_pointer + 1), True, False, False, True, temp_reversed_order
                    if temp_card[1] == "Reverse":
                        del self.Hand[i]
                        temp_pile.append(temp_card)
                        if not temp_reversed_order:
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, True
                        else:
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, False
                if i == (len(self.Hand) - 1):
                    for count in range(len(self.Hand)):
                        validPlayedCard = validCard(self.Hand[count], temp_pile, temp_pile_pointer)
                        if validPlayedCard:
                            temp_card = self.Hand[count]
                            del self.Hand[count]
                            temp_pile.append(temp_card)
                            return temp_pile, (temp_pile_pointer + 1), True, False, False, False, temp_reversed_order
            return temp_pile, temp_pile_pointer, False, False, False, False, temp_reversed_order


def readFile():
    # Opens files in read mode
    usernameReadFile = open("username.txt", "r")
    passwordReadFile = open("password.txt", "r")
    winCountReadFile = open("winCount.txt", "r")

    global users
    users = []

    # Splits all files into single length lists
    usernames = (usernameReadFile.readline()).split()
    passwords = (passwordReadFile.readline()).split()
    winCounts = (winCountReadFile.readline()).split()

    # Combines all lists creating a 2D array of users
    for count in range(len(usernames)):
        users.append([usernames[count], passwords[count], winCounts[count]])


def writeFile(tempUsername, tempPassword, tempWinCount):
    # Opens files in append mode
    usernameWriteFile = open("username.txt", "a")
    passwordWriteFile = open("password.txt", "a")
    winCountWriteFile = open("winCount.txt", "a")

    # Encrypts entered password
    encodedPass = tempPassword.encode('utf-8')
    hashPassword = hashlib.sha3_256(encodedPass).hexdigest()

    # Appends User to files.
    usernameWriteFile.write(" " + tempUsername)
    passwordWriteFile.write(" " + str(hashPassword))
    winCountWriteFile.write(" " + str(tempWinCount))


def editFile():
    # Opens files in write mode
    usernameEditFile = open("username.txt", "w")
    passwordEditFile = open("password.txt", "w")
    winCountEditFile = open("winCount.txt", "w")
    global users

    # Splits users into singular parts, allocating them into corresponding files
    for count in range(len(users)):
        usernameEditFile.write(users[count][0]+" ")
        passwordEditFile.write(users[count][1] + " ")
        winCountEditFile.write(str(users[count][2]) + " ")


def signUp():
    # Initialise all variables used in sign-up
    global run
    submit = False
    goBack = False
    nameInputBox = pygame.Rect(125, 150, 1000, 65)
    passOneInputBox = pygame.Rect(125, 275, 1000, 65)
    passTwoInputBox = pygame.Rect(125, 400, 1000, 65)
    colourInactive = pygame.Color('White')
    colourActive = pygame.Color('Black')
    nameColour = colourInactive
    passOneColour = colourInactive
    passTwoColour = colourInactive
    tempFont = pygame.font.Font(None, 82)
    enterNameText = False
    enterOnePassText = False
    enterTwoPassText = False
    enteredNameText = ""
    enteredOnePassText = ""
    enteredTwoPassText = ""

    # Load all images used in log-in
    backImage = pygame.image.load('PNGs/Back.png').convert_alpha()
    signUpImage = pygame.image.load('PNGs/Sign-Up.png').convert_alpha()

    # Initialise all buttons in log-in
    backButton = Button(10, 10, backImage, 1)
    signUpButton = Button(480, 500, signUpImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not submit and not goBack:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nameInputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterNameText = not enterNameText  # Toggle the enterText variable
                    enterOnePassText = False
                    enterTwoPassText = False
                else:
                    enterNameText = False

                if passOneInputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterOnePassText = not enterOnePassText  # Toggle the enterText variable
                    enterNameText = False
                    enterTwoPassText = False
                else:
                    enterOnePassText = False

                if passTwoInputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterTwoPassText = not enterTwoPassText  # Toggle the enterText variable
                    enterNameText = False
                    enterOnePassText = False
                else:
                    enterTwoPassText = False
            nameColour = colourActive if enterNameText else colourInactive  # Change the colour of the input box if
            # highlighted
            passOneColour = colourActive if enterOnePassText else colourInactive  # Change the colour of the input
            # box if highlighted
            passTwoColour = colourActive if enterTwoPassText else colourInactive  # Change the colour of the input
            # box if highlighted
            if event.type == pygame.KEYDOWN:
                if enterNameText:
                    if event.key == pygame.K_BACKSPACE:
                        enteredNameText = enteredNameText[:-1]
                    else:
                        enteredNameText += event.unicode
                if enterOnePassText:
                    if event.key == pygame.K_BACKSPACE:
                        enteredOnePassText = enteredOnePassText[:-1]
                    else:
                        enteredOnePassText += event.unicode
                if enterTwoPassText:
                    if event.key == pygame.K_BACKSPACE:
                        enteredTwoPassText = enteredTwoPassText[:-1]
                    else:
                        enteredTwoPassText += event.unicode

        # Setting displayed GUI
        window.fill((186, 40, 0))
        name_txt_surface = tempFont.render(enteredNameText, True, nameColour)
        passOne_txt_surface = tempFont.render(enteredOnePassText, True, passOneColour)
        passTwo_txt_surface = tempFont.render(enteredTwoPassText, True, passTwoColour)
        drawText("Enter your username: ", 75, 112)
        drawText("Enter your password: ", 75, 242)
        drawText("Re-Enter your password: ", 75, 362)
        window.blit(name_txt_surface, (nameInputBox.x + 5, nameInputBox.y + 5))
        window.blit(passOne_txt_surface, (passOneInputBox.x + 5, passOneInputBox.y + 5))
        window.blit(passTwo_txt_surface, (passTwoInputBox.x + 5, passTwoInputBox.y + 5))
        pygame.draw.rect(window, nameColour, nameInputBox, 2)
        pygame.draw.rect(window, passOneColour, passOneInputBox, 2)
        pygame.draw.rect(window, passTwoColour, passTwoInputBox, 2)

        if backButton.draw():
            time.sleep(1)
            goBack = True

        if signUpButton.draw():
            time.sleep(1)

            # Validating username and checking for a strong password
            specialCharacter = False
            capitalCharacter = False
            containsSpace = False
            # Character check for if specific characters have been entered in password to help strength.
            for i in range(len(enteredOnePassText)):
                if enteredOnePassText[i] == "@" or enteredOnePassText[i] == "!" or enteredOnePassText[i] == "?" \
                        or enteredOnePassText[i] == "&" or enteredOnePassText[i] == "#" \
                        or enteredOnePassText[i] == "+" or enteredOnePassText[i] == "-" \
                        or enteredOnePassText[i] == "=" or enteredOnePassText[i] == "_":
                    specialCharacter = True
                if enteredOnePassText[i].isupper():
                    capitalCharacter = True
                if enteredOnePassText[i] == " ":
                    containsSpace = True

            for i in range(len(enteredNameText)):
                if enteredNameText[i] == " ":
                    containsSpace = True

            takenName = False
            readFile()
            for count in range(len(users)):
                if users[count][0] == enteredNameText:
                    takenName = True

            # Presence checks
            if len(enteredNameText) == 0:
                errorOutput("No username entered")

            elif len(enteredOnePassText) == 0:
                errorOutput("No password entered")

            # Check if username is taken
            elif takenName:
                errorOutput("Username taken")

            # Length Check
            elif len(enteredOnePassText) < 8:
                errorOutput("Password too short")

            # Character check output
            elif not specialCharacter:
                errorOutput("Password doesn't contain special character")
            elif not capitalCharacter:
                errorOutput("Password does not contain a capital character")
            elif containsSpace:
                errorOutput("Contains space")

            # Double entry check
            elif enteredTwoPassText != enteredOnePassText:
                errorOutput("Passwords do not match")

            else:
                # Write new user to database
                writeFile(enteredNameText, enteredOnePassText, 0)
                submit = True

        pygame.display.update()


def logIn():
    # Initialise all variables used in log-in
    global run
    submit = False
    nameInputBox = pygame.Rect(125, 150, 1000, 100)
    passInputBox = pygame.Rect(125, 350, 1000, 100)
    colourInactive = pygame.Color('White')
    colourActive = pygame.Color('Black')
    nameColour = colourInactive
    passColour = colourInactive
    tempFont = pygame.font.Font(None, 82)
    enterNameText = False
    enterPassText = False
    enteredNameText = ""
    enteredPassText = ""

    # Load all images used in log-in
    backImage = pygame.image.load('PNGs/Back.png').convert_alpha()
    signUpImage = pygame.image.load('PNGs/Sign-Up.png').convert_alpha()
    logInImage = pygame.image.load('PNGs/Log-In.png').convert_alpha()

    # Initialise all buttons in log-in
    backButton = Button(10, 10, backImage, 1)
    signUpButton = Button(1100, 10, signUpImage, 0.5)
    logInButton = Button(480, 500, logInImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not submit:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nameInputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterNameText = not enterNameText  # Toggle the enterText variable
                    enterPassText = False
                else:
                    enterNameText = False

                if passInputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterPassText = not enterPassText  # Toggle the enterText variable
                    enterNameText = False
                else:
                    enterPassText = False
            nameColour = colourActive if enterNameText else colourInactive  # Change the colour of the input box if
            # highlighted
            passColour = colourActive if enterPassText else colourInactive  # Change the colour of the input box if
            # highlighted

            if event.type == pygame.KEYDOWN:
                if enterNameText:
                    if event.key == pygame.K_BACKSPACE:
                        enteredNameText = enteredNameText[:-1]
                    else:
                        enteredNameText += event.unicode
                if enterPassText:
                    if event.key == pygame.K_BACKSPACE:
                        enteredPassText = enteredPassText[:-1]
                    else:
                        enteredPassText += event.unicode

        # Setting displayed GUI
        window.fill((186, 40, 0))
        name_txt_surface = tempFont.render(enteredNameText, True, nameColour)
        pass_txt_surface = tempFont.render(enteredPassText, True, passColour)
        drawText("Enter your username: ", 75, 100)
        drawText("Enter your password: ", 75, 300)
        window.blit(name_txt_surface, (nameInputBox.x + 5, nameInputBox.y + 5))
        window.blit(pass_txt_surface, (passInputBox.x + 5, passInputBox.y + 5))
        pygame.draw.rect(window, nameColour, nameInputBox, 2)
        pygame.draw.rect(window, passColour, passInputBox, 2)

        if backButton.draw():
            time.sleep(1)
            return None, False

        if logInButton.draw():
            time.sleep(1)
            found = False
            count = 0
            # checks files to see if user is present
            readFile()
            while not found and count < len(users):
                if users[count][0] == enteredNameText:
                    found = True
                else:
                    count += 1
            if not found:
                errorOutput("Not valid username")
            else:
                encodedPass = enteredPassText.encode('utf-8')
                hashPassword = hashlib.sha3_256(encodedPass).hexdigest()
                if users[count][1] == hashPassword:
                    return enteredNameText, True
                    # Returns Username, Login
                else:
                    errorOutput("Incorrect Password")

        if signUpButton.draw():
            time.sleep(1)
            signUp()

        pygame.display.update()


def shuffle_deck(temp_deck):
    shuffled_deck = []  # This is a 2D array which will hold the cards in a random order
    temp_length = len(temp_deck)  # This is an integer which will hold the length of the array temp_deck

    while temp_length > 0:  # This is used to ensure it will loop through this block of code
        # until there are no cards held in temp_deck
        shuffle_random = random.randint(0, (temp_length - 1))  # This is used to get a random index
        # between 0 and the final index of temp_deck
        shuffled_deck.append(temp_deck[shuffle_random])  # Adds the card held in index shuffle_random
        # to the shuffled_deck array
        del temp_deck[shuffle_random]  # Removes the card held in index shuffle_random from temp_deck
        # to ensure it will not be duplicated
        temp_length = len(temp_deck)  # Reassign the new length of temp_deck to temp_length

    return shuffled_deck


def build_deck():
    deck_builder = []  # This is a 2D array which will hold all cards that are needed in UNO!
    for i in range(4):  # Loop for each colour
        for _ in range(2):  # Loop for each copy of a numbered/action card
            for x in range(12):  # Loop for each value a card stores in UNO!
                newCard = [i, x]  # Assigning a new array for each card
                if i == 0:
                    newCard = ["Red", str(x + 1)]  # Will assign the card the colour red, as well as making
                    # its value x+1 to compensate for the fact x is an index value
                if i == 1:
                    newCard = ["Blue", str(x + 1)]  # Will assign the card the colour blue, as well as making
                    # its value x+1 to compensate for the fact x is an index value
                if i == 2:
                    newCard = ["Yellow", str(x + 1)]  # Will assign the card the colour yellow, as well as making
                    # its value x+1 to compensate for the fact x is an index value
                if i == 3:
                    newCard = ["Green", str(x + 1)]  # Will assign the card the colour green, as well as making
                    # its value x+1 to compensate for the fact x is an index value
                if x == 9:
                    newCard = [newCard[0], "Block"]  # When the value of x is 9, the value of the new card
                    # will be set to the action block
                if x == 10:
                    newCard = [newCard[0], "Reverse"]  # When the value of x is 9, the value of the new card
                    # will be set to the action Reverse
                if x == 11:
                    newCard = [newCard[0], "+2"]  # When the value of x is 9, the value of the new card
                    # will be set to the action +2
                deck_builder.append(newCard)  # Add each iteration of newCard to deck_builder array

    for i in range(4):  # Loop for each colour
        if i == 0:
            newCard = ["Red", "0"]  # Will assign the card the colour red, with value 0
            deck_builder.append(newCard)  # Add newCard to deck_builder array
        if i == 1:
            newCard = ["Blue", "0"]  # Will assign the card the colour blue, with value 0
            deck_builder.append(newCard)  # Add newCard to deck_builder array
        if i == 2:
            newCard = ["Yellow", "0"]  # Will assign the card the colour yellow, with value 0
            deck_builder.append(newCard)  # Add newCard to deck_builder array
        if i == 3:
            newCard = ["Green", "0"]  # Will assign the card the colour green, with value 0
            deck_builder.append(newCard)  # Add newCard to deck_builder array

    for i in range(2):  # Loop for each value of card
        for _ in range(4):  # Loop for each copy of cards
            if i == 0:
                newCard = ["Wild", "+4"]  # Will set newCard to Wild with a value of +4
            else:
                newCard = ["Wild", "+0"]  # Will set newCard to Wild with a value of +0
            deck_builder.append(newCard)  # Add newCard to deck_builder array

    new_pointer = len(deck_builder) - 1  # Will assign new_pointer the index of the last value in new_pointer
    deck_builder = shuffle_deck(deck_builder)  # Will call the shuffle_deck function, which
    # will return the deck in a random order

    return deck_builder, new_pointer


def pop(temp_deck, temp_dpointer):
    if temp_dpointer > 0:  # Check if the current deck is empty
        drawn_card = temp_deck[temp_dpointer]  # Takes the top card of stack temp_deck and assign it to drawn_card
        del temp_deck[temp_dpointer]  # Removes the top card of stack temp_deck
        temp_dpointer -= 1  # Decrease temp_dpointer by one
    else:  # Runs if deck is empty
        temp_deck, temp_dpointer = build_deck()  # Creates a new deck by calling build_deck
        drawn_card = temp_deck[temp_dpointer]  # Takes the top card of stack temp_deck and assign it to drawn_card
        del temp_deck[temp_dpointer]  # Removes the top card of stack temp_deck
        temp_dpointer -= 1  # Decrease temp_dpointer by one

    return drawn_card, temp_deck, temp_dpointer


def validCard(played_card, temp_pile, temp_pile_pointer):  # Ensures the entered card is a valid card to be played
    validPlayedCard = False
    if played_card[0] == "Wild":
        validPlayedCard = True
    if played_card[0] == temp_pile[temp_pile_pointer][0]:
        validPlayedCard = True
    if played_card[1] == temp_pile[temp_pile_pointer][1]:
        validPlayedCard = True
    return validPlayedCard


def drawText(tempText, x, y):
    global font
    text = font.render(tempText, True, (0, 0, 0))
    window.blit(text, (x, y))


def errorOutput(cause):
    global run
    goBack = False
    pygame.display.set_caption("Error Screen")

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not goBack:
        for tempAction in pygame.event.get():
            window.fill((186, 40, 0))

            # Identify cause and output corresponding error message
            if cause == "Invalid Input":
                drawText("You have entered an invalid input, Please try again:", 50, 100)
                goBack = True

            if cause == "Invalid Bot settings":
                drawText("You have not entered correct bot settings, Please try again:", 50, 100)
                goBack = True

            if cause == "Invalid Player Count":
                drawText("Your bot and player count is not within 2-4 players, Please try again:", 50, 100)
                goBack = True

            if cause == "Invalid Bot settings And Player Count":
                drawText("Your bot and player count is not within 2-4 players, Please try again:", 50, 100)
                drawText("You have not entered correct bot settings, Please try again:", 50, 150)
                goBack = True

            if cause == "No username entered":
                drawText("You have not entered a username. Please try again:", 50, 150)
                goBack = True

            if cause == "No password entered":
                drawText("You have not entered a password. Please try again:", 50, 150)
                goBack = True

            if cause == "Password too short":
                drawText("Your password must be at least 8 characters. Please try again:", 50, 150)
                goBack = True

            if cause == "Password doesn't contain special character":
                drawText("Your password must contain one of the following: @, !, ?, &, #, +, -, _, +. "
                         "Please try again:", 50, 150)
                goBack = True

            if cause == "Password does not contain a capital character":
                drawText("Your password must contain a capital character. Please try again:", 50, 150)
                goBack = True

            if cause == "Passwords do not match":
                drawText("Your passwords do not match. Please try again:", 50, 150)
                goBack = True

            if cause == "Username taken":
                drawText("This username is already taken! Please try again:", 50, 150)
                goBack = True

            if cause == "Not valid username":
                drawText("There is not a user with this username. Please try again", 50, 150)
                goBack = True

            if cause == "Contains space":
                drawText("Your username or password contains a space, this is not allowed. Please try again:", 50, 150)
                goBack = True

            if cause == "Incorrect Password":
                drawText("The inputted password is incorrect! Please try again.", 50, 150)
                goBack = True

            if cause == "Not valid card":
                drawText("You cannot play this card, Please try again.", 50, 150)
                goBack = True

            if tempAction.type == pygame.QUIT:
                run = False
        pygame.display.update()

    time.sleep(3)


def leaderboard():

    # Initialises variables used in leaderboard
    global run
    global users
    users = []
    readFile()
    goBack = False

    # Insertion sort to sort the user's in descending order in terms of winCount
    for count in range(len(users)):
        while count > 0 and users[count][2] > users[count - 1][2]:
            temp = users[count]
            users[count] = users[count - 1]
            users[count - 1] = temp
            count = count - 1

    # Load all images used in leaderboard
    backImage = pygame.image.load('PNGs/Back.png').convert_alpha()

    # Initialise all buttons in leaderboard
    backButton = Button(10, 10, backImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not goBack:
        # Setting displayed GUI
        window.fill((186, 40, 0))

        drawText("Username:", 50, 100)
        drawText("Win Count:", 400, 100)

        for i in range(len(users)):
            if i == 0:
                drawText(str(users[0][0]), 65, 155)
                drawText(str(users[0][2]), 415, 155)
            if i == 1:
                drawText(str(users[1][0]), 65, 205)
                drawText(str(users[1][2]), 415, 205)
            if i == 2:
                drawText(str(users[2][0]), 65, 255)
                drawText(str(users[2][2]), 415, 255)
            if i == 3:
                drawText(str(users[3][0]), 65, 305)
                drawText(str(users[3][2]), 415, 305)
            if i == 4:
                drawText(str(users[4][0]), 65, 355)
                drawText(str(users[4][2]), 415, 355)

        if backButton.draw():
            time.sleep(1)
            goBack = True

        for tempAction in pygame.event.get():
            if tempAction.type == pygame.QUIT:
                run = False

        pygame.display.update()


def botSettings(botNumber, botDifficulty):
    global run
    submit = False

    # Load all images used in Bot Settings
    oneBotImage = pygame.image.load('PNGs/OneBot.png').convert_alpha()
    twoBotImage = pygame.image.load('PNGs/TwoBot.png').convert_alpha()
    threeBotImage = pygame.image.load('PNGs/ThreeBot.png').convert_alpha()
    easyBotImage = pygame.image.load('PNGs/EasyBot.png').convert_alpha()
    mediumBotImage = pygame.image.load('PNGs/MediumBot.png').convert_alpha()
    hardBotImage = pygame.image.load('PNGs/HardBot.png').convert_alpha()
    saveChangesImage = pygame.image.load('PNGs/SaveChanges.png').convert_alpha()

    # Initialise all buttons in Bot Settings
    oneBotButton = Button(245, 75, oneBotImage, 0.5)
    twoBotButton = Button(565, 75, twoBotImage, 0.5)
    threeBotButton = Button(885, 75, threeBotImage, 0.5)
    easyBotButton = Button(245, 375, easyBotImage, 0.5)
    mediumBotButton = Button(565, 375, mediumBotImage, 0.5)
    hardBotButton = Button(885, 375, hardBotImage, 0.5)
    saveChangesButton = Button(480, 600, saveChangesImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not submit:
        pygame.display.set_caption("Bot Settings")
        for tempAction in pygame.event.get():
            window.fill((186, 40, 0))

            drawText("Select number of bots:", 50, 25)
            if oneBotButton.draw():
                time.sleep(1)
                botNumber = 1

            if twoBotButton.draw():
                time.sleep(1)
                botNumber = 2

            if threeBotButton.draw():
                time.sleep(1)
                botNumber = 3

            drawText("Select difficulty of bots:", 50, 300)
            if easyBotButton.draw():
                time.sleep(1)
                botDifficulty = "Easy"

            if mediumBotButton.draw():
                time.sleep(1)
                botDifficulty = "Normal"

            if hardBotButton.draw():
                time.sleep(1)
                botDifficulty = "Hard"

            if saveChangesButton.draw():
                time.sleep(1)
                if botDifficulty is not None and 0 <= botNumber <= 3:
                    return botNumber, botDifficulty
                else:
                    errorOutput("Invalid Input")

            if tempAction.type == pygame.QUIT:
                run = False

        pygame.display.update()


def playerSettings(playerNumber):
    global run
    submit = False

    # Load all images used in Player Settings
    onePlayerImage = pygame.image.load('PNGs/OnePlayer.png').convert_alpha()
    twoPlayerImage = pygame.image.load('PNGs/TwoPlayer.png').convert_alpha()
    threePlayerImage = pygame.image.load('PNGs/ThreePlayer.png').convert_alpha()
    fourPlayerImage = pygame.image.load('PNGs/FourPlayer.png').convert_alpha()
    saveChangesImage = pygame.image.load('PNGs/SaveChanges.png').convert_alpha()

    # Load all images used in Player Settings
    onePlayerButton = Button(75, 250, onePlayerImage, 0.5)
    twoPlayerButton = Button(385, 250, twoPlayerImage, 0.5)
    threePlayerImage = Button(715, 250, threePlayerImage, 0.5)
    fourPlayerImage = Button(1035, 250, fourPlayerImage, 0.5)
    saveChangesButton = Button(480, 600, saveChangesImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not submit:
        pygame.display.set_caption("Player Settings")
        for tempAction in pygame.event.get():
            window.fill((186, 40, 0))

            drawText("How many players are playing:", 50, 200)

            if onePlayerButton.draw():
                time.sleep(1)
                playerNumber = 1

            if twoPlayerButton.draw():
                time.sleep(1)
                playerNumber = 2

            if threePlayerImage.draw():
                time.sleep(1)
                playerNumber = 3

            if fourPlayerImage.draw():
                time.sleep(1)
                playerNumber = 4

            if saveChangesButton.draw():
                time.sleep(1)
                if 1 <= playerNumber <= 4:
                    return playerNumber
                else:
                    errorOutput("Invalid Input")

            if tempAction.type == pygame.QUIT:
                run = False
        pygame.display.update()


def initialiseLocalGame():
    global run
    goBack = False
    botNumber = 0
    botDifficulty = None
    playerNumber = 0

    # Load all images used in Initialisation
    botSettingsImage = pygame.image.load('PNGs/BotSettings.png').convert_alpha()
    playerSettingsImage = pygame.image.load('PNGs/PlayerSettings.png').convert_alpha()
    tempPlayGameButton = pygame.image.load('PNGs/TempPlayGame.png').convert_alpha()
    backImage = pygame.image.load('PNGs/Back.png').convert_alpha()

    # Initialise all buttons in Initialisation
    botSettingsButton = Button(480, 200, botSettingsImage, 0.5)
    playerSettingsButton = Button(480, 300, playerSettingsImage, 0.5)
    tempPlayGameButton = Button(400, 450, tempPlayGameButton, 0.75)
    backButton = Button(10, 10, backImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not goBack:
        pygame.display.set_caption("Local play initialisation")
        for tempAction in pygame.event.get():
            window.fill((186, 40, 0))

            if botSettingsButton.draw():
                time.sleep(1)
                botNumber, botDifficulty = botSettings(botNumber, botDifficulty)

            if playerSettingsButton.draw():
                time.sleep(1)
                playerNumber = playerSettings(playerNumber)

            if tempPlayGameButton.draw():
                time.sleep(1)

                if (2 <= (playerNumber + botNumber) <= 4 and (botDifficulty is not None or
                                                              (botNumber == 0 and playerNumber != 1)) and
                        playerNumber != 0):
                    playGame(playerNumber, botNumber, botDifficulty)

                else:
                    # Validating received inputs
                    if ((botNumber + playerNumber) < 2 or (botNumber + playerNumber) > 4) and botDifficulty is None:
                        errorOutput("Invalid Bot settings And Player Count")
                    else:
                        if botDifficulty is None:
                            errorOutput("Invalid Bot settings")

                        else:
                            errorOutput("Invalid Player Count")

            if backButton.draw():
                goBack = True

            if tempAction.type == pygame.QUIT:
                run = False
        pygame.display.update()


def initialiseGame():
    global run
    global playGameImage
    goBack = False

    # Load all images used in Initialisation
    localPlayImage = pygame.image.load('PNGs/LocalPlay.png').convert_alpha()
    onlinePlayImage = pygame.image.load('PNGs/OnlinePlay.png').convert_alpha()
    backImage = pygame.image.load('PNGs/Back.png').convert_alpha()

    # Initialise all buttons in Initialisation
    localPlayButton = Button(96, 72, localPlayImage, 1)
    onlinePlayButton = Button(736, 72, onlinePlayImage, 1)
    backButton = Button(10, 10, backImage, 1)

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not goBack:
        pygame.display.set_caption("Initialisation")

        for tempAction in pygame.event.get():
            window.fill((186, 40, 0))

            if localPlayButton.draw():
                time.sleep(1)
                initialiseLocalGame()
                break

            if onlinePlayButton.draw():
                time.sleep(1)
                print("Online")

            if backButton.draw():
                time.sleep(1)
                goBack = True

            if tempAction.type == pygame.QUIT:
                run = False

        pygame.display.update()


def inputName(count):
    # Initialise variables used in inputName
    global run
    inputBox = pygame.Rect(125, 200, 1000, 100)
    colourInactive = pygame.Color('White')
    colourActive = pygame.Color('Black')
    colour = colourInactive
    tempFont = pygame.font.Font(None, 82)
    enterText = False
    enteredText = ""

    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputBox.collidepoint(event.pos):  # If user clicks on the user clicks the input box
                    enterText = not enterText  # Toggle the enterText variable
                else:
                    enterText = False
            colour = colourActive if enterText else colourInactive  # Change the colour of the input box if highlighted

            if event.type == pygame.KEYDOWN:
                if enterText:
                    if event.key == pygame.K_RETURN:
                        return enteredText
                    elif event.key == pygame.K_BACKSPACE:
                        enteredText = enteredText[:-1]
                    else:
                        enteredText += event.unicode

        # Update the display
        window.fill((186, 40, 0))
        txt_surface = tempFont.render(enteredText, True, colour)
        drawText(("What is Player " + str([count + 1]) + "'s name?: "), 75, 100)
        window.blit(txt_surface, (inputBox.x + 5, inputBox.y + 5))
        pygame.draw.rect(window, colour, inputBox, 2)

        pygame.display.update()


def cardToDisplay(tempCard):

    tempReturn = []
    # Determines the colour of the card needed to display
    if tempCard[0] == "Blue":
        tempReturn.append("B")
    if tempCard[0] == "Red":
        tempReturn.append("R")
    if tempCard[0] == "Green":
        tempReturn.append("G")
    if tempCard[0] == "Yellow":
        tempReturn.append("Y")
    if tempCard[0] == "Wild":
        tempReturn.append("Wild")

    # Determines the value of the card needed to display
    for i in range(0, 10):
        if tempCard[1] == str(i):
            tempReturn.append(str(i))
            break
    if tempCard[1] == "Block":
        tempReturn.append("B")
    if tempCard[1] == "Reverse":
        tempReturn.append("R")
    if tempCard[1] == "+2":
        tempReturn.append("+2")
    if tempCard[1] == "+4":
        tempReturn.append("+4")
    if tempCard[1] == "+0":
        tempReturn.append("+0")

    return tempReturn


def getWildColour(tempValue):
    global run
    pygame.display.set_caption("Wild Colour Selector")

    # Determines the value of the wild card
    if tempValue == "+0":
        redWild = pygame.image.load('PNGs/Uno Cards/R+0.png')
        yellowWild = pygame.image.load('PNGs/Uno Cards/Y+0.png')
        greenWild = pygame.image.load('PNGs/Uno Cards/G+0.png')
        blueWild = pygame.image.load('PNGs/Uno Cards/B+0.png')
    else:
        redWild = pygame.image.load('PNGs/Uno Cards/R+4.png')
        yellowWild = pygame.image.load('PNGs/Uno Cards/Y+4.png')
        greenWild = pygame.image.load('PNGs/Uno Cards/G+4.png')
        blueWild = pygame.image.load('PNGs/Uno Cards/B+4.png')

    # Initialises the coloured wild card buttons
    redWildButton = Button(218, 200, redWild, 1)
    yellowWildButton = Button(474, 200, yellowWild, 1)
    greenWildButton = Button(730, 200, greenWild, 1)
    blueWildButton = Button(986, 200, blueWild, 1)

    # Allows user's to select the colour of the wild card they are playing
    while run:
        window.fill((186, 40, 0))
        if redWildButton.draw():
            time.sleep(1)
            return "Red"
        if blueWildButton.draw():
            time.sleep(1)
            return "Blue"
        if greenWildButton.draw():
            time.sleep(1)
            return "Green"
        if yellowWildButton.draw():
            time.sleep(1)
            return "Yellow"

        for tempAction in pygame.event.get():
            if tempAction.type == pygame.QUIT:
                run = False

        pygame.display.update()


def playGame(inputPlayerNumb, inputBotNumb, tempDifficulty):
    # The main program that allows the user to play the game Uno!

    # Initialising variables to be used in the game
    playerList = []
    global run
    global loggedIn
    global Username
    gameWon = False
    reversedOrder = False
    drawTwo = False
    drawFour = False
    blocked = False
    playerNumb = inputPlayerNumb + inputBotNumb
    playerPointer = 0
    Pile = []
    pilePointer = 0

    '''
    # Used to get bot and player number before GUI was implemented

    validPNumber = False
    validBNumber = False
    validTNumber = False

    while not validTNumber:
        while not validPNumber:  # While loop to validate the user's input
            try:
                playerNumb = int(input("How many people are playing? (1-4): "))

                if 1 <= playerNumb <= 4:
                    validPNumber = True
                else:
                    print("Invalid player number.")
            except ValueError:
                print("Erroneous player number.")

        while not validBNumber:  # While loop used to validate the user's input
            try:
                botNumb = int(input("How many Bots would you like to play? (0-3): "))

                if 0 <= botNumb <= 3:
                    validBNumber = True
                else:
                    print("Invalid bot number.")
            except ValueError:
                print("Erroneous bot number.")

        if 2 <= (playerNumb + botNumb) <= 4:
            validTNumber = True
        else:
            print("Invalid total number.")
            validPNumber = False
            validBNumber = False
    '''

    for i in range(inputPlayerNumb):  # Initialising the amount of players the user has asked to play

        if loggedIn and i == 0:
            tempName = Username
        else:
            tempName = inputName(i)
        if i == 0:
            Player1 = Player(tempName)
            playerList.append(Player1)
        if i == 1:
            Player2 = Player(tempName)
            playerList.append(Player2)
        if i == 2:
            Player3 = Player(tempName)
            playerList.append(Player3)
        if i == 3:
            Player4 = Player(tempName)
            playerList.append(Player4)

    for i in range(inputBotNumb):  # Initialising the amount of bots the user has asked to play
        if i == 0:
            Bot1 = Bot(tempDifficulty)
            playerList.append(Bot1)
        if i == 1:
            Bot2 = Bot(tempDifficulty)
            playerList.append(Bot2)
        if i == 2:
            Bot3 = Bot(tempDifficulty)
            playerList.append(Bot3)

    '''
            # Used to get bot difficulty before GUI was implemented 
    for i in range(botNumb):  # Initialising the amount of bots the user has asked to play

        # Used to get bot difficulty before GUI was implemented 

        validDiff = False
        while not validDiff:
            tempDifficulty = input("What is the difficulty of bot" + str(i + 1) + "? (Easy/Normal/Hard): ").title()
            if tempDifficulty == "Easy" or tempDifficulty == "Normal" or tempDifficulty == "Hard":
                validDiff = True
            else:
                print("Invalid difficulty.")

        if i == 0:
            Bot1 = Bot(tempDifficulty)
            playerList.append(Bot1)
        if i == 1:
            Bot2 = Bot(tempDifficulty)
            playerList.append(Bot2)
        if i == 2:
            Bot3 = Bot(tempDifficulty)
            playerList.append(Bot3)


        # Object creation used when Bot testing
        if i == 3:
            Bot4 = Bot(tempDifficulty)
            playerList.append(Bot4)
        '''

    '''
    # Initialisation used when testing bot difficulty
    Bot1 = Bot("Hard")
    Bot2 = Bot("Normal")
    Bot3 = Bot("Easy")
    playerNumb = 3
    playerList = [Bot1, Bot2, Bot3]
    '''

    Deck, deckPointer = build_deck()
    startingCard, Deck, deckPointer = pop(Deck, deckPointer)
    if startingCard[0] == "Wild":
        randInt = random.randint(1, 4)
        if randInt == 1:
            startingCard[0] = "Red"
        if randInt == 2:
            startingCard[0] = "Blue"
        if randInt == 3:
            startingCard[0] = "Yellow"
        if randInt == 4:
            startingCard[0] = "Green"
    Pile.append(startingCard)

    for i in range(playerNumb):  # Initialising player's initial hands

        for x in range(7):
            Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
        playerPointer += 1

    playerPointer = 0  # Resetting the playerPointer for the game to be played

    # While loop to refresh the page consistently, also allowing the pygame window to be closed.
    while run and not gameWon:

        pageIndex = 0
        inputCont = False
        calledUno = False

        window.fill((186, 40, 0))

        # Load all images used in the main game
        pygame.display.set_caption("Play Game")
        tempDisplayPile = cardToDisplay(Pile[pilePointer])
        displayPileImage = pygame.image.load('PNGS/Uno Cards/' + tempDisplayPile[0] + tempDisplayPile[1] +
                                             ".png").convert_alpha()
        cardBackImage = pygame.image.load('PNGs/Uno Cards/CardBack.png').convert_alpha()
        callUnoImage = pygame.image.load('PNGs/CallUNO.png').convert_alpha()
        nextPageImage = pygame.image.load('PNGs/NextPage.png').convert_alpha()
        analyseImage = pygame.image.load('PNGs/Analyse.png').convert_alpha()

        # Initialise all buttons in the main game.
        drawPileButton = Button(522, 310, cardBackImage, 1)
        callUnoButton = Button(687, 323, callUnoImage, 0.5)
        nextPageButton = Button(875, 625, nextPageImage, 1)
        analyseButton = Button(1000, 615, analyseImage, 0.75)

        if blocked:  # If the last played card was a block card, will skip the player's turn
            blocked = False
            inputCont = True
            drawText((playerList[playerPointer].Name + "'s turn has been skipped!"), 427, 250)
            pygame.display.update()
            time.sleep(2)

        if drawTwo:  # If the last played card was a +2, will skip player's turn and force them to draw 2 cards
            for _ in range(2):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
            drawTwo = False
            inputCont = True
            drawText((playerList[playerPointer].Name + "'s turn has been skipped, they drew 2 cards!"), 427, 250)
            pygame.display.update()
            time.sleep(2)

        if drawFour:  # If the last played card was a +4, will skip player's turn and force them to draw 4 cards
            for _ in range(4):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
            drawFour = False
            inputCont = True
            drawText((playerList[playerPointer].Name + "'s turn has been skipped, they drew 4 cards!"), 427, 250)
            pygame.display.update()
            time.sleep(2)

        pygame.display.update()

        # While loop to refresh the page consistently, also allowing the pygame window to be closed
        # and buttons to be pressed.
        while not inputCont and run:  # Create a loop to ensure player inputs a valid input

            playerList[playerPointer].sortHand()
            pygame.display.set_caption("Play Game")
            window.fill((186, 40, 0))

            window.blit(displayPileImage, (602, 310))

            if playerList[playerPointer].Type == "Player":  # Checks to see if it's a player's turn.

                # Displays opponent to the right of current player's cards, name and card number
                if playerNumb >= 2:
                    tempPlayerPointer = playerPointer + 1
                    if tempPlayerPointer >= (playerNumb - 1):
                        tempPlayerPointer = tempPlayerPointer - playerNumb
                    if len(playerList[playerPointer].Hand) >= 3:
                        tempDisplayCard = 3
                    else:
                        tempDisplayCard = len(playerList[playerPointer].Hand)
                    for i in range(tempDisplayCard):
                        if i == 0:
                            window.blit(cardBackImage, (1195, 300))
                        if i == 1:
                            window.blit(cardBackImage, (1195, 375))
                        if i == 2:
                            window.blit(cardBackImage, (1195, 450))
                    drawText(playerList[tempPlayerPointer].Name, 1075, 220)
                    drawText(str(len(playerList[tempPlayerPointer].Hand)), 1075, 260)

                # Displays opponent opposite of current player's cards, name and card number
                if playerNumb >= 3:
                    tempPlayerPointer = playerPointer + 2
                    if tempPlayerPointer >= (playerNumb - 1):
                        tempPlayerPointer = tempPlayerPointer - playerNumb
                    if len(playerList[playerPointer].Hand) >= 7:
                        tempDisplayCard = 7
                    else:
                        tempDisplayCard = len(playerList[playerPointer].Hand)
                    for i in range(tempDisplayCard):
                        if i == 0:
                            window.blit(cardBackImage, (270, 10))
                        if i == 1:
                            window.blit(cardBackImage, (355, 10))
                        if i == 2:
                            window.blit(cardBackImage, (440, 10))
                        if i == 3:
                            window.blit(cardBackImage, (525, 10))
                        if i == 4:
                            window.blit(cardBackImage, (610, 10))
                        if i == 5:
                            window.blit(cardBackImage, (695, 10))
                        if i == 6:
                            window.blit(cardBackImage, (780, 10))
                    drawText(playerList[tempPlayerPointer].Name, 865, 10)
                    drawText(str(len(playerList[tempPlayerPointer].Hand)), 865, 50)

                # Displays opponent to the left of current player's cards, name and card number
                if playerNumb >= 4:
                    tempPlayerPointer = playerPointer + 3
                    if tempPlayerPointer >= (playerNumb - 1):
                        tempPlayerPointer = tempPlayerPointer - playerNumb
                    if len(playerList[playerPointer].Hand) >= 3:
                        tempDisplayCard = 3
                    else:
                        tempDisplayCard = len(playerList[playerPointer].Hand)
                    for i in range(tempDisplayCard):
                        if i == 0:
                            window.blit(cardBackImage, (10, 300))
                        if i == 1:
                            window.blit(cardBackImage, (10, 375))
                        if i == 2:
                            window.blit(cardBackImage, (10, 450))
                        drawText(playerList[tempPlayerPointer].Name, 10, 220)
                        drawText(str(len(playerList[tempPlayerPointer].Hand)), 10, 260)

                # Checks for how many pages of cards there are
                numberOfCardPages = (len(playerList[playerPointer].Hand) // 7)
                if (len(playerList[playerPointer].Hand) % 7) > 0:
                    numberOfCardPages += 1
                # Revert pageIndex back to 0 when it exceeds its range.
                if pageIndex == numberOfCardPages:
                    pageIndex = 0

                # Determines how many cards on the current page
                tempCountControl = len(playerList[playerPointer].Hand) % 7
                if tempCountControl == 0:
                    tempCountControl = 7

                # Initialises and Displays all card buttons that are on the current page card
                if pageIndex == (numberOfCardPages - 1):
                    for i in range(tempCountControl):
                        tempDisplayHand = cardToDisplay(playerList[playerPointer].Hand[i + (pageIndex * 7)])
                        if i == 0:
                            displayHand1 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand1Button = Button(270, 600, displayHand1, 1)
                        if i == 1:
                            displayHand2 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand2Button = Button(355, 600, displayHand2, 1)
                        if i == 2:
                            displayHand3 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand3Button = Button(440, 600, displayHand3, 1)
                        if i == 3:
                            displayHand4 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand4Button = Button(525, 600, displayHand4, 1)
                        if i == 4:
                            displayHand5 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand5Button = Button(610, 600, displayHand5, 1)
                        if i == 5:
                            displayHand6 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand6Button = Button(695, 600, displayHand6, 1)
                        if i == 6:
                            displayHand7 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand7Button = Button(780, 600, displayHand7, 1)

                    if displayHand1Button.draw():
                        time.sleep(1)
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                 (0 + (pageIndex * 7)))

                    if tempCountControl > 1:
                        if displayHand2Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (1 + (pageIndex * 7)))
                    if tempCountControl > 2:
                        if displayHand3Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (2 + (pageIndex * 7)))
                    if tempCountControl > 3:
                        if displayHand4Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (3 + (pageIndex * 7)))
                    if tempCountControl > 4:
                        if displayHand5Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (4 + (pageIndex * 7)))
                    if tempCountControl > 5:
                        if displayHand6Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (5 + (pageIndex * 7)))
                    if tempCountControl > 6:
                        if displayHand7Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (6 + (pageIndex * 7)))

                else:
                    for i in range(7):
                        tempDisplayHand = cardToDisplay(playerList[playerPointer].Hand[i + (pageIndex * 7)])
                        if i == 0:
                            displayHand1 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand1Button = Button(270, 600, displayHand1, 1)
                        if i == 1:
                            displayHand2 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand2Button = Button(355, 600, displayHand2, 1)
                        if i == 2:
                            displayHand3 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand3Button = Button(440, 600, displayHand3, 1)
                        if i == 3:
                            displayHand4 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand4Button = Button(525, 600, displayHand4, 1)
                        if i == 4:
                            displayHand5 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand5Button = Button(610, 600, displayHand5, 1)
                        if i == 5:
                            displayHand6 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand6Button = Button(695, 600, displayHand6, 1)
                        if i == 6:
                            displayHand7 = pygame.image.load(
                                'PNGS/Uno Cards/' + tempDisplayHand[0] + tempDisplayHand[1] +
                                ".png").convert_alpha()
                            displayHand7Button = Button(780, 600, displayHand7, 1)

                    if displayHand1Button.draw():
                        time.sleep(1)
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                 (0 + (pageIndex * 7)))

                    if len(playerList[playerPointer].Hand) > 1:
                        if displayHand2Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (1 + (pageIndex * 7)))
                    if len(playerList[playerPointer].Hand) > 2:
                        if displayHand3Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (2 + (pageIndex * 7)))
                    if len(playerList[playerPointer].Hand) > 3:
                        if displayHand4Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (3 + (pageIndex * 7)))
                    if len(playerList[playerPointer].Hand) > 4:
                        if displayHand5Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (4 + (pageIndex * 7)))
                    if len(playerList[playerPointer].Hand) > 5:
                        if displayHand6Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (5 + (pageIndex * 7)))
                    if len(playerList[playerPointer].Hand) > 6:
                        if displayHand7Button.draw():
                            time.sleep(1)
                            Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                                playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder,
                                                                     (6 + (pageIndex * 7)))

                # Buttons for player's actions
                if callUnoButton.draw():
                    time.sleep(1)
                    calledUno = playerList[playerPointer].callUno()

                if drawPileButton.draw():
                    time.sleep(1)
                    Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                    inputCont = True

                if analyseButton.draw():
                    time.sleep(1)
                    playerList[playerPointer].getAnalysis(Pile, pilePointer, calledUno)

                if len(playerList[playerPointer].Hand) > 7:
                    if nextPageButton.draw():
                        time.sleep(1)
                        pageIndex += 1

                for tempAction in pygame.event.get():
                    if tempAction.type == pygame.QUIT:
                        run = False

            if playerList[playerPointer].Type == "Bot":  # Checks to see if it's a bot's turn.

                if playerList[playerPointer].Difficulty == "Easy":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        botMove = random.randint(1, 2)  # Assigning a random variable to the bot's move,to
                        # allow the bot to make a 'mistake' giving player an advantage
                        if botMove == 1:
                            calledUno = playerList[playerPointer].callUno()
                    botMove = random.randint(1, 7)  # Assigning a random variable to the bot's move,to
                    # allow the bot to make a 'mistake' giving player an advantage
                    if botMove < 7:
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                        if not inputCont:  # If the bot is unable to play a card, it will draw a card
                            Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                            inputCont = True
                            drawText((playerList[playerPointer].Name + " drew a card"), 427, 250)
                        else:
                            drawText(
                                (playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer])),
                                427, 250)
                    if botMove == 7:
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        drawText((playerList[playerPointer].Name + " drew a card"), 427, 250)

                if playerList[playerPointer].Difficulty == "Normal":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        calledUno = playerList[playerPointer].callUno()
                    botMove = random.randint(1, 10)  # Assigning a random variable to the bot's move,to
                    # allow the bot to make a 'mistake' giving player an advantage
                    if botMove < 10:
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                        if not inputCont:  # If the bot is unable to play a card, it will draw a card
                            Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                            inputCont = True
                            drawText((playerList[playerPointer].Name + " drew a card"), 427, 250)
                        else:
                            drawText(
                                (playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer])),
                                427, 250)
                    if botMove == 10:
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        drawText((playerList[playerPointer].Name + " drew a card"), 427, 250)

                if playerList[playerPointer].Difficulty == "Hard":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        calledUno = playerList[playerPointer].callUno()
                    Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                        playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                    if not inputCont:  # If the bot is unable to play a card, it will draw a card
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        drawText((playerList[playerPointer].Name + " drew a card"), 427, 250)
                    else:
                        drawText((playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer])),
                                 427, 250)

            pygame.display.update()

        if len(playerList[playerPointer].Hand) == 1 and not calledUno:  # Player will receive a penalty (draw 2 cards)
            # for breaking rules if they do not call Uno! when they have 1 card left
            drawText((playerList[playerPointer].Name + " did not call UNO! They must draw 2 cards."), 427, 250)
            pygame.display.update()
            time.sleep(2)
            for i in range(2):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)

        if len(playerList[playerPointer].Hand) == 0:  # Checking if the current player has won the game
            drawText((playerList[playerPointer].Name + " has won the game!"), 427, 250)
            pygame.display.update()
            time.sleep(2)
            if playerPointer == 0 and loggedIn:
                found = False
                count = 0
                # add database check when database is made
                readFile()
                while not found and count < len(users):
                    if users[count][0] == Username:
                        found = True
                    else:
                        count += 1
                if found:
                    users[count][2] = int(users[count][2]) + 1
                    editFile()
            gameWon = True
            break

        if not reversedOrder:  # Incrementing the playerPointer when the order is not reversed
            playerPointer += 1
            if playerPointer > (playerNumb - 1):
                playerPointer = 0

        else:  # incrementing the playerPointer while the order is reversed
            playerPointer -= 1
            if playerPointer < 0:
                playerPointer = (playerNumb - 1)

        if playerList[playerPointer].Type == "Player":
            window.fill((186, 40, 0))
            drawText(("Please pass the device to " + playerList[playerPointer].Name), 427, 250)
            pygame.display.update()
            time.sleep(3)

        pygame.display.update()
        time.sleep(2)

    '''
    while not gameWon:  # Create a loop for if the game has not been won yet

        time.sleep(1)

        inputCont = False
        calledUno = False

        if blocked:  # If the last played card was a block card, will skip the player's turn
            blocked = False
            inputCont = True
            print("----------------------------------------------------------------------------------------------------"
                  "---\n" + playerList[playerPointer].Name + "'s turn was skipped!")

        if drawTwo:  # If the last played card was a +2, will skip player's turn and force them to draw 2 cards
            for _ in range(2):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
            drawTwo = False
            inputCont = True
            print("----------------------------------------------------------------------------------------------------"
                  "---\n" + playerList[playerPointer].Name + "'s turn was skipped, and they drew 2 cards!")

        if drawFour:  # If the last played card was a +4, will skip player's turn and force them to draw 4 cards
            for _ in range(4):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
            drawFour = False
            inputCont = True

            print("----------------------------------------------------------------------------------------------------"
                  "---\n" + playerList[playerPointer].Name + "'s turn was skipped, and they drew 4 cards!")

        while not inputCont:  # Create a loop to ensure player inputs a valid input

            time.sleep(1)
            print("-------------------------------------------------"
                  "------------------------------------------------------")
            print("It is currently " + playerList[playerPointer].Name + "'s turn.")
            print("The top card of the pile is:\n" + str(Pile[pilePointer]))
            playerList[playerPointer].sortHand()
            print("-------------------------------------------------"
                  "------------------------------------------------------")

            time.sleep(1)

            if playerList[playerPointer].Type == "Player":  # Checks to see if it's a player's turn.
                print(playerList[playerPointer].Name + "'s hand is currently:\n" + str(
                    playerList[playerPointer].getHand()))
                playerInput = input("What would Player" + str(playerPointer + 1) + " Like to do? (Draw/Play/"
                                                                                   "Call_Uno/Get_Analysis): ").title()

                if playerInput == "Draw":
                    Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                    inputCont = True

                elif playerInput == "Play":
                    Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                        playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)

                elif playerInput == "Call_Uno":
                    calledUno = playerList[playerPointer].callUno()

                elif playerInput == "Get_Analysis":
                    playerList[playerPointer].getAnalysis(Pile, pilePointer, calledUno)

                else:
                    print("Invalid input, please try again.")

            if playerList[playerPointer].Type == "Bot":  # Checks to see if it's a bot's turn.

                if playerList[playerPointer].Difficulty == "Easy":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        botMove = random.randint(1, 2)  # Assigning a random variable to the bot's move,to
                        # allow the bot to make a 'mistake' giving player an advantage
                        if botMove == 1:
                            calledUno = playerList[playerPointer].callUno()
                    botMove = random.randint(1, 7)  # Assigning a random variable to the bot's move,to
                    # allow the bot to make a 'mistake' giving player an advantage
                    if botMove < 7:
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                        if not inputCont:  # If the bot is unable to play a card, it will draw a card
                            Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                            inputCont = True
                            print(playerList[playerPointer].Name + " drew a card")
                        else:
                            print(playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer]))
                    if botMove == 7:
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        print(playerList[playerPointer].Name + " drew a card")

                if playerList[playerPointer].Difficulty == "Normal":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        calledUno = playerList[playerPointer].callUno()
                    botMove = random.randint(1, 10)  # Assigning a random variable to the bot's move,to
                    # allow the bot to make a 'mistake' giving player an advantage
                    if botMove < 10:
                        Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                            playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                        if not inputCont:  # If the bot is unable to play a card, it will draw a card
                            Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                            inputCont = True
                            print(playerList[playerPointer].Name + " drew a card")
                        else:
                            print(playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer]))
                    if botMove == 10:
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        print(playerList[playerPointer].Name + " drew a card")

                if playerList[playerPointer].Difficulty == "Hard":  # Checks current bot's difficulty
                    if len(playerList[playerPointer].Hand) == 2:
                        calledUno = playerList[playerPointer].callUno()
                    Pile, pilePointer, inputCont, drawTwo, drawFour, blocked, reversedOrder = \
                        playerList[playerPointer].play_cards(Pile, pilePointer, reversedOrder)
                    if not inputCont:  # If the bot is unable to play a card, it will draw a card
                        Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)
                        inputCont = True
                        print(playerList[playerPointer].Name + " drew a card")
                    else:
                        print(playerList[playerPointer].Name + " has played the card: " + str(Pile[pilePointer]))

        if len(playerList[playerPointer].Hand) == 1 and not calledUno:  # Player will receive a penalty (draw 2 cards)
            # for breaking rules if they do not call Uno! when they have 1 card left
            print("You did not call Uno! Draw 2 cards.")
            for i in range(2):
                Deck, deckPointer = playerList[playerPointer].draw_cards(Deck, deckPointer)

        if len(playerList[playerPointer].Hand) == 0:  # Checking if the current player has won the game
            print("----------------------------------------------------------------------------------------------------"
                  "---\n" + playerList[playerPointer].Name + " has won the game!")
            gameWon = True
            # return playerList[playerPointer].Difficulty  # Used when testing bots

        if not reversedOrder:  # Incrementing the playerPointer when the order is not reversed
            playerPointer += 1
            if playerPointer > (playerNumb - 1):
                playerPointer = 0
        else:  # incrementing the playerPointer while the order is reversed
            playerPointer -= 1
            if playerPointer < 0:
                playerPointer = (playerNumb - 1)

        '''


## Main Program ##

# Initialising data for main program
users = []
'''
  # Used as test data for read/writing

writeFile("AdminTest", "AdminTest@Password", 0)
writeFile("SecondPlayer", "MediocerPlayer@1234", 35)
writeFile("WorstPlayer", "UnoHater!234", 1)
writeFile("ThirdPlayer", "UnoLover@142134", 24)
writeFile("BestPlayer", "Goodplayer@1234", 78)
'''
pygame.init()
windowWidth = 1280
windowHeight = 720
window = pygame.display.set_mode((windowWidth, windowHeight))
font = pygame.font.Font(None, 30)

# Load all images used in main menu
logoImage = pygame.image.load('PNGs/Logo.png').convert_alpha()
playGameImage = pygame.image.load('PNGs/PlayGame.png').convert_alpha()
settingsImage = pygame.image.load('PNGs/Settings.png').convert_alpha()
leaderboardImage = pygame.image.load('PNGs/Leaderboard.png').convert_alpha()
quitImage = pygame.image.load('PNGs/Quit.png').convert_alpha()
SuLiImage = pygame.image.load('PNGs/SuLi.png').convert_alpha()

# Initialise all buttons in main menu.
playGameButton = Button(480, 300, playGameImage, 1)
settingsButton = Button(480, 380, settingsImage, 1)
leaderboardButton = Button(480, 460, leaderboardImage, 1)
quitButton = Button(480, 540, quitImage, 1)
SuLiButton = Button(1100, 10, SuLiImage, 0.5)

loggedIn = False
run = True

# While loop to refresh the page consistently, also allowing the pygame window to be closed.
while run:

    pygame.display.set_caption("Main Menu")
    window.fill((186, 40, 0))
    window.blit(logoImage, (425, 25))

    if playGameButton.draw():
        time.sleep(1)
        initialiseGame()
        playGameButton.draw()
    if settingsButton.draw():
        time.sleep(1)
        continue
    if quitButton.draw():
        time.sleep(1)
        run = False
    if not loggedIn:
        if SuLiButton.draw():
            time.sleep(1)
            Username, loggedIn = logIn()
    if leaderboardButton.draw():
        time.sleep(1)
        leaderboard()
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            run = False

    pygame.display.update()

'''
# Used to test bots
HWin = 0
NWin = 0
EWin = 0
while True:
    Won = playGame()

    print("Hard Wins: " + str(HWin) + "\n Normal Wins: " + str(NWin) + "\n Easy Wins: " + str(EWin))
'''
