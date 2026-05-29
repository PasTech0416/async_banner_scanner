**Asynchronous Network Scanner & Banner Grabber**

Nel contesto della sicurezza informatica e del penetration testing, l'efficienza nella fase di ricognizione attiva è fondamentale. Per esplorare a fondo le potenzialità dell'I/O non bloccante, ho sviluppato un network scanner TCP ad alte prestazioni focalizzato sulla velocità e sull'accuratezza.

Il tool esegue la ricognizione attiva dei servizi di rete identificando le porte aperte e catturando il banner di benvenuto dei protocolli per l'analisi preliminare delle vulnerabilità. 💻

---

### 🛠️ Caratteristiche Tecniche Principali

* **Modello Asincrono Non Bloccante:** Sfrutta un'architettura a coroutine in grado di gestire centinaia di connessioni simultanee su un singolo thread, superando i limiti di overhead del multi-threading tradizionale. 🧵
* **Controllo del Flusso e della Concorrenza:** Implementa un semaforo asincrono (`asyncio.Semaphore`) per limitare il numero di socket aperti in contemporanea, prevenendo la perdita di pacchetti e il sovraccarico della banda. 📊
* **Banner Grabbing Dinamico:** Interagisce attivamente con il socket remoto inviando una sonda generica per forzare la risposta del servizio ed estrarre metadati e versioni del software. 🔍
* **Interfaccia CLI Modulare:** Fornisce un'interfaccia da linea di comando robusta basata su `argparse`, con parsing flessibile per range di porte complessi. ⚙️

---

### 📂 Architettura e Design del Software

L'architettura del progetto è strutturata in modo modulare, separando nettamente la logica di rete (all'interno della cartella `src`) dal file `main` che funge da entry point dell'applicazione. Questo approccio garantisce scalabilità e manutenibilità del codice, rendendolo ideale per attività di penetration testing e vulnerability assessment avanzate. 🎯



