import asyncio
import sys
import time
from src.cli import get_arguments, parse_ports
from src.scanner import run_scanner

def print_banner():
    """
    Stampa il banner grafico iniziale del tool.
    """
    print("=" * 70)
    print("        ASYNC PORT SCANNER & BANNER GRABBER (CyberSec Portfolio Tool)  ")
    print("=" * 70)

def main():
    print_banner()
    args = get_arguments()
    
    try:
        ports = parse_ports(args.ports)
    except Exception as e:
        print(f"[-] Errore configurazione porte: {e}")
        sys.exit(1)

    print(f"[*] Target:       {args.target}")
    print(f"[*] Porte:        {args.ports} ({len(ports)} porte totali)")
    print(f"[*] Concorrenza:  {args.concurrency} task simultanei")
    print(f"[*] Timeout:      {args.timeout} secondi")
    print("[*] Scansione avviata...\n")
    
    start_time = time.time()
    
    # Esegue il loop di eventi asincroni
    try:
        results = asyncio.run(run_scanner(args.target, ports, args.concurrency, args.timeout))
    except KeyboardInterrupt:
        print("\n[-] Scansione interrotta dall'utente.")
        sys.exit(0)
        
    duration = time.time() - start_time
    
    # Stampa l'output finale in formato tabella pulita
    if results:
        print(f"{'PORTA':<10}{'STATO':<10}{'SERVIZIO':<15}{'BANNER / INFO':<35}")
        print("-" * 70)
        for res in results:
            # Tronca il banner troppo lungo per preservare il layout della tabella
            banner_truncated = res['banner'][:45] + '...' if len(res['banner']) > 45 else res['banner']
            print(f"{res['port']:<10}{res['status']:<10}{res['service']:<15}{banner_truncated:<35}")
    else:
        print("[+] Nessuna porta aperta trovata nel range specificato.")
        
    print("\n" + "=" * 70)
    print(f"[+] Scansione completata in {duration:.2f} secondi.")
    print("=" * 70)

if __name__ == "__main__":
    main()