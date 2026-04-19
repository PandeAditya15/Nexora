from rich import print

def alert(ip, score):
    print(f"[bold red]⚠ MALICIOUS IP:[/bold red] {ip} (Score: {score})")