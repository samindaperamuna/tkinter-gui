from time import strftime

import cv2


class VideoCapture:

    def __init__(self, video_source=0):
        # Open the video source.
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get the video source width and height.
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            # Read the video.
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR.
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None

    def take_snapshot(self):
        # Get a frame from the video source.
        ret, frame = self.get_frame()

        if ret:
            cv2.imwrite("frame-" + strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
