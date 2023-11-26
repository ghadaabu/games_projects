import pygame, sys, time, random
from pygame.locals import *
import pygame.freetype


class SpeedTypeTest:
    WINDOWWIDTH = 1000#640  # size of window's width in pixels
    WINDOWHEIGHT = 700#480  # size of windows' height in pixels

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

    FONT_TYPE = "RobotoMono-Regular.ttf" # using Google's font - RobotoMono-Regular font
    # the purpose of using a monospace font is to deal with wrong typed letters so the text surface won't change size
    FONT_SIZE = 24
    BG_COLOR = BITCOIN_GRAY
    letter_colors = {'r': WHITE, 'w': AMARANTH, 'e': AMARANTH_RED, 'n': BATTLESHIP_GRAY}
    reset_box_size = (WINDOWWIDTH/2-30, WINDOWHEIGHT-60, 60, 30)
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
        self.words_number = 6

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('Type Speed Test')

        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        alphabet = 'abcdefghijklmnopqrstuvwxyz| ,._!ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        metrics = font.get_metrics(alphabet)
        # getting the sizes of all the letters in the english alphabet
        self.font_metrics = dict(zip(alphabet, metrics))


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
                    if self.reset_box_size[0] <= x <= self.reset_box_size[0]+self.reset_box_size[2] \
                        and self.reset_box_size[1] <= y <= self.reset_box_size[1] + self.reset_box_size[3]:
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()

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
                            self.input_sentence += event.unicode
                            self.draw_sentence(self.sentence, self.input_sentence, self.SCREEN)


                        except:
                            pass

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
        words = open("wordlist.10000.txt")
        sentence = random.sample(list(words.readlines()), self.words_number)
        sentence = [word[:-1] for word in sentence]
        delimiter = " "
        sentence = delimiter.join(sentence)
        words.close()
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
        font = pygame.freetype.Font(self.FONT_TYPE, self.FONT_SIZE)
        # origin is the position of the original text and font_height is the scaled height of the font in pixels
        font.origin = True
        font_height = font.get_sized_height()

        # taking the item in index 4 as the horizontal advance
        # to know how much space each letter takes during rendering
        M_ADV_X = 4
        text_surf_rect = font.get_rect(self.sentence+' ')
        baseline = text_surf_rect.y
        text_surf_rect.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2 - 50)
        # creating a surface to render the text on and center it to the screen
        text_surf = pygame.Surface(text_surf_rect.size)

        text_surf.fill(self.BG_COLOR)
        # print("....")
        current_h_adv = 0
        for ind, char in enumerate(self.input_sentence):
            if char == (self.sentence)[ind]:
                color = self.WHITE
            else:
                color = self.AMARANTH
            font.render_to(text_surf, (current_h_adv, baseline), char, color)
            current_h_adv += self.font_metrics[char][M_ADV_X]

        # saving the upper left corner position of the cursor
        cursor_position = (text_surf_rect.left + current_h_adv - 1, text_surf_rect.center[1]-3)



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

        # textRectObj = font.get_rect('|')  # taking into account the cursor
        # textRectObj.center = cursor_position
        #
        # textSurfaceObj = pygame.Surface(textRectObj.size)
        # textSurfaceObj.fill(self.BG_COLOR)
        # font.render_to(textSurfaceObj, cursor_position, '|', self.LIGHT_CYAN)
        # self.SCREEN.blit(textSurfaceObj, textRectObj)

        # pygame.display.flip()



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
        pygame.draw.rect(screen, self.BATTLESHIP_GRAY, self.reset_box_size)
        fontObj = pygame.font.Font(None, 18)
        textSurfaceObj = fontObj.render('Reset', True, self.WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT - 45)
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

            results = [f'Total time: {self.total_time:.2f}  secs',\
                       f'Accuracy: {self.accuracy:.2f}  %',
                       f'Typing speed: {self.speed:.2f}  wpm']
            for ind, txt in enumerate(results):
                self.print_text(txt, ind*40)
            pygame.display.update()



    def print_text(self, text, pos):
        fontObj = pygame.font.Font(self.FONT_TYPE, 20)
        textSurfaceObj = fontObj.render(text, True, self.BITCOIN_ORANGE)
        # textRectObj = textSurfaceObj.get_rect()
        # textRectObj.center = (self.WINDOWWIDTH/2, self.WINDOWHEIGHT/2 + pos)
        self.SCREEN.blit(textSurfaceObj, (100, self.WINDOWHEIGHT/2 + 40 + pos))
        # self.SCREEN.blit(textSurfaceObj, textRectObj)

SpeedTypeTest().run_game()

