import quandl
import pickle

def DownloadQuandlData(quandl_data):
    df=quandl.get(quandl_data)
    file=open('quandl_data.pickle','wb')
    pickle.dump(df,file)
    file.close()

def GetQuandlData(filename):
    file=open(filename,'rb')
    df=pickle.load(file)
    file.close()
    return df

if __name__=='__main__':
    DownloadQuandlData('WIKI/GOOGL')
