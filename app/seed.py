
from app import app
from models import Power, Hero, HeroPower, db
import random

with app.app_context():

    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    

    heroes_names=([
        { "name": "Kamala Khan","super_name": "Ms. Marvel" },
        { "name": "Doreen Green", "super_name": "Squirrel Girl" },
        { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
        { "name": "Janet Van Dyne", "super_name": "The Wasp" },
        { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
        { "name": "Carol Danvers", "super_name": "Captain Marvel" },
        { "name": "Jean Grey", "super_name": "Dark Phoenix" },
        { "name": "Ororo Munroe", "super_name": "Storm" },
        { "name": "Kitty Pryde", "super_name": "Shadowcat" },
        { "name": "Elektra Natchios", "super_name": "Elektra" }
    ])

    powers_info=([
        {"name": "super strength", "description": "gives the wielder super-human strengths" },
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths" }
    ])

    strengths = ["Strong", "Weak", "Average"]

    print("🦸‍♀️ Seeding powers...")

    for power in powers_info:
        new_power=Power(
            name=power['name'],
            description=power['description']
        )
        db.session.add(new_power)
    db.session.commit()    

    print("🦸‍♀️ Seeding heroes...")
     
    for hero in heroes_names:
        new_hero=Hero(
            name=hero['name'],
            super_name=hero['super_name']
        )
        
        for p in range(random.randint(1,len(powers_info))):
            power= random.choice(Power.query.all())
            strength=random.choice(strengths)
            hero_power=HeroPower(
                heroes=new_hero,
                powers=power,
                strength=strength)
            db.session.add(hero_power)
        db.session.add(new_hero)
    db.session.commit()    
