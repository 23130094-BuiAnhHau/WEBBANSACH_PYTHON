def format_currency_vnd(amount: int | float) -> str:
    """Định dạng số thành tiền VNĐ."""
    try:
        return f"{amount:,.0f} ₫".replace(",", ".")
    except Exception:
        return str(amount)
