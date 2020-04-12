import cv2
import sys
from os import path
import argparse

WIN_NAME = 'Preview'
FILE_FMT = '000000.jpg'

def rotate(frame, degrees):
    rows = frame.shape[0]
    cols = frame.shape[1]

    M = cv2.getRotationMatrix2D((cols/2, rows/2), degrees, 1)

    return cv2.warpAffine(frame, M, (cols, rows))

def togray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def render(dirname, dest, fps, size):
    cap = cv2.VideoCapture(path.join(dirname, FILE_FMT))

    if (not cap.isOpened()):
        print('Unable to open image sequence.')
        return

    filename = path.join(dirname, dest)

    vid = cv2.VideoWriter(filename, -1, fps, size)

    if (not vid.isOpened()):
        print('Unable to create video file.')
        return

    print('Rendering video...')

    while(True):
        res, frame = cap.read()

        if (not res):
            break

        # resize frame to target resolution
        frame = cv2.resize(frame, size)

        frame = togray(frame)
        # frame = rotate(frame, 180)

        # update preview
        cv2.imshow(WIN_NAME, frame)
        cv2.waitKey(5)

        # write fame
        vid.write(frame)

    print('Video saved as {:s}'.format(filename))

    vid.release()
    cap.release()
    cv2.destroyWindow(WIN_NAME)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a video from a sequence of images.')
    parser.add_argument('directory', type=str, help='directory containing a sequence of images')
    parser.add_argument('filename', type=str, help='output video file')
    parser.add_argument('-f', '--fps', type=int, help='video framerate', default=30)
    parser.add_argument('-s', '--size', type=int, help='video width and height', nargs=2, metavar=('WIDTH', 'HEIGHT'), default=[640, 480])

    args = parser.parse_args()

    render(args.dir, args.out, args.fps, tuple(args.size))
