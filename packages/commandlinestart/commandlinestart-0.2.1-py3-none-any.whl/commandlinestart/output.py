from rich.console import Console
from rich.table import Table


def table_print(*headers):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    console.print(table)
