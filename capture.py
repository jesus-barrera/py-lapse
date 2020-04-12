import cv2
import time
import os
import re
import argparse
from datetime import datetime

WIN_NAME = 'Stream'
FILE_FMT = '{:06d}.jpg'
DATE_FMT = '%d/%m/%Y %H:%M:%S'
DIR_FMT = '%Y%m%d_%H%M%S'
DEFAULT_INTERVAL = 30

controls = '''
Controls:
s = start/stop timelapse
d = increase interval
a = decrease interval
c = take single shot
q = exit
'''

def log(message):
    print('[{:s}] {:s}'.format(datetime.now().strftime(DATE_FMT), message))

def save_frame(dirname, count, frame):
    filename = os.path.join(dirname, FILE_FMT.format(count))
    cv2.imwrite(filename, frame)

    log('Frame saved at {:s}'.format(filename))

def get_frame_count(dirname):
    count = 0

    for file in os.listdir(dirname):
        match = re.search('^(\d{6})\.jpg$', file)

        if match:
            count = max(count, int(match.group(1)))

    return count

def use_dir(dirname):
    if (os.path.exists(dirname)):
        is_new = False
        count = get_frame_count(dirname)
    else:
        os.mkdir(dirname)
        is_new = True
        count = 0

    return (is_new, count)

def remove_dir(dirname):
    if (os.path.isdir(dirname) and not os.listdir(dirname)):
        os.rmdir(dirname)

def main(device, dirname):
    interval = DEFAULT_INTERVAL
    capture = False
    current_time = None
    capture_time = None

    if (device.isdigit()):
        cam = cv2.VideoCapture(int(device))
    else:
        cam = cv2.VideoCapture(device)

    if (not cam.isOpened()):
        print('Unable to open camera at {:s}'.format(device))
        return

    print('Camera opened at {:s}'.format(device))

    # Set the output directory
    is_new, count = use_dir(dirname)

    if (is_new):
        print('Frames will be saved in {:s}'.format(dirname))
    else:
        print('Using existing directory {:s}. Last frame was {:06}'.format(dirname, count))

    while(True):
        current_time = time.time()

        key = chr(cv2.waitKey(5) & 0xFF)

        # Handle key events
        if (capture):
            if (key == 's'):
                capture = False
                capture_time = None

                log('Timelapse stoped')
        else:
            if (key == 's'):
                capture = True
                capture_time = current_time

                log('Timelapse started')

            elif (key == 'd'):
                interval = interval + 1

                log('Interval set to {:d}'.format(interval))

            if (key == 'a' and interval > 1):
                interval = interval - 1

                log('Interval set to {:d}'.format(interval))

        if (key == 'q'):
            break

        # Read next frame
        res, frame = cam.read()

        if (not res):
            log('Camera disconnected')
            break

        # Update camera feed
        cv2.imshow(WIN_NAME, frame)

        # Determine to save the frame or not
        use_frame = False

        if (capture):
            # Capture next frame
            if (current_time >= capture_time):
                use_frame = True
                capture_time = current_time + interval
        else:
            # Take single shot
            if (key == 'c'):
                use_frame = True

        if (use_frame):
            count = count + 1
            save_frame(dirname, count, frame)

    # If not photos taken remove output directory
    if (is_new and count == 0):
        remove_dir(dirname)

    log('Exiting...')

    cam.release()
    cv2.destroyWindow(WIN_NAME)

if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(description='Opens a video stream to capture a sequence of images.')
    parser.add_argument('-d', '--device', type=str, help='camera index or IP', default='0')
    parser.add_argument('-o', '--output', type=str, metavar="DIR", help='output directory', default=datetime.now().strftime(DIR_FMT))

    args = parser.parse_args()

    main(args.device, args.output)
