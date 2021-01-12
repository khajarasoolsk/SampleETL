import pandas as pd
import datetime as dt
import os
import csv

FILEMASTERS = 'C:\\Users\\KhajaShaik\\Downloads\\masters.csv'

def DateCal():
#   Getting the Current Business date value from Calendar
    currentdt = dt.date.today()
    businessdt = currentdt - dt.timedelta(days=1)
    businessdate = businessdt.strftime("%Y-%m-%d")
    return businessdate

# One way of getting Header (Business Date) of Data File
def getHeaderDate(FileName):
#   Getting the Header Business Date value from Data file
    with open(FileName, newline = '') as f:
        reader = csv.reader(f)
        csv_header = next(reader)
    
    headerValue = csv_header[0]
    BDDataFile = headerValue[:len(headerValue)-8][len(headerValue[:len(headerValue)-8])-8:]
    #print("Business Date of the Data file: ",BDDataFile) #Businessdate Value

    return BDDataFile

def getRecordCount(fileNm):
#   Getting the Record Count Value from Data file 
#   recCount = 0
#   with open(fileNm, 'rb') as f:
#        for line in f:
#            recCount += 1
    df = pd.read_csv(fileNm, names = ['ID', 'LastName', 'FirstName', 'Name'], engine = 'python', skiprows = 1, skipfooter = 1)
    recCount = df.shape[0]

    return recCount

# Another way to get Header (BusinessDate) and Trailer record count of the Data File
def getHeaderTrailer(fileNm):
#   Validates the Header date, Trailer Count and return's values    
    recCount = 0
    with open(fileNm, 'r') as f:
        first_line = f.readline()
        BDData = first_line[:len(first_line)-9][len(first_line[:len(first_line)-9])-8:]
        BDDataFile = str(dt.datetime.strptime(BDData, '%Y%m%d').date())
        
        for last_line in f:
            pass
        TlrCnt = int(last_line[len(last_line)-8:])
        rcrdCnt = getRecordCount(fileNm)
        rcrdCntVal = 'Yes' if TlrCnt == rcrdCnt else 'No'

        currBD = DateCal()
        BDValidate = 'Yes' if BDDataFile == currBD else 'No'

        return BDDataFile, TlrCnt, BDValidate, rcrdCntVal

def extractDataFile(fileNm):
#   Extract the data and normalize the data along with Business date appended

    DataFileParam = getHeaderTrailer(fileNm)
    BusiDFile = DataFileParam[0]
    ExtractDataFileNm = os.path.splitext(fileNm)[0] + '_' + BusiDFile + '_' +'Extracted' + '_' + dt.datetime.now().strftime('%Y%m%d%H%M%S') + os.path.splitext(fileNm)[1]

    df = pd.read_csv(fileNm, names = ['ID', 'LastName', 'FirstName', 'Name'], engine = 'python', skiprows = 1, skipfooter = 1, doublequote = False)
    
    print("Business date of the Data file:", BusiDFile)
    print("Trailer Count of the Data file:", DataFileParam[1])

    if DataFileParam[2] != 'Yes':        
        print("Business date Validation Failed @ ", dt.datetime.now().strftime('%Y%m%d%H%M%S'))
        exit()

    else:
        print("Business date Validation Passed @ ", dt.datetime.now().strftime('%Y%m%d%H%M%S'))

        if DataFileParam[3] != 'Yes':            
            print("Trailer Count Validation Failed @ ", dt.datetime.now().strftime('%Y%m%d%H%M%S'))
            exit()

        else:
            print("Trailer Count Validation Passed @ ", dt.datetime.now().strftime('%Y%m%d%H%M%S'))

            try:
                df['Name'] = df['Name'].str.replace(r"[\"\',]", '', regex=True)
                df['BusinessDate'] = BusiDFile
                df.to_csv(ExtractDataFileNm, doublequote = False, index = False)

            except Exception as e:
                print(e)

            finally:
                print("Extraction Completed @ ",dt.datetime.now().strftime('%Y%m%d%H%M%S'))

def main():

    extractDataFile(FILEMASTERS)            

if __name__ == "__main__":
    main()
