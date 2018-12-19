def hexToBinary(data):
    return bin(int(data, 16))[2:].zfill(8)

def binaryToDecimal(data):
    return int(data, 2)

def getMeasurementType(data):
    if data[0] == "0" and data[1] == "0":
        return "Single Measurement"
    elif data[0] == "1" and data[1] == "0":
        return "Multi-Read Measurement"
    elif data[0] == "1" and data[1] == "1":
        return "Average of Multi-Read"
    else:
        return "Error"

class MeasurementMemoryData():
    def __init__(self, data):
        try:
            hexData = data.split(" ")[1]
            hexData = hexData.split("-")
            if len(hexData) != 13:
                raise Exception("format error")
            binaryData = [hexToBinary(each) for each in hexData]

            # BYTE00 (initial year + measurement data byte00 bit7-4 + base year number (2000 decimal))
            self.year = 16 + binaryToDecimal(binaryData[4][0:4]) + 2000
            self.month = binaryToDecimal(binaryData[4][4:8])

            # BYTE01
            self.day = binaryToDecimal(binaryData[5][3:8])

            # BYTE02
            self.hour = binaryToDecimal(binaryData[6][4:8])
            self.ihbFlag = "IHB" if binaryToDecimal(binaryData[6][3]) == 1 else "none IHB"
            self.measurementType = getMeasurementType(binaryData[6][1:3])
            self.ampm = "AM" if binaryToDecimal(binaryData[6][0]) == 0 else "PM"

            # BYTE03
            self.minute = binaryToDecimal(binaryData[7][2:8])

            # BYTE04
            self.systolicHundredDigit = binaryToDecimal(binaryData[8][0:4])
            self.diastolicHundredDigit = binaryToDecimal(binaryData[8][4:8])

            # BYTE05
            self.systolicTensUnitsDigit = 10 * binaryToDecimal(binaryData[9][0:4]) + binaryToDecimal(binaryData[9][4:8])

            # BYTE06
            self.diastolicTensUnitsDigit = 10 * binaryToDecimal(binaryData[10][0:4]) + binaryToDecimal(binaryData[10][4:8])

            # BYTE07
            self.heartRate = binaryToDecimal(binaryData[11])

            self.systolic = 100 * self.systolicHundredDigit + self.systolicTensUnitsDigit
            self.diastolic = 100 * self.diastolicHundredDigit + self.diastolicTensUnitsDigit
        except Exception as exception:
            self.year = None
            self.month = None
            self.day = None
            self.hour = None
            self.ihbFlag = None
            self.measurementType = None
            self.ampm = None
            self.minute = None
            self.systolic = None
            self.diastolic = None
            self.heartRate = None
            print("Exception occurs: {}, data: {}".format(exception, data))

if __name__ == "__main__":
    data = "(0x) 33-38-09-04-01-01-05-0A-10-19-64-4E-2A"
    testData = MeasurementMemoryData(data)
    print("Date:\n{}/{}/{} {}:{}{}\n".format(testData.year, testData.month, testData.day, testData.hour, testData.minute, testData.ampm))
    print("Measurement information:\nSystolic: {}\nDiastolic: {}\nHeart Rate: {}\n".format(testData.systolic, testData.diastolic, testData.heartRate))
    print("Other information:\nIHB Flag: {}\nMeasurement Type(Single, Multi-Read...): {}\n".format(testData.ihbFlag, testData.measurementType))
