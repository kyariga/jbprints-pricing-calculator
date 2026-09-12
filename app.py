import math
import streamlit as st

st.set_page_config(
    page_title="JB Prints Pricing Calculator",
    page_icon="🧵",
    layout="wide"
)

# -----------------------------
# Helpers
# -----------------------------
def calculate_price(
    width: float,
    height: float,
    fabric_price: float,
    fabric_adjustment: float,
    labor_cost: float,
    profit_pct: float,
    etsy_fees: float,
):
    area = width * height
    size_factor = area / 1296
    adjusted_fabric_price = fabric_price + fabric_adjustment
    material_cost = size_factor * adjusted_fabric_price
    subtotal = material_cost + labor_cost
    profit_amount = subtotal * (profit_pct / 100)
    price_before_fees = subtotal + profit_amount
    final_price = price_before_fees + etsy_fees

    return {
        "area": area,
        "size_factor": size_factor,
        "adjusted_fabric_price": adjusted_fabric_price,
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "subtotal": subtotal,
        "profit_amount": profit_amount,
        "price_before_fees": price_before_fees,
        "etsy_fees": etsy_fees,
        "final_price": final_price,
    }


def round_to_99(price: float) -> float:
    """Round up to the next .99 price point."""
    if price <= 0:
        return 0.99
    whole = math.floor(price)
    candidate = whole + 0.99
    if candidate < price:
        candidate = whole + 1 + 0.99
    return round(candidate, 2)


def money(value: float) -> str:
    return f"${value:,.2f}"


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 1.4rem 1.5rem;
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 18px;
            margin-bottom: 1.25rem;
        }

        .hero h1 {
            margin: 0 0 .35rem 0;
            font-size: 2rem;
        }

        .hero p {
            margin: 0;
            opacity: .75;
        }

        .price-card {
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 18px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }

        .price-label {
            font-size: .95rem;
            opacity: .70;
            margin-bottom: .35rem;
        }

        .price-value {
            font-size: 2.7rem;
            font-weight: 750;
            line-height: 1.05;
        }

        .small-note {
            opacity: .68;
            font-size: .9rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.20);
            padding: 14px;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🧵 JB Prints Pricing Calculator</h1>
        <p>Calculate a selling price from pillow size, fabric cost, labor, profit, and Etsy fees.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar assumptions
# -----------------------------
with st.sidebar:
    st.header("Pricing settings")

    labor_cost = st.number_input(
        "Labor cost",
        min_value=0.0,
        value=50.0,
        step=1.0,
        format="%.2f",
        help="Default labor cost added to each item.",
    )

    profit_pct = st.number_input(
        "Profit markup (%)",
        min_value=0.0,
        value=30.0,
        step=1.0,
        format="%.1f",
        help="Applied after material cost and labor are added.",
    )

    etsy_fees = st.number_input(
        "Etsy fees",
        min_value=0.0,
        value=12.0,
        step=1.0,
        format="%.2f",
    )

    fabric_adjustment = st.number_input(
        "Fabric price adjustment",
        value=10.0,
        step=1.0,
        format="%.2f",
        help="Your formula adds $10 to the entered fabric price before multiplying by the size factor.",
    )

    st.divider()
    st.caption(
        "Formula: (((Width × Height) ÷ 1296) × (Fabric Price + Adjustment) + Labor) "
        "× (1 + Profit %) + Etsy Fees"
    )

# -----------------------------
# Main calculator inputs
# -----------------------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Product details")

    c1, c2 = st.columns(2)
    with c1:
        width = st.number_input(
            "Width (inches)",
            min_value=1.0,
            value=20.0,
            step=1.0,
            format="%.1f",
        )
    with c2:
        height = st.number_input(
            "Height (inches)",
            min_value=1.0,
            value=20.0,
            step=1.0,
            format="%.1f",
        )

    fabric_price = st.number_input(
        "Fabric price",
        min_value=0.0,
        value=75.0,
        step=1.0,
        format="%.2f",
        help="Enter the base fabric price used in your pricing formula.",
    )

    use_etsy_rounding = st.toggle(
        "Show Etsy-friendly .99 price",
        value=True,
        help="Rounds UP to the next price ending in .99 so the rounded price never falls below your calculated price.",
    )

    result = calculate_price(
        width=width,
        height=height,
        fabric_price=fabric_price,
        fabric_adjustment=fabric_adjustment,
        labor_cost=labor_cost,
        profit_pct=profit_pct,
        etsy_fees=etsy_fees,
    )

with right:
    st.subheader("Recommended price")

    st.markdown(
        f"""
        <div class="price-card">
            <div class="price-label">Calculated selling price</div>
            <div class="price-value">{money(result["final_price"])}</div>
            <div class="small-note">Includes your configured profit and Etsy fee amount.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if use_etsy_rounding:
        rounded_price = round_to_99(result["final_price"])
        st.success(f"Suggested Etsy price: **{money(rounded_price)}**")

    metric1, metric2 = st.columns(2)
    metric1.metric("Material cost", money(result["material_cost"]))
    metric2.metric("Profit amount", money(result["profit_amount"]))

# -----------------------------
# Breakdown
# -----------------------------
st.divider()
st.subheader("Pricing breakdown")

rows = [
    ("Size", f'{width:g}" × {height:g}"'),
    ("Area", f'{result["area"]:,.2f} sq in'),
    ("Area ÷ 1296", f'{result["size_factor"]:.4f}'),
    ("Fabric price", money(fabric_price)),
    ("Fabric price + adjustment", money(result["adjusted_fabric_price"])),
    ("Calculated material cost", money(result["material_cost"])),
    ("Labor", money(result["labor_cost"])),
    ("Subtotal before profit", money(result["subtotal"])),
    (f"Profit markup ({profit_pct:g}%)", money(result["profit_amount"])),
    ("Price before Etsy fees", money(result["price_before_fees"])),
    ("Etsy fees", money(result["etsy_fees"])),
    ("Final calculated price", money(result["final_price"])),
]

st.table(
    {
        "Item": [row[0] for row in rows],
        "Amount / Value": [row[1] for row in rows],
    }
)

# -----------------------------
# Example calculation
# -----------------------------
with st.expander("Show calculation"):
    st.markdown(
        f"""
**1. Size area**

`{width:g} × {height:g} = {result["area"]:,.2f}`

**2. Divide by 1296**

`{result["area"]:,.2f} ÷ 1296 = {result["size_factor"]:.4f}`

**3. Add the fabric adjustment**

`${fabric_price:,.2f} + ${fabric_adjustment:,.2f} = {money(result["adjusted_fabric_price"])}`

**4. Calculate material cost**

`{result["size_factor"]:.4f} × {money(result["adjusted_fabric_price"])} = {money(result["material_cost"])}`

**5. Add labor**

`{money(result["material_cost"])} + {money(labor_cost)} = {money(result["subtotal"])}`

**6. Add {profit_pct:g}% profit**

`{money(result["subtotal"])} × {1 + profit_pct / 100:.2f} = {money(result["price_before_fees"])}`

**7. Add Etsy fees**

`{money(result["price_before_fees"])} + {money(etsy_fees)} = {money(result["final_price"])}`

**Final selling price: {money(result["final_price"])}**
"""
    )

# -----------------------------
# Multi-size quick pricing
# -----------------------------
st.divider()
st.subheader("Quick size comparison")
st.caption("See how the same fabric price would be priced across common pillow sizes.")

common_sizes = [
    (12, 12),
    (12, 20),
    (14, 26),
    (18, 18),
    (20, 20),
    (22, 22),
    (24, 24),
    (26, 26),
]

comparison = []
for w, h in common_sizes:
    r = calculate_price(
        width=w,
        height=h,
        fabric_price=fabric_price,
        fabric_adjustment=fabric_adjustment,
        labor_cost=labor_cost,
        profit_pct=profit_pct,
        etsy_fees=etsy_fees,
    )
    comparison.append(
        {
            "Size": f'{w}" × {h}"',
            "Material Cost": money(r["material_cost"]),
            "Calculated Price": money(r["final_price"]),
            "Suggested Etsy Price": money(round_to_99(r["final_price"])),
        }
    )

st.dataframe(comparison, use_container_width=True, hide_index=True)

st.caption(
    "JB Prints Pricing Calculator • Adjust the settings in the sidebar whenever your labor, profit target, or Etsy fee assumptions change."
)
