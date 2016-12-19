from GUI import Window, View, Image, application, Dialog, Label
from GUI.Geometry import offset_rect, rect_sized
from GUI.StdColors import white

import os, sys, serial, time, pyglet, wave
pyglet.options['audio'] = ('openal', 'silent')
f = serial.Serial('/dev/cu.usbmodemFD121' , 9600, timeout = .3)


#open images
here = sys.path[0]
image_path = os.path.join(here, "room.jpg")
room = Image(file = image_path)
image_path = os.path.join(here, "m_off.png")
m_off = Image(file = image_path)
image_path = os.path.join(here, "m_on.png")
m_on = Image(file = image_path)
image_path = os.path.join(here, "n_off.png")
n_off = Image(file = image_path)
image_path = os.path.join(here, "n_on.png")
n_on = Image(file = image_path)
image_path = os.path.join(here, "p_off.png")
p_off = Image(file = image_path)
image_path = os.path.join(here, "p_on.png")
p_on = Image(file = image_path)



class dashboard(View):

    tags = 0
    present = False
    alarm = False
    monitor1 = m_off
    monitor2 = m_off
    phone1 = p_off
    phone2 = p_off
    nurse = n_off
    start = time.time()
    moncount = 0
    pstate = 0

    def key_down(self, event):
        if event.char == 'q':
            self.tags = (self.tags + 1) % 2
            if self.tags % 2 == 1:
                self.present = True
                self.nurse = n_on
            else:
                self.present = False
                self.nurse = n_off

        if event.char == 'm':
            print play1.playing
            play1.pause()
        if event.char == 'a':
            self.start = time.time()
            self.monitor1 = m_on
            self.alarm = True
            self.pstate = 1
        if event.char == 's':
            self.alarm = False
            self.pstate = 0
            self.phone1 = p_off
            self.phone2 = p_off
            self.monitor1 = m_off
            self.monitor2 = m_off
            self.invalidate_rect(rect_sized((0, 0), (1300, 700)))
            self.update()
        if event.char == 'u':
            if self.alarm == True:           #counter to play monitor sounds
                self.moncount = (self.moncount + 1) % 2
                if self.moncount == 1:
                    mwav = pyglet.media.load('monitor2.mp3')
                    mwav.play()
            txt = f.read(500)       #reading from usb
            if len(txt) > 0:
                self.tags = (self.tags + 1) % 2
                if self.tags % 2 == 1:
                    self.present = True
                    self.nurse = n_on
                else:
                    self.present = False
                    self.nurse = n_off
            self.invalidate_rect(rect_sized((0, 0), (1300, 700)))
            self.update()


            if self.alarm:
                curr = time.time()
                if (curr - self.start > 23) and (self.pstate == 3):
                    self.pstate += 1
                    if self.present == False:
                        self.phone1 = p_on
                        self.phone2 = p_off
                        pwav = pyglet.media.load('phone.mp3')
                        pwav.play()
                elif (curr - self.start > 13) and (self.pstate == 2):
                    self.pstate += 1
                    pwav = pyglet.media.load('phone.mp3')
                    pwav.play()
                    self.phone2 = p_on
                    self.phone1 = p_off
                elif (curr - self.start > 3) and (self.pstate == 1):
                    self.pstate += 1
                    if self.present == False:
                        pwav = pyglet.media.load('phone.mp3')
                        pwav.play()
                        self.phone1 = p_on


    def draw(self, c, r):
        c.erase_rect(r)
        c.fillcolor = white
        orig = (0,0)

        src_r = room.bounds
        dst_r = rect_sized((0, 0), (340, 670))
        room.draw(c, src_r, dst_r)   #draw the monitor on left side

        src_r = p_on.bounds
        dst_r = rect_sized((450, 210), (156, 208))
        self.phone1.draw(c, src_r, dst_r)    #draw the top phone

        src_r = p_on.bounds
        dst_r = rect_sized((450, 440), (156, 208))
        self.phone2.draw(c, src_r, dst_r)    #draw the bottom phone

        src_r = rect_sized((0,250), (1000, 500))
        dst_r = rect_sized((380, 20), (300, 150))
        self.nurse.draw(c, src_r, dst_r)    #draw the nurse sign

        src_r = m_on.bounds
        dst_r = rect_sized((800, 2), (390, 325))
        self.monitor1.draw(c, src_r, dst_r)    #draw the top monitor

        src_r = m_on.bounds
        dst_r = rect_sized((800, 350), (390, 325))
        self.monitor2.draw(c, src_r, dst_r)    #draw the bottom monitor

win = Window(size = (1300, 700))
view = dashboard(size = win.size)
win.add(view)
view.become_target()
win.show()

room1 = Label(text = "Current Room")
room2 = Label(text = "Other Room")
n1 = Label(text = "Nurse's Phone")
n2 = Label(text = "Partner's Phone")

view.place(room1, left = 1160, top = 25)
view.place(room2, left = 1160, top = 375)
view.place(n1, left = 485, top = 190)
view.place(n2, left = 480, top = 420)



application().run()
