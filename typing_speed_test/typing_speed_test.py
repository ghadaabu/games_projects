import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype
from math import ceil


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

    TEXT_COLOR = {'dark': WHITE, 'light': BLACK}
    # BG_COLOR = {'dark': BITCOIN_GRAY, 'light': WHITE}
    BG_COLOR = BITCOIN_GRAY

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


# -------------------------- WordsMode ---------------------------------------------------------------------------------

class WordsMode(Constants):
    def __init__(self):
        self.start_time = 0
        self.total_time = 0
        self.accuracy = 0
        self.speed = 0
        self.sentence = ''
        self.input_sentence = ''
        self.word_count = 10  # setting the default word count to 10 words_file

        self.running = False  # states whether the user is on the screen of the game
        self.active = False  # states whether the user started the test
        self.end = False  # states whether the test ended
        self.update_screen = True  # states whether to update the screen's display
        self.numbers = False  # if True, the test will have numbers
        self.punctuations = False  # if True, the test will have punctuation marks

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

        # Saving the sizes of all the letters in the english alphabet
        # Note: In case you choose to use a font that is not a monospace font, you will need to use font_metric for the
        # calculation of the space each letter takes (for each letter it is stored in index 4 of the tuple)
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        metrics = font.get_metrics(self.ALPHABET)
        # getting the sizes of all the letters in the english alphabet
        self.font_metrics = dict(zip(self.ALPHABET, metrics))
        # Since I use monospace font, all the letters have the same horizontal size
        self.letter_width = self.font_metrics['a'][4]
        self.row_len = self.WINDOWWIDTH - 2 * self.MARGIN

        # (x_top_left_corner, y_top_left, width, height)
        self.MENU_BAR_ELEMENTS = {'Words': (self.MARGIN, self.MARGIN, len("Words") * self.letter_width, 30),
                                  'Time': (self.MARGIN + 76, self.MARGIN, len("Time") * self.letter_width, 30),
                                  '10': (self.MARGIN + 141, self.MARGIN, 30, 30),
                                  '20': (self.MARGIN + 173, self.MARGIN, 30, 30),
                                  '30': (self.MARGIN + 205, self.MARGIN, 30, 30),
                                  'Numbers': (self.MARGIN + 258, self.MARGIN, len("Numbers") * self.letter_width, 30),
                                  'Punctuation': (
                                      self.MARGIN + 356, self.MARGIN, len("Punctuation") * self.letter_width, 30)}

    def run_game(self, theme):
        self.reset_game()
        while True:
            if self.update_screen:
                # clock = pygame.time.Clock()
                self.SCREEN.fill(self.BG_COLOR)
                self.draw_game()
                self.draw_sentence()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # pressed anywhere on the screen
                    if 0 <= x <= self.WINDOWWIDTH and 0 <= y <= self.WINDOWHEIGHT and not self.running:
                        self.running = True

                    # position of reset box
                    elif self.RESET_BOX_SIZE[0] <= x <= self.RESET_BOX_SIZE[0] + self.RESET_BOX_SIZE[2] \
                            and self.RESET_BOX_SIZE[1] <= y <= self.RESET_BOX_SIZE[1] + self.RESET_BOX_SIZE[3]:
                        self.reset_game()

                    # checking if the user pressed on a key from the menu bar
                    elif self.MENU_BAR_ELEMENTS['Words'][1] <= y <= self.MENU_BAR_ELEMENTS['Words'][1] + \
                            self.MENU_BAR_ELEMENTS['Words'][3]:
                        # check if Time mode is selected
                        if self.MENU_BAR_ELEMENTS['Time'][0] <= x <= self.MENU_BAR_ELEMENTS['Time'][0] + \
                                self.MENU_BAR_ELEMENTS['Time'][2]:
                            return False, theme
                        # check if word count is selected
                        elif self.MENU_BAR_ELEMENTS['10'][0] <= x <= self.MENU_BAR_ELEMENTS['10'][0] + \
                                self.MENU_BAR_ELEMENTS['10'][2] \
                                and self.word_count != 10:
                            self.word_count = 10
                            self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['20'][0] <= x <= self.MENU_BAR_ELEMENTS['20'][0] + \
                                self.MENU_BAR_ELEMENTS['20'][2] \
                                and self.word_count != 20:
                            self.word_count = 20
                            self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['30'][0] <= x <= self.MENU_BAR_ELEMENTS['30'][0] + \
                                self.MENU_BAR_ELEMENTS['30'][2] \
                                and self.word_count != 30:
                            self.word_count = 30
                            self.reset_game()
                        # check if Numbers is selected
                        elif self.MENU_BAR_ELEMENTS['Numbers'][0] <= x <= self.MENU_BAR_ELEMENTS['Numbers'][0] + \
                                self.MENU_BAR_ELEMENTS['Numbers'][2]:
                            self.numbers = not self.numbers
                            self.reset_game()
                        # check if Punctuation is selected
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
                                self.draw_sentence()
                        except:
                            pass
                        # checking if the test ended where all the letters are entered
                        input_words = self.input_sentence.split(' ')
                        if len(input_words) >= self.word_count:
                                # and len(input_words[-1]) >= len(
                                # self.sentence.split(' ')[-1]):
                            self.SCREEN.fill(self.BG_COLOR)
                            self.draw_game()
                            # self.draw_sentence()
                            self.active = False
                            self.end = True
                            self.show_result()
                            self.update_screen = False

            pygame.display.update()
        clock.tick(60)

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
            puncs = [self.PUNCTUATION_MARKS[random.randint(0, len(self.PUNCTUATION_MARKS) - 1)] for i in
                     range(0, int(self.word_count * 0.2))]
            for pun in puncs:
                ind = random.choice(range(0, self.word_count))
                words[ind] = words[ind] + pun
        if self.numbers:
            nums = random.sample(range(0, 10), int(self.word_count * 0.2))
            for num in nums:
                ind = random.choice(range(0, self.word_count))
                words[ind] = words[ind] + str(num)
        delimiter = " "
        sentence = delimiter.join(words)
        words_file.close()
        return sentence

    def draw_sentence(self):
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
        self.LINES_SPACING = 50
        line_ind = 0
        sentence_words = self.sentence.split(' ')
        input_sen_words = self.input_sentence.split(' ')
        current_h_adv = 900

        cursor_x = None
        cursor_y = None

        # # if the test has started, draws the word-counter above the sentence
        # if self.active:
        #     self.draw_txt(f'{len(input_sen_words) - 1} / {self.word_count}', self.FONT_SIZE, self.BITCOIN_ORANGE,
        #                   left_corner=self.TIMER_POSITION)

        for i, word in enumerate(sentence_words):
            in_word = input_sen_words[i] if i < len(input_sen_words) else ''
            # check if there is enough space left on the current line for the current word, if not creates a new line.
            if max(len(word), len(in_word)) * self.letter_width + current_h_adv > self.row_len:
                if line_ind != 0:  # if line is the first, no need to blit the surface to the screen
                    self.SCREEN.blit(text_surf, text_surf_rect)
                font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.ALPHABET + self.ALPHABET)  # (x,y,w,h)
                # text_surf_rect = font.get_rect(self.ALPHABET + '                         ')  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.topleft = (self.MARGIN, self.WINDOWHEIGHT // 2 - 100 + self.LINES_SPACING * line_ind)
                text_surf.fill(self.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.MARGIN + current_h_adv + len(in_word) * self.letter_width

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = self.WHITE
                else:
                    color = self.AMARANTH
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += self.letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.AMARANTH_RED)
                    current_h_adv += self.letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.BATTLESHIP_GRAY)
                    current_h_adv += self.letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', self.BATTLESHIP_GRAY)
            current_h_adv += self.letter_width
            self.SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(self.FONT_TYPE, self.FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, self.BITCOIN_ORANGE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            self.SCREEN.blit(textSurfaceObj, textRectObj)

    def reset_game(self):
        """
        Function to reset the game, resets the relevant flags to prepare to new game, and generates a new sentence
        :return: None
        """
        self.start_time = 0
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.update_screen = True
        self.SCREEN.fill(self.BG_COLOR)

        # initializing sentence by getting a random new one
        self.sentence = self.randomize_sentence()

    def draw_game(self):
        """
        Function that draws the game, it draws the reset button and the word count buttons.
        :return: None
        """
        # drawing the reset button
        spacing = 10
        pos_shift = 8
        center_position = (self.RESET_BOX_SIZE[0] + self.RESET_BOX_SIZE[2] / 2,
                           self.RESET_BOX_SIZE[1] + self.RESET_BOX_SIZE[3] / 2)
        self.draw_txt('Reset', self.BUTTONS_FONT_SIZE, self.WHITE,
                      center_position=center_position,
                      box_size=self.RESET_BOX_SIZE, box_color=self.BATTLESHIP_GRAY)

        # Drawing the menu bar
        pos = (self.MENU_BAR_ELEMENTS['Words'][0], self.MENU_BAR_ELEMENTS['Words'][1])
        self.draw_txt('Words', self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE, left_corner=pos)

        pos = (pos[0] + len('Words') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Time'][0], self.MENU_BAR_ELEMENTS['Time'][1])
        self.draw_txt('Time', self.BUTTONS_FONT_SIZE, self.WHITE, left_corner=pos)

        pos = (pos[0] + len('Time') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        for count in range(10, 40, 10):
            pos = (self.MENU_BAR_ELEMENTS[str(count)][0], self.MENU_BAR_ELEMENTS[str(count)][1])
            self.draw_txt(str(count), self.BUTTONS_FONT_SIZE,
                          self.BITCOIN_ORANGE if count == self.word_count else self.WHITE, left_corner=pos)

        pos = (pos[0] + len(str(count)) * self.letter_width + spacing, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        # drawing punctuation and numbers button
        pos = (self.MENU_BAR_ELEMENTS['Numbers'][0], self.MENU_BAR_ELEMENTS['Numbers'][1])
        self.draw_txt("Numbers", self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE if self.numbers else self.WHITE,
                      left_corner=pos)

        pos = (pos[0] + len('Numbers') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Punctuation'][0], self.MENU_BAR_ELEMENTS['Punctuation'][1])
        self.draw_txt("Punctuation", self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE if self.punctuations else self.WHITE,
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
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            self.SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            self.SCREEN.blit(textSurfaceObj, left_corner)

    def show_result(self):
        """
        Function that draws the results on the screen, it first, calculates the results:
        - total time
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :return: None
        """
        if self.end:
            # total time calculation
            self.total_time = time.time() - self.start_time

            # Calculate accuracy
            correct_chars = self.word_count - 1  # counting the spaces
            sentence_words = self.sentence.split(' ')
            input_sen_words = self.input_sentence.split(' ')
            for i, word in enumerate(sentence_words):
                for j, c in enumerate(word):
                    try:
                        if c == input_sen_words[i][j]:
                            correct_chars += 1
                    except:
                        pass
            self.accuracy = correct_chars / len(self.sentence) * 100

            # Calculate speed (word per minute wpm)
            self.speed = len(self.input_sentence) * 60 / (5 * self.total_time)

            if len(self.input_sentence) < 0.5 * len(self.sentence):
                self.accuracy = 'NA'
            results = [f'Total time: {self.total_time:.2f} secs',
                       f'Accuracy: {self.accuracy:.2f} %' if self.accuracy != 'NA' else f'Accuracy: {self.accuracy}',
                       f'Typing speed: {ceil(self.speed)} wpm']
            for ind, txt in enumerate(results):
                self.draw_txt(txt, self.FONT_SIZE, self.BITCOIN_ORANGE,
                              left_corner=(100, self.WINDOWHEIGHT / 2 + ind * 40))
                # self.print_results_text(txt, ind * 40, self.FONT_SIZE)
            pygame.display.update()


# -------------------------- TimeMode ----------------------------------------------------------------------------------
class TimeMode(Constants):
    def __init__(self):
        self.start_time = 0
        self.accuracy = 0
        self.speed = 0
        self.sentence = ''
        self.input_sentence = ''
        self.time_limit = 15  # setting the default time limit to 15 secs
        self.word_count = int(300 * self.time_limit / 60)
        self.running = False  # states whether the user is on the screen of the game
        self.active = False  # states whether the user started the test
        self.end = False  # states whether the test ended
        self.update_screen = True  # states whether to update the screen's display
        self.numbers = False  # if True, the test will have numbers
        self.punctuations = False  # if True, the test will have punctuation marks
        self.timer = self.time_limit
        self.print_from_line = 0

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

        # Saving the sizes of all the letters in the english alphabet
        # Note: In case you choose to use a font that is not a monospace font, you will need to use font_metric for the
        # calculation of the space each letter takes (for each letter it is stored in index 4 of the tuple)
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        metrics = font.get_metrics(self.ALPHABET)
        # getting the sizes of all the letters in the english alphabet
        self.font_metrics = dict(zip(self.ALPHABET, metrics))
        # Since I use monospace font, all the letters have the same horizontal size
        self.letter_width = self.font_metrics['a'][4]
        self.row_len = self.WINDOWWIDTH - 2 * self.MARGIN

        # (x_top_left_corner, y_top_left, width, height)
        self.MENU_BAR_ELEMENTS = {'Words': (self.MARGIN, self.MARGIN, len("Words") * self.letter_width, 30),
                                  'Time': (self.MARGIN + 76, self.MARGIN, len("Time") * self.letter_width, 30),
                                  '15': (self.MARGIN + 141, self.MARGIN, 30, 30),
                                  '30': (self.MARGIN + 173, self.MARGIN, 30, 30),
                                  '60': (self.MARGIN + 205, self.MARGIN, 30, 30),
                                  'Numbers': (self.MARGIN + 258, self.MARGIN, len("Numbers") * self.letter_width, 30),
                                  'Punctuation': (
                                      self.MARGIN + 356, self.MARGIN, len("Punctuation") * self.letter_width, 30)}

    def run_game(self, theme):
        self.reset_game()
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)

        while True:
            if self.update_screen:
                # clock = pygame.time.Clock()
                self.SCREEN.fill(self.BG_COLOR)
                self.draw_game()
                self.update_timer()
                self.draw_sentence()
                pygame.display.update()

            for event in pygame.event.get():
                if time.time() >= self.start_time + self.time_limit and self.active:
                    self.SCREEN.fill(self.BG_COLOR)
                    self.draw_game()
                    self.active = False
                    self.end = True
                    self.show_result()
                    self.update_screen = False
                if event.type == TIMEREVENT and self.active:
                    self.timer -= 1
                    self.update_timer()

                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # pressed anywhere on the screen
                    if 0 <= x <= self.WINDOWWIDTH and 0 <= y <= self.WINDOWHEIGHT and not self.running:
                        self.running = True

                    # position of reset box
                    elif self.RESET_BOX_SIZE[0] <= x <= self.RESET_BOX_SIZE[0] + self.RESET_BOX_SIZE[2] \
                            and self.RESET_BOX_SIZE[1] <= y <= self.RESET_BOX_SIZE[1] + self.RESET_BOX_SIZE[3]:
                        self.reset_game()

                    # checking if the user pressed on a key from the menu bar
                    elif self.MENU_BAR_ELEMENTS['Words'][1] <= y <= self.MENU_BAR_ELEMENTS['Words'][1] + \
                            self.MENU_BAR_ELEMENTS['Words'][3]:
                        # check if Time mode is selected
                        if self.MENU_BAR_ELEMENTS['Words'][0] <= x <= self.MENU_BAR_ELEMENTS['Words'][0] + \
                                self.MENU_BAR_ELEMENTS['Words'][2]:
                            return True, theme
                        # check if word count is selected
                        elif self.MENU_BAR_ELEMENTS['15'][0] <= x <= self.MENU_BAR_ELEMENTS['15'][0] + \
                                self.MENU_BAR_ELEMENTS['15'][2] \
                                and self.time_limit != 15:
                            self.word_count = int(300 * 15 / 60)
                            self.time_limit = 15
                            self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['30'][0] <= x <= self.MENU_BAR_ELEMENTS['30'][0] + \
                                self.MENU_BAR_ELEMENTS['30'][2] \
                                and self.time_limit != 30:
                            self.word_count = int(300 * 15 / 60)
                            self.time_limit = 30
                            self.reset_game()
                        elif self.MENU_BAR_ELEMENTS['60'][0] <= x <= self.MENU_BAR_ELEMENTS['60'][0] + \
                                self.MENU_BAR_ELEMENTS['60'][2] \
                                and self.time_limit != 60:
                            self.word_count = int(300 * 15 / 60)
                            self.time_limit = 60
                            self.reset_game()
                        # check if Numbers is selected
                        elif self.MENU_BAR_ELEMENTS['Numbers'][0] <= x <= self.MENU_BAR_ELEMENTS['Numbers'][0] + \
                                self.MENU_BAR_ELEMENTS['Numbers'][2]:
                            self.numbers = not self.numbers
                            self.reset_game()
                        # check if Punctuation is selected
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
                                self.draw_sentence()
                        except:
                            pass
            pygame.display.update()
        clock.tick(60)

    def randomize_sentence(self):
        """
        generates a random sentence that's length mathces the time limit. the calculation is done as follows:
        word_count = 300*(time_limit/60sec)
        The function gets the words_file from a txt file specified in the initialization of the game.
        :return: string - random sentence
        """
        word_count = int(300 * self.time_limit / 60)
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

    def draw_sentence(self):
        line_ind = 0
        sentence_words = self.sentence.split(' ')
        input_sen_words = self.input_sentence.split(' ')
        current_h_adv = 900

        cursor_x = None
        cursor_y = None

        for i, word in enumerate(sentence_words):
            in_word = input_sen_words[i] if i < len(input_sen_words) else ''
            # check if there is enough space left on the current line for the current word, if not creates a new line.
            if max(len(word), len(in_word)) * self.letter_width + current_h_adv > self.row_len:
                if (self.print_from_line != 0 and line_ind > self.print_from_line + 3) or (
                        self.print_from_line == 0 and line_ind > self.print_from_line + 5):
                    break
                if self.print_from_line < line_ind <= self.print_from_line + 4:
                    self.SCREEN.blit(text_surf, text_surf_rect)

                font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.ALPHABET + self.ALPHABET)  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                shift = 1 if self.print_from_line > 0 else 0
                text_surf_rect.topleft = (self.MARGIN, self.WINDOWHEIGHT // 2 - 100 + self.LINES_SPACING * (
                        line_ind - self.print_from_line + shift))
                text_surf.fill(self.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.MARGIN + current_h_adv + len(in_word) * self.letter_width
                if line_ind >= self.print_from_line + 2:
                    self.print_from_line += 1

            for ind in range(min(len(word), len(in_word))):
                if word[ind] == in_word[ind]:
                    color = self.WHITE
                else:
                    color = self.AMARANTH
                font.render_to(text_surf, (current_h_adv, baseline), word[ind], color)
                current_h_adv += self.letter_width
            if len(word) < len(in_word):  # the user typed extra letters
                for letter in in_word[len(word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.AMARANTH_RED)
                    current_h_adv += self.letter_width
            elif len(word) > len(in_word):
                for letter in word[len(in_word):]:
                    font.render_to(text_surf, (current_h_adv, baseline), letter, self.BATTLESHIP_GRAY)
                    current_h_adv += self.letter_width
            # adding a space after the word
            font.render_to(text_surf, (current_h_adv, baseline), ' ', self.BATTLESHIP_GRAY)
            current_h_adv += self.letter_width
            if self.print_from_line <= line_ind <= self.print_from_line + 3:
                self.SCREEN.blit(text_surf, text_surf_rect)

        # drawing the cursor on the screen
        if cursor_x is not None and cursor_y is not None:
            fontObj = pygame.font.Font(self.FONT_TYPE, self.FONT_SIZE + 10)
            textSurfaceObj = fontObj.render('|', True, self.BITCOIN_ORANGE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y + 5)
            self.SCREEN.blit(textSurfaceObj, textRectObj)

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
        self.SCREEN.fill(self.BG_COLOR)
        self.print_from_line = 0

        # initializing sentence by getting a random new one
        self.sentence = self.randomize_sentence()

    def update_timer(self):
        # if the test has started, draws the count-down above the sentence
        if self.active:
            self.draw_txt(str(self.timer), self.FONT_SIZE, self.BITCOIN_ORANGE, left_corner=self.TIMER_POSITION)


    def draw_game(self):
        """
        Function that draws the game, it draws the reset button and the word count buttons.
        :return: None
        """
        # drawing the reset button
        spacing = 10
        pos_shift = 8
        center_position = (self.RESET_BOX_SIZE[0] + self.RESET_BOX_SIZE[2] / 2,
                           self.RESET_BOX_SIZE[1] + self.RESET_BOX_SIZE[3] / 2)
        self.draw_txt('Reset', self.BUTTONS_FONT_SIZE, self.WHITE,
                      center_position=center_position,
                      box_size=self.RESET_BOX_SIZE, box_color=self.BATTLESHIP_GRAY)

        # Drawing the menu bar
        pos = (self.MENU_BAR_ELEMENTS['Words'][0], self.MENU_BAR_ELEMENTS['Words'][1])
        self.draw_txt('Words', self.BUTTONS_FONT_SIZE, self.WHITE, left_corner=pos)

        pos = (pos[0] + len('Words') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Time'][0], self.MENU_BAR_ELEMENTS['Time'][1])
        self.draw_txt('Time', self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE, left_corner=pos)

        pos = (pos[0] + len('Time') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        for count in (15, 30, 60):
            pos = (self.MENU_BAR_ELEMENTS[str(count)][0], self.MENU_BAR_ELEMENTS[str(count)][1])
            self.draw_txt(str(count), self.BUTTONS_FONT_SIZE,
                          self.BITCOIN_ORANGE if count == self.time_limit else self.WHITE, left_corner=pos)

        pos = (pos[0] + len(str(count)) * self.letter_width + spacing, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        # drawing punctuation and numbers button
        pos = (self.MENU_BAR_ELEMENTS['Numbers'][0], self.MENU_BAR_ELEMENTS['Numbers'][1])
        self.draw_txt("Numbers", self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE if self.numbers else self.WHITE,
                      left_corner=pos)

        pos = (pos[0] + len('Numbers') * self.letter_width, pos[1])
        self.draw_txt('|', 24, self.WHITE, left_corner=(pos[0], pos[1] - pos_shift))

        pos = (self.MENU_BAR_ELEMENTS['Punctuation'][0], self.MENU_BAR_ELEMENTS['Punctuation'][1])
        self.draw_txt("Punctuation", self.BUTTONS_FONT_SIZE, self.BITCOIN_ORANGE if self.punctuations else self.WHITE,
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
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        if center_position is not None:
            textRectObj.center = center_position
            self.SCREEN.blit(textSurfaceObj, textRectObj)
        elif left_corner is not None:
            self.SCREEN.blit(textSurfaceObj, left_corner)

    def show_result(self):
        """
        Function that draws the results on the screen, it first, calculates the results:
        - total time
        - accuracy: #correct_letters / #total_letters * 100
        - typing speed (wpm): #total_letters / (5 * total_time) where 5 is based on the assumption that avg letter
          count in an english word is 5
        :return: None
        """
        if self.end:
            # Calculate accuracy
            sentence_words = self.sentence.split(' ')
            input_sen_words = self.input_sentence.split(' ')
            correct_chars = len(input_sen_words) - 1  # counting the spaces

            for i, word in enumerate(sentence_words):
                for j, c in enumerate(word):
                    try:
                        if c == input_sen_words[i][j]:
                            correct_chars += 1
                    except:
                        pass
            self.accuracy = correct_chars / len(self.sentence) * 100

            # Calculate speed (word per minute wpm)
            self.speed = len(self.input_sentence) * 60 / (5 * self.time_limit)


            results = [f'Total words: {len(input_sen_words)}',
                       f'Accuracy: {self.accuracy:.2f} %',
                       f'Typing speed: {ceil(self.speed)} wpm']
            for ind, txt in enumerate(results):
                self.draw_txt(txt, self.FONT_SIZE, self.BITCOIN_ORANGE,
                              left_corner=(100, self.WINDOWHEIGHT / 2 + ind * 40))
            pygame.display.update()


class SpeedTypingTest(Constants):
    def __init__(self):
        self.mode = False
        self.words_test = WordsMode()
        self.time_test = TimeMode()
        self.theme = 'Dark'  # theme is by default dark, can be changed to light

    def play(self):
        while True:
            if self.mode:
                self.mode, self.theme = self.words_test.run_game(self.theme)
            else:
                self.mode, self.theme = self.time_test.run_game(self.theme)


SpeedTypingTest().play()
