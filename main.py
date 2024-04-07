#NOTE main modules and packages imports
from tkinter import *
from translate import Translator
from tkinter import ttk
from set_ups import *
from gtts import gTTS
import sounddevice as sd
import soundfile as sf 
import datetime
import os
#NOTE NON-OOP CODE

#creating a Tk() instance
window : Tk = Tk()
#making the screen not resizable
window.resizable(False, False)
#defining screen dimensions then I add some configuration
screen_width = 1000
screen_height = 600

window.geometry(f"{screen_width}x{screen_height}")
window.title("Basic Translator")
window.config(background='#101010')

#NOTE creating the main labels 

label1 = Label(window,
              bg='#242424',
              relief=RAISED,
              bd=5,
              padx=10,
              pady=10,
              width=46,
              height=15)

label1.pack()
label1.place(x=40,y=190)    

label2 = Label(window,
              bg='#242424',
              relief=RAISED,
              bd=5,
              padx=10,
              pady=10,
              width=46,
              height=15)

label2.pack()
label2.place(x=580,y=190)   

#creating a list with the availeable languages
options =  [key for key in lang_dict.keys()]


#NOTE
#adding some dropdowns so user can select the language they translate from and the language they translate to
#default languages are ENGLISH -> ROMANIAN

selected_option1 = StringVar(window)
selected_option1.set(options[8])


dropdown_lang1 = ttk.Combobox(window, values=options, textvariable=selected_option1, width=20,height=5,state="readonly",
                        font=("SansSerif",12,'normal'))
dropdown_lang1.pack()
dropdown_lang1.place(x=120,y=165)

selected_option2 = StringVar(window)
selected_option2.set(options[35])

dropdown_lang2 = ttk.Combobox(window, values=options, textvariable=selected_option2, width=20,height=5,state="readonly",
                        font=("SansSerif",12,'normal'))
dropdown_lang2.pack()
dropdown_lang2.place(x=655,y=165)
 
#NOTE create an entry box where you can type the text in order to translate it from the selected language to another one
_entry = Text(window,font=("SansSerif",12,'normal'),width = 33,height=12,
             background='#242424',foreground="#f4f4f4",padx=10,pady=5,
             insertbackground="#f4f4f4")

_entry.pack()

_entry.place(x=56,y=203)

#NOTE create an exit box where the translated text will be displayed
_exit = Text(window,font=("SansSerif",12,'normal'),width = 33,height=12,
             background='#242424',foreground="#f4f4f4",padx=10,pady=5,state=DISABLED)
_exit.pack(side = LEFT)

_exit.place(x=596,y=203)


#NOTE this function translates the text from the _entry box and writes the translated text into the _exit box 
def translate_click():
    lang1 : str = lang_dict[selected_option1.get()]
    lang2 : str = lang_dict[selected_option2.get()]
    trans : Translator = Translator(from_lang=lang1,
                   to_lang=lang2)
    
    _exit.config(state='normal')
    answer = trans.translate(_entry.get("1.0", "end-1c"))
    _exit.delete("1.0","end")
    _exit.insert(END, answer)
    _exit.config(state='disabled')

#NOTE this function switches the text from the _entry box and _exit box and vice versa  
def switch_click():
    _exit.config(state='normal')
    first_text = _entry.get("1.0", "end-1c")
    second_text = _exit.get("1.0", "end-1c")
    
    _exit.delete("1.0","end")
    _entry.delete("1.0","end")
    
    _entry.insert("1.0", second_text)
    _exit.insert("1.0", first_text)
    _exit.config(state='disabled')
    
    first_lang = selected_option1.get()
    second_lang = selected_option2.get()
    
    selected_option1.set(second_lang) 
    selected_option2.set(first_lang)

#NOTE when you click this button it triggers "the translate_click" function
button_translate = Button(window,text="Translate",command=translate_click,
                          font=("SansSerif",15,'normal'),fg="#f4f4f4",bg="#202020",
                          activeforeground="#f4f4f4",activebackground="#202020",width=8)

switch_image_light = PhotoImage(file = r"translator_app\imgs\swap_black.png").subsample(7,10)
switch_image_dark = PhotoImage(file = r"translator_app\imgs\swap_white.png").subsample(7,10)

#NOTE when you click this button it triggers "the switch_click" function
button_switch = Button(window,image = switch_image_dark,command=switch_click,
                          font=("SansSerif",15,'normal'),bg="#202020",
                          activebackground="#202020",width=92 )

button_translate.pack()
button_translate.place(x=440,y=210)

button_switch.pack()
button_switch.place(x=440,y=260)


#NOTE instantiating some PhotoImage objects ,also I scale the images to be smaller with the "subsample" method

sound_image_dark = PhotoImage(file = r"translator_app\imgs\speaker_white.png").subsample(30,30)
sound_image_light = PhotoImage(file = r"translator_app\imgs\speaker_black.png").subsample(30,30)
dark_mode_moon = PhotoImage(file = r"translator_app\imgs\moon_white.png").subsample(10,10)
light_mode_moon = PhotoImage(file = r"translator_app\imgs\moon_black.png").subsample(10,10)

time_label = Label(window,text="",bg="#242424",fg="#f4f4f4",font=("SansSerif",20,'normal'),relief=RAISED ,bd=3)

#NOTE creating a function that displays the current time
def update_time():
    
    time_label.config(text =  datetime.datetime.now().strftime("%H:%M:%S")) 
    time_label.after(1000, update_time)

time_label.pack()
time_label.place(x=15,y=10)

#NOTE this functions convert the text from the _entry box ,convert the text into voice ,save the data in a ".wav"
# file then the sound file will be played 

def speak1():
    try:
        tts = gTTS(_entry.get("1.0", "end-1c"),lang=lang_dict[selected_option1.get()])
        tts.save("translator_app/mysave.wav")
        data, fs = sf.read("translator_app/mysave.wav")
        
        sd.play(data,fs)
        sd.wait()
    except AssertionError:
        pass
    except ValueError:
        print(f"Unfortunately I can't assist you in order to listen in {selected_option1.get()} language")

def speak2():
    try:
        tts = gTTS(_exit.get("1.0", "end-1c"),lang=lang_dict[selected_option2.get()])
        tts.save("translator_app/mysave.wav")
        data, fs = sf.read("translator_app/mysave.wav")
        
        sd.play(data,fs)
        sd.wait()
    except AssertionError:
        pass
    except ValueError:
        print(f"Unfortunately I can't assist you in order to listen in {selected_option2.get()} language")

#NOTE this function is used to switch the main theme 
def switch_mode():
    if window.cget("background") == "#101010":
        #NOTE changeing colors and images in order to switch form dark mode to light mode
        window.config(background="#FFFFF0")
        label1.config(background='#F0EFE6') 
        label2.config(background='#F0EFE6')
        button_translate.config(fg= "#242424",bg="#f4f4f4",activeforeground="#242424",activebackground="#f4f4f4")
        button_switch.config(image= switch_image_light,bg="#f4f4f4",activebackground="#f4f4f4")
        sound_button1.config(image= sound_image_light,bg="#f4f4f4",activebackground="#f4f4f4")
        sound_button2.config(image= sound_image_light,bg="#f4f4f4",activebackground="#f4f4f4")
        _entry.config(insertbackground="#202020",background='#f4f4f4',foreground="#202020")
        _exit.config(background='#f4f4f4',foreground="#202020")
        switch_mode_button.config(image=light_mode_moon,bg="#f4f4f4",activebackground="#f4f4f4") 
        time_label.config(fg="#202020",bg="#f4f4f4")    
    else:
        #NOTE changeing colors and images in order to switch form light mode to dark mode
        window.config(background="#101010")
        label1.config(background='#242424') 
        label2.config(background='#242424') 
        button_translate.config(fg= "#f4f4f4",bg="#242424",activeforeground="#f4f4f4",activebackground="#242424")
        button_switch.config(image= switch_image_dark,bg="#242424",activebackground="#242424")
        sound_button1.config(image= sound_image_dark,bg="#242424",activebackground="#242424")
        sound_button2.config(image= sound_image_dark,bg="#242424",activebackground="#242424")
        _entry.config(insertbackground="#f4f4f4",background='#242424',foreground="#f4f4f4")
        _exit.config(background='#242424',foreground="#f4f4f4")
        switch_mode_button.config(image=dark_mode_moon,bg="#242424",activebackground="#242424")
        time_label.config(fg="#f4f4f4",bg="#202020") 
     
#NOTE creating 2 audio buttons for vocal assistant        
sound_button1 = Button(window,image = sound_image_dark,
                        command = speak1,
                        font=("SansSerif",15,'normal'),bg="#202020",
                        activebackground="#202020",
                        width=20,height=20,padx=3,pady=3)

"git remote add origin https://github.com/Daniel-Lazar21/Basic_Translator"
sound_button2 = Button(window,image = sound_image_dark,
                        command = speak2,
                        font=("SansSerif",15,'normal'),bg="#202020",
                        activebackground="#202020",
                        width=20,height=20 ,padx=3,pady=3)

#NOTE creating the switch button which triggers the "switch_mode" function

switch_mode_button = Button(window,image = dark_mode_moon,
                        command = switch_mode,
                        font=("SansSerif",15,'normal'),bg="#202020",
                        activebackground="#202020",
                        width=60,height=60 ,padx=2,pady=2)

sound_button1.pack()
sound_button1.place(x=95,y=163)

sound_button2.pack()
sound_button2.place(x=630,y=163)

switch_mode_button.pack()
switch_mode_button.place(x=920,y=15)

#NOTE running and updating the window
update_time()
window.mainloop()

#NOTE removing the audio file after you close the app
try:
    os.remove(r"translator_app\mysave.wav")
except FileNotFoundError:
    pass

#TODO maybe add some new stuff in the near future 
#FIXME fix te arabic language problems 
