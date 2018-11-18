import numpy as np
import cv2
import time
import math
# from threading import Thread

uniform = np.random.uniform

info = dict()
info['balls_list'] = []
info['mouse_angle'] = 45


class Board:
    PARAMS = {'size': (1080, 1920),
              'cannon_size': 100,
              'wall0':  (0, 70, 1620, 75)
              }

    def __init__(self):
        # self.mouseclick = MouseClick()
        self.ball = []
        self.time_check = time.time()
        self.cannon_pos = [0, 100]
        self.cannon_pos_target = [0, 100]
        self.to_shoot = True
        self.max_balls = 200
        self.angle = 45 / 180 * np.pi
        self.angle_target = 45 / 180 * np.pi
        self.wall_thickness = 30
        self.board = np.zeros((Board.PARAMS['size'] + (3,)), dtype=np.uint8)
        self.empty()
        self.num = 0

    def run(self):
        cv2.namedWindow('Frame', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, 1)
        # cv2.setMouseCallback('Frame', self.mouseclick.record_click)
        global info
        while True:
            self.num += 1
            self.empty()

            # info['mouse_angle'] = self.mouseclick.angle
            self.updateball()
            self.drawball()
            if self.to_shoot:
                if self.num % 4 == 0:
                    self.shootball()

            self.draw_wall()
            self.get_cannon()
            # cv2.rectangle(self.board, (0, 0), (1920, 1080), (0, 128, 128), 15, cv2.LINE_AA)
            self.board = np.flipud(self.board).copy()

            cv2.imshow('Frame', self.board)
            self.key_pressed = cv2.waitKey(10)
            if self.key_pressed == 27:
                break
            elif self.key_pressed == 81:
                self.angle_target += 5 / 180 * np.pi
            elif self.key_pressed == 82:
                self.cannon_pos_target[1] += 50
            elif self.key_pressed == 83:
                self.angle_target -= 5 / 180 * np.pi
            elif self.key_pressed == 84:
                self.cannon_pos_target[1] -= 50
            elif self.key_pressed == ord('s'):
                self.to_shoot = not self.to_shoot
            if self.key_pressed != -1:
                print(self.key_pressed)

            if self.cannon_pos_target[1] == self.cannon_pos[1]:
                pass
            elif self.cannon_pos_target[1] > self.cannon_pos[1]:
                self.cannon_pos[1] += 4
            elif self.cannon_pos_target[1] < self.cannon_pos[1]:
                self.cannon_pos[1] -= 4
            if self.angle_target == self.angle:
                pass
            elif self.angle_target > self.angle:
                self.angle += 0.04
            elif self.angle_target < self.angle:
                self.angle -= 0.04

    def draw_wall(self):
        x0, y0, x1, y1 = Board.PARAMS['wall0']
        cv2.rectangle(self.board, (x0 - 10, y0 - 10), (x1 + 10, y1 + 10), (128, 128, 128), 15, cv2.LINE_AA)
        cv2.rectangle(self.board, (x0 - 10, y0 - 10), (x1 + 10, y1 + 10), (0, 0, 255), -1, cv2.LINE_AA)

    def empty(self):
        self.board = np.zeros((Board.PARAMS['size'] + (3,)), dtype=np.uint8)
        cv2.rectangle(self.board, (0, 0), (1920, 1080), (0, 128, 128), 15, cv2.LINE_AA)
        cv2.rectangle(self.board, (0, 0), (200, 50), (0, 0, 0), -1)

    def get_cannon(self):
        # try:
        #     m = ((self.cannon_pos[1] - self.mouseclick.pos[1])) / ((self.cannon_pos[0] - self.mouseclick.pos[0]))
        # except ZeroDivisionError:
        #     m = 999
        #
        # angle = math.atan(m)
        # self.mouseclick.angle = angle
        cv2.line(
            self.board,
            (self.cannon_pos[0], self.cannon_pos[1]),
            (self.cannon_pos[0] + int(Board.PARAMS['cannon_size'] * math.cos(self.angle)),
             self.cannon_pos[1] + int(Board.PARAMS['cannon_size'] * math.sin(self.angle))),
            (128, 0, 128), 30,
            cv2.LINE_8)

    def shootball(self):
        vx = 800 * math.cos(self.angle) * uniform(0.95, 1, 1)
        vy = 800 * math.sin(self.angle) * np.random.uniform(0.95, 1, 1)
        self.ball.append([
            self.random_colour(),
            [self.cannon_pos[0], self.cannon_pos[1]],
            [vx, vy],
            True
        ])

    def drawball(self):
        if not self.ball == []:
            for ball_coluor, ball_pos, _, to_draw in self.ball:
                if to_draw:
                    cv2.circle(self.board, tuple(ball_pos), 8, ball_coluor, -1)
                    cv2.circle(self.board, tuple(ball_pos), 9, (128, 128, 128), 2)
                    cv2.circle(self.board, (ball_pos[0] - 3, ball_pos[1] + 3), 2, (255, 255, 255), 2)

    def updateball(self):
        step = 0.04
        if not self.ball == []:
            for idx in range(len(self.ball)):

                self.ball[idx][1][0] = int(self.ball[idx][1][0] + self.ball[idx][2][0] * step)
                self.ball[idx][1][1] = int(self.ball[idx][1][1] + self.ball[idx][2][1] * step)
                self.ball[idx][2][1] = self.ball[idx][2][1] - 200 * step

                if self.ball[idx][1][0] < 15:
                    self.ball[idx][1][0] = 15
                    self.ball[idx][2][0] *= uniform(-0.8, -1, 1)
                elif self.ball[idx][1][0] > 1905:
                    self.ball[idx][1][0] = 1905
                    self.ball[idx][2][0] *= uniform(-0.8, -1, 1)
                elif self.ball[idx][1][1] > 1065:
                    self.ball[idx][1][1] = 1065
                    self.ball[idx][2][1] *= uniform(-1, -1, 1)
                elif self.ball[idx][1][1] < 15:
                    if not self.ball[idx][1][0] < 200:
                        self.ball[idx][1][1] = 15
                        self.ball[idx][2][1] *= uniform(-0.1, -0.5, 1)
                    else:
                        pass

                if self.ball[idx][1][1] < 0:
                    self.ball[idx][3] = False

                    # wall 0
                x0, y0, x1, y1 = Board.PARAMS['wall0']

                if x0 - self.wall_thickness < self.ball[idx][1][0] < x1 - self.wall_thickness and (
                    y0 - self.wall_thickness) < self.ball[idx][1][1] < (y1 + self.wall_thickness):

                    if (self.ball[idx][1][1] - (y1 + y0) / 2) > 0:
                        self.ball[idx][1][1] = y1 + self.wall_thickness
                        self.ball[idx][2][1] *= uniform(-0.5, -0.8, 1)
                    else:
                        self.ball[idx][1][1] = y0 - self.wall_thickness
                        self.ball[idx][2][1] *= uniform(-0.5, -0.8, 1)

        self.get_kinetic()

    @staticmethod
    def random_colour():
        return tuple(np.random.randint(255) for _ in range(3))

    def get_kinetic(self):
        # if time.time() - self.time_check > 30:
        #     self.time_check = time.time()
        #     self.ball = [x for x in self.ball if (x[2][0] ** 2 + x[2][1] ** 2) > 8000]
        #     self.ball = [x for x in self.ball if not (x[1][0] < 100 and x[1][1] < 20)]
        if len(self.ball) > self.max_balls:
            del self.ball[0:len(self.ball) - self.max_balls]


if __name__ == '__main__':
    board = Board()
    board.run()
    # board_ = Thread(target=board.run).start()
