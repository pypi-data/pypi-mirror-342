import typer
from sympy import sympify

app = typer.Typer()

@app.command()
def calculate(expression: str):
    """
    This function performs a simple calculation.
    """
    try:
        result = sympify(expression)
        typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}")   

if __name__ == "__main__":
    app()
    