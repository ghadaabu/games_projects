import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype
from math import ceil
from abc import ABC
import darkdetect


# -------------------- Constants class ---------------------------------------------------------------------------------
class Constants:
    """
    class for the constants of the game such as colors, positions of objects, font related parameters.
    """
    WINDOWWIDTH = 1100  # 640  # size of window's width in pixels
    WINDOWHEIGHT = 600  # 480  # size of windows' height in pixels

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz| :;,._!ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    PUNCTUATION_MARKS = [':', '.', ',', '!', ';']
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BATTLESHIP_GRAY = (132, 132, 130)
    LIGHT_GREY = (188, 188, 188)
    BITCOIN_GRAY = (77, 77, 78)  # darker
    BLACK_COFFEE = (59, 47, 47)
    FATHOM_GREY = (41, 44, 51)
    AMARANTH = (211, 33, 45)
    AMARANTH_RED = (150, 27, 45)  # darker
    BITCOIN_ORANGE = (242, 169, 0)
    LIGHT_CYAN = (224, 255, 255)
    DARKER_WHITE = (228, 228, 228)

    # using Google's font - RobotoMono-Regular font. https://fonts.google.com/specimen/IBM+Plex+Mono?query=mono
    FONT_TYPE = "RobotoMono-Regular.ttf"
    # https://www.mit.edu/~ecprice/wordlist.10000 link to data file
    DATA_FILE_NAME = "wordlist.10000.txt"
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size

    FONT_SIZE = 20

    MARGIN = 100

    REPEAT_POSITION = (WINDOWWIDTH / 2 - 30, WINDOWHEIGHT - 100)
    NEXT_POSITION = (WINDOWWIDTH / 2 - 70, WINDOWHEIGHT - 100)

    # Menu bar and buttons related constants
    BUTTONS_FONT_SIZE = 16
    BUTTONS_VERTICAL_SIZE = 30
    MENU_STARTING_POSITION = (MARGIN, MARGIN)
    MENU_BUTTONS_HORIZONTAL_SHIFT = 10
    MENU_BUTTONS_VERTICAL_SHIFT = 10

    LINES_SPACING = 50
    COUNT_DOWN_POSITION = (WINDOWWIDTH // 2, MARGIN + 50)

    ICONS_SIZE = (30, 30)
    MOON_POSITION = (WINDOWWIDTH - MARGIN, MARGIN * .5)
    SUN_POSITION = (WINDOWWIDTH - MARGIN - ICONS_SIZE[0] - 5, MARGIN * .5)


# ------------------------- ABSTRACT CLASS for modes -------------------------------------------------------------------
class ModesABC(ABC):
    """
    An abstract base class for the game's mode, to make adding modes to the game easier.
    """

    def __init__(self):
        pass

    def get_word_count(self):
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

    def check_end_game(self, *args):
        pass

    def update_count_down(self, *args):
        pass

    def draw_game(self, *args):
        pass

    def draw_sentence(self, *args):
        pass

    def draw_txt(self, *args):
        pass

    def show_result(self, *args):
        pass


# -------------------------- WordsMode ---------------------------------------------------------------------------------

class WordsMode(ModesABC):
    """
    Words mode module.
    contains all the words mode related functions.
    """

    def __init__(self, word_count, punctuations, numbers):
        """
        :param word_count: the number of words in the test, int = [10, 20, 30]
        :param punctuations: boolean parameter, which indicates if the test has punctuations
        :param numbers: boolean parameter, which indicates if the test has numbers
        """
        self.word_count = word_count
        self.punctuations = punctuations
        self.numbers = numbers
        self.constants = Constants()

    def get_word_count(self):
        return self.word_count

    def menu_button_words(self):
        return False

    def menu_button_time(self):
        return True

    def menu_button_numbers1(self):
        if self.word_count != 10:
            self.word_count = 10
            return self.word_count
        return None

    def menu_button_numbers2(self):
        if self.word_count != 20:
            self.word_count = 20
            return self.word_count
        return None

    def menu_button_numbers3(self):
        if self.word_count != 30:
            self.word_count = 30
            return self.word_count
        return None

    def menu_button_numbers(self):
        self.numbers = not self.numbers
        return False if self.numbers else True

    def menu_button_punctuations(self):
        self.punctuations = not self.punctuations
        return False if self.punctuations else True

    def check_end_game(self, sentence, input_sentence, **kwargs):
        """
        checks if the game has ended. returns True if ended, else False.
        there are two scenarios to end the test:
        1. the user entered all the letters of the last word in the sentence.
        2. the user didn't enter the last word (or partially) and pressed space.
        :param sentence: the original sentence of the test
        :param input_sentence: the user's typed sentence
        :return: Boolean value
        """
        input_words = input_sentence.split(' ')
        if (len(input_words) == self.word_count and len(input_words[-1]) == len(
                sentence.split(' ')[-1])) or (
                len(input_words) > self.word_count and input_sentence[-1] == ' '):
            return True
        return False

    def update_count_down(self, theme, input_sentence, letter_width, SCREEN, **kwargs):
        """
        Updates the count-down and prints it on the screen.
        In this module the words counter is updated whenever the user moves to the next words.
        :param theme: the theme of the game.
        :param input_sentence: the user's typed sentence
        :param letter_width: font related parameter
        :param SCREEN: the screen object to draw the text over
        :return: None
        """
        input_sen_words = input_sentence.split(' ')
        self.draw_txt(SCREEN, f'{len(input_sen_words) - 1} / {self.word_count}', theme.FONT_SIZE, theme.COUNTER_COLOR,
                      left_corner=self.constants.COUNT_DOWN_POSITION)

    def draw_game(self, MENU_BAR_ELEMENTS, theme, letter_width, end, SCREEN, **kwargs):
        """
        Draws the menu bar and highlights the relevant and selected modes.
        :param MENU_BAR_ELEMENTS: Contains the information about the positions of the menu bar buttons.
        :param theme: the theme of the game.
        :param letter_width: the width of a letter in points.
        :param end: flag for the end of the game. True when the game ends.
        :param SCREEN: The screen of the game to blit to.
        :return: None
        """
        pos = (MENU_BAR_ELEMENTS['Words'][0], MENU_BAR_ELEMENTS['Words'][1])
        self.draw_txt(SCREEN, 'Words', theme.BUTTONS_FONT_SIZE, theme.MENU_SELECTED_BUTTONS, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Words'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Time'][0], MENU_BAR_ELEMENTS['Time'][1])
        self.draw_txt(SCREEN, 'Time', theme.BUTTONS_FONT_SIZE, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Time'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        for i, op in enumerate((10, 20, 30)):
            pos = (MENU_BAR_ELEMENTS['options'][str(i + 1)][0], MENU_BAR_ELEMENTS['options'][str(i + 1)][1])
            self.draw_txt(SCREEN, str(op), self.constants.BUTTONS_FONT_SIZE,
                          theme.MENU_SELECTED_BUTTONS if op == self.word_count else theme.DEFAULT_TEXT_COLOR,
                          left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['options']['3'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        # drawing punctuation and numbers button
        pos = (MENU_BAR_ELEMENTS['Numbers'][0], MENU_BAR_ELEMENTS['Numbers'][1])
        self.draw_txt(SCREEN, "Numbers", self.constants.BUTTONS_FONT_SIZE,
                      theme.MENU_SELECTED_BUTTONS if self.numbers else theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Numbers'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Punctuation'][0], MENU_BAR_ELEMENTS['Punctuation'][1])
        self.draw_txt(SCREEN, "Punctuation", self.constants.BUTTONS_FONT_SIZE,
                      theme.MENU_SELECTED_BUTTONS if self.punctuations else theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        SCREEN.blit(theme.moon_icon, self.constants.MOON_POSITION)
        SCREEN.blit(theme.sun_icon, self.constants.SUN_POSITION)
        if end:
            SCREEN.blit(theme.next_icon, self.constants.NEXT_POSITION)
        SCREEN.blit(theme.repeat_icon, (self.constants.REPEAT_POSITION[0], self.constants.REPEAT_POSITION[1]))

    def draw_sentence(self, sentence, input_sentence, letter_width, row_len, SCREEN, theme, **kwargs):
        """
        Function that draws the sentence on the screen, it colors the letters with different colors based on the
        accuracy of the entered words_file where:
        - correct entered letter: white
        - wrong entered letter: Red
        - extra entered letter: dark red
        - not entered yet: light grey
        It also draws a cursor where the next letter to be entered.
        :param sentence: the original sentence of the test.
        :param input_sentence: the user's typed sentence.
        :param letter_width: the width of a letter in points.
        :param row_len: the length of the row. (in points)
        :param SCREEN: the screen of the game to blit to.
        :param theme: the game's theme.
        :return: None
        """
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
                if line_ind != 0:  # if line is the first, no need to blit the surface to the screen
                    SCREEN.blit(text_surf, text_surf_rect)
                font = pygame.freetype.Font(self.constants.FONT_TYPE, self.constants.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.constants.ALPHABET + self.constants.ALPHABET)  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.topleft = (
                    self.constants.MARGIN,
                    self.constants.WINDOWHEIGHT // 2 - 100 + self.constants.LINES_SPACING * line_ind)
                text_surf.fill(theme.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.constants.MARGIN + current_h_adv + len(in_word) * letter_width

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = theme.DEFAULT_TEXT_COLOR
                else:
                    color = theme.WRONG_LETTER_COLOR
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, theme.EXTRA_LETTER_COLOR)
                    current_h_adv += letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, theme.BASE_SENTENCE_COLOR)
                    current_h_adv += letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', theme.BASE_SENTENCE_COLOR)
            current_h_adv += letter_width
            SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(self.constants.FONT_TYPE, self.constants.FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, theme.CURSOR_COLOR)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            SCREEN.blit(textSurfaceObj, textRectObj)

    def draw_txt(self, SCREEN, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None,
                 box_color=None):
        """
        Function for rendering the text on the screen.
        the position of the text can be either the top left corner or the center position.
        the text can be drawn with a box behind it, if the size and the color of the box are provided.
        :param SCREEN: The game's screen to blit to.
        :param txt: the text to be rendered.
        :param txt_size: Font size.
        :param txt_color: Font color.
        :param left_corner: the top left corner of the text rectangle. by default is set to None.
        :param center_position: the center position of the text rectangle. by default is set to None.
        :param box_size: the box size. by default None.
        :param box_color: the box color. by default None.
        :return: None
        """
        if box_size:
            pygame.draw.rect(SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(self.constants.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            textRectObj.topleft = left_corner
            SCREEN.blit(textSurfaceObj, textRectObj)

    def show_result(self, start_time, end_game_time, sentence, input_sentence, theme, SCREEN, **kwargs):
        """
        Calculates and prints the results of the test. The results are as follows:
        - total time
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :param start_time: the starting time of the test.
        :param end_game_time: the end time of the test.
        :param sentence: the original sentence of the test.
        :param input_sentence: the user's typed sentence.
        :param theme: the theme of the game.
        :param SCREEN: the game's screen to blit to.
        :return: None
        """
        # total time calculation
        total_time = end_game_time - start_time

        # Calculate accuracy
        correct_chars = self.word_count - 1  # counting the spaces
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
            self.draw_txt(SCREEN, txt, self.constants.FONT_SIZE, theme.RESULTS_COLOR,
                          left_corner=(100, self.constants.WINDOWHEIGHT / 2 + ind * 40))
        pygame.display.update()


# -------------------------- TimeMode ----------------------------------------------------------------------------------
class TimeMode(ModesABC):

    def __init__(self, time_limit, punctuations, numbers):
        self.time_limit = time_limit
        self.punctuations = punctuations
        self.numbers = numbers
        self.word_count = int(300 * time_limit / 60)
        self.print_from_line = 0
        self.constants = Constants()

    def get_word_count(self):
        return self.word_count

    def menu_button_words(self):
        return True

    def menu_button_time(self):
        return False

    def menu_button_numbers1(self):
        if self.time_limit != 15:
            self.time_limit = 15
            return self.time_limit
        return None

    def menu_button_numbers2(self):
        if self.time_limit != 30:
            self.time_limit = 30
            return self.time_limit
        return None

    def menu_button_numbers3(self):
        if self.time_limit != 60:
            self.time_limit = 60
            return self.time_limit
        return None

    def menu_button_numbers(self):
        self.numbers = not self.numbers
        return False if self.numbers else True

    def menu_button_punctuations(self):
        self.punctuations = not self.punctuations
        return False if self.punctuations else True

    def check_end_game(self, input_sentence, start_time, **kwargs):
        """
        checks if the game has ended. returns True if ended, else False.
        The game ends when the time elapses.
        :param input_sentence: the user's typed sentence
        :param start_time: the starting time of the test.
        :return: True if the game ended, else False.
        """
        if time.time() >= start_time + self.time_limit:
            return True
        return False

    def update_count_down(self, theme, timer, input_sentence, SCREEN, **kwargs):
        """
        Updates the count-down and prints it on the screen.
        In this module the timer is updated after every passing second.
        :param theme: the theme of the game.
        :param timer: timer.
        :param input_sentence: the user's typed sentence
        :param SCREEN: the screen object to draw the text over
        :return: None
        """
        self.draw_txt(SCREEN, str(timer), theme.FONT_SIZE, theme.COUNTER_COLOR,
                      left_corner=self.constants.COUNT_DOWN_POSITION)

    def draw_game(self, MENU_BAR_ELEMENTS, theme, letter_width, end, SCREEN, **kwargs):
        """
        Draws the menu bar and highlights the relevant and selected modes.
        :param MENU_BAR_ELEMENTS: Contains the information about the positions of the menu bar buttons.
        :param theme: the theme of the game.
        :param letter_width: the width of a letter in points.
        :param end: flag for the end of the game. True when the game ends.
        :param SCREEN: The screen of the game to blit to.
        :return: None
        """
        pos = (MENU_BAR_ELEMENTS['Words'][0], MENU_BAR_ELEMENTS['Words'][1])
        self.draw_txt(SCREEN, 'Words', theme.BUTTONS_FONT_SIZE, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Words'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Time'][0], MENU_BAR_ELEMENTS['Time'][1])
        self.draw_txt(SCREEN, 'Time', theme.BUTTONS_FONT_SIZE, theme.MENU_SELECTED_BUTTONS, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Time'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        for i, count in enumerate((15, 30, 60)):
            pos = (MENU_BAR_ELEMENTS['options'][str(i + 1)][0], MENU_BAR_ELEMENTS['options'][str(i + 1)][1])
            self.draw_txt(SCREEN, str(count), self.constants.BUTTONS_FONT_SIZE,
                          theme.MENU_SELECTED_BUTTONS if count == self.time_limit else theme.DEFAULT_TEXT_COLOR,
                          left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['options']['3'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        # drawing punctuation and numbers button
        pos = (MENU_BAR_ELEMENTS['Numbers'][0], MENU_BAR_ELEMENTS['Numbers'][1])
        self.draw_txt(SCREEN, "Numbers", self.constants.BUTTONS_FONT_SIZE,
                      theme.MENU_SELECTED_BUTTONS if self.numbers else theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Numbers'][2] + self.constants.MENU_BUTTONS_HORIZONTAL_SHIFT,
               pos[1] - self.constants.MENU_BUTTONS_VERTICAL_SHIFT)
        self.draw_txt(SCREEN, '|', 24, theme.DEFAULT_TEXT_COLOR, left_corner=pos)

        pos = (MENU_BAR_ELEMENTS['Punctuation'][0], MENU_BAR_ELEMENTS['Punctuation'][1])
        self.draw_txt(SCREEN, "Punctuation", self.constants.BUTTONS_FONT_SIZE,
                      theme.MENU_SELECTED_BUTTONS if self.punctuations else theme.DEFAULT_TEXT_COLOR,
                      left_corner=pos)

        SCREEN.blit(theme.moon_icon, self.constants.MOON_POSITION)
        SCREEN.blit(theme.sun_icon, self.constants.SUN_POSITION)
        if end:
            SCREEN.blit(theme.next_icon, self.constants.NEXT_POSITION)
        SCREEN.blit(theme.repeat_icon, (self.constants.REPEAT_POSITION[0], self.constants.REPEAT_POSITION[1]))

    def draw_sentence(self, sentence, input_sentence, letter_width, row_len, SCREEN, theme, **kwargs):
        """
        Function that draws four rows of the sentence on the screen and updates the rows based on the user's advancement
        It colors the letters with different colors based on the validity of the entered letters, where:
        - correct letter: white in dark theme and black in light theme.
        - wrong entered letter: Red.
        - extra entered letter: dark red.
        - not entered yet: light grey.
        It also draws a cursor where the next letter to be entered.
        :param sentence: the original sentence of the test.
        :param input_sentence: the user's typed sentence.
        :param letter_width: the width of a letter in points.
        :param row_len: the length of the row. (in points)
        :param SCREEN: the screen of the game to blit to.
        :param theme: the game's theme.
        :return: None
        """
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

                font = pygame.freetype.Font(self.constants.FONT_TYPE, self.constants.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.constants.ALPHABET + self.constants.ALPHABET)  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                shift = 1 if self.print_from_line > 0 else 0
                text_surf_rect.topleft = (
                    self.constants.MARGIN, self.constants.WINDOWHEIGHT // 2 - 100 + self.constants.LINES_SPACING * (
                            line_ind - self.print_from_line + shift))
                text_surf.fill(theme.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.constants.MARGIN + current_h_adv + len(in_word) * letter_width
                if line_ind >= self.print_from_line + 2:
                    self.print_from_line += 1

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = theme.DEFAULT_TEXT_COLOR
                else:
                    color = theme.WRONG_LETTER_COLOR
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, theme.EXTRA_LETTER_COLOR)
                    current_h_adv += letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, theme.BASE_SENTENCE_COLOR)
                    current_h_adv += letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', theme.BASE_SENTENCE_COLOR)
            current_h_adv += letter_width
            if self.print_from_line <= line_ind <= self.print_from_line + 3:
                SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(self.constants.FONT_TYPE, self.constants.FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, theme.CURSOR_COLOR)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            SCREEN.blit(textSurfaceObj, textRectObj)

    def draw_txt(self, SCREEN, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None,
                 box_color=None):
        """
        Function for rendering the text on the screen.
        the position of the text can be either the top left corner or the center position.
        the text can be drawn with a box behind it, if the size and the color of the box are provided.
        :param SCREEN: The game's screen to blit to.
        :param txt: the text to be rendered.
        :param txt_size: Font size.
        :param txt_color: Font color.
        :param left_corner: the top left corner of the text rectangle. by default is set to None.
        :param center_position: the center position of the text rectangle. by default is set to None.
        :param box_size: the box size. by default None.
        :param box_color: the box color. by default None.
        :return: None
        """
        if box_size:
            pygame.draw.rect(SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(self.constants.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            SCREEN.blit(textSurfaceObj, left_corner)

    def show_result(self, sentence, input_sentence, theme, SCREEN, **kwargs):
        """
        Calculates and prints the results of the test. The results are as follows:
        - total words
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :param sentence: the original sentence of the test.
        :param input_sentence: the user's typed sentence.
        :param theme: the theme of the game.
        :param SCREEN: the game's screen to blit to.
        :return: None
        """
        # Accuracy calculation
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
        speed = len(input_sentence) * 60 / (5 * self.time_limit)

        results = [f'Total words: {len(input_sen_words)}',
                   f'Accuracy: {accuracy:.2f} %',
                   f'Typing speed: {ceil(speed)} wpm']
        for ind, txt in enumerate(results):
            self.draw_txt(SCREEN, txt, self.constants.FONT_SIZE, theme.RESULTS_COLOR,
                          left_corner=(100, self.constants.WINDOWHEIGHT / 2 + ind * 40))
        pygame.display.update()


# ---------------------- Theme classes ---------------------------------------------------------------------------------

class DarkTheme(Constants):
    """
    This class defines the colores and objects that are dark theme related.
    """

    def __init__(self):
        self.BG_COLOR = super().BITCOIN_GRAY
        self.DEFAULT_TEXT_COLOR = super().WHITE
        self.BASE_SENTENCE_COLOR = super().BATTLESHIP_GRAY
        self.WRONG_LETTER_COLOR = super().AMARANTH
        self.EXTRA_LETTER_COLOR = super().AMARANTH_RED
        self.CURSOR_COLOR = super().BITCOIN_ORANGE
        self.MENU_SELECTED_BUTTONS = super().BITCOIN_ORANGE
        self.RESET_BOX_COLOR = super().BATTLESHIP_GRAY
        self.COUNTER_COLOR = super().BITCOIN_ORANGE
        self.RESULTS_COLOR = super().BITCOIN_ORANGE

        self.moon = 'white_moon_icon.png'
        self.sun = 'white_sun_icon.png'
        self.repeat_icon_name = 'white_repeat_icon.png'
        self.next_name = 'white_next_icon.png'
        self.moon_icon = pygame.transform.smoothscale(pygame.image.load(self.moon), super().ICONS_SIZE)
        self.sun_icon = pygame.transform.smoothscale(pygame.image.load(self.sun), super().ICONS_SIZE)
        self.repeat_icon = pygame.transform.smoothscale(pygame.image.load(self.repeat_icon_name), super().ICONS_SIZE)
        self.next_icon = pygame.transform.smoothscale(pygame.image.load(self.next_name), super().ICONS_SIZE)


class LightTheme(Constants):
    """
    This class defines the colores and objects that are light theme related.
    """

    def __init__(self):
        self.BG_COLOR = super().DARKER_WHITE
        self.DEFAULT_TEXT_COLOR = super().BLACK
        self.BASE_SENTENCE_COLOR = super().LIGHT_GREY
        self.WRONG_LETTER_COLOR = super().AMARANTH
        self.EXTRA_LETTER_COLOR = super().AMARANTH_RED
        self.CURSOR_COLOR = super().BITCOIN_ORANGE
        self.MENU_SELECTED_BUTTONS = super().BITCOIN_ORANGE
        self.RESET_BOX_COLOR = super().BATTLESHIP_GRAY
        self.COUNTER_COLOR = super().BITCOIN_ORANGE
        self.RESULTS_COLOR = super().BITCOIN_ORANGE

        self.moon = 'black_moon_icon.png'
        self.sun = 'black_sun_icon.png'
        self.repeat_icon_name = 'black_repeat_icon.png'
        self.next_name = 'black_next_icon.png'
        self.moon_icon = pygame.transform.smoothscale(pygame.image.load(self.moon), super().ICONS_SIZE)
        self.sun_icon = pygame.transform.smoothscale(pygame.image.load(self.sun), super().ICONS_SIZE)
        self.repeat_icon = pygame.transform.smoothscale(pygame.image.load(self.repeat_icon_name), super().ICONS_SIZE)
        self.next_icon = pygame.transform.smoothscale(pygame.image.load(self.next_name), super().ICONS_SIZE)


# ----------------- The main class - the game class --------------------------------------------------------------------
class SpeedTypingTest(Constants):
    """
    The main class and it manages the game.
    The game has two modes: words mode and time mode, and works with two themes: dark theme and light theme.
    The game starts by default with words mode and the system's theme (if the system uses dark theme then the game also starts with dark theme)
    """

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
        self.hover = {'repeat': False, 'next': False, 'sun': False, 'moon': False}
        self.limit = 10
        self.TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMEREVENT, 1000)
        if darkdetect.isDark():
            self.theme = DarkTheme()
        else:
            self.theme = LightTheme()

        self.numbers = False  # if True, the test will have numbers
        self.punctuations = False  # if True, the test will have punctuation marks
        self.mode = WordsMode(self.limit, self.punctuations, self.numbers)

        self.accuracy = 0
        self.start_time = None
        self.input_sentence = ''
        self.end = False  # flag that states whether the game ended.
        self.active = False  # flag that states whether the game has started. (True when the first letter is typed)
        self.running = False  # flag that states whether the user pressed on the game's screen.
        self.timer = None
        self.end_game_time = None

        # initializing sentence by getting a random new one
        self.sentence = self.randomize_sentence()

        self.MENU_BAR_ELEMENTS = None
        self.init_menu_bar_positions()

    def switch_mode(self):
        """
        switches the game's mode. it initialzes the relevant mode with the default word count/ time limit.
        :return: None
        """
        if isinstance(self.mode, WordsMode):
            self.limit = 15
            self.mode = TimeMode(self.limit, self.punctuations, self.numbers)
        else:
            self.limit = 10
            self.mode = WordsMode(self.limit, self.punctuations, self.numbers)

    def switch_theme(self):
        """
        switches the game's theme.
        :return: None
        """
        if isinstance(self.theme, DarkTheme):
            self.theme = LightTheme()
        else:
            self.theme = DarkTheme()

    def init_menu_bar_positions(self):
        """
        initializes the menu bar buttons positions.
        :return: None
        """
        self.MENU_BAR_ELEMENTS = {'Words': None, 'Time': None, 'options': {'1': None, '2': None, '3': None},
                                  'Numbers': None,
                                  'Punctuation': None}
        pos = super().MENU_STARTING_POSITION
        for button in self.MENU_BAR_ELEMENTS:
            if button != 'options':
                fontObj = pygame.font.Font(super().FONT_TYPE, super().BUTTONS_FONT_SIZE)
                textSurfaceObj = fontObj.render(button, True, super().BLACK)
                textRectObj = textSurfaceObj.get_rect()
                size = textRectObj.topright[0]
                self.MENU_BAR_ELEMENTS[button] = (pos[0], pos[1], pos[0] + size)

                pos = (pos[0] + size + 3 * super().MENU_BUTTONS_HORIZONTAL_SHIFT, pos[1])
            else:
                fontObj = pygame.font.Font(super().FONT_TYPE, super().BUTTONS_FONT_SIZE)
                textSurfaceObj = fontObj.render('10', True, super().BLACK)
                textRectObj = textSurfaceObj.get_rect()
                size = textRectObj.topright[0]
                for option in self.MENU_BAR_ELEMENTS[button]:
                    self.MENU_BAR_ELEMENTS[button][option] = (pos[0], pos[1], pos[0] + size)
                    pos = (pos[0] + 3 * super().MENU_BUTTONS_HORIZONTAL_SHIFT, pos[1])
                pos = (pos[0] + size + int(.5 * super().MENU_BUTTONS_HORIZONTAL_SHIFT), pos[1])

    def play(self):
        """
        the main loop of the game.
        :return: None
        """
        self.reset_game()
        while True:
            self.SCREEN.fill(self.theme.BG_COLOR)
            self.mode.draw_game(**self.__dict__)

            if self.active:
                self.mode.update_count_down(**self.__dict__)
            self.mode.draw_sentence(**self.__dict__)

            if self.end:
                self.end_test()
            if any(self.hover.values()):
                self.hover_fuc()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == self.TIMEREVENT and self.active:
                    self.timer -= 1

                # checking the cursor's movement for the hovering functions.
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if self.REPEAT_POSITION[0] <= x <= self.REPEAT_POSITION[0] + \
                            super().ICONS_SIZE[0] and self.REPEAT_POSITION[1] <= y <= \
                            self.REPEAT_POSITION[1] + super().ICONS_SIZE[1]:
                        self.hover['repeat'] = True
                    elif super().SUN_POSITION[0] <= x <= super().SUN_POSITION[0] + \
                            super().ICONS_SIZE[0] and super().SUN_POSITION[1] <= y <= \
                            super().SUN_POSITION[1] + super().ICONS_SIZE[1]:
                        self.hover['sun'] = True
                    elif super().MOON_POSITION[0] <= x <= super().MOON_POSITION[0] + \
                            super().ICONS_SIZE[0] and super().MOON_POSITION[1] <= y <= \
                            super().MOON_POSITION[1] + super().ICONS_SIZE[1]:
                        self.hover['moon'] = True
                    elif self.end and super().NEXT_POSITION[0] <= x <= super().NEXT_POSITION[0] + \
                            super().ICONS_SIZE[0] and super().NEXT_POSITION[1] <= y <= \
                            super().NEXT_POSITION[1] + super().ICONS_SIZE[1]:
                        self.hover['next'] = True
                    else:
                        self.hover = {'repeat': False, 'next': False, 'sun': False, 'moon': False}

                # checking if the user pressed on a button.
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # pressed anywhere on the screen
                    if not self.running and 0 <= x <= self.WINDOWWIDTH and 0 <= y <= self.WINDOWHEIGHT:
                        self.running = True

                    # position of next box
                    elif self.end and self.NEXT_POSITION[0] <= x <= self.NEXT_POSITION[0] + self.ICONS_SIZE[0] \
                            and self.NEXT_POSITION[1] <= y <= self.NEXT_POSITION[1] + self.ICONS_SIZE[1]:
                        self.reset_game()

                    # position of repeat box
                    elif self.REPEAT_POSITION[0] <= x <= self.REPEAT_POSITION[0] + self.ICONS_SIZE[0] \
                            and self.REPEAT_POSITION[1] <= y <= self.REPEAT_POSITION[1] + self.ICONS_SIZE[1]:
                        if self.end:
                            self.reset_game(randomize=False)
                        else:
                            self.reset_game()

                    # checking if the user pressed on a button from the menu bar
                    # checking if one of the menu bar buttons was pressed.
                    elif self.MENU_BAR_ELEMENTS['Words'][1] <= y <= self.MENU_BAR_ELEMENTS['Words'][1] + \
                            super().BUTTONS_VERTICAL_SIZE:
                        # check if the user changed the test mode
                        if self.MENU_BAR_ELEMENTS['Words'][0] <= x <= self.MENU_BAR_ELEMENTS['Words'][2]:
                            if self.mode.menu_button_words():
                                self.switch_mode()
                                self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['Time'][0] <= x <= self.MENU_BAR_ELEMENTS['Time'][2]:
                            if self.mode.menu_button_time():
                                self.switch_mode()
                                self.reset_game()

                        # checking if the user changed the test limit.
                        elif self.MENU_BAR_ELEMENTS['options']['1'][0] <= x <= self.MENU_BAR_ELEMENTS['options']['1'][
                            2]:
                            lim = self.mode.menu_button_numbers1()
                            if lim:
                                self.limit = lim
                                self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['options']['2'][0] <= x <= self.MENU_BAR_ELEMENTS['options']['2'][
                            2]:
                            lim = self.mode.menu_button_numbers2()
                            if lim:
                                self.limit = lim
                                self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['options']['3'][0] <= x <= self.MENU_BAR_ELEMENTS['options']['3'][
                            2]:
                            lim = self.mode.menu_button_numbers3()
                            if lim:
                                self.limit = lim
                                self.reset_game()

                        # check if Numbers mode button is presses
                        elif self.MENU_BAR_ELEMENTS['Numbers'][0] <= x <= self.MENU_BAR_ELEMENTS['Numbers'][2]:
                            self.mode.menu_button_numbers()
                            self.numbers = not self.numbers
                            self.reset_game()
                        # check if Punctuation mode button is presses
                        elif self.MENU_BAR_ELEMENTS['Punctuation'][0] <= x <= self.MENU_BAR_ELEMENTS['Punctuation'][2]:
                            self.mode.menu_button_punctuations()
                            self.punctuations = not self.punctuations
                            self.reset_game()

                    # checking if the user pressed on the theme buttons
                    elif super().MOON_POSITION[1] <= y <= super().MOON_POSITION[1] + super().ICONS_SIZE[1] and \
                            ((super().MOON_POSITION[0] <= x <= super().MOON_POSITION[0] + super().ICONS_SIZE[0] and
                              not isinstance(self.theme, DarkTheme)) or (
                                     super().SUN_POSITION[0] <= x <= super().SUN_POSITION[0] + super().ICONS_SIZE[0]
                                     and not isinstance(self.theme, LightTheme))):
                        self.switch_theme()

                # checks if the user typed on the keyboard.
                elif event.type == pygame.KEYDOWN:
                    # if the game hasn't started yet and the user started typing, then it starts the game.
                    if self.running and not self.active and not self.end:
                        self.start_time = time.time()
                        self.active = True
                    # checking if the user pressed backspace
                    if event.key == pygame.K_BACKSPACE:
                        self.input_sentence = self.input_sentence[:-1]

                    elif self.active and not self.end:
                        try:
                            # checks if the entered key is an alphabet letter or punctuation marks
                            if event.unicode in self.ALPHABET:
                                self.input_sentence += event.unicode
                                self.mode.draw_sentence(**self.__dict__)
                        except:
                            pass
            # checking whether the game has ended.
            if self.active and self.mode.check_end_game(**self.__dict__):
                self.end_game_time = time.time()
                self.end_test()

            pygame.display.update()

    def hover_fuc(self):
        """
        This function manages the hovering functionality and prints the relevant button's label.
        :return: None
        """
        if self.hover['repeat']:
            if self.end:
                self.draw_txt('Repeat test', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                              center_position=(self.REPEAT_POSITION[0] + 20, self.REPEAT_POSITION[1] + 50))
            else:
                self.draw_txt('Restart test', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                              center_position=(self.REPEAT_POSITION[0] + 20, self.REPEAT_POSITION[1] + 50))
        elif self.hover['next']:
            self.draw_txt('Next test', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                          center_position=(self.NEXT_POSITION[0] + 20, self.NEXT_POSITION[1] + 50))
        elif self.hover['sun']:
            self.draw_txt('Light theme', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                          center_position=(self.SUN_POSITION[0] + 20, self.SUN_POSITION[1] + 50))
        elif self.hover['moon']:
            self.draw_txt('Dark theme', super().BUTTONS_FONT_SIZE, self.theme.DEFAULT_TEXT_COLOR,
                          center_position=(self.MOON_POSITION[0], self.MOON_POSITION[1] + 50))

    def reset_game(self, randomize=True):
        """
        This function resets the game, it resets the relevant flags to prepare to new game, and generates a new
        sentence if randomize parameter is set to True.
        :param randomize: flag for generating a new sentence. if False, the sentence doesn't change.
        :return: None
        """
        self.start_time = 0
        self.timer = self.limit
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.SCREEN.fill(self.theme.BG_COLOR)
        self.hover['next'] = False

        # initializing sentence with new random words.
        if randomize:
            self.sentence = self.randomize_sentence()

        try:
            self.mode.print_from_line = 0
        except:
            pass

    def randomize_sentence(self):
        """
        generates a random sentence of the length of word_count the is determined by the user.
        gets the words_file from .txt file specified in the initialization of the game.
        :return: string - random sentence
        """
        word_count = self.mode.get_word_count()
        words_file = open(self.DATA_FILE_NAME)
        words = random.sample(list(words_file.readlines()), word_count)
        words = [word[:-1] for word in words]
        if self.punctuations:
            puncs = [self.PUNCTUATION_MARKS[random.randint(0, len(self.PUNCTUATION_MARKS) - 1)] for i in
                     range(0, int(word_count * 0.2))]
            for pun in puncs:
                ind = random.choice(range(0, word_count))
                words[ind] = words[ind] + pun
        if self.numbers:
            nums = [random.randint(0, 10) for i in range(0, int(word_count * 0.2))]
            for num in nums:
                ind = random.choice(range(0, word_count))
                words[ind] = words[ind] + str(num)
        delimiter = " "
        sentence = delimiter.join(words)
        words_file.close()
        return sentence

    def draw_txt(self, txt, txt_size, txt_color, left_corner=None, center_position=None, box_size=None, box_color=None):
        """
        Function for rendering the text on the screen.
        the position of the text can be either the top left corner or the center position.
        the text can be drawn with a box behind it, if the size and the color of the box are provided.
        :param txt: the text to be rendered.
        :param txt_size: Font size.
        :param txt_color: Font color.
        :param left_corner: the top left corner of the text rectangle. by default is set to None.
        :param center_position: the center position of the text rectangle. by default is set to None.
        :param box_size: the box size. by default None.
        :param box_color: the box color. by default None.
        :return: None
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
        """
        this funciton is called when the test has ended, it prints the results and resets the relevant flags to the
        end of the game.
        :return: None
        """
        self.SCREEN.fill(self.theme.BG_COLOR)
        self.end = True
        self.mode.draw_game(**self.__dict__)
        self.active = False
        self.mode.show_result(**self.__dict__)


# -----------------------------------------------------------------------------------------------------------------------

typing_game = SpeedTypingTest()
typing_game.play()
