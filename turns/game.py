import logging
import random
import time

weather_map = [
    'NEVER_WILL_HAPPEN',
    'Completely Arid',
    'Arid',
    'Arid',
    'Arid',
    'Arid',
    'Fair',
    'Fair',
    'Fair',
    'Fair',
    'Fair',
    'Moist',
    'Moist',
    'Moist',
    'Moist',
    'Rainy',
    'Rainy',
    'Rainy',
    'Rainy',
    'Monsoon',
    'Bounteous Rainfall'
]
weather_multiplier = [0,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]

SERF_EATS = 2
SERF_PER_LAND = 6
SERF_GROWTH = 0.2
SERF_DIEOFF = 0.15
SERF_DESERT = 0.15
GOLD_PER_FOOD = 10
GRANARY_STORAGE = 10000
FOOD_MULTIPLIER = 20
TAX_RATE=4

class Game:
    '''The game logic'''

    def __init__(self):
        self.lands = 100
        self.food = 100
        self.serfs = 2
        self.gold = 100
        self.granaries = 1
        self.happiness = 0.5
        random.seed(time.time())
        pass

    def sell_food(self):
        if self.food > 5000:
            selling = self.food - 5000
            moneyback = (selling*GOLD_PER_FOOD)
            self.gold += moneyback
            self.food -= selling
            logging.info("You sold {} food for {} gold.  {} food remains.".format(selling, moneyback, self.food))
        else:
            logging.info("You can only sell if you have more than 5000 food.")


    def run_turn(self):
        self.check_growth()
        self.check_consumption()
        self.check_population()
        self.check_spoilage()
        self.collect_taxes()
        logging.info(f"You have {self.lands} lands, {self.serfs} serfs, {self.gold} gold, and {self.food} food.")

    def collect_taxes(self):
        taxes = self.serfs*TAX_RATE
        self.gold += taxes
        logging.info("You have collected {} gold from your subjects.".format(taxes))

    def check_consumption(self):
        consumption = (self.serfs*SERF_EATS)
        logging.info("Your serfs have eaten {} food.".format(consumption))
        self.food -= consumption
        if self.food < 0:
            self.food = 0
            logging.info("Widespread famine has culled your population.")
            self.serfs = int(self.serfs * SERF_DIEOFF)
            self.happiness -= 0.05


    def check_spoilage(self):
        granary_max = self.granaries*GRANARY_STORAGE
        if self.food >= granary_max:
            loss = self.food - granary_max
            self.food = granary_max
            logging.info("Unfortunately, {} food has spoiled.  Build more granaries!".format(loss))

    def check_population(self):

        if self.serfs == 0:
            logging.info("Game over.")
            raise Exception("All is lost.")

        max_serfs = SERF_PER_LAND * self.lands


        if ((self.serfs >= 2) and (self.serfs <= max_serfs)):
            if self.food >= 5:
                self.happiness += 0.01
                if self.happiness > 0.5:
                    logging.debug("Your harvests have caused our serfs to have children")
                    density = self.serfs / max_serfs
                    serf_growth_rate = 1 - density
                    self.serfs += int((self.serfs*(serf_growth_rate)))
                    if (max_serfs - self.serfs) < 5:
                        logging.info("Overcrowding is contributing to loss of happiness.")
                        self.happiness -= 0.015
                else:
                    logging.info("You would have gained population but your serfs are miserable.")
            else:
                logging.info("You barely had enough food to feed our population, sire.")
        elif (self.serfs == 1):
            logging.info("Your kingdom consists of only you.  Without a miracle, you are doomed.")
            roll = self.d20()
            if roll == 20:
                logging.info("Unbelievably, a family has come to your kingdom!")
                self.serfs += 10
        else:
            logging.info("Your land is overcrowded, sire.  Some of your serfs have moved to neighboring lands.")
            self.serfs = int(self.serfs-(self.serfs*SERF_DESERT))



    def check_growth(self):
        weather = self.check_weather()
        plusfood = abs(int(((((weather['value'])*self.lands)*FOOD_MULTIPLIER)+1)))
        self.food += plusfood
        logging.info("This turn, the weather was {}.  You gained {} food.".format(weather['word'], plusfood))

    def check_weather(self):
        roll = self.d20()
        logging.debug("Weather roll was a {}".format(roll))
        return {'value': weather_multiplier[roll], 'word': weather_map[roll] }

    def d20(self):
        return random.randint(1,20)

    def d20_interp(self, num):
        return num*5
