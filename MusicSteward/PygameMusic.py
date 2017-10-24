# -*- coding: utf8 -*-
import pygame
import time

# By Niuxuan(zuomu) QQ:79069622
pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

def PlayWord(filename):
    words = pygame.mixer.Sound(filename)
    words.set_volume(100)
    words.play()

def PlayMusic(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(1)
        TRACK_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(TRACK_END)

        pygame.mixer.music.play()
        isBusy = True
        while isBusy:
            for event in pygame.event.get():
                if event.type == TRACK_END:
                    isBusy = False
        return 1
    
    except Exception,e:
        print e
        return 0
    
 
def IsBusy():
    return pygame.mixer.music.get_busy()
