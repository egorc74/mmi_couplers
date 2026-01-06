TODO

1)
python -m venv venv

2)
add lumapi.pth file into venv/lib/site-packages (change path in it if neccessary)

3)
venv/scripts/activate

4)
pip install -r requirements.txt


Potrebno je pognati skripto convergence_tests v mapi mmi_1x2\convergence_tests\convergence_tests.py

V Skripti se nahajata najprej simulacije za TE mode in nato za TM mode.

V args pri vsaki simulacije je potrebno vpisati optimalne vrednosti spremenljivk (npr. z_span FDTD domene, za katerega se odlocimo, da je optimalen) 

V args se tudi vpise cello obmocje na katerem delamo teste konvergence (npr. z_span=np.linspace(1.8e-6,2.5e-6,10)) 

