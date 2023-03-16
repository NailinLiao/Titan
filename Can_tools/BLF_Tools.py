import os

import pandas as pd
import cantools

from canIO.blf import BLFReader

# from canIO.asc import ASCReader
# from log import logger

# BOSCH_DBC_PATH = r'canIO\dbc\Bosch_FR5_CR5_Common_32FRSGU_v12.dbc'
DBC_PATH = r'canIO\dbc\DeepWay_SXXT1_CAN(FD)_ADCU3_ADBackboneCANFD_Matrix_V3.1_20221212.dbc'


class BLF_Tools:

    @staticmethod
    def bosch_asc2csv(input_dir, output_dir, dbc_path=DBC_PATH):
        input_file_list = [file_name for file_name in os.listdir(input_dir) if file_name.endswith('.blf')]
        # input_file_list.sort(key = lambda x: int(x[:-4]))
        db = cantools.database.load_file(dbc_path)
        # print(db.messages[0].name, db.messages[0].frame_id, )
        for file_name in input_file_list:
            print('parsing %s' % (file_name))

            with BLFReader(os.path.join(input_dir, file_name)) as asclog:
                radar_status_dict = {}
                for mesg in asclog:

                    try:
                        mesg_name = db.get_message_by_frame_id(mesg.arbitration_id).name
                    except Exception as e:
                        # print('Error:', e)
                        continue
                    timestamp = mesg.timestamp
                    # print(mesg.timestamp, asclog.start_time, timestamp)
                    if mesg_name not in radar_status_dict:
                        radar_status_dict[mesg_name] = []
                    radar_status_data = db.decode_message(mesg.arbitration_id, mesg.data)
                    radar_status_data['Mesg_TimeStamp'] = timestamp
                    radar_status_dict[mesg_name].append(radar_status_data)
                for mesg_name in radar_status_dict:
                    status_dataframe = pd.DataFrame(radar_status_dict[mesg_name])
                    status_dataframe.to_csv('%s/%s_%s.csv' % (output_dir, file_name[:-4], mesg_name), index=False)
                continue


if __name__ == '__main__':
    input_dir = r'Y:\昆易G3试采数据'
    output_dir = r"Y:\昆易G3试采数据\can_output"
    # bosch_asc2csv(input_dir, output_dir)
