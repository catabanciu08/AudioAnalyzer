# AudioAnalyzer
Python Project that analyzes an audio file, extracting the time intervals where the discussion gets heated  
------
Prezentul proiect de Python vizează analiza unui fișier audio și determinarea intervalelor de timp unde discuția devine încinsă. 
Salut, sunt Cătălin Banciu și am absolvit track-ul de Web Development Intermediar în 2024, fiind de asemenea Ambasador Generația Tech. 
Stăpânesc limbajul de programare Python la un nivel junior. Pentru prezentul proiect, am folosit librăria de Python librosa, care mi s-a părut a fi cea mai potrivită, având în vedere sarcina dată. 
Identificarea intervalelor de timp unde discuția devine încinsă a fost realizată în trei moduri diferite:
1.	Folosind amplitudinea semnalului pe diferite porțiuni din înregistrare
2.	Folosind o „învelitoare” (envelope) aplicată pe semnal
3.	Folosind spectrul de frecvențe ale fișierului audio, determinat cu ajutorul transformatei Fourier
Fiecare abordare este scrisă într-un fișier .py, iar intervalele de timp sunt exportate în format .csv (într-un fișier corespunzător, distinct pentru fiecare abordare) 
----
Mai multe detalii se găsesc în fișierul Raport.docx
