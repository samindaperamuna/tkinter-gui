import os
from time import strftime

import cv2


class VideoCapture:

    def __init__(self, video_source=0, snapshot_dir=None):
        self.snapshot_dir = snapshot_dir

        # Open the video source.
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get the video source width and height.
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self, pref_width=None, pref_height=None):
        if self.vid.isOpened():
            # Read the video.
            ret, frame = self.vid.read()

            # Scale the frame if pref-width is set.
            if pref_width is not None and pref_height is not None:
                height = int(pref_width / self.width * self.height)

                # If the new height is larger than the canvas height
                # calculate the width and use it.
                if height > pref_height:
                    width = int(self.width / self.height * pref_height)
                    pref_width = width
                else:
                    pref_height = height

                frame = cv2.resize(frame, (pref_width, pref_height))

            if ret:
                # Return a boolean success flag and the current frame converted to BGR.
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None

    def take_snapshot(self):
        # Get a frame from the video source.
        ret, frame = self.get_frame()

        if ret:
            # Create write directory if not exists.
            if not os.path.exists(self.snapshot_dir):
                os.makedirs(self.snapshot_dir)
            cv2.imwrite(self.snapshot_dir + "/frame-" + strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            return True
        return False

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
