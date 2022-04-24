Quanto ho capito su dc2 (warning: lungo)

Immaginiamo di avere un intervallo chiuso sulla retta reale (al caso discreto pensiamo dopo), dato da [x_min, x_MAX]. Immaginiamo di scegliere a caso un numero reale che vive in questo intervallo, con una distribuzione di probabilità costante: λ = 1/(x_MAX - x_min). Aggiungiamolo ad una partizione dell'intervallo P_1 = {x_min, x_1, x_MAX}, e ripetiamo il processo N volte (scegliamo gli indici non in ordine di estrazione, ma in ordine crescente). Avremo una partizione P_N = {x_min, x_1, x_2, ..., x_N, x_MAX} dell'intervallo data da N+2 elementi. Dimentichiamoci di x_min e x_MAX e concentriamoci sugli N elementi estratti. Come sono distribuiti?

Questo che ho appena descritto è il [processo di Poisson](https://en.wikipedia.org/wiki/Poisson_point_process). È il modello nullo di eventi indipendenti del problema che dobbiamo risolvere in dc2. Si chiama così perché, scelto un sottointervallo [a,b], il numero di elementi che ci aspettiamo di trovarci dentro è dato da una distribuzione di Poisson. Se ci pensate è evidente: il numero medio di elementi che mi aspetto di trovare in [a,b] è N x λ x (b - a), e la distribuzione che descrive quanti elementi mi aspetto di trovare sapendo la media è proprio la distribuzione di Poisson.

Se adesso guardo gli incrementi (Δx_i = x_{i+1} - x_i), detti _interarrivals_, come sono distribuiti? La risposta è: una [distribuzione esponenziale](https://en.wikipedia.org/wiki/Exponential_distribution), cioè una funzione esponenziale normalizzata dal coefficiente negativo. Non solo, posso anche dire quale sia il coefficiente: λ! La distribuzione ha infatti forma f(x,λ) = λ exp(-λx). La dimostrazione di questi due fatti si trova di solito nei libri di statistica (vedi bibliografia di wikipedia), che io non comprerò, ma credo basterà affermare questo fatto come se fosse un fatto (che del resto è) senza indugi nel report.

Ok, adesso ho in mente un possibile test per capire se un dataset segue il modello nullo. Basta confermare che gli interarrivals seguono una distribuzione esponenziale, per esempio con un fit. Oppure potrei scegliere tantissimi sottointervalli di uguale lunghezza e vedere Poisson (lame). 

Sugli stimatori: qui non serve fare niente, sono già stati fatti da matematici molto più svegli di noi. Il più famoso e meglio tagliato per questo problema è la [statistica di Hopkins](https://en.wikipedia.org/wiki/Hopkins_statistic). L'anno scorso alcuni studenti hanno anche provato a fare altre cose, tipo [Anderson-Darling](https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test) o [Kolmogorov–Smirnov](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).

Sostanzialmente dc2 è molto su binari. Quello che dobbiamo fare, a quanto ho capito, è:

1. Definire una procedura sensata per usare gli stimatori e interpretare quello che dicono (la base è usare solo Hopkins, per essere fancy se ne può scegliere ance un altro). 
2. Provarla su dati simulati (facoltativo). In merito a ciò uno degli studenti dello scorso anno aveva fatto uno script in Python per farlo e lo ha caricato sul suo Git, ve lo linko dopo.
3. Provarla su dati veri.
4. Provare a costruire un modello positivo di aggregazione (facoltativo, hard).
