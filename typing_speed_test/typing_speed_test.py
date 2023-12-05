import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype
from math import ceil


class SpeedTypeTest:
    WINDOWWIDTH = 1200  # 640  # size of window's width in pixels
    WINDOWHEIGHT = 800  # 480  # size of windows' height in pixels

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz| ,._!ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BATTLESHIP_GRAY = (132, 132, 130)
    BITCOIN_GRAY = (77, 77, 78)  # darker
    BLACK_COFFEE = (59, 47, 47)
    FATHOM_GREY = (41, 44, 51)
    AMARANTH = (211, 33, 45) #(229, 43, 80)
    AMARANTH_RED = (150, 27, 45)  # darker
    BITCOIN_ORANGE = (242, 169, 0)
    LIGHT_CYAN = (224, 255, 255)

    # using Google's font - RobotoMono-Regular font. https://fonts.google.com/specimen/IBM+Plex+Mono?query=mono
    FONT_TYPE = "RobotoMono-Regular.ttf"
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size
    FONT_SIZE = 20
    BG_COLOR = BITCOIN_GRAY
    MARGIN = 150
    letter_colors = {'r': WHITE, 'w': AMARANTH, 'e': AMARANTH_RED, 'n': BATTLESHIP_GRAY}
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
        self.end = False
        self.active = False
        self.reset = True
        self.running = False
        self.word_count = 10

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

        # Saving the sizes of all the letters in the english alphabet
        # this is needed in case the font is not monospace font
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        metrics = font.get_metrics(self.ALPHABET)
        # getting the sizes of all the letters in the english alphabet
        self.font_metrics = dict(zip(self.ALPHABET, metrics))
        self.letter_width = self.font_metrics['a'][4]
        self.row_len = self.WINDOWWIDTH - 2 * self.MARGIN
        # print(self.letter_width, self.row_len)

    def run_game(self):
        self.reset_game()
        while True:
            if self.reset:
                clock = pygame.time.Clock()
                self.SCREEN.fill(self.BG_COLOR)
                self.draw_game(self.SCREEN)
                self.draw_sentence(self.sentence, self.input_sentence, self.SCREEN)
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
                        # x, y = pygame.mouse.get_pos()

                    # checking if user selected new word count
                    elif self.word_count_box_size[1] <= y <= self.word_count_box_size[1] + self.word_count_box_size[3]:
                        if self.word_count_box_size[0] <= x <= self.word_count_box_size[0] + self.word_count_box_size[2] \
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
                        # x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                    if self.running and not self.active:
                        self.start_time = time.time()
                        self.active = True
                    # if event.key == pygame.K_RETURN and len(self.input_sentence) == len(self.sentence):
                    #     self.running = False
                    if event.key == pygame.K_BACKSPACE:
                        self.input_sentence = self.input_sentence[:-1]
                    elif self.active and not self.end:
                        # print(len(self.input_sentence), len(self.sentence), self.sentence, "   ", self.input_sentence)
                        try:
                            # checks if the entered key is an alphabet letter or punctuation marks
                            if event.unicode in self.ALPHABET:

                                self.input_sentence += event.unicode
                                self.draw_sentence(self.sentence, self.input_sentence, self.SCREEN)
                        except:
                            pass
                        # checking if the test ended where all the letters are entered
                        input_words = self.input_sentence.split(' ')
                        if len(input_words) >= self.word_count and len(input_words[-1]) >= len(self.sentence.split(' ')[-1]):
                            self.SCREEN.fill(self.BG_COLOR)
                            self.draw_game(self.SCREEN)
                            self.draw_sentence(self.sentence, self.input_sentence, self.SCREEN)
                            self.active = False
                            self.end = True
                            self.show_result()
                            self.reset = False
                            # self.reset_game()

            pygame.display.update()
        clock.tick(60)

    def get_sentence(self):
        # returns a random sentence from sentences file
        sentences = open("sentences_1.txt")
        sentence = random.choice(list(sentences.readlines()))
        sentences.close()
        return sentence[:-1]

    def randomize_sentence(self):
        # returns a random sentence from sentences file
        words = open("wordlist.10000.txt")  # https://www.mit.edu/~ecprice/wordlist.10000 link to file
        sentence = random.sample(list(words.readlines()), self.word_count)
        sentence = [word[:-1] for word in sentence]
        delimiter = " "
        sentence = delimiter.join(sentence)
        words.close()
        return sentence


    def draw_sentence(self, original_sen, input_sen, screen):
        # font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        # # origin is the position of the original text and font_height is the scaled height of the font in pixels
        # font.origin = True

        lines_spacing = 50
        line_ind = 0
        sentence_words = self.sentence.split(' ')
        # print(sentence_words)
        input_sen_words = self.input_sentence.split(' ')
        current_h_adv = 900

        for i, word in enumerate(sentence_words):
            in_word = input_sen_words[i] if i < len(input_sen_words) else ''
            # check if there is space left on the current line
            if max(len(word), len(in_word)) * self.letter_width + current_h_adv > self.row_len:
                if line_ind != 0:
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
            if i == len(input_sen_words) - 1:  # the word to the cursor position
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

        # adding cursor
        if cursor_x != None and cursor_y != None:
            fontObj = pygame.font.Font(self.FONT_TYPE, self.FONT_SIZE + 10)
            # fontObj.set_bold(True)
            textSurfaceObj = fontObj.render('|', True, self.LIGHT_CYAN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (cursor_x, cursor_y)
            self.SCREEN.blit(textSurfaceObj, textRectObj)

    def split_sentence_into_rows(self, sentence, letter_size, max_row_len):
        # splits the sentence into rows of maximum row_size and returns a list of strings - the rows

        rows_num = len(sentence) * letter_size / max_row_len
        print(rows_num)
        if ceil(rows_num) <= 1:
            return [sentence]

        rows = ['']
        words = sentence.split(' ')
        row_ind = 0
        for word in words:
            if (len(rows[row_ind]) + len(word)) * letter_size <= max_row_len:
                rows[row_ind] = rows[row_ind] + word
            else:  # the row is full - starting a new row
                row_ind += 1
                rows = rows + [word]
            if (len(rows[row_ind]) + 1) * letter_size <= max_row_len:
                rows[row_ind] = rows[row_ind] + ' '
        return rows

    def reset_game(self):
        self.start_time = 0
        self.input_sentence = ''
        self.end = False
        self.active = False
        self.reset = True
        # self.running = False
        self.SCREEN.fill(self.BG_COLOR)

        # initializing sentence by getting a random new one
        # self.sentence = self.get_sentence()
        self.sentence = self.randomize_sentence()
        print(self.sentence)

    def draw_game(self, screen):
        # drawing the reset button
        self.draw_box_with_txt((self.WINDOWWIDTH / 2, self.WINDOWHEIGHT - 45), self.reset_box_size, 'Reset', 12,
                               self.BATTLESHIP_GRAY, self.WHITE, screen)
        txt_pos = (self.MARGIN, self.word_count_box_size[1] + self.word_count_box_size[2] / 2)
        self.draw_txt(txt_pos, 'Word count:', 16, self.WHITE, screen)
        # drawing the word count buttons
        for count in range(10, 40, 10):
            pos_shift = self.boxes_shift * (count / 10 - 1)
            center_position = (self.word_count_box_size[0] + pos_shift + self.word_count_box_size[2] / 2,
                               self.word_count_box_size[1] + self.word_count_box_size[2] / 2)

            self.draw_txt(center_position, str(count), 16, self.WHITE, screen)

    def draw_box_with_txt(self, center_position, box_size, txt, txt_size, box_color, txt_color, screen):
        """
        # this funtion renders a box with text.
        :param center_position: the center position of the box
        :param box_size: box size
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param box_color: the color of the box
        :param txt_color: the color of the text
        :param screen: the screen to blit the objects to
        """
        pygame.draw.rect(screen, box_color, box_size)
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = center_position
        screen.blit(textSurfaceObj, textRectObj)

    def draw_txt(self, center_position, txt, txt_size, txt_color, screen):
        """
        # this funtion renders text.
        :param center_position: the center position of the box
        :param txt: the text to be rendered
        :param txt_size: the size of the font
        :param txt_color: the color of the text
        :param screen: the screen to blit the objects to
        """
        fontObj = pygame.font.Font(self.FONT_TYPE, txt_size)
        textSurfaceObj = fontObj.render(txt, True, txt_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = center_position
        screen.blit(textSurfaceObj, textRectObj)

    def show_result(self):
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
                self.print_results_text(txt, ind * 40)
            pygame.display.update()

    def print_results_text(self, text, pos):
        fontObj = pygame.font.Font(self.FONT_TYPE, 20)
        textSurfaceObj = fontObj.render(text, True, self.BITCOIN_ORANGE)
        # textRectObj = textSurfaceObj.get_rect()
        # textRectObj.center = (self.WINDOWWIDTH/2, self.WINDOWHEIGHT/2 + pos)
        self.SCREEN.blit(textSurfaceObj, (100, self.WINDOWHEIGHT / 2 + 100 + pos))
        # self.SCREEN.blit(textSurfaceObj, textRectObj)


SpeedTypeTest().run_game()
