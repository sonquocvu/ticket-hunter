from stageData import nhaHatBenThanh
from stageData import nhaVanHoaThanhNien
class StateDataHandling:
    def __init__(self):
        self.__seatCoordinateTable = {
            "nha-hat-ben-thanh": nhaHatBenThanh,
            "nha-van-hoa-thanh-nien": nhaVanHoaThanhNien
        }

        self.__rowList = {
            "nha-hat-ben-thanh": {
                "Vip": ["E", "F", "G", "H"],
                "Normal": ["O", "P", "Q", "R"]
            },
            "nha-van-hoa-thanh-nien": {
                "Vip": ["C", "D", "E", "F"],
                "Normal": ["J", "K", "L", "M"]
            }
        }

        self.__rowKeyList = {
            "Vip": ["-VIP-1-", "-VIP-2-", "-VIP-3-", "-VIP-4-"],
            "Normal": ["-NORMAL-1-", "-NORMAL-2-", "-NORMAL-3-", "-NORMAL-4-"]
        }

        self.__stageList = {
            "Nhà Hát Bến Thành": "nha-hat-ben-thanh",
            "Nhà Văn Hóa Thanh Niên": "nha-van-hoa-thanh-nien",
            "Sân Khấu Kịch Idecaf": "san-khau-kich-Idecaf",
            "Sân Khấu Kịch Trương Hùng Minh": "san-khau-kich-truong-hung-minh"
        }

    def get_seats_coordinate(self, stageName: str):
        m_stageName = self.__stageList[stageName]
        return self.__seatCoordinateTable[m_stageName]

    def get_stage_list(self):
        return list(self.__stageList.keys())

    def get_row(self, stageName: str):
        m_stageName = self.__stageList[stageName]
        return self.__rowList[m_stageName]

    def get_row_key(self):
        return self.__rowKeyList
