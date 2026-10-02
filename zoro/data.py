"""ZoroLogistics, the synthetic freight dataset that powers the whole AI Engineering Lab program.

Deterministic (seeded) generators for the running case study. Everything here is
designed to look like real freight data, including its flaws, so data-cleaning
weeks have something to find. No API keys, no network. Dependencies: numpy, pandas.

Usage:
    from zoro import data
    df = data.shipments(n=100_000, seed=42)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Carriers
# ---------------------------------------------------------------------------
CARRIER_NAMES = [
    "Atlas Freight", "BlueHarbor Lines", "Cascade Cargo", "Delta Haulage",
    "Everest Express", "Falcon Freight", "GulfStream Logistics", "HarborLink",
    "IronRoad Carriers", "Jupiter Transport", "Kestrel Cargo", "Lakeside Logistics",
    "Meridian Freight", "NorthStar Shipping", "Orion Haulage", "Pioneer Lines",
    "Quantum Freight", "Redwood Carriers", "Summit Logistics", "Tundra Transport",
]


def carriers(n: int = 20, seed: int = 7) -> pd.DataFrame:
    """Generate carrier master data with reliability profiles."""
    rng = np.random.default_rng(seed)
    names = rng.choice(CARRIER_NAMES, size=n, replace=False)
    reliability = np.clip(rng.normal(0.88, 0.06, size=n), 0.60, 0.99) # on-time rate
    base_rate = np.clip(rng.normal(1.35, 0.35, size=n), 0.6, 2.6) # USD per km per ton
    region = rng.choice(["North", "South", "East", "West", "Central"], size=n)
    fleet = rng.integers(50, 4000, size=n)
    return pd.DataFrame({
        "carrier_id": [f"C{i:03d}" for i in range(1, n + 1)],
        "carrier_name": names,
        "region": region,
        "on_time_rate": reliability.round(4),
        "base_rate_usd_per_km_ton": base_rate.round(3),
        "fleet_size": fleet,
    })


# ---------------------------------------------------------------------------
# Lanes
# ---------------------------------------------------------------------------
LANE_CITIES = [
    ("Chicago", "Memphis"), ("Los Angeles", "Phoenix"), ("New York", "Boston"),
    ("Houston", "New Orleans"), ("Seattle", "Portland"), ("Atlanta", "Miami"),
    ("Denver", "Salt Lake City"), ("Dallas", "Oklahoma City"), ("Kansas City", "St. Louis"),
    ("Cincinnati", "Cleveland"), ("Detroit", "Columbus"), ("Charlotte", "Richmond"),
    ("Nashville", "Louisville"), ("Minneapolis", "Milwaukee"), ("San Diego", "Las Vegas"),
    ("Baltimore", "Philadelphia"), ("Pittsburgh", "Buffalo"), ("Jacksonville", "Orlando"),
    ("Austin", "San Antonio"), ("Sacramento", "Fresno"),
]
PORTS = ["Long Beach", "Oakland", "Savannah", "Newark", "Houston", "Tacoma", "Miami", "Charleston"]
COMMODITIES = [
    "electronics", "auto parts", "apparel", "food & beverage", "pharmaceuticals",
    "construction materials", "chemicals", "paper products", "furniture", "machinery",
    "textiles", "perishables",
]


def lanes(n: int = 20, seed: int = 11) -> pd.DataFrame:
    """Generate lane master data (origin, destination, distance, transit norms)."""
    rng = np.random.default_rng(seed)
    pairs = rng.choice(len(LANE_CITIES), size=n, replace=True)
    distance_km = np.clip(rng.normal(900, 300, size=n), 120, 4200).round(0).astype(int)
    avg_transit_days = np.clip(distance_km / 750 + rng.normal(0, 0.4, size=n), 0.5, None).round(1)
    lanes_df = pd.DataFrame({
        "lane_id": [f"L{i:03d}" for i in range(1, n + 1)],
        "origin": [LANE_CITIES[p][0] for p in pairs],
        "destination": [LANE_CITIES[p][1] for p in pairs],
        "distance_km": distance_km,
        "avg_transit_days": avg_transit_days,
        "toll_km": (rng.random(size=n) * distance_km * 0.4).round(0).astype(int),
        "port_region": rng.choice(PORTS, size=n),
    })
    # occasional data-quality issues, on purpose (Week 2 finds these)
    lanes_df.loc[lanes_df.sample(frac=0.05, random_state=seed).index, "distance_km"] = np.nan
    return lanes_df


# ---------------------------------------------------------------------------
# Shipments
# ---------------------------------------------------------------------------
def shipments(n: int = 100_000, seed: int = 42, n_carriers: int = 20, n_lanes: int = 20) -> pd.DataFrame:
    """Generate shipment records with realistic delays and status.

    delay_hours depends on carrier on-time rate, lane distance, and weather noise.
    is_on_time = actual_arrival <= planned_arrival + 2h grace.
    """
    rng = np.random.default_rng(seed)
    car = carriers(n_carriers, seed=7)
    lan = lanes(n_lanes, seed=11)

    carrier_idx = rng.integers(0, n_carriers, size=n)
    lane_idx = rng.integers(0, n_lanes, size=n)
    planned_departure = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 364, size=n), unit="D")
    planned_departure += pd.to_timedelta(rng.integers(0, 24 * 60, size=n), unit="m")

    transit_hours = lan["avg_transit_days"].iloc[lane_idx].to_numpy() * 24
    weather_severity = rng.choice(
        ["clear", "light", "moderate", "severe"], size=n, p=[0.65, 0.20, 0.10, 0.05])
    weather_p_late = {"clear": 0.01, "light": 0.06, "moderate": 0.14, "severe": 0.35}
    weather = np.array([weather_p_late[w] for w in weather_severity])
    carrier_reliability = car["on_time_rate"].iloc[carrier_idx].to_numpy()
    p_late = np.clip((1 - carrier_reliability) + weather + rng.normal(0, 0.03, size=n), 0.01, 0.65)
    is_late = rng.random(size=n) < p_late
    # on-time: delay within the 2h grace window; late: hours to days late
    delay = np.where(
        is_late,
        np.clip(2.5 + rng.lognormal(2.2, 0.9, size=n), 2.5, 240),
        np.clip(rng.normal(0.4, 1.0, size=n), -4.0, 2.0),
    )
    planned_arrival = planned_departure + pd.to_timedelta(transit_hours, unit="h")
    actual_arrival = planned_arrival + pd.to_timedelta(delay, unit="h")
    is_on_time = delay <= 2.0

    status = np.where(
        actual_arrival < pd.Timestamp("2026-01-01"), "Delivered",
        np.where(planned_departure > pd.Timestamp("2026-01-01"), "Booked", "In Transit"))

    weight_kg = np.clip(rng.normal(850, 400, size=n), 5, 20_000).round(0).astype(int)
    value_usd = (weight_kg * rng.lognormal(4.2, 0.7, size=n)).round(2)

    df = pd.DataFrame({
        "shipment_id": [f"S{i:07d}" for i in range(1, n + 1)],
        "carrier_id": car["carrier_id"].iloc[carrier_idx].to_numpy(),
        "lane_id": lan["lane_id"].iloc[lane_idx].to_numpy(),
        "commodity": rng.choice(COMMODITIES, size=n),
        "weight_kg": weight_kg,
        "value_usd": value_usd,
        "planned_departure": planned_departure,
        "planned_arrival": planned_arrival,
        "actual_arrival": actual_arrival,
        "delay_hours": delay.round(2),
        "is_on_time": is_on_time,
        "status": status,
        "weather_severity": weather_severity,
    })
    # planted data-quality issues for Week 2: dupes, impossible values, blanks
    df = pd.concat([df, df.sample(frac=0.002, random_state=seed)]) # duplicates
    bad = df.sample(frac=0.003, random_state=seed + 1).index
    df.loc[bad, "weight_kg"] = np.nan
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Support tickets
# ---------------------------------------------------------------------------
TICKET_TEMPLATES = [
    ("tracking", "Where is my shipment {shipment_id}? It was supposed to arrive {date}."),
    ("damage", "The pallet for {shipment_id} arrived damaged. The {commodity} boxes are crushed."),
    ("refund", "I want a refund for shipment {shipment_id}. It arrived {delay} hours late."),
    ("documents", "Can you resend the bill of lading for {shipment_id}? We lost the copy."),
    ("customs", "Customs is holding {shipment_id} at {port}. What documents do you need?"),
    ("billing", "The invoice for {shipment_id} has the wrong weight. We shipped {weight} kg."),
]


def support_tickets(n: int = 1_000, seed: int = 99, n_shipments: int = 50_000) -> pd.DataFrame:
    """Generate support tickets referencing real shipment ids."""
    rng = np.random.default_rng(seed)
    ship = shipments(n_shipments, seed=42)
    rows = []
    for _ in range(n):
        cat, tpl = TICKET_TEMPLATES[rng.integers(0, len(TICKET_TEMPLATES))]
        s = ship.sample(1, random_state=rng.integers(0, 2**31 - 1)).iloc[0]
        text = tpl.format(
            shipment_id=s["shipment_id"],
            date=s["planned_arrival"].date(),
            delay=abs(s["delay_hours"]).round(0).astype(int),
            commodity=s["commodity"],
            port=rng.choice(PORTS),
            weight=s["weight_kg"] if not np.isnan(s["weight_kg"]) else "unknown",
        )
        rows.append({
            "ticket_id": f"T{len(rows)+1:06d}",
            "shipment_id": s["shipment_id"],
            "customer_id": f"CU{rng.integers(1, 500):04d}",
            "category": cat,
            "priority": rng.choice(["low", "medium", "high", "critical"], p=[0.4, 0.35, 0.2, 0.05]),
            "created_at": pd.Timestamp("2026-01-05") + pd.to_timedelta(rng.integers(0, 200, 1)[0], unit="D"),
            "text": text,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Policy documents (for RAG weeks)
# ---------------------------------------------------------------------------
def policy_docs() -> list[dict]:
    """Shipping/claims/refund policy documents as plain text with section markers."""
    return [
        {"doc_id": "POL-001", "title": "Shipping & Delivery Policy",
         "text": """# ZoroLogistics Shipping & Delivery Policy
## Transit times
Standard ground transit is 2 to 7 business days depending on lane distance. Lane SLAs are
published per lane; average transit for L001 to L010 is 3.2 days.
## Tracking
Every shipment receives a tracking id at booking. Tracking updates are emitted at
pickup, in-transit checkpoints, and delivery.
## Weather
During declared severe weather, delivery SLAs are extended by 48 hours without penalty.
## Address changes
Address changes are free before pickup and $85 after pickup.
"""},
        {"doc_id": "POL-002", "title": "Refund & Claims Policy",
         "text": """# ZoroLogistics Refund & Claims Policy
## Late delivery refunds
Shipments arriving more than 48 hours late are eligible for a 10% freight refund.
More than 7 days late: 50% freight refund.
## Damage claims
Damage claims must be filed within 7 days of delivery with photo evidence.
Approved claims refund the declared value up to $5,000.
## Refund approval
Refunds over $500 require supervisor approval. All refunds are issued within 10 business days.
"""},
        {"doc_id": "POL-003", "title": "Dangerous Goods Policy",
         "text": """# ZoroLogistics Dangerous Goods Policy
## Prohibited items
Lithium batteries over 100 Wh, explosives, and unapproved chemicals cannot be shipped.
## Documentation
DG shipments require a signed shipper's declaration and UN number on the bill of lading.
## Placarding
Vehicles carrying DG must display placards and follow hazmat routing.
"""},
        {"doc_id": "POL-004", "title": "Customs & Border Policy",
         "text": """# ZoroLogistics Customs & Border Policy
## Documentation
Cross-border shipments require a commercial invoice and bill of lading. Missing documents
add 1 to 3 days at the border.
## Duties
Duties and taxes are the consignee's responsibility unless prepaid at booking.
## Holds
Customs holds beyond 5 days incur a $40/day storage fee.
"""},
    ]


# ---------------------------------------------------------------------------
# Bills of lading (for extraction weeks)
# ---------------------------------------------------------------------------
def bol_samples(n: int = 20, seed: int = 5) -> list[dict]:
    """Synthetic bills of lading as raw text blocks with ground-truth fields."""
    rng = np.random.default_rng(seed)
    samples = []
    for i in range(n):
        c = carriers(20, seed=7).sample(1, random_state=seed + i).iloc[0]
        commodity = COMMODITIES[i % len(COMMODITIES)]
        weight = int(rng.integers(100, 18_000))
        qty = int(rng.integers(1, 48))
        value = round(weight * float(rng.lognormal(4.2, 0.5)), 2)
        port_load = PORTS[i % len(PORTS)]
        port_disch = PORTS[(i + 3) % len(PORTS)]
        date = pd.Timestamp("2026-02-01") + pd.to_timedelta(rng.integers(0, 60, 1)[0], unit="D")
        bol = f"""BILL OF LADING No. ZRL-{10000 + i}
SHIPPER: {c['carrier_name']} Logistics Div.
CONSIGNEE: ZoroLogistics Customer #{i:03d}
NOTIFY PARTY: Same as consignee
PORT OF LOADING: {port_load}
PORT OF DISCHARGE: {port_disch}
VESSEL: MV Signal Runner {i % 9 + 1}
COMMODITY: {commodity}
QUANTITY: {qty} pallets
GROSS WEIGHT: {weight} KG
DECLARED VALUE: USD {value}
DATE OF ISSUE: {date.date()}
FREIGHT TERMS: {'PREPAID' if i % 2 == 0 else 'COLLECT'}
"""
        samples.append({
            "bol_id": f"ZRL-{10000 + i}",
            "text": bol,
            "fields": {
                "shipper": c["carrier_name"],
                "consignee": f"ZoroLogistics Customer #{i:03d}",
                "port_of_loading": port_load,
                "port_of_discharge": port_disch,
                "commodity": commodity,
                "quantity": qty,
                "gross_weight_kg": weight,
                "declared_value_usd": value,
                "freight_terms": "PREPAID" if i % 2 == 0 else "COLLECT",
                "date_of_issue": str(date.date()),
            },
        })
    return samples


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------
def save_all(out_dir: str = "data", seed: int = 42, n: int = 100_000) -> dict:
    """Generate and persist the full ZoroLogistics dataset."""
    import pathlib
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    car = carriers()
    lan = lanes()
    ship = shipments(n=n, seed=seed)
    tickets = support_tickets(n=2_000, seed=99, n_shipments=n)
    car.to_csv(out / "carriers.csv", index=False)
    lan.to_csv(out / "lanes.csv", index=False)
    ship.to_csv(out / "shipments.csv", index=False)
    tickets.to_csv(out / "support_tickets.csv", index=False)
    return {"carriers": car, "lanes": lan, "shipments": ship, "tickets": tickets}


if __name__ == "__main__":
    saved = save_all()
    for name, df in saved.items():
        print(f"{name:<10} {len(df):>9,} rows")
    print("Saved to data/")
