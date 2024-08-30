"""Read depth file coming from the Depth-Anything-V2 and display it with Open3D
Press <SPACE> to start/pause/resume frames
In paused mode, press <N> to go to next frame
"""

from argparse import ArgumentParser
import open3d
from time import time
import os

class Model:
    def __init__(self):
        self.__vis = open3d.visualization.VisualizerWithKeyCallback()
        self.__vis.create_window()

        self.pcd = None

        self.__vis.register_key_callback(32, self.pause)
        self.__vis.register_key_callback(78, self.next_frame)
        self.__vis.get_render_option().point_size = 3
        self.is_paused = False
        self.next_frame = False

    def set_view(self):
        ctr = self.__vis.get_view_control()
        ctr.set_front((0.0, 0.0, -1.0))
        ctr.set_up((0.0, -1.0, 0.0))
        ctr.set_lookat((0.0, 0.0, 0.0))
        ctr.set_zoom(0.1)

    def pause(self, _):
        self.is_paused = not self.is_paused

    def next_frame(self, _):
        self.next_frame = True

    def add_xyz(self, xyz, rgb):
        self.pcd = open3d.geometry.PointCloud()

        self.pcd.points = open3d.utility.Vector3dVector(xyz)
        self.pcd.colors = open3d.utility.Vector3dVector(rgb)

        self.__vis.add_geometry(self.pcd)
        self.__vis.poll_events()
        self.__vis.update_renderer()

    def show(self):
        self.__vis.update_geometry(self.pcd)
        self.__vis.poll_events()
        self.__vis.update_renderer()

    def kill(self):
        return not self.__vis.poll_events()



def display_point_cloud():
    
    model = Model()

    model.set_view()

    start = time()

    nb_frames = len(os.listdir(f"{args.sample}/"))
    i = 1
    while i <= nb_frames and not model.kill():

        if model.is_paused:
            if not model.next_frame:
                model.show()
                continue
            else:
                model.next_frame = False
            
        pcd = open3d.io.read_point_cloud(f"{args.sample}/image_{i:03d}.ply")

        if model.pcd is None:
            model.add_xyz(pcd.points, pcd.colors)
            model.set_view()
        model.pcd.points = open3d.utility.Vector3dVector(pcd.points)
        model.pcd.colors = open3d.utility.Vector3dVector(pcd.colors)

        model.show()

        start = time()

        i += 1

    while not model.kill():
        model.show()




if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Read and display the content of a Depth Anyything sequence"
    )
    parser.add_argument('sample')
    args = parser.parse_args()

    display_point_cloud()
