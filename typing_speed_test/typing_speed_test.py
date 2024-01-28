import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype
from math import ceil
from abc import ABC


# -------------------- Constants class ---------------------------------------------------------------------------------
class Constants:
    WINDOWWIDTH = 1100  # 640  # size of window's width in pixels
    WINDOWHEIGHT = 600  # 480  # size of windows' height in pixels

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz| :;,._!ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    PUNCTUATION_MARKS = [':', '.', ',', '!', ';']
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BATTLESHIP_GRAY = (132, 132, 130)
    BITCOIN_GRAY = (77, 77, 78)  # darker
    BLACK_COFFEE = (59, 47, 47)
    FATHOM_GREY = (41, 44, 51)
    AMARANTH = (211, 33, 45)
    AMARANTH_RED = (150, 27, 45)  # darker
    BITCOIN_ORANGE = (242, 169, 0)
    LIGHT_CYAN = (224, 255, 255)

    # using Google's font - RobotoMono-Regular font. https://fonts.google.com/specimen/IBM+Plex+Mono?query=mono
    FONT_TYPE = "RobotoMono-Regular.ttf"
    # https://www.mit.edu/~ecprice/wordlist.10000 link to data file
    DATA_FILE_NAME = "wordlist.10000.txt"
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size

    FONT_SIZE = 20

    MARGIN = 100

    RESET_BOX_SIZE = (WINDOWWIDTH / 2 - 30, WINDOWHEIGHT - 100, 60, 30)

    BUTTONS_FONT_SIZE = 16
    LINES_SPACING = 50
    TIMER_POSITION = (WINDOWWIDTH // 2, MARGIN + 50)


# ------------------------- ABSTRACT CLASS for modes -------------------------------------------------------------------
class ModesABC(ABC):
    def __init__(self):
        pass

    def menu_button_words(self):
        pass

    def menu_button_time(self):
        pass

    def menu_button_numbers1(self):
        pass

    def menu_button_numbers2(self):
        pass

    def menu_button_numbers3(self):
        pass

    def menu_button_numbers(self):
        pass

    def menu_button_punctuations(self):
        pass

    def check_end_game(self):
        pass


# -------------------------- WordsMode ---------------------------------------------------------------------------------

class WordsMode(ModesABC):
    def __init__(self):
        self.numbers = None
        self.punctuations = None
        self.word_count = None

    def menu_button_words(self):
        return False

    def menu_button_time(self):
        return True

    def menu_button_numbers1(self):
        if self.word_count != 10:
            self.word_count = 10
            return 10
        else:
            return None

    def menu_button_numbers2(self):
        if self.word_count != 20:
            self.word_count = 20
            return 20
        else:
            return None

    def menu_button_numbers3(self):
        if self.word_count != 30:
            self.word_count = 30
            return 30
        else:
            return None

    def menu_button_numbers(self):
        self.numbers = not self.numbers
        return False if self.numbers else True

    def menu_button_punctuations(self):
        self.punctuations = not self.punctuations
        return False if self.punctuations else True

    def check_end_game(self, input_sentence):
        # checks if the game has ended. returns True if ended, else False
        # checking if the test ended in Words mode. there is two scenarios to end the test,
        # 1- the user entered all the letters of the last word in the sentence. 2- the user didn't
        # enter the last word (or partially) and pressed space.
        input_words = input_sentence.split(' ')
        if (len(input_words) == self.word_count and len(input_words[-1]) == len(
                self.sentence.split(' ')[-1])) or (
                len(input_words) > self.word_count and input_sentence[-1] == ' '):
            return True
        return False

    def draw_sentence(self, sentence, input_sentence, active, word_count, letter_width, row_len, SCREEN, theme):
        """
        Function that draws the sentence on the screen, it colors the letters with different colors based on the
        accuracy of the entered words_file where:
        - correct entered letter: white
        - wrong entered letter: Red
        - extra entered letter: dark red
        - not entered yet: light grey
        It also draws a cursor where the next letter to be entered.
        :return: None
        """
        line_ind = 0
        sentence_words = sentence.split(' ')
        input_sen_words = input_sentence.split(' ')
        current_h_adv = 900

        cursor_x = None
        cursor_y = None

        # if the test has started, draws the word-counter above the sentence
        if active:
            self.draw_txt(f'{len(input_sen_words) - 1} / {word_count}', self.FONT_SIZE, self.BITCOIN_ORANGE,
                          left_corner=self.TIMER_POSITION)

        for i, word in enumerate(sentence_words):
            in_word = input_sen_words[i] if i < len(input_sen_words) else ''
            # check if there is enough space left on the current line for the current word, if not creates a new line.
            if max(len(word), len(in_word)) * letter_width + current_h_adv > row_len:
                if line_ind != 0:  # if line is the first, no need to blit the surface to the screen
                    SCREEN.blit(text_surf, text_surf_rect)
                font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.ALPHABET + self.ALPHABET)  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.topleft = (self.MARGIN, self.WINDOWHEIGHT // 2 - 100 + self.LINES_SPACING * line_ind)
                text_surf.fill(theme.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.MARGIN + current_h_adv + len(in_word) * letter_width

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = theme.DEFAULT_TEXT_COLOR
                else:
                    color = self.AMARANTH
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.AMARANTH_RED)
                    current_h_adv += letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.BATTLESHIP_GRAY)
                    current_h_adv += letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', self.BATTLESHIP_GRAY)
            current_h_adv += letter_width
            SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(self.FONT_TYPE, self.FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, self.BITCOIN_ORANGE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            SCREEN.blit(textSurfaceObj, textRectObj)

    def draw_txt(self, SCREEN, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None,
                 box_color=None):
        """
        # this funtion renders a text and a box if specified.
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param txt_color: the color of the text
        :param left_corner: the left corner position of the box, default None
        :param center_position: the center position of the box, default None
        :param box_size: box size, default None
        :param box_color: the color of the box, default None
        """
        if box_size:
            pygame.draw.rect(SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            SCREEN.blit(textSurfaceObj, left_corner)

    def show_result(self, end, start_time, word_count, sentence, input_sentence, time_limit, SCREEN):
        """
        Function that draws the results on the screen, it first, calculates the results:
        - total time
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :return: None
        """
        if end:
            # total time calculation
            total_time = time.time() - start_time

            # Calculate accuracy
            correct_chars = word_count - 1  # counting the spaces
            sentence_words = sentence.split(' ')
            input_sen_words = input_sentence.split(' ')
            for i, word in enumerate(sentence_words):
                for j, c in enumerate(word):
                    try:
                        if c == input_sen_words[i][j]:
                            correct_chars += 1
                    except:
                        pass
            accuracy = correct_chars / len(sentence) * 100

            # Calculate speed (word per minute wpm)
            speed = len(input_sentence) * 60 / (5 * total_time)

            if len(input_sentence) < 0.5 * len(sentence):
                accuracy = 'NA'
            results = [f'Total time: {total_time:.2f} secs',
                       f'Accuracy: {accuracy:.2f} %' if accuracy != 'NA' else f'Accuracy: {accuracy}',
                       f'Typing speed: {ceil(speed)} wpm']
            for ind, txt in enumerate(results):
                self.draw_txt(txt, super().FONT_SIZE, super().BITCOIN_ORANGE,
                              left_corner=(100, super().WINDOWHEIGHT / 2 + ind * 40))
            pygame.display.update()


# -------------------------- TimeMode ----------------------------------------------------------------------------------
class TimeMode(ModesABC):

    def __init__(self):
        self.time_limit = None
        self.punctuations = None
        self.numbers = None
        self.word_count = None
        self.print_from_line = 0

    def __init__(self):
        self.numbers = None
        self.punctuations = None
        self.word_count = None

    def menu_button_words(self):
        return True

    def menu_button_time(self):
        return False

    def menu_button_numbers1(self):
        if self.word_count != 15:
            self.word_count = 15
            return 15
        else:
            return None

    def menu_button_numbers2(self):
        if self.word_count != 30:
            self.word_count = 30
            return 30
        else:
            return None

    def menu_button_numbers3(self):
        if self.word_count != 60:
            self.word_count = 60
            return 60
        else:
            return None

    def menu_button_numbers(self):
        self.numbers = not self.numbers
        return False if self.numbers else True

    def menu_button_punctuations(self):
        self.punctuations = not self.punctuations
        return False if self.punctuations else True

    def check_end_game(self, start_time):
        # checks if the game has ended. returns True if ended, else False.
        # if the test is in time mode, checks if the time is elapsed, if yes, ends the test and shows
        # results
        if time.time() >= self.start_time + self.time_limit:
            return True
        return False

    def draw_sentence(self, sentence, input_sentence, active, word_count, letter_width, row_len, SCREEN, theme):
        line_ind = 0
        sentence_words = sentence.split(' ')
        input_sen_words = input_sentence.split(' ')
        current_h_adv = 900

        cursor_x = None
        cursor_y = None

        for i, word in enumerate(sentence_words):
            in_word = input_sen_words[i] if i < len(input_sen_words) else ''
            # check if there is enough space left on the current line for the current word, if not creates a new line.
            if max(len(word), len(in_word)) * letter_width + current_h_adv > row_len:
                if (self.print_from_line != 0 and line_ind > self.print_from_line + 3) or (
                        self.print_from_line == 0 and line_ind > self.print_from_line + 5):
                    break
                if self.print_from_line < line_ind <= self.print_from_line + 4:
                    SCREEN.blit(text_surf, text_surf_rect)

                font = pygame.freetype.Font(super().FONT_TYPE, super().FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(super().ALPHABET + super().ALPHABET)  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                shift = 1 if self.print_from_line > 0 else 0
                text_surf_rect.topleft = (super().MARGIN, super().WINDOWHEIGHT // 2 - 100 + super().LINES_SPACING * (
                        line_ind - self.print_from_line + shift))
                text_surf.fill(theme.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = super().MARGIN + current_h_adv + len(in_word) * letter_width
                if line_ind >= self.print_from_line + 2:
                    self.print_from_line += 1

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = theme.DEFAULT_TEXT_COLOR
                else:
                    color = super().AMARANTH
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, super().AMARANTH_RED)
                    current_h_adv += letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, super().BATTLESHIP_GRAY)
                    current_h_adv += letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', super().BATTLESHIP_GRAY)
            current_h_adv += letter_width
            if self.print_from_line <= line_ind <= self.print_from_line + 3:
                SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(super().FONT_TYPE, super().FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, super().BITCOIN_ORANGE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            SCREEN.blit(textSurfaceObj, textRectObj)

    def update_timer(self, SCREEN, timer):
        # if the test has started, draws the count-down above the sentence
        self.draw_txt(SCREEN, str(timer), super().FONT_SIZE, super().BITCOIN_ORANGE, left_corner=super().TIMER_POSITION)

    def draw_txt(self, SCREEN, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None,
                 box_color=None):
        """
        # this funtion renders a text and a box if specified.
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param txt_color: the color of the text
        :param left_corner: the left corner position of the box, default None
        :param center_position: the center position of the box, default None
        :param box_size: box size, default None
        :param box_color: the color of the box, default None
        """
        if box_size:
            pygame.draw.rect(SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            SCREEN.blit(textSurfaceObj, left_corner)

    def show_result(self, end, start_time, word_count, sentence, input_sentence, time_limit, SCREEN):
        """
        Function that draws the results on the screen, it first, calculates the results:
        - total time
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :return: None
        """
        if end:
            # Calculate accuracy
            sentence_words = sentence.split(' ')
            input_sen_words = input_sentence.split(' ')
            correct_chars = len(input_sen_words) - 1  # counting the spaces

            for i, word in enumerate(sentence_words):
                for j, c in enumerate(word):
                    try:
                        if c == input_sen_words[i][j]:
                            correct_chars += 1
                    except:
                        pass
            accuracy = correct_chars / len(sentence) * 100

            # Calculate speed (word per minute wpm)
            speed = len(input_sentence) * 60 / (5 * time_limit)

            results = [f'Total words: {len(input_sen_words)}',
                       f'Accuracy: {accuracy:.2f} %',
                       f'Typing speed: {ceil(speed)} wpm']
            for ind, txt in enumerate(results):
                self.draw_txt(SCREEN, txt, super().FONT_SIZE, super().BITCOIN_ORANGE,
                              left_corner=(100, super().WINDOWHEIGHT / 2 + ind * 40))
            pygame.display.update()


# -----------------------------------------------------------------------------------------------------------------------


class DarkTheme(Constants):
    def __init__(self):
        self.BG_COLOR = super().BITCOIN_GRAY
        self.DEFAULT_TEXT_COLOR = super().WHITE
        self.BASE_SENTENCE_COLOR = super().BATTLESHIP_GRAY
        self.WRONG_LETTER_COLOR = super().AMARANTH
        self.EXTRA_LETTER_COLOR = super().AMARANTH_RED
        self.CURSOR_COLOR = super().BITCOIN_ORANGE
        self.MENU_SELECTED_BUTTONS = super().BITCOIN_ORANGE
        self.RESET_BOX_COLOR = super().BATTLESHIP_GRAY

        self.moon = 'white_moon_icon.png'
        self.sun = 'white_sun_icon.png'


class LightTheme(Constants):
    def __init__(self):
        self.BG_COLOR = super().WHITE
        self.DEFAULT_TEXT_COLOR = super().BLACK
        self.BASE_SENTENCE_COLOR = super().BATTLESHIP_GRAY
        self.WRONG_LETTER_COLOR = super().AMARANTH
        self.EXTRA_LETTER_COLOR = super().AMARANTH_RED
        self.CURSOR_COLOR = super().BITCOIN_ORANGE
        self.MENU_SELECTED_BUTTONS = super().BITCOIN_ORANGE
        self.RESET_BOX_COLOR = super().BATTLESHIP_GRAY

        self.moon = 'black_moon_icon.png'
        self.sun = 'black_sun_icon.png'


class SpeedTypingTest(Constants):

    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

        # Saving the sizes of all the letters in the english alphabet
        # Note: In case you choose to use a font that is not a monospace font, you will need to use font_metric for the
        # calculation of the space each letter takes (for each letter it is stored in index 4 of the tuple)
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        # getting the sizes of all the letters in the english alphabet
        self.font_metrics = dict(zip(self.ALPHABET, font.get_metrics(self.ALPHABET)))
        # Since I use monospace font, all the letters have the same horizontal size
        self.letter_width = self.font_metrics['a'][4]
        self.row_len = self.WINDOWWIDTH - 2 * self.MARGIN

        # defining the defaults
        self.word_count = 10
        self.time_limit = 15
        self.TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMEREVENT, 1000)
        self.theme = DarkTheme()
        self.mode = WordsMode()
        self.numbers = False  # if True, the test will have numbers
        self.punctuations = False  # if True, the test will have punctuation marks
        self.update_screen = True  # states whether to update the screen's display

        self.accuracy = 0
        self.start_time = 0
        self.timer = self.time_limit
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.running = False  # states whether the user is on the screen of the game

        # initializing sentence by getting a random new one
        self.sentence = self.randomize_sentence()

        self.MENU_BAR_ELEMENTS = {'Words': (self.MARGIN, self.MARGIN, len("Words") * self.letter_width, 30),
                                  'Time': (self.MARGIN + 76, self.MARGIN, len("Time") * self.letter_width, 30),
                                  '1': (self.MARGIN + 141, self.MARGIN, 30, 30),
                                  '2': (self.MARGIN + 173, self.MARGIN, 30, 30),
                                  '3': (self.MARGIN + 205, self.MARGIN, 30, 30),
                                  'Numbers': (self.MARGIN + 258, self.MARGIN, len("Numbers") * self.letter_width, 30),
                                  'Punctuation': (
                                      self.MARGIN + 356, self.MARGIN, len("Punctuation") * self.letter_width, 30)}

    def switch_mode(self):
        if isinstance(self.mode, WordsMode):
            self.mode = TimeMode()
            self.time_limit = 15
            self.word_count = int(300 * self.time_limit / 60)
        else:
            self.mode = WordsMode()
            self.word_count = 10

    def switch_theme(self):
        if isinstance(self.theme, DarkTheme):
            self.theme = LightTheme()
        else:
            self.theme = DarkTheme()

    def play(self):
        self.reset_game()
        while True:
            if self.update_screen:
                self.SCREEN.fill(self.theme.BG_COLOR)
                self.draw_game()
                if isinstance(self.mode, TimeMode) and self.active:
                    self.mode.update_timer(self.SCREEN, self.timer)
                self.mode.draw_sentence(self.sentence, self.input_sentence, self.active, self.word_count,
                                        self.letter_width, self.row_len, self.SCREEN, self.theme)
                pygame.display.update()

            for event in pygame.event.get():
                if isinstance(self.mode, TimeMode):
                    # if the test is in time mode, checks if the time is elapsed, if yes, ends the test and shows
                    # results
                    # if time.time() >= self.start_time + self.time_limit and self.active:
                    #     self.end_test()
                    if event.type == self.TIMEREVENT and self.active:
                        self.timer -= 1
                        self.mode.update_timer(self.SCREEN, self.timer)
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # pressed anywhere on the screen
                    if not self.running and 0 <= x <= self.WINDOWWIDTH and 0 <= y <= self.WINDOWHEIGHT:
                        self.running = True

                    # position of reset box
                    elif self.RESET_BOX_SIZE[0] <= x <= self.RESET_BOX_SIZE[0] + self.RESET_BOX_SIZE[2] \
                            and self.RESET_BOX_SIZE[1] <= y <= self.RESET_BOX_SIZE[1] + self.RESET_BOX_SIZE[3]:
                        self.reset_game()

                    # checking if the user pressed on a button from the menu bar
                    elif self.MENU_BAR_ELEMENTS['Words'][1] <= y <= self.MENU_BAR_ELEMENTS['Words'][1] + \
                            self.MENU_BAR_ELEMENTS['Words'][3]:
                        # check if the user changed the test mode
                        if self.MENU_BAR_ELEMENTS['Words'][0] <= x <= self.MENU_BAR_ELEMENTS['Words'][0] + \
                                self.MENU_BAR_ELEMENTS['Words'][2]:
                            if self.mode.menu_button_words():
                                self.switch_mode()
                                self.reset_game()

                        elif self.MENU_BAR_ELEMENTS['Time'][0] <= x <= self.MENU_BAR_ELEMENTS['Time'][0] + \
                                self.MENU_BAR_ELEMENTS['Time'][2]:
                            if self.mode.menu_button_numbers():
                                self.switch_mode()
                                self.reset_game()
                        # checking if the user changed the word count on word mode
                        elif isinstance(self.mode, WordsMode) and self.MENU_BAR_ELEMENTS['1'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['1'][0] + \
                                self.MENU_BAR_ELEMENTS['1'][2] and self.word_count != 10:
                            self.word_count = 10
                            self.reset_game()
                        elif isinstance(self.mode, WordsMode) and self.MENU_BAR_ELEMENTS['2'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['2'][0] + \
                                self.MENU_BAR_ELEMENTS['2'][2] and self.word_count != 20:
                            self.word_count = 20
                            self.reset_game()
                        elif isinstance(self.mode, WordsMode) and self.MENU_BAR_ELEMENTS['3'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['3'][0] + \
                                self.MENU_BAR_ELEMENTS['3'][2] and self.word_count != 30:
                            self.word_count = 30
                            self.reset_game()
                        # checking if the user changed the time limit on time mode
                        elif isinstance(self.mode, TimeMode) and self.MENU_BAR_ELEMENTS['1'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['1'][0] + \
                                self.MENU_BAR_ELEMENTS['1'][2] and self.time_limit != 15:
                            self.word_count = int(300 * 15 / 60)
                            self.time_limit = 15
                            self.reset_game()
                        elif isinstance(self.mode, TimeMode) and self.MENU_BAR_ELEMENTS['2'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['2'][0] + \
                                self.MENU_BAR_ELEMENTS['2'][2] and self.time_limit != 30:
                            self.word_count = int(300 * 30 / 60)
                            self.time_limit = 30
                            self.reset_game()
                        elif isinstance(self.mode, TimeMode) and self.MENU_BAR_ELEMENTS['3'][0] <= x <= \
                                self.MENU_BAR_ELEMENTS['3'][0] + \
                                self.MENU_BAR_ELEMENTS['3'][2] and self.time_limit != 60:
                            self.word_count = int(300 * 60 / 60)
                            self.time_limit = 60
                            self.reset_game()
                        # check if Numbers button is presses
                        elif self.MENU_BAR_ELEMENTS['Numbers'][0] <= x <= self.MENU_BAR_ELEMENTS['Numbers'][0] + \
                                self.MENU_BAR_ELEMENTS['Numbers'][2]:
                            self.numbers = not self.numbers
                            self.reset_game()
                        # check if Punctuation button is presses
                        elif self.MENU_BAR_ELEMENTS['Punctuation'][0] <= x <= self.MENU_BAR_ELEMENTS['Punctuation'][0] + \
                                self.MENU_BAR_ELEMENTS['Punctuation'][2]:
                            self.punctuations = not self.punctuations
                            self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.running and not self.active:
                        self.start_time = time.time()
                        self.active = True
                    if event.key == pygame.K_BACKSPACE:
                        self.input_sentence = self.input_sentence[:-1]

                    elif self.active and not self.end:
                        try:
                            # checks if the entered key is an alphabet letter or punctuation marks
                            if event.unicode in self.ALPHABET:
                                self.input_sentence += event.unicode
                                self.mode.draw_sentence()
                        except:
                            pass
                if self.active and self.mode.check_end_game(self.input_sentence):
                    self.end_test()

            pygame.display.update()
        clock.tick(60)

    def reset_game(self):
        """
        Function to reset the game, resets the relevant flags to prepare to new game, and generates a new sentence
        :return: None
        """
        self.start_time = 0
        self.timer = self.time_limit
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.update_screen = True
        self.SCREEN.fill(self.theme.BG_COLOR)
        self.print_from_line = 0

        # initializing sentence by getting a random new one
        self.sentence = self.randomize_sentence()
        if isinstance(self.mode, TimeMode):
            self.mode.print_from_line = 0

    def randomize_sentence(self):
        """
        generates a random sentence of the length of word_count the is determined by the user.
        gets the words_file from .txt file specified in the initialization of the game.
        :return: string - random sentence
        """
        words_file = open(self.DATA_FILE_NAME)
        words = random.sample(list(words_file.readlines()), self.word_count)
        words = [word[:-1] for word in words]
        if self.punctuations:
            puncs = [super().PUNCTUATION_MARKS[random.randint(0, len(super().PUNCTUATION_MARKS) - 1)] for i in
                     range(0, int(self.word_count * 0.2))]
            for pun in puncs:
                ind = random.choice(range(0, self.word_count))
                words[ind] = words[ind] + pun
        if self.numbers:
            nums = [random.randint(0, 10) for i in range(0, int(self.word_count * 0.2))]
            for num in nums:
                ind = random.choice(range(0, self.word_count))
                words[ind] = words[ind] + str(num)
        delimiter = " "
        sentence = delimiter.join(words)
        words_file.close()
        return sentence

    def draw_game(self):
        """
        Function that draws the game, it draws the reset button and the word count buttons.
        :return: None
        """
        # drawing the reset button
        spacing = 10
        pos_shift = 8
        center_position = (super().RESET_BOX_SIZE[0] + super().RESET_BOX_SIZE[2] / 2,
                           super().RESET_BOX_SIZE[1] + super().RESET_BOX_SIZE[3] / 2)
        self.draw_txt('Reset', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                      center_position=center_position,
                      box_size=super().RESET_BOX_SIZE, box_color=self.theme.RESET_BOX_COLOR)

        # Drawing the menu bar
        pos = (self.MENU_BAR_ELEMENTS['Words'][0], self.MENU_BAR_ELEMENTS['Words'][1])
        self.draw_txt('Words', super().BUTTONS_FONT_SIZE,
                      self.theme.MENU_SELECTED_BUTTONS if isinstance(self.mode,
                                                                     WordsMode) else self.theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        pos = (pos[0] + len('Words') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.theme.DEFAULT_TEXT_COLOR, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Time'][0], self.MENU_BAR_ELEMENTS['Time'][1])
        self.draw_txt('Time', super().BUTTONS_FONT_SIZE,
                      self.theme.MENU_SELECTED_BUTTONS if isinstance(self.mode,
                                                                     TimeMode) else self.theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        pos = (pos[0] + len('Time') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.theme.DEFAULT_TEXT_COLOR, left_corner=(pos[0], pos[1] - pos_shift))

        r = (15, 30, 60) if isinstance(self.mode, TimeMode) else (10, 20, 30)
        for i, count in enumerate(r):
            pos = (self.MENU_BAR_ELEMENTS[str(i + 1)][0], self.MENU_BAR_ELEMENTS[str(i + 1)][1])
            self.draw_txt(str(count), self.BUTTONS_FONT_SIZE,
                          self.theme.MENU_SELECTED_BUTTONS if count == self.time_limit else self.theme.DEFAULT_TEXT_COLOR,
                          left_corner=pos)

        pos = (pos[0] + len(str(count)) * self.letter_width + spacing, pos[1])
        self.draw_txt('|', 24, self.theme.DEFAULT_TEXT_COLOR, left_corner=(pos[0], pos[1] - pos_shift))

        # drawing punctuation and numbers button
        pos = (self.MENU_BAR_ELEMENTS['Numbers'][0], self.MENU_BAR_ELEMENTS['Numbers'][1])
        self.draw_txt("Numbers", super().BUTTONS_FONT_SIZE,
                      self.theme.MENU_SELECTED_BUTTONS if self.numbers else self.theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        pos = (pos[0] + len('Numbers') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.theme.DEFAULT_TEXT_COLOR, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Punctuation'][0], self.MENU_BAR_ELEMENTS['Punctuation'][1])
        self.draw_txt("Punctuation", super().BUTTONS_FONT_SIZE,
                      self.theme.MENU_SELECTED_BUTTONS if self.punctuations else self.theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

    def draw_txt(self, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None, box_color=None):
        """
        # this funtion renders a text and a box if specified.
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param txt_color: the color of the text
        :param left_corner: the left corner position of the box, default None
        :param center_position: the center position of the box, default None
        :param box_size: box size, default None
        :param box_color: the color of the box, default None
        """
        if box_size:
            pygame.draw.rect(self.SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(super().FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            self.SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            self.SCREEN.blit(textSurfaceObj, left_corner)

    def end_test(self):
        self.SCREEN.fill(self.theme.BG_COLOR)
        self.draw_game()
        self.active = False
        self.end = True
        self.mode.show_result(self.end, self.start_time, self.word_count, self.sentence, self.input_sentence,
                              self.time_limit, self.SCREEN)
        self.update_screen = False


# -----------------------------------------------------------------------------------------------------------------------

typing_game = SpeedTypingTest()
print(typing_game.__dict__)

typing_game.play()
