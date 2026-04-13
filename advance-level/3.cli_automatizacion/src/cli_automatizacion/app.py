import typer
from rich.console import Console
from rich.table import Table

from .client import create_order, delete_order, list_orders

app = typer.Typer(name="orders", help="Manage orders via the Orders API.")
console = Console()


@app.command("list")
def list_cmd() -> None:
    """List all orders."""
    try:
        orders = list_orders()
    except Exception as exc:
        console.print(f"[red]Error fetching orders:[/red] {exc}")
        raise typer.Exit(code=1)

    if not orders:
        console.print("[yellow]No orders found.[/yellow]")
        return

    table = Table("ID", "User ID", "Total ($)", "Products", title="Orders")
    for order in orders:
        table.add_row(
            str(order.get("id", "-")),
            str(order.get("userId", "-")),
            str(order.get("total", "-")),
            str(len(order.get("products", []))),
        )
    console.print(table)


@app.command("create")
def create_cmd(
    user_id: int = typer.Option(..., "--user-id", "-u", help="User ID for the order."),
    product_id: int = typer.Option(
        ..., "--product-id", "-p", help="Product ID to add."
    ),
    quantity: int = typer.Option(
        1, "--quantity", "-q", help="Quantity of the product."
    ),
) -> None:
    """Create a new order."""
    try:
        order = create_order(user_id, product_id, quantity)
    except Exception as exc:
        console.print(f"[red]Error creating order:[/red] {exc}")
        raise typer.Exit(code=1)

    console.print(
        f"[green]Order created:[/green] "
        f"ID={order.get('id')}  "
        f"User={order.get('userId')}  "
        f"Total=${order.get('total', 0):.2f}"
    )


@app.command("delete")
def delete_cmd(
    order_id: int = typer.Argument(..., help="ID of the order to delete."),
) -> None:
    """Delete an order by ID."""
    try:
        result = delete_order(order_id)
    except Exception as exc:
        console.print(f"[red]Error deleting order:[/red] {exc}")
        raise typer.Exit(code=1)

    if result.get("isDeleted"):
        console.print(f"[red]Order {order_id} deleted successfully.[/red]")
    else:
        console.print(
            f"[yellow]Order {order_id} response received (isDeleted not confirmed).[/yellow]"
        )
