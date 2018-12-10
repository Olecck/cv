import numpy as np
import cv2
import os.path as osp
from video import Video


class ROIPoly:
    def __init__(self):
        self.points = []
        self.frame = None

    def select_point(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            if len(self.points) != 0:
                cv2.line(self.frame, self.points[-1], (x, y), (0, 0, 255), 2)    # color is in BGR
            cv2.circle(self.frame, (x, y), 4, (100,100,100), 2)
            self.points.append((x, y))
        if event == cv2.EVENT_RBUTTONDBLCLK:
            if len(self.points) != 0:
                cv2.line(self.frame, self.points[-1], self.points[0], (0, 0, 255), 2)  # color is in BGR

    def roi_poly(self, img, title="Frame"):
        self.frame = img
        cv2.namedWindow(title + "- ESC when done")
        cv2.setMouseCallback(title + "- ESC when done", self.select_point)
        while (1):
            cv2.imshow(title + "- ESC when done", self.frame)
            k = cv2.waitKey(20) & 0xFF  # escape character ?
            if k == 27:
                break

        cv2.destroyAllWindows()

        mask = np.zeros(frame.shape, np.uint8)
        if len(self.points) == 0:
            return mask
        poly = np.array(self.points, np.int32)
        poly = poly.reshape((-1, 1, 2))
        mask = cv2.fillConvexPoly(mask, poly, (255, 255, 255))
        while (1):
            cv2.imshow(title + " mask" + "- ESC to quit", mask)
            k = cv2.waitKey(20) & 0xFF  # escape character ?
            if k == 27:
                break
        cv2.destroyAllWindows()
        self.points = []    # reinit points
        return mask


if __name__ == '__main__':
    """
    Here we do the processing over specific frames of a video, 
    but this could be done on a single image in two lines:
    r = ROIPoly()
    mask = r.roi_poly(f, filename)
    """
    video_file = "test.mp4"
    loc_and_name = osp.join('images', video_file.split('/')[-1].split('.')[0])
    v = Video(video_file)
    r = ROIPoly()

    masks = []
    for instant in np.linspace(0, v.length, v.length/v.duration):
        instant = int(instant)
        title = 'Frame at {}'.format(instant)

        frame = v.get_frame(instant)
        if frame is not None:
            f = np.copy(frame)
            mask = r.roi_poly(f, title)

            if np.count_nonzero(mask) != 0:
                masks.append(mask)
                cv2.imwrite(loc_and_name + '-' + str(instant) + '.png', frame)
                cv2.imwrite(loc_and_name + '-' + str(instant) + '_mask.png', mask)

    print('{} images masked'.format(len(masks)))
