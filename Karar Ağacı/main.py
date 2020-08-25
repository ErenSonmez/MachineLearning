import pandas as pd
import math
import pickle

#Verisetini karıştırmak için
from sklearn.utils import shuffle

class karar_agaci():
    def __init__(self,veriseti,veriseti_test,label_sutun_adi):
        self.veriseti=veriseti
        self.veriseti_test=veriseti_test
        self.label_sutun_adi=label_sutun_adi

        self.dugum_adi=None
        self.dugumler=None
        self.kategoriler=None

        for sutun in self.veriseti:
            for hucre in sutun:
                if str(hucre)=='NaN':
                    hucre=None
        
    #Verisetindeki sayısal değer içeren sütunları değerlerine göre
    #3 kategoriye ayırır : D (düşük), O(orta), Y(yüksek)
    def veriseti_donustur(self,csv_dosya_kayit_adi=None):    
        min_degerler=self.veriseti.min()
        max_degerler=self.veriseti.max()
        
        for sutun in self.veriseti.columns:
            if type(max_degerler[sutun])==int or type(max_degerler[sutun])==float:
                fark=max_degerler[sutun]-min_degerler[sutun]
                #Alt limitten küçükse düşük
                #Alt limitle üst limit arasındaysa orta
                #Üst limitten büyükse yüksek
                alt_limit=min_degerler[sutun]+(fark*0.33)
                ust_limit=min_degerler[sutun]+(fark*0.66)
                for satir in self.veriseti.index:
                    if self.veriseti.loc[satir,sutun]<alt_limit:
                        self.veriseti.loc[satir,sutun]='D'
                    elif self.veriseti.loc[satir,sutun]<ust_limit:
                        self.veriseti.loc[satir,sutun]='O'
                    else:
                        self.veriseti.loc[satir,sutun]='Y'

        if csv_dosya_kayit_adi!=None:##
            self.veriseti.to_csv(csv_dosya_kayit_adi,index=False)

    def dallanma(self):
        label_entropi=self.entropi_hesapla(self.label_sutun_adi)
        sutun_entropileri={}
        kazanc=float('-inf')
        kazanc_sutun=None

        #label_entropi 0 çıktığından terminal node'a ulaştığımızı
        #anlayıp değerini atıyoruz.
        if label_entropi==0:
            print('Terminal nodea ulaşıldı:')
            print(self.veriseti[self.label_sutun_adi].tolist())
            if len(self.veriseti[self.label_sutun_adi].tolist())<1:
                return
            
            print(self.label_sutun_adi+':'+self.veriseti[self.label_sutun_adi].tolist()[0])
            #self.dugum_adi=self.label_sutun_adi+':'+self.veriseti[self.label_sutun_adi].tolist()[0]
            self.dugum_adi=self.veriseti[self.label_sutun_adi].tolist()[0]
            self.dugumler='Terminal'
            return
        
        print()
        print()
        print('Entropiler hesaplanıyor...')
        print()
        print()
        
        for sutun in self.veriseti.columns:
            if sutun==self.label_sutun_adi:
                continue

            print(sutun,'entropisi hesaplanıyor...')
            sutun_entropileri[sutun]=self.entropi_hesapla(sutun)
            temp=label_entropi-sutun_entropileri[sutun]
            print(sutun,'entropisi:',sutun_entropileri[sutun])
            print()
            print()
            
            if temp>kazanc:
                kazanc=temp
                kazanc_sutun=sutun
                
        print('Entropiler:')
        print(sutun_entropileri)
        
        print('Kazancı en yuksek sutun:',kazanc_sutun)
        #Bulduğumuz düğümü düğüm adı olarak kaydedip
        #dallanmadan gelecek düğümleri dictionary olarak
        #tutuyorum
        self.dugum_adi=kazanc_sutun
        self.dugumler={}

        for kategori in self.kategoriler[kazanc_sutun]:
            if kategori==None:
                continue
            temp=self.veriseti.copy()
            
            silinecek_indexler=temp[temp[kazanc_sutun]!=kategori].index
            temp.drop(silinecek_indexler,axis='index',inplace=True)
            temp.drop(kazanc_sutun,axis='columns',inplace=True)

            self.dugumler[kategori]=karar_agaci(temp,None,self.label_sutun_adi)
            print(temp)
            print(self.dugumler)
            self.dugumler[kategori].dallanma()
        
    #İsmi verilen sütunun kategorilerini sayar.
    #DataFrame olarak döndürülür.
    def kategori_sayisi(self,sutun_adi):
        self.kategori_bul()
        hucre_kategori=self.kategoriler[sutun_adi]
        kategori_sayi=[]
        
        for i in range(len(hucre_kategori)):#None olan hücreleri çıkarmak için.
            if hucre_kategori[i]==None:
                hucre_kategori.pop(i)

        for i in range(len(hucre_kategori)):
            kategori_sayi.append(0)
        
        df=pd.DataFrame(kategori_sayi,index=self.kategoriler[sutun_adi], columns=['total'])
        for hucre in self.veriseti[sutun_adi]:
            df.loc[hucre]+=1

        for label_kategori in self.kategoriler[self.label_sutun_adi]:
            if label_kategori!=None:
                df[label_kategori]=0
        
        for satir in self.veriseti.index:     
            df.loc[self.veriseti.loc[satir,sutun_adi],self.veriseti.loc[satir,self.label_sutun_adi]]+=1
        
        return df

    def entropi_hesapla(self,sutun_adi):
        kategori_sayisi=self.kategori_sayisi(sutun_adi)
        toplam=0
        entropi=0
        print(kategori_sayisi)
        #Tek attribute ile entropi
        if sutun_adi==self.label_sutun_adi:
            for hucre in kategori_sayisi['total']:
                toplam+=hucre

            for index in kategori_sayisi.index:
                oran=float(kategori_sayisi.loc[index,'total'])/float(toplam)
                entropi-=oran*math.log(oran,2)
        #İki attribute ile entropi
        elif sutun_adi in self.kategoriler.columns:
            for hucre in kategori_sayisi['total']:
                toplam+=hucre
                
            for index in kategori_sayisi.index:
                oran=float(kategori_sayisi.loc[index,'total'])/float(toplam)
                entropi+=oran*(self.entropi_sayisal(index,kategori_sayisi))
        else:
            print('Hatalı sütun adı')
            return

        return entropi
        
    #İki attribute ile entropi formülünün daha okunaklı
    #olması için bu fonksiyonu yazdım
    def entropi_sayisal(self,satir_adi,kategori_sayisi):
        entropi=0
        for sutun in kategori_sayisi.loc[satir_adi,:].index:
            if sutun!='total':
                oran=float(kategori_sayisi.loc[satir_adi,sutun])/float(kategori_sayisi.loc[satir_adi,'total'])

                if oran==1:
                    return 0
                if oran==0:
                    continue
                entropi-=oran*math.log(oran,2)
        return entropi

    
    
    #Verisetinin kategorilerini tespit eder ve DataFrame olarak kaydeder.
    def kategori_bul(self):
        kategoriler=[]
        for sutun in self.veriseti.columns:
            kategoriler.append([])
            i=len(kategoriler)-1
            for satir in self.veriseti.index:
                hucre=self.veriseti.loc[satir,sutun]
                if (hucre in kategoriler[i])==False:
                    kategoriler[i].append(hucre)
                    
        df=pd.DataFrame(kategoriler,index=self.veriseti.columns)
        self.kategoriler=df.transpose()
        self.kategoriler.replace('NaN',None,inplace=True)
        self.kategoriler_tam_yazdir()

    def veriseti_tam_yazdir(self):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self.veriseti)

    def kategoriler_tam_yazdir(self):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self.kategoriler)

    def karar_agaci_yazdir(self):
        while True:
            if self.dugumler=='Terminal':
                print('Düğüm:',self.dugum_adi)
                print('Yapraklar: Terminal node')

                secim=str(input('Terminal nodea ulaşıldı. Geri gitmek için -1 girin: '))
                if secim=='-1':
                    print()
                    print()
                    break
                else:
                    print('Hatalı girdi')
                    print()
                    print()
            else:
                print('Düğüm:',self.dugum_adi)
                print('Yapraklar: ',end='')
                for index in self.dugumler.keys():
                    print(index+' ', end='')
                print()
                
                secim=str(input('Gitmek istediğiniz yaprağı girin (Geri gitmek için -1 girin): '))
                if secim=='-1':
                    print()
                    print()
                    break
                elif secim in self.dugumler.keys():
                    print()
                    print()
                    self.dugumler[secim].karar_agaci_yazdir()
                else:
                    print('Hatalı girdi')
                    print()
                    print()

    def accuracy(self):
        dogru_tahmin=0
        
        for i in self.veriseti_test.index:
            dugumler=self.dugumler
            dugum_adi=self.dugum_adi
            while dugumler!='Terminal':
                temp=dugumler
                dugumler=temp[self.veriseti_test.loc[i,dugum_adi]].dugumler
                dugum_adi=temp[self.veriseti_test.loc[i,dugum_adi]].dugum_adi

            if dugum_adi==self.veriseti_test.loc[i,self.label_sutun_adi]:
                dogru_tahmin+=1
                
        return dogru_tahmin/len(self.veriseti_test)


    #Karar ağacını pickle ile kaydeder.
def karar_agaci_kaydet(ka,dosya_adi):
    f=open(dosya_adi,'wb')
    pickle.dump(ka,f)
    f.close()


#Önceden kaydedilmiş karar ağacını pickle ile yükler
def karar_agaci_yukle(dosya_adi):
    f=open(dosya_adi,'rb')
    ka=pickle.load(f)
    f.close()
    return ka

if __name__=='__main__':
    df=pd.read_csv('mushrooms.csv')
    
    #Verisetini karıştırmak için.
    df=shuffle(df)
    
    test_orani=0.2
    test_baslangic_index=int(len(df)*(1-test_orani))

    df_train=df.iloc[:test_baslangic_index,:]
    df_test=df.iloc[test_baslangic_index:,:]

    ka=karar_agaci(df_train,df_test,'class')

    ka.dallanma()
    print('Accuracy: 'ka.accuracy())
    
    ka.karar_agaci_yazdir()
