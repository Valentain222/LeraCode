import socket

import cv2
import random


class Point:
    def __init__(self, number: int, coordinate):
        self.number = number
        self.coordinate = coordinate

    def __str__(self):
        return f'{self.number}|{self.coordinate[0]},{self.coordinate[1]}'


LEN_X = 3.04
LEN_Y = 5.4

my_map = cv2.imread('map.png')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)
print('Server start!')

points = []

def add_points(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(my_map, (x, y), 10, (0, 0, 255), -1)
        points.append(Point(len(points)+1, (x/(my_map.shape[1] / LEN_X), (my_map.shape[0]-y)/(my_map.shape[0] / LEN_Y))))

def main():
    once = True
    while True:
        cv2.imshow('MAIN', my_map)
        cv2.setMouseCallback('MAIN', add_points)
        key = cv2.waitKey(10)
        if key == 13 and once:
            once = False
            client_socket, addr = server.accept()
            print(f"Подключено к {addr}")

            while True:
                data = client_socket.recv(1024).decode()
                if data == 'get coordinates':
                    print('Send coordinates')
                    client_socket.sendall(('Coordinates' + ';'.join(map(str, points))).encode())
                elif data == 'done':
                    print('Client stop')
                    break

            client_socket.close()
            server.close()


if __name__== '__main__':
    main()
