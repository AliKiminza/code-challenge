from random import choice as rc
from faker import Faker

from app import app, db
from models import Power, Hero_power, Hero



# Seeding powers
powers_dict = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

for power_info in powers_dict:
    power = Power(name=rc(power.name), description=rc(power.description))
    db.session.add(power)

# Seeding heroes
heroes_dict = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

fake = Faker()

with app.app_context():

    Hero.query.delete()
    Power.query.delete()
    Hero_power.query.delete()
    
for hero_info in heroes_dict:
    hero = Hero(name=rc(hero.name), super_name=rc(hero.super_name))
    db.session.add(hero)

# Adding powers to heroes
strengths = ["Strong", "Weak", "Average"]
all_powers = Power.query.all()

for hero in Hero.query.all():
    for i in range(rc(1, 4)):  # Randomly assign 1-3 powers to each hero
        power = rc(all_powers)
        hero_power = Hero_power(hero=hero, power=power, strength=rc(strengths))
        db.session.add(hero_power)

# Commit changes to the database
db.session.commit()

print("🦸‍♀️ Done seeding!")
