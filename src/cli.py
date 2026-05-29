import argparse
from typing import List

def parse_ports(port_arg: str) -> List[int]:
    """
    Parsa la stringa delle porte supportando il formato singolo, a virgola o a intervallo.
    """
    ports = set()
    try:
        for part in port_arg.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part))
        return sorted([p for p in ports if 1 <= p <= 65535])
    except ValueError:
        raise argparse.ArgumentTypeError(f"Formato porte non valido: '{port_arg}'. Usa es. '22,80' o '1-1024'")

def get_arguments() -> argparse.Namespace:
    """
    Configura il parser degli argomenti da linea di comando.
    """
    parser = argparse.ArgumentParser(
        description="Async Port Scanner & Banner Grabber professionale per attività di Cyber Security Reconnaissance."
    )
    parser.add_argument("-t", "--target", required=True, help="IP del target o nome di dominio (es. 192.168.1.1 o scanme.nmap.org)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Porte da scansionare. Es: '22,80,443' o '1-1024' (Default: 1-1024)")
    parser.add_argument("-c", "--concurrency", type=int, default=100, help="Numero massimo di task asincroni simultanei (Default: 100)")
    parser.add_argument("--timeout", type=float, default=2.0, help="Timeout di connessione in secondi (Default: 2.0)")
    
    return parser.parse_args()