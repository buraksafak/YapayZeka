"""
OZEL KUVVETLER ASKERI PERSONEL ALIM ALGORITMASI
* Girisler
   - 'fiziksel_guc'
      * Adayin fiziksel gucu 0 ile 10 arasinda ne derecede?
      * Fuzzy kumeler: kotu, orta, iyi
   - 'psikolojik_guc'
      * Adayin psikolojik gucu 0 ile 10 arasinda ne derecede?
      * Fuzzy kumeler: kotu, orta, iyi
   - 'atis_yetenegi'
      * Adayin atis yetenegi 0 ile 10 arasinda ne derecede?
      * Fuzzy kumeler: kotu, orta, iyi
* Cikis
   - 'kabul_edilme'
      * %0'dan %100'e kabul edilme ihtimali nedir?
      * Fuzzy kumeler: yok, belki, kesin
* Kurallar
   - Eger *fiziksel_guc* iyi *ve* *psikolojik_guc* iyi *ve* *atis_yetenegi* iyi     ise kabul edilme olasiligi kesin 
   - Eger *fiziksel_guc* iyi *ve* *psikolojik_guc* orta *ve* *atis_yetenegi* iyi     ise kabul edilme olasiligi kesin
   - Eger *fiziksel_guc* orta *ve* *psikolojik_guc* iyi *ve* *atis_yetenegi* iyi     ise kabul edilme olasiligi kesin
   - Eger *fiziksel_guc* iyi *ve* *psikolojik_guc* iyi *ve* *atis_yetenegi* orta     ise kabul edilme olasiligi kesin
   - Eger *fiziksel_guc* orta *ve* *psikolojik_guc* orta *ve* *atis_yetenegi* iyi     ise kabul edilme olasiligi belki
   - Eger *fiziksel_guc* orta *ve* *psikolojik_guc* iyi *ve* *atis_yetenegi* orta     ise kabul edilme olasiligi belki
   - Eger *fiziksel_guc* iyi *ve* *psikolojik_guc* orta *ve* *atis_yetenegi* orta     ise kabul edilme olasiligi belki
   - Eger *fiziksel_guc* kotu *ya da* *psikolojik_guc* kotu *ya da* *atis_yetenegi* kotu     ise kabul edilme olasiligi yok
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as karar

fiziksel_guc = karar.Antecedent(np.arange(0, 11, 1), 'fiziksel_guc')
psikolojik_guc = karar.Antecedent(np.arange(0, 11, 1), 'psikolojik_guc')
atis_yetenegi = karar.Antecedent(np.arange(0, 11, 1), 'atis_yetenegi')
kabul_edilme = karar.Consequent(np.arange(0, 101, 1), 'kabul edilme olasiligi')

fiziksel_guc['kotu'] = fuzz.trimf(fiziksel_guc.universe, [0, 0, 5])
fiziksel_guc['orta'] = fuzz.trimf(fiziksel_guc.universe, [0, 5, 10])
fiziksel_guc['iyi'] = fuzz.trimf(fiziksel_guc.universe, [5, 10, 10])

psikolojik_guc['kotu'] = fuzz.trimf(psikolojik_guc.universe, [0, 0, 7])
psikolojik_guc['orta'] = fuzz.trimf(psikolojik_guc.universe, [0, 7, 10])
psikolojik_guc['iyi'] = fuzz.trimf(psikolojik_guc.universe, [7, 10, 10])

atis_yetenegi['kotu'] = fuzz.trimf(atis_yetenegi.universe, [0, 0, 7])
atis_yetenegi['orta'] = fuzz.trimf(atis_yetenegi.universe, [0, 7, 10])
atis_yetenegi['iyi'] = fuzz.trimf(atis_yetenegi.universe, [7, 10, 10])

kabul_edilme['yok'] = fuzz.trimf(kabul_edilme.universe, [0, 0, 51])
kabul_edilme['belki'] = fuzz.trimf(kabul_edilme.universe, [0, 51, 101])
kabul_edilme['kesin'] = fuzz.trimf(kabul_edilme.universe, [51, 101, 101])

#fiziksel_guc.view()

kural1 = karar.Rule(fiziksel_guc['iyi'] & psikolojik_guc['iyi'] & atis_yetenegi['iyi'], kabul_edilme['kesin'])
kural2 = karar.Rule(fiziksel_guc['iyi'] & psikolojik_guc['orta'] & atis_yetenegi['iyi'], kabul_edilme['kesin'])
kural4 = karar.Rule(fiziksel_guc['orta'] & psikolojik_guc['iyi'] & atis_yetenegi['iyi'], kabul_edilme['kesin'])
kural5 = karar.Rule(fiziksel_guc['iyi'] & psikolojik_guc['iyi'] & atis_yetenegi['orta'], kabul_edilme['kesin'])
kural6 = karar.Rule(fiziksel_guc['orta'] & psikolojik_guc['orta'] & atis_yetenegi['iyi'], kabul_edilme['belki'])
kural3 = karar.Rule(fiziksel_guc['orta'] & psikolojik_guc['iyi'] & atis_yetenegi['orta'], kabul_edilme['belki'])
kural7 = karar.Rule(fiziksel_guc['iyi'] & psikolojik_guc['orta'] & atis_yetenegi['orta'], kabul_edilme['belki'])
kural8 = karar.Rule(fiziksel_guc['kotu'] | psikolojik_guc['kotu'] | atis_yetenegi['kotu'], kabul_edilme['yok'])

teklif_ = karar.ControlSystemSimulation(karar.ControlSystem([kural1, kural2, kural3, kural4, kural5, kural6, kural7, kural8]))

teklif_.input['fiziksel_guc'] = 10
teklif_.input['psikolojik_guc'] = 5
teklif_.input['atis_yetenegi'] = 10

teklif_.compute()

print(teklif_.output['kabul edilme olasiligi'])
kabul_edilme.view(sim=teklif_)
