# ProjektR

3.11.2022<br />
-dodan trenutni dataset, podlozno promjeni<br />
-proveden prvi OCR ne daje ocekivane rezultate, problem se pojavljuje kod slike sa blijedim tekstom<br />
-na dodanim slikama proveden samo threshold, iako sharpen i promjena kontrasta za neke slike daju bolje rezultate<br />
<br />
4.11.22<br />
-dodan folder za procesirane slike<br />
-popravljen route izmedu test.py i dataset foldera<br />
-modificiran path da radi za svakog usera koji klonira repo<br />
<br />
14.11.22<br />
-dodana deskew.py funkcija koja se koristi kod korekcije kuta slike<br />
-postavljen route izmedu dataset foldera i deskew.py, slike se uspjesno ucitavaju i spremaju u odgovarajuce foldere<br />