__author__ = '8.Ball'

import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, RiseInTransition
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.audio import SoundLoader



#Keeping a fixed window size
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'width', '500')

#Getting audio into program
global soundPal, soundNonPal
soundPal = SoundLoader.load('audio/soundPal.mp3')
soundNonPal = SoundLoader.load('audio/soundNonPal.mp3')

"""
Builder .kv specs
"""
Builder.load_string("""
<HomeScreen>
    GridLayout:
        #Displaying the icon
        Image:
            source: 'images/icon_validator.png'
            size: (350, 350)
            x: 75
            y: 110

        #Displaying the Check Button
        Button:
            text: 'Check'
            size: (100,30)
            x: 192
            y: 150
            background_color: (0, 255, 1, 1)
            on_press: root.generate()

        #Displaying the entry area
        DNAInput:
            id: input
            hint_text: 'Input sequence here'
            multiline: False
            size: (370, 30)
            x: 70
            y: 190
            on_text_validate: root.generate()
            focus: True


        #Displaying 5 prime(start of sequence)
        Label:
            text: "[b]5'"
            font_size: 27
            markup: True
            x: 5
            y: 155

        #Displaying 3 prime(end of sequence)
        Label:
            text: "[b]3'"
            font_size: 27
            markup: True
            x: 410
            y: 157

        #Displaying the Clear Button
        Button:
            text: '×'
            font_size: 22
            color: (215, 215, 215, 1)
            background_color: (228, 228, 228, .1)
            size: (29, 27)
            x: 411
            y: 192
            on_press: root.clearText()

        #Displaying Help Button
        Button:
            text: 'Help   |'
            font_size: 10
            background_color: (0, 0, 0, 0)
            size: (45, 20)
            x: 420
            y: 0
            on_press: root.showHelp()

        #Displaying the About Button
        Button:
            text: 'About'
            font_size: 10
            background_color: (0, 0, 0, 0)
            size: (45, 20)
            x: 455
            y: 0
            on_press: root.showAbout()

        #Displaying copyright tag
        Label:
            text: 'Copyright © 2019  |_aiben'
            font_size: 11
            x: 27
            y: -40


<helpPopup>
    title: 'Help'
    GridLayout:
        Button:
            text: 'Close'
            size: (100, 30)
            x: 385
            y: 20
            on_press: root.dismiss()

        Image:
            source: 'images/helpIcon.png'
            size: (85, 85)
            x: 15
            y: 230

        Label:
            text: 'Input one strand of the DNA sequence and '
            font_size: 14
            markup: True
            x: 202
            y: 240

        Label:
            text: 'DNA Palindrome Sequencer 1.0.0 will generate'
            font_size: 14
            markup: True
            x: 212
            y: 221

        Label:
            text: 'the complimentary base pair sequence.'
            font_size: 14
            markup: True
            x: 190
            y: 205

        Label:
            text: 'Everything is accessible in the environment.'
            font_size: 14
            markup: True
            x: 204
            y: 160

        Label:
            text: 'The environment will highlight the palindromic'
            font_size: 14
            markup: True
            x: 210
            y: 110

        Label:
            text: 'DNA sequence found in the DNA helix.'
            font_size: 14
            markup: True
            x: 186
            y: 93

        Label:
            text: 'Contact us on  [size=12]info@palindrome.org  [size=14]if you face any challenges.'
            font_size: 14
            markup: True
            x: 198
            y: 30

<aboutPopup>
    title: 'About'
    GridLayout:
        Button:
            text: 'Close'
            size: (100, 30)
            x: 385
            y: 20
            on_press: root.dismiss()

        Image:
            source: 'images/icon.png'
            size: (125, 125)
            x: 30
            y: 150

        Label:
            text: 'Copyright © 2019  |_aiben'
            font_size: 11
            x: 31
            y: -33

        Label:
            text: '[b]DNA  Palindrome  Sequencer'
            markup: True
            font_size: 23
            x: 285
            y: 270

        Label:
            text: '1.0.0  Maiden'
            markup: True
            font_size: 17
            x: 188
            y: 240

        Label:
            text: 'DNA Palindrome Sequencer is full-featured '
            markup: True
            font_size: 13
            x: 260
            y: 193

        Label:
            text: 'environment aiming to show all palindromic'
            markup: True
            font_size: 13
            x: 258
            y: 178

        Label:
            text: 'paired DNA in a DNA helix.'
            markup: True
            font_size: 13
            x: 210
            y: 163

        Label:
            text: 'A palindrome is a string(combination of characters)'
            markup: True
            font_size: 13
            x: 282
            y: 130

        Label:
            text: 'that reads the same backwards and forwards.'
            markup: True
            font_size: 13
            x: 267
            y: 115

        Label:
            text: 'ENJOY!'
            markup: True
            font_size: 13
            x: 159
            y: 100

        Label:
            text: 'Help and join us!'
            markup: True
            font_size: 12
            x: 183
            y: 55

        Label:
            text: 'info@palindrome.org'
            markup: True
            font_size: 11
            x: 188
            y: 38

        Label:
            text: 'http://wwww.palindrome.org'
            markup: True
            font_size: 11
            x: 208
            y: 23

<DisplayScreen>
    GridLayout:
        #Back button
        Button:
            text: 'Back'
            size: (70, 30)
            x: 420
            y: 10
            on_press: root.manager.current = 'home'

<DNAInput>
    id: input

""")

#Create Screens
class HomeScreen(Screen):
    #Function to show help pop up
    def showHelp(self):
        helpPopup().open()

    #Function to show about pop up
    def showAbout(self):
        aboutPopup().open()

    def clearText(self):
        self.ids.input.text = ''

    #Function for screen transition
    def generate(self):
        if self.ids.input.text == '':
            self.showHelp()
        else:
            sm.transition = RiseInTransition()
            sm.current = 'display'
            self.start()

    def start(self, *args):
        global userInput
        userInput = self.ids.input.text
        self.manager.get_screen('display').display()
    pass

class helpPopup(Popup):
    pass

class aboutPopup(Popup):
    pass

class DisplayScreen(Screen):
    #Fade in animation function
    def animate(self, what):
        anim = Animation(opacity=0, duration=0)
        anim += Animation(opacity=1, duration=1)
        anim.start(what)

    #Function to generate the complimentary base sequence
    def generateSequence(self, sequence):
        compSequence = ''
        for base in sequence:
            if base == 'A':
                compSequence = compSequence+'T'
            elif base == 'T':
                compSequence = compSequence+'A'
            elif base == 'G':
                compSequence = compSequence+'C'
            elif base == 'C':
                compSequence = compSequence+'G'
        return compSequence

    #Function to check if the DNA sequence is palindromic and return palindromic part
    def palindromeDNA(self, sequence, compSequence):
        palDNA = ''
        k = 0
        global start, end, status
        start = end = 0
        status = False
        for i in range(0, len(sequence)):
            if sequence[i] == compSequence[-i-1]:
                status = True
                palDNA = palDNA+sequence[i]
                #Getting the starting and ending parts
                if k == 0:
                    start = i
                    k += 1
                elif k == 1:
                    end = i
                try:
                    if sequence[i+1] != compSequence[-i-1-1]:
                        break
                except:
                    continue
        if len(palDNA) == 1 or len(palDNA) == 2:
            status = False

        return palDNA

    def display(self):
        #Getting the complimentary base sequence
        compSequence = self.generateSequence(userInput)
        palDNA = self.palindromeDNA(userInput, compSequence)

        #When the DNA Sequence is not a palindromic sequence
        if status == False:
            #Clearing the area
            clearStatus = Image(source='images/clearStatus.png',

                                x =0,
                                y = 70)
            self.add_widget(clearStatus)

            talk = Label(text='[b]DNA Sequence : ',
                         font_size= 25,
                         markup = True,
                         x = 0,
                         y = 165)
            self.add_widget(talk)

            if len(userInput)>=1 and len(userInput)<=25:
                DNAseq = Label(text="5'   " + userInput + "   3'",
                               font_size = 25,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence + "   5'",
                               font_size = 25,
                               x = 0,
                               y = 75)
                self.add_widget(COMPseq)

            if len(userInput)>=26 and len(userInput)<=35:
                DNAseq = Label(text="5'   " + userInput + "   3'",
                               font_size = 20,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence + "   5'",
                               font_size = 20,
                               x = 0,
                               y = 75)
                self.add_widget(COMPseq)

            if len(userInput)>=36 and len(userInput)<=45:
                DNAseq = Label(text="5'   " + userInput + "   3'",
                               font_size = 15,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence + "   5'",
                               font_size = 15,
                               x = 0,
                               y = 75)
                self.add_widget(COMPseq)

            if len(userInput)>=46:
                DNAseq = Label(text="5'   " + userInput + "   3'",
                               font_size = 7,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence + "   5'",
                               font_size = 7,
                               x = 0,
                               y = 75)
                self.add_widget(COMPseq)

            #Clear the area
            check = Image(source= 'images/Blank.png',
                            size_hint= (.3,.3),
                               x = 175,
                               y = 70)
            self.add_widget(check)

            #Display icon
            check = Image(source= 'images/xIcon.PNG',
                            size_hint= (.3,.3),
                            x = 175,
                            y = 70)
            self.add_widget(check)
            self.animate(check)

            #Play sound
            soundNonPal = SoundLoader.load('audio/soundNonPal.mp3')
            soundNonPal.play()

            #Clear text area
            clearStatusText = Image(source= 'images/clearStatus.png',
                                    size_hint= (.7,.7),
                                    x = 50,
                                    y = -100)
            self.add_widget(clearStatusText)

            #Display Text
            statusText = Label(text= 'Non-Palindromic',
                                    color= (41, 0, 0, 1),
                                    font_size= 25,
                                    x = 0,
                                    y = -150)
            self.add_widget(statusText)
            self.animate(statusText)



        #When DNA is a palindromic sequence
        if status == True:
            #Clearing the area
            clearStatus = Image(source='images/clearStatus.png',

                                x =0,
                                y = 70)
            self.add_widget(clearStatus)

            talk = Label(text='[b]DNA Sequence : ',
                         font_size= 25,
                         markup = True,
                         x = 0,
                         y = 165)
            self.add_widget(talk)

            if len(userInput)>=1 and len(userInput)<=25:
                DNAseq = Label(text="5'   " + userInput[0:start] + '[color=00b050]' + kivy.utils.escape_markup(userInput[start:end+1])+ '[/color]' + userInput[end+1::] + "   3'",
                               markup = True,
                               font_size = 25,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence[0:start] + '[color=00b050]' + kivy.utils.escape_markup(compSequence[start:end+1]) + '[/color]' + compSequence[end+1::] + "   5'",
                                markup = True,
                                font_size = 25,
                                x = 0,
                                y = 75)
                self.add_widget(COMPseq)

            if len(userInput)>=26 and len(userInput)<=35:
                DNAseq = Label(text="5'   " + userInput[0:start] + '[color=00b050]' + kivy.utils.escape_markup(userInput[start:end+1])+ '[/color]' + userInput[end+1::] + "   3'",
                               markup = True,
                               font_size = 20,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence[0:start] + '[color=00b050]' + kivy.utils.escape_markup(compSequence[start:end+1]) + '[/color]' + compSequence[end+1::] + "   5'",
                                markup = True,
                                font_size = 20,
                                x = 0,
                                y = 75)
                self.add_widget(COMPseq)

            if len(userInput)>=36 and len(userInput)<=45:
                DNAseq = Label(text="5'   " + userInput[0:start] + '[color=00b050]' + kivy.utils.escape_markup(userInput[start:end+1])+ '[/color]' + userInput[end+1::] + "   3'",
                               markup = True,
                               font_size = 15,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence[0:start] + '[color=00b050]' + kivy.utils.escape_markup(compSequence[start:end+1]) + '[/color]' + compSequence[end+1::] + "   5'",
                                markup = True,
                                font_size = 15,
                                x = 0,
                                y = 75)
                self.add_widget(COMPseq)

            if len(userInput) > 46:
                DNAseq = Label(text="5'   " + userInput[0:start] + '[color=00b050]' + kivy.utils.escape_markup(userInput[start:end+1])+ '[/color]' + userInput[end+1::] + "   3'",
                               markup = True,
                               font_size = 7,
                               x = 0,
                               y = 40)
                self.add_widget(DNAseq)

                COMPseq = Label(text="3'   " + compSequence[0:start] + '[color=00b050]' + kivy.utils.escape_markup(compSequence[start:end+1]) + '[/color]' + compSequence[end+1::] + "   5'",
                                markup = True,
                                font_size = 7,
                                x = 0,
                                y = 75)
                self.add_widget(COMPseq)


            #Clear the area
            check = Image(source= 'images/Blank.png',
                            size_hint= (.3,.3),
                               x = 175,
                               y = 70)
            self.add_widget(check)

            #Display icon
            check = Image(source= 'images/checkIcon.PNG',
                            size_hint = (.3,.3),
                            x = 175,
                            y = 70)

            self.add_widget(check)
            self.animate(check)

            #Play sound
            soundPal = SoundLoader.load('audio/soundPal.mp3')
            soundPal.play()

            #Clear text area
            clearStatusText = Image(source= 'images/clearStatus.png',
                                    size_hint= (.7,.7),
                                    x = 50,
                                    y = -100)
            self.add_widget(clearStatusText)

            #Display Text
            statusText = Label(text= 'Palindromic',
                                    color= (0, 79, 175, 1),
                                    font_size= 25,
                                    x = 0,
                                    y = -150,)
            self.add_widget(statusText)
            self.animate(statusText)

    pass

class DNAInput(TextInput):
    #Function to restrict input
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        if 'A' in s:
            return super(DNAInput, self).insert_text(s, from_undo=from_undo)
        elif 'T' in s:
            return super(DNAInput, self).insert_text(s, from_undo=from_undo)
        elif 'G' in s:
            return super(DNAInput, self).insert_text(s, from_undo=from_undo)
        elif 'C' in s:
            return super(DNAInput, self).insert_text(s, from_undo=from_undo)
        else:
            return super(DNAInput, self).insert_text('', from_undo=from_undo)


#Create Screen Manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(DisplayScreen(name='display'))

class PalindromeDNAValidator(App):
    def build(self):
        self.title = 'DNA Palindrome Sequencer'
        self.icon = 'images/icon.png'

        return sm

PalindromeDNAValidator().run()