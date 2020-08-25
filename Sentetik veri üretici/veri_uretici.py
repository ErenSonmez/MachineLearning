import pandas as pd
from random import randint

class sentetik_veri_uretici():
    def __init__(self, oznitelik_bilgileri, veri_sayisi, korelasyon_katsayisi):
        self.oznitelik_bilgileri=oznitelik_bilgileri
        self.veri_sayisi=veri_sayisi
        self.korelasyon_katsayisi=korelasyon_katsayisi
        
        self.veriseti=None
        
    def veri_uret(self):
        veriseti=[]
        for i in range(self.veri_sayisi):
            veriseti.append([])
            for oznitelik in self.oznitelik_bilgileri[1]:
                if oznitelik[0]>oznitelik[1]:
                    temp=oznitelik[0]
                    oznitelik[0]=oznitelik[1]
                    oznitelik[1]=temp
                    
                oznitelik_deger=float(randint(oznitelik[0], oznitelik[1]))
                veriseti[len(veriseti)-1].append(oznitelik_deger)
                
        self.veriseti=pd.DataFrame(veriseti, columns=self.oznitelik_bilgileri[0])
        
    def veri_ekle(self,veriseti,veri_sayisi):
        for i in range(veri_sayisi):
            veriseti.append([])
            for oznitelik in self.oznitelik_bilgileri[1]:
                if oznitelik[0]>oznitelik[1]:
                    temp=oznitelik[0]
                    oznitelik[0]=oznitelik[1]
                    oznitelik[1]=temp
                    
                oznitelik_deger=float(randint(oznitelik[0], oznitelik[1]))
                veriseti[len(veriseti)-1].append(oznitelik_deger)
                
        self.veriseti=pd.DataFrame(veriseti, columns=self.oznitelik_bilgileri[0])
        
    def korelasyon_kontrol(self):
        korelasyon_katsayisi=self.korelasyon_katsayisi_hesapla()
        satir_etkisi=[]#Her satırın korelasyon katsayısını ne kadar etkilediğini tutar.
        ortalamalar=[]
        cikarilacaklar=[]
        
        temp=1
        print('Korelasyon katsayısı : ',korelasyon_katsayisi)
        if self.korelasyon_katsayisi<0:#Bu durumda satır etkisinin en küçük olmasını isteriz. En büyükleri çıkaracagız
            while korelasyon_katsayisi>self.korelasyon_katsayisi:
                veriseti=self.veriseti.values.tolist()
                
                for sutun in self.veriseti.columns:
                    ortalamalar.append(self.veriseti.loc[:,sutun].mean())
                    
                for satir in veriseti:
                    for i in range(len(satir)):
                        temp*=float(satir[i]-ortalamalar[i])
                    satir_etkisi.append(temp)
                    temp=1
                    
                temp_list=satir_etkisi[:]
                print(temp_list)
                
                cikarilacak_eleman_sayisi=int(len(temp_list)/100)
                
                for i in range(cikarilacak_eleman_sayisi):
                    index=temp_list.index(max(temp_list))
                    temp_list[index]=float('-inf')#Bu indexi tekrar seçmemesi için.
                    cikarilacaklar.append(index)
                    print(index)
                    
                cikarilacaklar.sort(reverse=True)#Sondan çıkarmaya baslaması icin.
                
                print(len(cikarilacaklar))
                print(cikarilacaklar)
                print(veriseti)
                
                for i in cikarilacaklar:
                    veriseti.pop(i)
                    
                self.veri_ekle(veriseti,cikarilacak_eleman_sayisi)
                korelasyon_katsayisi=self.korelasyon_katsayisi_hesapla()
                cikarilacaklar=[]
                satir_etkisi=[]
                print('Korelasyon katsayısı : ',korelasyon_katsayisi,len(veriseti))
        
        elif self.korelasyon_katsayisi>0:#Bu durumda satır etkisinin en büyük olmasını isteriz. En küçükleri çıkaracagız.
            while korelasyon_katsayisi<self.korelasyon_katsayisi:
                veriseti=self.veriseti.values.tolist()
                
                for sutun in self.veriseti.columns:
                    ortalamalar.append(self.veriseti.loc[:,sutun].mean())
                    
                for satir in veriseti:
                    for i in range(len(satir)):
                        temp*=float(satir[i]-ortalamalar[i])
                    satir_etkisi.append(temp)
                    temp=1
                    
                temp_list=satir_etkisi[:]
                print(temp_list)

                cikarilacak_eleman_sayisi=int(len(temp_list)/100)
                
                for i in range(cikarilacak_eleman_sayisi):
                    index=temp_list.index(min(temp_list))
                    temp_list[index]=float('inf')#Bu indexi tekrar seçmemesi için.
                    cikarilacaklar.append(index)
                    print(index)
                    
                cikarilacaklar.sort(reverse=True)#Sondan çıkarmaya baslaması icin.
                
                print(len(cikarilacaklar))
                print(cikarilacaklar)
                print(veriseti)
                
                for i in cikarilacaklar:
                    print(veriseti[i])
                    veriseti.pop(i)
                    
                self.veri_ekle(veriseti,cikarilacak_eleman_sayisi)
                korelasyon_katsayisi=self.korelasyon_katsayisi_hesapla()
                cikarilacaklar=[]
                satir_etkisi=[]
                print('Korelasyon katsayısı : ', korelasyon_katsayisi,len(veriseti))
            
        
    def normalizasyon_minmax(self):
        min_degerler=self.veriseti.min()
        max_degerler=self.veriseti.max()
        
        for i in range(len(max_degerler)):
            hucre_min=float(min_degerler[i])
            hucre_max=float(max_degerler[i])
            
            for j in range(len(self.veriseti.index)):
                hucre=float(self.veriseti.iloc[j][i])
                self.veriseti.iloc[j][i]=(hucre-hucre_min)/(hucre_max-hucre_min)
                
    def normalizasyon_z_score(self):
        for sutun in self.veriseti.columns:
            if sutun!='Sınıf':
                standart_sapma=self.veriseti.loc[:,sutun].std()
                ortalama=self.veriseti.loc[:,sutun].mean()
                for satir in self.veriseti.index:
                    hucre=float(self.veriseti.loc[satir,sutun])
                    self.veriseti.loc[satir,sutun]=float((hucre-ortalama)/standart_sapma)
        
    def korelasyon_katsayisi_hesapla(self):
        ortalamalar=[]
        
        standart_sapmalar=[]
        standart_sapmalar_carpimi=float(1)
        
        kovaryans=float(0)
        temp=float(1)
        
        df=self.veriseti
        veriseti=df.values.tolist()
        for sutun in df.columns:
            ortalamalar.append(df.loc[:,sutun].mean())
            standart_sapmalar.append(df.loc[:,sutun].std())
            
        for satir in veriseti:
            for i in range(len(satir)):
                temp*=float(satir[i]-ortalamalar[i])
                
            kovaryans+=temp
            temp=float(1)
        kovaryans/=float(len(veriseti)-1)
        
        for ss in standart_sapmalar:
            standart_sapmalar_carpimi*=float(ss)
            
        korelasyon_katsayisi=float(kovaryans/standart_sapmalar_carpimi)
        
            
        return korelasyon_katsayisi
        
    def yazdir(self):
        print(self.veriseti)
