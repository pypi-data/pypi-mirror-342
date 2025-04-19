from typing import Annotated

from typer import Argument, Option, Typer


app = Typer(pretty_exceptions_enable=False)


@app.command()
def main(
    name: Annotated[str, Argument(help="Mandatory name")] = "world",
    greeting: Annotated[str, Option(help="Optional greeting")] = "Hello",
):
    print(f"{greeting}, {name}!")
