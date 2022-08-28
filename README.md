# Algorithmic-Trading

SPY strategi:
Veldig enkel strategi. Algoritmen vil umiddelbart foreta et et kjøp av SPY. <br/>
Deretter vil algoritmen overvåke posisjonen, <br/>
og så fort posisjonen enten har en profit på over 10% eller et tap over 10% vil den likvidere hele posisjonen. <br/>
Etter posisjonen er likvidert, vil bot-en vente 30 dager, før syklusen starter på nytt. <br/>
<br/>
VOO strategi:
Bruker bot-en til å identifisere om VOO er i en uptrend eller downtrend. <br/>
For å bestemme dette bruker jeg simple moving average (SMA). <br/>
Samtidig sammenligner jeg nåværende pris med den 52-week high og 52-week low. <br/>
Derretter tas følgende beslutning:<br/>
Dersom VOO above SMA + near 52-week high = buy <br/>
Dersom VOO below SMA + near 52-week low = sell <br/>
Alle andre situasjoner = ingen aktiv posisjon <br/>



## VOO trade results:
<img width="732" alt="Screenshot 2022-08-28 at 11 28 07" src="https://user-images.githubusercontent.com/91557392/187067379-599b4350-e185-4c63-8bed-aee8eff7067d.png">
<img width="642" alt="Screenshot 2022-08-28 at 11 29 10" src="https://user-images.githubusercontent.com/91557392/187067380-61686b26-1996-4917-a9af-fc88dd3de9ad.png">
<img width="643" alt="Screenshot 2022-08-28 at 11 31 37" src="https://user-images.githubusercontent.com/91557392/187067382-5947786b-cd7e-438a-acd9-c94585849ffb.png">


## SPY trade results:
<img width="1071" alt="Screenshot 2022-08-28 at 11 34 03" src="https://user-images.githubusercontent.com/91557392/187067478-8bfe81ad-86a4-4669-9ddf-ea398df13f61.png">
<img width="884" alt="Screenshot 2022-08-28 at 11 34 13" src="https://user-images.githubusercontent.com/91557392/187067479-09479aad-8ac8-42af-98af-0df4d55d2543.png">
