import datetime
import logging
import pathlib
from typing import Optional
import sys
import cv2
import csv
import numpy as np
from omegaconf import DictConfig

from .common import Face, FacePartsName, Visualizer
from .gaze_estimator import GazeEstimator
from .utils import get_3d_face_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_percent_done(count_in, total, bar_len=50, title_input='Please wait'):
    percent_done = count_in / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '=' * done
    togo_str = '_' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')
    sys.stdout.flush()


# This function is to change frame count to time in second
def frame_count_to_time(frame_count_input, frame_rate_input):
    return frame_count_input / frame_rate_input


def add_line_info(value_in, dict_in, side="") -> dict:
    for line_name in value_in:
        dict_in = assign_xyz(line_name, value_in[line_name][0], dict_in, f"{side}{line_name}_start")
        dict_in = assign_xyz(line_name, value_in[line_name][1], dict_in, f"{side}{line_name}_end")
    return dict_in


def assign_xyz(key_in, array_in, dict_in, extra_str=None) -> dict:
    # print("key", key_in)
    # print("dict_in",  dict_in)
    # print("array_in", array_in)
    # print("extra_str", extra_str)
    if extra_str is None:
        extra_str = key_in
    if key_in == "normalized_gaze_angles" or key_in == "avg_normalized_gaze_angles":
        dict_in[f"{extra_str}_elevation"] = array_in[0]
        dict_in[f"{extra_str}_azimuth"] = array_in[1]
    else:
        if len(array_in) == 3:
            dict_in[f"{extra_str}_x"] = array_in[0]
            dict_in[f"{extra_str}_y"] = array_in[1]
            dict_in[f"{extra_str}_z"] = array_in[2]
        elif len(array_in) == 2:
            dict_in[f"{extra_str}_x"] = array_in[0]
            dict_in[f"{extra_str}_y"] = array_in[1]
        else:
            pass
    return dict_in


class Demo:
    QUIT_KEYS = {27, ord('q')}

    def __init__(self, config: DictConfig):
        # print("start in init")
        self.config = config
        # print("start gaze_estimator")
        self.gaze_estimator = GazeEstimator(config)
        # print("start in get_3d_face_model")
        face_model_3d = get_3d_face_model(config)
        # print("start in Visualizer")
        self.visualizer = Visualizer(self.gaze_estimator.camera,
                                     face_model_3d.NOSE_INDEX)
        # print("start in _create_capture")
        self.cap = self._create_capture()
        # print("start in _create_output_dir")
        self.output_dir = self._create_output_dir()
        # print("start in _create_video_writer")
        self.writer = self._create_video_writer()
        self.stop = False
        self.show_bbox = self.config.demo.show_bbox
        self.show_head_pose = self.config.demo.show_head_pose
        self.show_landmarks = self.config.demo.show_landmarks
        self.show_normalized_image = self.config.demo.show_normalized_image
        self.show_template_model = self.config.demo.show_template_model
        self.csv_data_array = []
        # print("end in init")

    def run(self) -> None:
        if self.config.demo.use_camera or self.config.demo.video_path:
            # print("_run_on_video")
            self._run_on_video()
        elif self.config.demo.image_path:
            # print("_run_on_image")
            # self._run_on_image()
            pass
        else:
            raise ValueError

    # def _run_on_image(self):
    #     image = cv2.imread(self.config.demo.image_path)
    #     self._process_image(image)
    #     if self.config.demo.display_on_screen:
    #         while True:
    #             key_pressed = self._wait_key()
    #             if self.stop:
    #                 break
    #             if key_pressed:
    #                 self._process_image(image)
    #             cv2.imshow('image', self.visualizer.image)
    #     if self.config.demo.output_dir:
    #         name = pathlib.Path(self.config.demo.image_path).name
    #         output_path = pathlib.Path(self.config.demo.output_dir) / name
    #         cv2.imwrite(output_path.as_posix(), self.visualizer.image)

    def _run_on_video(self) -> None:
        count = 0
        while True:
            if self.config.demo.display_on_screen:
                self._wait_key()
                if self.stop:
                    break

            ok, frame = self.cap.read()
            # print("ok and frame")
            if not ok:
                break
            count += 1
            self._process_image(frame, count)
            print_percent_done(count, self.frame_count)
            # print("after process image")

            if self.config.demo.display_on_screen:
                cv2.imshow('frame', self.visualizer.image)
        self.cap.release()
        if self.writer:
            self.writer.release()
        print("")
        print(f"Output video : {self.output_path} is created.")
        self._write_csv_data()

    def _process_image(self, image, frame_count) -> None:
        undistorted = cv2.undistort(
            image, self.gaze_estimator.camera.camera_matrix,
            self.gaze_estimator.camera.dist_coefficients)

        self.visualizer.set_image(image.copy())
        faces = self.gaze_estimator.detect_faces(undistorted)
        # print(faces)
        face_id = 1
        for face in faces:
            self.gaze_estimator.estimate_gaze(undistorted, face)
            self._draw_face_bbox(face)
            rot_vec = face.head_pose_rot.as_rotvec()
            self._draw_head_pose(face)
            self._draw_landmarks(face)
            self._draw_face_template_model(face)
            gaze_data_array = self._draw_gaze_vector(face)
            data_dict = {}
            data_dict["frame_index"] = frame_count
            data_dict["face_id"] = face_id
            data_dict["timestamp"] = frame_count_to_time(frame_count, self.frame_rate)
            if self.config.mode == 'MPIIGaze':
                eye_data_name_array = ["center", "normalized_gaze_angles",
                                       "normalized_gaze_vector", "gaze_vector",
                                       "gaze_vector_line_start", "gaze_vector_line_end"]
                for dict_ele in gaze_data_array:
                    side = dict_ele["eye_side"]
                    if side == "right_eye" or side == "left_eye":
                        for key in dict_ele:
                            if key == "line_info":
                                line_info = dict_ele[key]
                                data_dict = add_line_info(line_info, data_dict, f"{side}_")
                            else:
                                if key in eye_data_name_array:
                                    data_dict = assign_xyz(key, dict_ele[key], data_dict, f"{side}_{key}")
                                else:
                                    pass
                    else:
                        for key in dict_ele:
                            if key == "avg_line_info":
                                line_info = dict_ele[key]
                                data_dict = add_line_info(line_info, data_dict, f"avg_")
                            else:
                                if key == "eye_side":
                                    pass
                                else:
                                    data_dict = assign_xyz(key, dict_ele[key], data_dict)
            elif self.config.mode == 'ETH-XGaze':
                data_dict["head_pose_rot_vector_x"] = rot_vec[0]
                data_dict["head_pose_rot_vector_y"] = rot_vec[1]
                data_dict["head_pose_rot_vector_z"] = rot_vec[2]
                eye_data_name_array = ["center", "normalized_gaze_angles", "normalized_gaze_vector",
                                       "gaze_vector", "head_position",
                                       "gaze_vector_line_start", "gaze_vector_line_end"]
                for dict_ele in gaze_data_array:
                    for key in dict_ele:
                        if key == "line_info":
                            line_info = dict_ele[key]
                            data_dict = add_line_info(line_info, data_dict)
                        else:
                            if key in eye_data_name_array:
                                data_dict = assign_xyz(key, dict_ele[key], data_dict)
                            else:
                                pass

            # print("gaze data array")
            # for kk in data_dict:
            #     print(f"{kk}: {data_dict[kk]}")
            # print("==========================================")
            # print("_draw_gaze_vector end")
            self._display_normalized_image(face)
            # print("_display_normalized_image end")
            self.csv_data_array.append(data_dict)
            face_id += 1
        # print("end in faces for loop")

        # print(self.config.demo.use_camera)
        if self.config.demo.use_camera:
            self.visualizer.image = self.visualizer.image[:, ::-1]

        # print(self.writer)
        if self.writer:
            # print("Here")
            self.writer.write(self.visualizer.image)

    def _write_csv_data(self) -> None:
        print("Start writing csv data...")
        out_csv_dir = self.output_dir / self.config.demo.out_csv_name
        array_length = len(self.csv_data_array)
        if array_length > 0:
            header_array = [key for key in self.csv_data_array[0]]
            with open(out_csv_dir, mode='w', newline="") as destination_file:
                header_names = header_array
                csv_writer = csv.DictWriter(destination_file, fieldnames=header_names)
                csv_writer.writeheader()
                for index, csv_data in enumerate(self.csv_data_array):
                    print_percent_done(index + 1, array_length)
                    csv_writer.writerow(csv_data)
                destination_file.close()
                print("")
                print(f"{out_csv_dir} is generated.")
        else:
            raise ValueError("THere is no data to write csv.")

    def _create_capture(self) -> Optional[cv2.VideoCapture]:
        if self.config.demo.image_path:
            return None
        if self.config.demo.use_camera:
            cap = cv2.VideoCapture(0)
        elif self.config.demo.video_path:
            cap = cv2.VideoCapture(self.config.demo.video_path)
        else:
            raise ValueError
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.gaze_estimator.camera.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.gaze_estimator.camera.height)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = frame_count
        self.frame_rate = frame_rate
        return cap

    def _create_output_dir(self) -> Optional[pathlib.Path]:
        if not self.config.demo.output_dir:
            return
        output_dir = pathlib.Path(self.config.demo.output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        return output_dir

    @staticmethod
    def _create_timestamp() -> str:
        dt = datetime.datetime.now()
        return dt.strftime('%Y%m%d_%H%M%S')

    def _create_video_writer(self) -> Optional[cv2.VideoWriter]:
        output_path = self.output_dir / self.config.demo.out_video_name
        self.output_path = output_path
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path.as_posix(), fourcc, 30,
                                 (self.gaze_estimator.camera.width,
                                  self.gaze_estimator.camera.height), True)
        if writer is None:
            raise RuntimeError(f"Error in creating video writer {output_path}")
        return writer

    def _wait_key(self) -> bool:
        key = cv2.waitKey(self.config.demo.wait_time) & 0xff
        if key in self.QUIT_KEYS:
            self.stop = True
        elif key == ord('b'):
            self.show_bbox = not self.show_bbox
        elif key == ord('l'):
            self.show_landmarks = not self.show_landmarks
        elif key == ord('h'):
            self.show_head_pose = not self.show_head_pose
        elif key == ord('n'):
            self.show_normalized_image = not self.show_normalized_image
        elif key == ord('t'):
            self.show_template_model = not self.show_template_model
        else:
            return False
        return True

    def _draw_face_bbox(self, face: Face) -> None:
        if not self.show_bbox:
            return
        self.visualizer.draw_bbox(face.bbox)

    def _draw_head_pose(self, face: Face) -> None:
        if not self.show_head_pose:
            return
        # Draw the axes of the model coordinate system
        length = self.config.demo.head_pose_axis_length
        self.visualizer.draw_model_axes(face, length, lw=2)

        euler_angles = face.head_pose_rot.as_euler('XYZ', degrees=True)
        pitch, yaw, roll = face.change_coordinate_system(euler_angles)
        # logger.info(f'[head] pitch: {pitch:.2f}, yaw: {yaw:.2f}, '
        #             f'roll: {roll:.2f}, distance: {face.distance:.2f}')

    def _draw_landmarks(self, face: Face) -> None:
        if not self.show_landmarks:
            return
        self.visualizer.draw_points(face.landmarks,
                                    color=(0, 255, 255),
                                    size=1)

    def _draw_face_template_model(self, face: Face) -> None:
        if not self.show_template_model:
            return
        self.visualizer.draw_3d_points(face.model3d,
                                       color=(255, 0, 525),
                                       size=1)

    def _display_normalized_image(self, face: Face) -> None:
        if not self.config.demo.display_on_screen:
            return
        if not self.show_normalized_image:
            return
        if self.config.mode == 'MPIIGaze':
            reye = face.reye.normalized_image
            leye = face.leye.normalized_image
            normalized = np.hstack([reye, leye])
        elif self.config.mode in ['MPIIFaceGaze', 'ETH-XGaze']:
            normalized = face.normalized_image
        else:
            raise ValueError
        if self.config.demo.use_camera:
            normalized = normalized[:, ::-1]
        cv2.imshow('normalized', normalized)

    def _draw_gaze_vector(self, face: Face) -> list:
        length = self.config.demo.gaze_visualization_length
        temp_array = []
        if self.config.mode == 'MPIIGaze':
            # print(self.config.mode)
            # print("Face obj")
            # print("-------------------------------------------------")
            # for attr, value in face.__dict__.items():
            #     if attr == "landmarks" or attr == "normalized_image":
            #         print(f"{attr}: {type(value)}")
            #     elif attr == "reye" or attr == "leye":
            #         print(attr)
            #         for k, v in value.__dict__.items():
            #             print(f"{k}: {v}")
            #         print("-------------------------------------------------")
            #     else:
            #         print(f"{attr}: {value}")
            # print("-------------------------------------------------")
            for key in [FacePartsName.REYE, FacePartsName.LEYE]:
                eye = getattr(face, key.name.lower())
                line_info = self.visualizer.draw_3d_line(
                    eye.center, eye.center + length * eye.gaze_vector)
                temp_dict = {}
                for k, v in eye.__dict__.items():
                    temp_dict[k] = v
                temp_dict["line_info"] = line_info
                temp_array.append(temp_dict)
                pitch, yaw = np.rad2deg(eye.vector_to_angle(eye.gaze_vector))
                # logger.info(
                #     f'[{key.name.lower()}] pitch: {pitch:.2f}, yaw: {yaw:.2f}')
            temp_array[0]["eye_side"] = "right_eye"
            temp_array[1]["eye_side"] = "left_eye"
            re_normalized_gaze_angles = temp_array[0]["normalized_gaze_angles"]
            le_normalized_gaze_angles = temp_array[1]["normalized_gaze_angles"]
            re_normalized_gaze_vector = temp_array[0]["normalized_gaze_vector"]
            le_normalized_gaze_vector = temp_array[1]["normalized_gaze_vector"]
            avg_angles = (re_normalized_gaze_angles + le_normalized_gaze_angles) / 2
            avg = (re_normalized_gaze_vector + le_normalized_gaze_vector) / 2
            norm_avg = np.linalg.norm(avg)
            avg_normalized_gaze_vector = (avg / norm_avg)
            avg_eye_center = (temp_array[0]["center"] + temp_array[1]["center"]) / 2
            avg_line_info = self.visualizer.draw_3d_line(
                avg_eye_center, avg_eye_center + length * avg_normalized_gaze_vector)
            gaze_dict = {}
            gaze_dict["eye_side"] = "average"
            gaze_dict["avg_normalized_gaze_angles"] = avg_angles
            gaze_dict["avg_normalized_gaze_vector"] = avg_normalized_gaze_vector
            gaze_dict["avg_eye_center"] = avg_eye_center
            gaze_dict["avg_line_info"] = avg_line_info
            temp_array.append(gaze_dict)
        elif self.config.mode in ['MPIIFaceGaze', 'ETH-XGaze']:
            # print(self.config.mode)
            # print("Face obj")
            # print("-------------------------------------------------")
            # for attr, value in face.__dict__.items():
            #     if attr == "landmarks" or attr == "normalized_image":
            #         print(f"{attr}: {type(value)}")
            #     elif attr == "reye" or attr == "leye":
            #         print(attr)
            #         for k, v in value.__dict__.items():
            #             print(f"{k}: {v}")
            #         print("-------------------------------------------------")
            #     else:
            #         print(f"{attr}: {value}")
            # print("-------------------------------------------------")
            line_info = self.visualizer.draw_3d_line(
                face.center, face.center + length * face.gaze_vector)
            pitch, yaw = np.rad2deg(face.vector_to_angle(face.gaze_vector))
            temp_dict = {}
            for k, v in face.__dict__.items():
                temp_dict[k] = v
            temp_dict["line_info"] = line_info
            temp_array.append(temp_dict)
            # logger.info(f'[face] pitch: {pitch:.2f}, yaw: {yaw:.2f}')
        else:
            raise ValueError
        return temp_array
