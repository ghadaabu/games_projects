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
    AMARANTH = (229, 43, 80)
    AMARANTH_RED = (211, 33, 45)  # darker
    BITCOIN_ORANGE = (242, 169, 0)
    LIGHT_CYAN = (224, 255, 255)

    # using Google's font - RobotoMono-Regular font. https://fonts.google.com/specimen/IBM+Plex+Mono?query=mono
    FONT_TYPE = "RobotoMono-Regular.ttf"
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size
    FONT_SIZE = 24
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
        print(self.letter_width, self.row_len)

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
                        if len(self.input_sentence) >= len(self.sentence):
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


    def extend_sentence(self, original_sen, input_sen):
        original_words = original_sen.split(" ")
        input_words = input_sen.split(" ")
        extended_sen = ''
        for i, word in enumerate(original_words):
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
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        # origin is the position of the original text and font_height is the scaled height of the font in pixels
        font.origin = True
        font_height = font.get_sized_height()

        # taking the item in index 4 as the horizontal advance
        # to know how much space each letter takes during rendering
        M_ADV_X = 4
        text_surf_rect = font.get_rect(self.sentence + ' ')
        baseline = text_surf_rect.y
        text_surf_rect.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2 - 50)
        # creating a surface to render the text on and center it to the screen
        text_surf = pygame.Surface(text_surf_rect.size)

        text_surf.fill(self.BG_COLOR)
        current_h_adv = 0
        for ind, char in enumerate(self.input_sentence):
            if char == (self.sentence)[ind]:
                color = self.WHITE
            else:
                color = self.AMARANTH
            font.render_to(text_surf, (current_h_adv, baseline), char, color)
            current_h_adv += self.font_metrics[char][M_ADV_X]

        # saving the upper left corner position of the cursor
        cursor_position = (text_surf_rect.left + current_h_adv - 1, text_surf_rect.center[1] - 3)

        for char in self.sentence[len(self.input_sentence):]:
            color = self.BATTLESHIP_GRAY
            font.render_to(text_surf, (current_h_adv, baseline), char, color)
            current_h_adv += self.font_metrics[char][M_ADV_X]
        self.SCREEN.blit(text_surf, text_surf_rect)

        # adding cursor
        fontObj = pygame.font.Font(self.FONT_TYPE, self.FONT_SIZE + 10)
        # fontObj.set_bold(True)
        textSurfaceObj = fontObj.render('|', True, self.LIGHT_CYAN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = cursor_position
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
            correct_chars = 0
            for i, c in enumerate(self.sentence):
                try:
                    if self.input_sentence[i] == c:
                        correct_chars += 1
                except:
                    pass
            self.accuracy = correct_chars / len(self.sentence) * 100

            # Calculate speed (word per minute wpm)
            self.speed = len(self.input_sentence) * 60 / (5 * self.total_time)
            self.end = False

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
        self.SCREEN.blit(textSurfaceObj, (100, self.WINDOWHEIGHT / 2 + 40 + pos))
        # self.SCREEN.blit(textSurfaceObj, textRectObj)


SpeedTypeTest().run_game()
