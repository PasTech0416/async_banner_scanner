import asyncio
import socket
from typing import Dict, Optional, List

# Timeout standard per la connessione (in secondi)
DEFAULT_TIMEOUT = 2.0

async def grab_banner(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> str:
    """
    Tenta di leggere il banner di benvenuto dal servizio.
    Invia una stringa generica se il servizio attende un input.
    """
    try:
        # Il protocollo potrebbe richiedere un input prima di rispondere
        # Invia una sonda generica non distruttiva
        writer.write(b"HEAD / HTTP/1.1\r\n\r\n")
        await writer.drain()
        
        # Legge i primi 1024 byte della risposta
        data = await asyncio.wait_for(reader.read(1024), timeout=1.5)
        return data.decode('utf-8', errors='ignore').strip().replace('\n', ' ')
    except asyncio.TimeoutError:
        return "Sconosciuto (Nessun banner inviato dal server)"
    except Exception:
        return "Sconosciuto (Errore nel grabbing)"
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def scan_port(target: str, port: int, timeout: float) -> Optional[Dict[str, str]]:
    """
    Scansiona una singola porta TCP. Se aperta, tenta il banner grabbing.
    """
    try:
        # Tenta la connessione TCP asincrona
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(target, port),
            timeout=timeout
        )
        
        # Il flag indica che la connessione ha avuto successo e la porta è aperta
        # Tenta il banner grabbing sul canale di comunicazione
        banner = await grab_banner(reader, writer)
        
        # Tenta di indovinare il servizio standard associato alla porta
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"

        return {
            "port": str(port),
            "status": "OPEN",
            "service": service,
            "banner": banner
        }
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        # Il target ha rifiutato la connessione o la porta è filtrata
        return None

async def run_scanner(target: str, ports: List[int], concurrency: int, timeout: float) -> List[Dict[str, str]]:
    """
    Gestisce il pool di worker asincroni limitando la concorrenza con un Semaphore.
    """
    semaphore = asyncio.Semaphore(concurrency)
    results = []

    async def worker(port: int):
        async with semaphore:
            res = await scan_port(target, port, timeout)
            if res:
                results.append(res)

    # Crea il task per ogni singola porta richiesta
    tasks = [worker(port) for port in ports]
    await asyncio.gather(*tasks)
    
    # Ordina il risultato finale in base al numero di porta
    return sorted(results, key=lambda x: int(x['port']))