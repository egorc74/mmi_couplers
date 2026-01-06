
Potrebno je pognati skripto convergence_tests v mapi mmi_1x2\convergence_tests\convergence_tests.py

1)V Skripti se nahajata najprej simulacije za TE mode in nato za TM mode.

2)V args pri vsaki simulacije je potrebno vpisati optimalne vrednosti spremenljivk (npr. z_span FDTD domene, za katerega se odlocimo, da je optimalen) 

3)V args se tudi vpise cello obmocje na katerem delamo teste konvergence (npr. z_span=np.linspace(1.8e-6,2.5e-6,10)) 


Vsak test v skripti ima parameter RUN_AGAIN=False. Vsaka iteracija se shrani v podmapi chunks. V primeru, da skripta crasha, ali se zgodi kaksna druga napaka, lahko nastavimo RUN_AGAIN=True , ki bo nadaljevala simulacijo od zadnje iteracije oz. od zadnjega shranjenega chunka, in bo zlepla vse rezultate v isto datoteko.
