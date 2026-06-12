import sys
sys.path.insert(0, '.')

from database import init_db, execute, query

SAMPLE_JOBS = [
    ("Waiter / Waitress", "Restoran Taman Sari", "Kuala Lumpur", "Join our team in a busy KL restaurant. Must have experience in F&B service. Weekend shifts included."),
    ("Kitchen Helper / 厨房助理", "Hai Tien Lo", "Penang", "Assist head chef in busy Chinese kitchen. Basic knife skills required. On-the-job training provided."),
    ("Restaurant Manager", "The Coffee Club", "Selangor", "Manage daily operations of a high-volume café. 3+ years management experience required. Salary RM 4000-5500."),
    ("Barista", "Bean Brothers", "Kuala Lumpur", "Specialty coffee experience preferred but will train the right candidate. Must love coffee and customer service."),
    ("Head Chef / 主厨", "Golden Palace Restaurant", "Johor Bahru", "Lead kitchen team in a 50-seat Chinese restaurant. 5+ years experience. Must know Cantonese cuisine."),
    ("Cashier / 收银员", "Family Mart", "Penang", "Handle POS transactions, customer inquiries, and store cleanliness. Shift work required. Fresh graduates welcome."),
    ("Sushi Chef", "Sushi Zen", "Kuala Lumpur", "Experienced sushi chef for Japanese restaurant. Must know fish preparation and rice techniques."),
    ("Shift Supervisor", "Starbucks", "Selangor", "Supervise store operations during shifts. 1+ year retail/F&B experience. Barista certified preferred."),
    ("Dishwasher / 洗碗工", "Marriott Hotel", "Kuala Lumpur", "Full-time position in hotel kitchen. No experience needed. Training provided. RM 1800-2200/month."),
    ("F&B Assistant", "IKEA Restaurant", "Selangor", "Serve customers in IKEA's busy cafeteria. Must be friendly and able to work in fast-paced environment."),
]

init_db()

for title, company, location, desc in SAMPLE_JOBS:
    pid = title.lower().replace(" ", "-")[:40]
    existing = query("SELECT id FROM jobs WHERE platform_id = ?", [pid])
    if not existing:
        execute(
            """INSERT INTO jobs (platform, platform_id, title, company, location, category, description, url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ["seed", pid, title, company, location, "餐饮", desc, "https://www.jobstreet.com.my"],
        )

print(f"Seeded {len(SAMPLE_JOBS)} jobs")
print(f"Total jobs: {query('SELECT COUNT(*) as c FROM jobs')[0]['c']}")
