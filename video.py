
import cv2


class Video:
    """
    This class allows you to quicly manipulate videos using openCV.
    It is intended to be used as a wrapper around opencv VideoCapture object.
    It gives you quick access over each frame of the video.
    You can give it a transform that it apply to each frame of the video once played.
    """
    def __init__(self, filename, title='Video', speed=1.0, transform=lambda x: x):
        self.stream = cv2.VideoCapture(filename)
        self.length = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.speed = speed
        self.duration = self.length/self.fps
        self.transform = transform
        self.title = title
        self.frame_delay_ms = int(1/self.fps*1000/self.speed)

    def play(self, with_transform=True):
        """
        Plays video and applies the transform if necessary
        :param with_transform: wether or not the transform should be applied
        """
        while self.stream.get(cv2.CAP_PROP_POS_FRAMES) <= self.length:
            ret, frame = self.stream.read()
            if ret == True:
                if with_transform:
                    frame = self.transform(frame)
                cv2.imshow(self.title, frame)
                if cv2.waitKey(self.frame_delay_ms) & 0xFF == ord('q'):
                    break
            else:
                break
        cv2.destroyAllWindows()
        self.reset()    # in case we play the video another time

    def get_frame(self, target_frame, with_transform=True):
        """
        Easy access to a specific frame of the video.
        :param target_frame: frame index in the video, calculated as int(time(s)*fps)
        :return: the requested frame
        """
        assert target_frame <= self.length
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = self.stream.read()
        if ret == True:
            frame = cv2.flip(frame, 0)
            if with_transform:
                    frame = self.transform(frame)

        self.reset()
        return frame

    def record(self, codec='MP4V', filename='output.mp4', fps=20.0, shape=(640, 480)):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(filename, fourcc, fps, shape)

        while self.stream.isOpened():
            ret, frame = self.stream.read()
            if ret == True:
                frame = cv2.flip(frame, 0)

                # write the flipped frame
                out.write(frame)
                cv2.imshow('Recording {}'.format(filename), frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cv2.destroyAllWindows()

    def reset(self):
        # sets the stream position back to 0
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def release(self):
        # release the videoCapture object
        self.stream.release()
        
if __name__ == "__main__":
	v = Video(0)
	v.record(filename='test.mp4')
	v.release()
	p = Video('test.mp4')
	p.play()
