import pandas as pd
import random

SAMPLE_LEADS = [
    {
        "id": "LEAD-4092",
        "name": "Sarah Jenkins",
        "type": "Institutional Investor",
        "budget": "$12.5M - $18.0M",
        "target_cap_rate": "7.2%+",
        "preferred_zoning": "Commercial / Mixed Use",
        "last_contact": "2 hours ago",
        "interaction_logs": [
            "Email: Interested in multi-family and mixed-use commercial assets near transit hubs.",
            "Phone: Wants properties with minimal immediate CapEx requirement. Hard cap rate floor > 7.0%.",
            "Chat: Target IRR is 14% with 5+ year holding period."
        ],
        "latent_motivations": [
            "Cap rate floor > 7.0%",
            "Prefers steady cash flow over speculative appreciation",
            "Wants pre-vetted compliance for fast closing"
        ],
        "scheduled_time": "10:30 AM EST"
    },
    {
        "id": "LEAD-8103",
        "name": "Marcus Vance",
        "type": "Family Office",
        "budget": "$5.0M - $8.5M",
        "target_cap_rate": "6.8%+",
        "preferred_zoning": "High Density Residential",
        "last_contact": "1 day ago",
        "interaction_logs": [
            "WhatsApp: Looking for 20-50 unit residential complexes in growth metros.",
            "Email: Asked about listings with short-term lease roll-offs to reset rents.",
            "Phone: Motivated by tax-deferred 1031 Exchange deadline (closing within 45 days)."
        ],
        "latent_motivations": [
            "Urgent 1031 Exchange deadline (45 days)",
            "Values rent upside over current yield",
            "Prefers fully occupied buildings with under-market leases"
        ],
        "scheduled_time": "11:45 AM EST"
    },
    {
        "id": "LEAD-1240",
        "name": "Elena Rostova",
        "type": "Industrial REIT",
        "budget": "$20.0M - $35.0M",
        "target_cap_rate": "6.5%+",
        "preferred_zoning": "Light Industrial / Warehouse",
        "last_contact": "3 hours ago",
        "interaction_logs": [
            "Call Note: Needs distribution centers near major interstate corridors.",
            "Email: Minimum 28ft clear height with dock-high loading doors.",
            "Chat: Board approval secured for $30M deployment this fiscal year."
        ],
        "latent_motivations": [
            "Specific structural specs (28ft+ clear height, dock doors)",
            "Capital approved for immediate deployment ($30M)",
            "Location near logistics corridors is priority"
        ],
        "scheduled_time": "02:15 PM EST"
    }
]

def generate_mock_listings(n=200):
    """Generates property listings data."""
    cities = ["Austin, TX", "Denver, CO", "Phoenix, AZ", "Atlanta, GA", "Dallas, TX"]
    
    featured = [
        {
            "id": "PROP-1001",
            "title": "Metro Gateway Plaza",
            "address": "450 Congress Ave, Austin, TX",
            "zoning": "Commercial / Mixed Use",
            "price": 14500000,
            "cap_rate": 7.4,
            "units_sqft": "45,000 sq ft",
            "occupancy": "94%",
            "status": "Verified",
            "description": "Prime commercial mixed-use plaza with high foot traffic near metro transit station."
        },
        {
            "id": "PROP-1002",
            "title": "Highland Park Residences",
            "address": "1280 Colorado Blvd, Denver, CO",
            "zoning": "High Density Residential",
            "price": 6800000,
            "cap_rate": 7.1,
            "units_sqft": "36 Units",
            "occupancy": "98%",
            "status": "Verified",
            "description": "36-unit apartment complex with value-add potential and 12-15% rent upside."
        },
        {
            "id": "PROP-1003",
            "title": "Interstate Logistics Hub",
            "address": "8900 Logistics Pkwy, Atlanta, GA",
            "zoning": "Light Industrial / Warehouse",
            "price": 24500000,
            "cap_rate": 6.8,
            "units_sqft": "120,000 sq ft",
            "occupancy": "100%",
            "status": "Verified",
            "description": "Class A distribution facility with 30ft clear height and long-term tenants."
        }
    ]
    
    data = list(featured)
    random.seed(42)
    for i in range(1004, 1004 + n):
        city = random.choice(cities)
        zoning = random.choice(["Commercial / Mixed Use", "High Density Residential", "Light Industrial / Warehouse"])
        cap = round(random.uniform(6.0, 9.0), 1)
        price = random.randrange(3000000, 25000000, 500000)
        
        data.append({
            "id": f"PROP-{i}",
            "title": f"{city.split(',')[0]} Asset {i}",
            "address": f"{random.randint(100, 999)} Main St, {city}",
            "zoning": zoning,
            "price": price,
            "cap_rate": cap,
            "units_sqft": f"{random.randint(15, 60)} Units",
            "occupancy": f"{random.randint(90, 100)}%",
            "status": "Verified",
            "description": f"Verified property in {city} with strong cash flow."
        })
        
    return pd.DataFrame(data)

def get_lead_by_id(lead_id):
    for lead in SAMPLE_LEADS:
        if lead["id"] == lead_id:
            return lead
    return SAMPLE_LEADS[0]
