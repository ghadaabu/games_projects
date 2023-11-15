import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype


class SpeedTypeTest:
    WINDOWWIDTH = 640  # size of window's width in pixels
    WINDOWHEIGHT = 480  # size of windows' height in pixels

    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BATTLESHIP_GRAY = (132, 132, 130)
    BITCOIN_GRAY = (77, 77, 78)  # darker
    AMARANTH = (299, 43, 80)
    AMARANTH_RED = (211, 33, 45)  # darker

    def __init__(self):
        self.start_time = 0
        self.sentence = ''
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.reset = True

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

    def get_sentence(self):
        # returns a random sentence from sentences file
        sentences = open("typing_speed_test/sentences.txt")
        sentence = random.choice(list(sentences.readlines()))
        sentences.close()
        return sentence

    def extend_sentence(self, original_sen, input_sen):
        original_words = original_sen.split(" ")
        input_words = input_sen.split(" ")
        extended_sen = ''
        for i, word in original_words:
            # noinspection PyBroadException
            try:  # the purpose is to handle the cases where the original sentence contains more words than the input
                if len(word) < len(input_words[i]):
                    extended_sen = extended_sen + input_words[i] + ' '
                else:
                    extended_sen = extended_sen + word + ' '
            except:
                extended_sen = extended_sen + word + ' '
        return extended_sen[:-1]  # discarding the last space

    def draw_sentence(self, original_sen, input_sen, screen):

        # if the test hasn't been started yet (the input is empty)
        if input_sen == '':
            fontObj = pygame.font.Font(None, 18)
            textSurfaceObj = fontObj.render(original_sen, True, self.BATTLESHIP_GRAY)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2 - 50)
            screen.blit(textSurfaceObj, textRectObj)
            pygame.display.update()
        else:
            font = pygame.freetype.Font(None, 18)
            # origin is the position of the original text and font_height is the scaled height of the font in pixels
            font.origin = True
            font_height = font.get_sized_height()

            # taking the item in index 4 as the horizontal advance
            # to know how much space each letter takes during rendering
            M_ADV_X = 4

            # calculating how big is the entire line of text is
            extended_sentence = self.extend_sentence(original_sen, input_sen)
            text_surf_rect = font.get_rect(extended_sentence)

            baseline = text_surf_rect.y
            # creating a surface to render the text on and center it to the screen
            text_surf = pygame.surface(text_surf_rect.size)
            text_surf_rect.center = (self.WINDOWWIDTH / 2,
                                     self.WINDOWHEIGHT / 2 - 50)
            # TODO if i add the new function, check how to make the new string go to the right and not rotate the hall text because it is set to center!
            metrics = font.get_metrics(extended_sentence)

            # for (idx, (letter,metric)) in enumerate(zip(extended_sentence, metrics)):
            #     # select the right color


    def reset_game(self):
        self.start_time = 0
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.reset = True
        self.SCREEN.fill(self.BITCOIN_GRAY)

        # initializing sentence by getting a random new one
        self.sentence = self.get_sentence()
