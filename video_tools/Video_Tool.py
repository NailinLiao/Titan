import cv2
import time
import os


class Video_Tools:

    @staticmethod
    def get_video_time(video_path, time_structure="%Y-%m-%d-%H-%M-%S"):
        # 匹配文件名获取起始时间戳
        start_frame_time = '-'.join(str(os.path.split(video_path)[-1]).split('_')[4:-2])
        print(start_frame_time)
        start_time = time.strptime(start_frame_time, time_structure)
        start_time = time.mktime(start_time)

        cap = cv2.VideoCapture(video_path)  # 若参数为0， 则是本地摄像头
        fps = int(cap.get(cv2.CAP_PROP_FPS))  #
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if frames > 10:
            one_frame_time = 1 / fps
            long_time = frames * one_frame_time
            end_time = start_time + long_time
            return start_time, end_time, long_time

        else:
            print('注意该视频文件受损:', video_path, '------》》》》并启用修复模式读取数据')
            # return 0, 0, 0
            count = 0
            while cap.isOpened():  # 当成功时
                ret, frame = cap.read()  # 若获取成功，ret为True，否则为False；frame是图像
                if ret:  # 成功获取图像
                    count += 1
                else:
                    break
            end_time = start_time + (count / fps)
            return start_time, end_time, end_time - start_time

    @staticmethod
    def cut_video_by_frames(video_path, save_path, cut_start_time, cut_end_time, additional_duration=1):
        # cut_end_time = cut_end_time_utc + (8 * 3600)
        # cut_start_time = cut_start_time_utc + (8 * 3600)
        video_name = str(os.path.split(video_path)[-1]).split('.')[0]
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        start_time, end_time, long_time = Video_Tools.get_video_time(video_path)
        cap = cv2.VideoCapture(video_path)  # 若参数为0， 则是本地摄像头
        fps = int(cap.get(cv2.CAP_PROP_FPS))  #
        one_frame_time = 1 / fps
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取原视频的宽
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取原视频的搞
        now_time = start_time
        save_file_name = video_name + str(int(cut_start_time)) + str(int(cut_end_time)) + '.mp4'
        end_save_path = os.path.join(save_path, save_file_name)
        out = cv2.VideoWriter(end_save_path, fourcc, fps, (width, height))

        while cap.isOpened():  # 当成功时
            ret, frame = cap.read()  # 若获取成功，ret为True，否则为False；frame是图像
            if ret:  # 成功获取图像
                now_time += one_frame_time
                if now_time > cut_start_time - additional_duration and now_time < cut_end_time + additional_duration:
                    # cv2.imshow('ima', frame)
                    # cv2.waitKey(1)
                    out.write(frame)  # 写入视频
            else:
                break
            # print(now_time, cut_start_time, cut_end_time)

        cap.release()  # 释放视频
        out.release()
        print('截取视频:', end_save_path)

    @staticmethod
    def fix_video(video_path, save_path):
        cap = cv2.VideoCapture(video_path)  # 若参数为0， 则是本地摄像头

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        video_name = str(os.path.split(video_path)[-1])
        end_save_path = os.path.join(save_path, video_name)
        fps = int(cap.get(cv2.CAP_PROP_FPS))  #
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取原视频的宽
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取原视频的搞
        out = cv2.VideoWriter(end_save_path, fourcc, fps, (width, height))
        while cap.isOpened():  # 当成功时
            ret, frame = cap.read()  # 若获取成功，ret为True，否则为False；frame是图像
            if ret:  # 成功获取图像
                out.write(frame)  # 写入视频
            else:
                break
        cap.release()  # 释放视频
        out.release()
        print('修复视频:', end_save_path)


if __name__ == '__main__':
    start_time_utc = 1678154482
    end_time_utc = 1678154534
    avi_path = r'C:\Users\NailinLiao\PycharmProjects\DocumentCheckingTool\test_data\rec_0330007_default_B02_2023-03-07-09_51_06_0_1.avi'
    save_path = r'./ret'
    Video_Tools.cut_video_by_frames(avi_path, save_path, start_time_utc, end_time_utc)
