#Customer Segmentation using RFM


##########################################################################################
#GOREV 1: Veriyi Anlama ve Hazırlama
##########################################################################################

#1. OnlineRetailIIexcelindeki2010-2011verisiniokuyunuz.Oluşturduğunuzdataframe’inkopyasınıoluşturunuz.

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x) #Buradaki fonksiyonun amacı nedir acaba bunu tam anlayamadan biraz kopyala yapıştır yaptım.

df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

#2. Veri setinin betimsel istatistiklerini inceleyiniz.

print("##################### Head #####################")
print(df.head())
print("##################### Shape #####################")
print(df.shape)
print("##################### Describe #####################")
print(df.describe().T)
print("##################### Types #####################")
print(df.dtypes)
print("##################### Quantity #####################")
print(df[df["Quantity"] < 0].head())

#Quantity değeri 0'dan küçük olan değerler var
#Bu sebeple iade işlemlerini hesaba katmayacağız
#df = df[~df["Invoice"].astype(str).str.contains("C", na=False)] bir nevi 8. soru cevabı


# Hızlı gözlem.
'''
   Hızlı bir gözlem
   ++++++++
   >>>>df.head()<<<
   Burada bir fatura üzerinden birden fazla ürün alınmış ve alınan ürünlerin adetleri birden farklı.
   Ayrıca bize ürünlerin birim fiyatlarını "Price" veriyor ama bir birim için veriyor.
   alınan toplam adetin ücreti mevcut değil,
   fatura başına ödenen ücret mevcut değil.
   Dert mi ?
   Tabi ki hayır. Biz yaparız.
   bize daha sonrası için fatura başına düşün ücret görmek istersek.
   Fatura kısmını groupby yaparız birde üstüne "total price sum()" ekledik mi ohh.
   Fatura çokluyor. Bundan dolayı CostumerID(Eşsiz kullanıcı kodları) ler çokluyor.Yine dert değillll.
   Ülkeler veriliyor.
   ++++++++++++++++++++
   >>>>df.shape()<<<<
    541910 gözlem var.
    ++++++++++++++++++++
   >>>>df.describe().T<<<<
   Sayısal değişkenlerin özet istatistiklerine baktığımızda 
   Quantity :  Satış mikatrı -80995 diyor. Vahit hoca rahatsız olmuştu. Bizde rahatsızız bu durumdan tabi.
               Şaka bir yana eksi miktarda adet olamayacağı için bizim dikkatimizi çekti.
               Çeyrekliklere baktığımızda ise %50-%75-max arası yine evlere şenlik dikkat çekici...
   Price :     Ortalama-9.5 std-218 min değer- -80995 arızalı bir veri belli işimiz var. 
               Ama kıyamadım seriside var tabii. 

   '''


#3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?

df.isnull().any()
df.isnull().sum()

print("##################### NA #####################")
print('Veri setinde', df.isnull().sum()[df.isnull().sum() > 0].index[0], 'degiskeninden',
      df.isnull().sum()[df.isnull().sum() > 0][0], df.isnull().sum()[df.isnull().sum() > 0].index[1], 'degiskeninden',
      df.isnull().sum()[df.isnull().sum() > 0][1] ,'eksik veri bulunmaktadir')

#4. Eksik gözlemleri verisetinden çıkartınız.Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.

df.dropna(inplace=True)

# Assignment ile de yapılabilirdi.
# Satırda, herhangi bir veya daha fazla sütuna ait değer boş ise satırı drop eder.
# Drop işleminden sonra boş değerin olmaması beklenir.

#5. Eşsiz ürün sayısı kaçtır?

df["StockCode"].nunique()

print('Veri setinde toplam', df['Description'].nunique(), 'essiz urun bulunmaktadir')

#6. Hangi üründen kaçar tane vardır?

df["Description"].value_counts().head()


#7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.

df.groupby("Invoice").agg({"Quantity": "sum"}).head(5).sort_values("Quantity", ascending=False)
df.head()
#burada ascending false dememizin bir sebebi nedir acaba ?

#8. Faturalardaki‘C’iptal edilen işlemleri göstermektedir.İptal edilen işlemleri veri setinden çıkartınız.

df = df[~df["Invoice"].str.contains("C", na=False)]

df = df[(df['Quantity'] > 0)]
df = df[(df['Price'] > 0)]

#9. Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.
df["TotalPrice"] = df["Quantity"] * df["Price"]

df.head()

##########################################################################################
#GOREV 2:RFM metriklerinin hesaplanması
##########################################################################################



# 1. Recency, Frequency ve Monetary tanımlarını yapınız.


#Recencey: En son tarih skoru. Burada 1 en yakın, 5 en uzak  tarih olmakta.
#Frequency:  Alışveriş sıklığı skoru.
#Monetary: Value: Bıraktığı parasal değer.



#2. Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
#3. Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.

#InvoiceDate --> Recency'e ulaşabilmek için
#Invoice --> Frequency'e ulaşabilmek için
#TotalPrice --> Monetary'e ulaşabilmek için


df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()

#Bir müşteriye gittik. Agg invoice date dediğimizde müşterinin yaptığı bütün alışveriş içinden en son alışveriş tarihini seçtik
#Frequency bulabilmek için müşterinin bütün Invoice larına gittik. Kaç tane unique fatura kesilmiş buna eriştik.
#Monetary erişmek için tüm faturalardaki toplam harcamasına eriştiğimiz TotalPrice'ı kullnadık



#4. Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

rfm.columns = ['recency', 'frequency', 'monetary']

# InvoiceData, Invoice, TotalPrice olan sütun adlarını değiştirmek için
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.
rfm = rfm[(rfm['monetary'] > 0)]


##########################################################################################
#GOREV 3:RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi
##########################################################################################


#1. Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
#2. Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

'''
#Recency değerinin küçük olması bizim açımızdan iyidir; bu sebeple labels'ı 5ten 1e yapılır
#qcut fonksiyonu ile 5 tane çeyrekliğe böl demiş oluyoruz. Küçükten büyüğe sıraladığı için küçük değer bizim için değerli olduğu için buna 5 değerini vererek başla demiş olduk.
#Daha küçük olan değerler skor tarafında 5 ile etiketlensin demiş olduk'
'''

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

'''
#Frekansta 1 değerlerinin çok olduğunu düşünelim. 100 tane mesela. 
# Bunu 5 parçaya böleceğiz. İlk aralıkta 20 tane 1. İkinci aralığa geçtiğimizde hala 1'ler devam ediyorsa bu rpoblem yaratıyor.
# Çünkü aralıkların unique olmasını istiyor fonksiyon. Bunun için rank(method="first") kullanılır. Böylece bu 1 değerleri 2 olarak etiketleyebiliyor.
'''

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])



rfm.head()








#Oluşan 2 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
#Örneğin;
#Ayrı ayrı değişkenlerde sırasıyla 5, 2 olan recency_score, frequency_score skorlarını RFM_SCORE değişkeni isimlendirmesi ile oluşturunuz.

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()

##########################################################################################
#GOREV 4:RFM skorlarının segment olarak tanımlanması
##########################################################################################


#Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız.
#Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()



##########################################################################################
#GOREV 5:Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;
#Hem aksiyon kararları açısından, hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız.
##########################################################################################
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])



#Recencey: En son tarih skoru. Burada 1 en yakın, 5 en uzak  tarih olmakta.
#Frequency:  Alışveriş sıklığı skoru.
#Monetary: Value: Bıraktığı parasal değer.


#NEW COSTUMER:##
# recency yüksek frequency düşüktür.Frequencyi artırmak ve kullanıcıları daha kalıcı hale
# getirmek için kampanya ya da indirim tanımlaması yapılabilir.

#CHAMPİONS:##
# recency düşük, frequency düşük. upsell & cross sell yapılabilir.
# İhtiyaçları olmasada alma eğilimlerini arttırmak için
# farklı kategorilerden birkaç ürünü birden içeren kombin ürünlere yönlendirme yapılabilir.

#CAN'T LOOSE:##
# Farklı kategorilerde ürün önerisi, indirim tanımlaması yapılabilir.

#"Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

rfm[rfm["segment"] == "loyal_customers"].head(14)


new_df = pd.DataFrame()
new_df["loyal_customers"] = rfm[rfm["segment"] == "loyal_customers"].index
new_df.head()
new_df.to_csv("loyal_customers.csv")



