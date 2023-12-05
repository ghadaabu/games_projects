import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype
from math import ceil


class SpeedTypeTest:
    WINDOWWIDTH = 1200  # 640  # size of window's width in pixels
    WINDOWHEIGHT = 800  # 480  # size of windows' height in pixels

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz| ,._!ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # set up the colors
    BLACK =           (  0,   0,   0)
    WHITE =           (255, 255, 255)
    BATTLESHIP_GRAY = (132, 132, 130)
    BITCOIN_GRAY =    ( 77,  77,  78)  # darker
    BLACK_COFFEE =    ( 59,  47,  47)
    FATHOM_GREY =     ( 41,  44,  51)
    AMARANTH =        (211,  33,  45)
    AMARANTH_RED =    (150,  27,  45)  # darker
    BITCOIN_ORANGE =  (242, 169,   0)
    LIGHT_CYAN =      (224, 255, 255)

    # using Google's font - RobotoMono-Regular font. https://fonts.google.com/specimen/IBM+Plex+Mono?query=mono
    FONT_TYPE = "RobotoMono-Regular.ttf"
    # https://www.mit.edu/~ecprice/wordlist.10000 link to data file
    DATA_FILE_NAME = "wordlist.10000.txt"
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size

    FONT_SIZE = 20
    BG_COLOR = BITCOIN_GRAY
    MARGIN = 150

    reset_box_size = (WINDOWWIDTH / 2 - 30, WINDOWHEIGHT - 60, 60, 30)
    word_count_box_size = (220, 100, 30, 30)  # (x_top_left_corner, y_top,-left, width, height)
    boxes_shift = 40  # the space between the options

    def __init__(self):
        self.start_time = 0
        self.total_time = 0
        self.accuracy = 0
        self.speed = 0
        self.sentence = ''
        self.input_sentence = ''
        self.word_count = 10 # setting the default word count to 10 words

        self.running = False # states whether the user is on the screen of the game
        self.active = False # states whether the user started the test
        self.end = False # states whether the test ended
        self.update_screen = True # states whether to update the screen's display

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

    def run_game(self):
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
                    elif self.reset_box_size[0] <= x <= self.reset_box_size[0] + self.reset_box_size[2] \
                            and self.reset_box_size[1] <= y <= self.reset_box_size[1] + self.reset_box_size[3]:
                        self.reset_game()

                    # checking if the user selected new word count
                    elif self.word_count_box_size[1] <= y <= self.word_count_box_size[1] + self.word_count_box_size[3]:
                        if self.word_count_box_size[0] <= x <= self.word_count_box_size[0] + self.word_count_box_size[2]\
                                and self.word_count != 10:
                            self.word_count = 10
                            self.reset_game()
                        elif self.word_count_box_size[0] <= x - self.boxes_shift <= self.word_count_box_size[0] + \
                                self.word_count_box_size[2] and self.word_count != 20:
                            self.word_count = 20
                            self.reset_game()
                        elif self.word_count_box_size[0] <= x - 2 * self.boxes_shift <= self.word_count_box_size[0] + \
                                self.word_count_box_size[2] and self.word_count != 30:
                            self.word_count = 30
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
                        if len(input_words) >= self.word_count and len(input_words[-1]) >= len(
                                self.sentence.split(' ')[-1]):
                            self.SCREEN.fill(self.BG_COLOR)
                            self.draw_game()
                            self.draw_sentence()
                            self.active = False
                            self.end = True
                            self.show_result()
                            self.update_screen = False

            pygame.display.update()
        clock.tick(60)

    def randomize_sentence(self):
        """
        generates a random sentence of the length of word_count the is determined by the user.
        gets the words from .txt file specified in the initialization of the game.
        :return: string - random sentence
        """
        words = open(self.DATA_FILE_NAME)
        sentence = random.sample(list(words.readlines()), self.word_count)
        sentence = [word[:-1] for word in sentence]
        delimiter = " "
        sentence = delimiter.join(sentence)
        words.close()
        return sentence

    def draw_sentence(self):
        """
        Function that draws the sentence on the screen, it colors the letters with different colors based on the
        accuracy of the entered words where:
        - correct entered letter: white
        - wrong entered letter: Red
        - extra entered letter: dark red
        - not entered yet: light grey
        It also draws a cursor where the next letter to be entered.
        :return: None
        """
        lines_spacing = 50
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
                if line_ind != 0:  # if line is the first, no need to blit the surface to the screen
                    self.SCREEN.blit(text_surf, text_surf_rect)
                font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
                # origin is the position of the original text and font_height is the scaled height of the font in pixels
                font.origin = True
                text_surf_rect = font.get_rect(self.ALPHABET + '                         ')  # (x,y,w,h)
                baseline = text_surf_rect.y
                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.topleft = (self.MARGIN - 50, self.WINDOWHEIGHT // 2 - 100 + lines_spacing * line_ind)
                text_surf.fill(self.BG_COLOR)
                current_h_adv = 0
                line_ind += 1

            if i == len(input_sen_words) - 1:  # setting the cursor position
                cursor_y = text_surf_rect.y
                cursor_x = self.MARGIN - 50 + current_h_adv + len(in_word) * self.letter_width

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
            textSurfaceObj = fontObj.render('|', True, self.LIGHT_CYAN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y)
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
        self.draw_box_with_txt((self.WINDOWWIDTH / 2, self.WINDOWHEIGHT - 45), self.reset_box_size, 'Reset', 12,
                               self.BATTLESHIP_GRAY, self.WHITE)
        txt_pos = (self.MARGIN, self.word_count_box_size[1] + self.word_count_box_size[2] / 2)
        self.draw_txt('Word count:', 16, self.WHITE, center_position=txt_pos)

        # drawing the word count buttons
        for count in range(10, 40, 10):
            pos_shift = self.boxes_shift * (count / 10 - 1)
            center_position = (self.word_count_box_size[0] + pos_shift + self.word_count_box_size[2] / 2,
                               self.word_count_box_size[1] + self.word_count_box_size[2] / 2)

            self.draw_txt(str(count), 16, self.WHITE, center_position=center_position)

    def draw_box_with_txt(self, center_position, box_size, txt, txt_size, box_color, txt_color):
        """
        # this funtion renders a box with text.
        :param center_position: the center position of the box
        :param box_size: box size
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param box_color: the color of the box
        :param txt_color: the color of the text
        """
        pygame.draw.rect(self.SCREEN, box_color, box_size)
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = center_position
        self.SCREEN.blit(textSurfaceObj, textRectObj)

    def draw_txt(self, txt, txt_size, txt_color, left_corner=None, center_position=None):
        """
        # this funtion renders text.
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param txt_color: the color of the text
        :param left_corner: the left corner position of the box, default None
        :param center_position: the center position of the box, default None
        """
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

            results = [f'Total time: {self.total_time:.2f} secs',
                       f'Accuracy: {self.accuracy:.2f} %',
                       f'Typing speed: {ceil(self.speed)} wpm']
            for ind, txt in enumerate(results):
                self.draw_txt(txt, self.FONT_SIZE, self.BITCOIN_ORANGE, left_corner=(100, self.WINDOWHEIGHT / 2 + 100 + ind * 40))
                # self.print_results_text(txt, ind * 40, self.FONT_SIZE)
            pygame.display.update()


SpeedTypeTest().run_game()
