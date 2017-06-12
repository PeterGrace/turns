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

SERF_EATS = 5
SERF_PER_LAND = 500
GOLD_PER_FOOD = 10

class Game:
    '''The game logic'''

    def __init__(self):
        self.lands = 1
        self.food = 100
        self.serfs = 2
        self.gold = 100
        random.seed(time.time())
        pass

    def sell_food(self):
        if self.food > 100:
            selling = self.food - 100
            self.gold += (selling*GOLD_PER_FOOD)
            self.food -= selling
            logging.info("You sold {} food for {} gold.  {} food remains.".format(selling, self.gold, self.food))


    def run_turn(self):
        self.check_growth()
        self.check_consumption()
        self.check_population()
        self.check_spoilage()
        logging.info("You have {} lands, {} serfs, {} gold, and {} food.".format(self.lands, self.serfs, self.gold, self.food))
    
    def check_consumption(self):
        for serf in range(1,self.serfs):
            self.food -= SERF_EATS 

    def check_spoilage(self):
        if self.food >= (self.serfs*(SERF_EATS*5)):
            spoilage = int(self.food/2)
            self.food -= spoilage
            logging.info("Unfortunately, {} food has spoiled.".format(spoilage))

    def check_population(self):
        if self.food <= 0:
            logging.info("A serf has died due to famine.")
            self.serfs -= 1
        
        if self.serfs == 0:
            logging.info("Game over.")
            raise Exception("All is lost.")

        max_serfs = SERF_PER_LAND * self.lands

        if ((self.serfs >= 2) and (self.serfs <= max_serfs)):
            if self.food >= 5:
                logging.info("Your harvests have caused our serfs to have children")
                self.serfs += int((self.serfs/2))
            else:
                logging.info("You barely had enough food to feed our population, sire.")
        else:
            logging.info("Your land is overcrowded, sire.")



    def check_growth(self):
        weather = self.check_weather()
        plusfood = int((((weather['value']+100)/100)*self.food)+1)
        self.food += plusfood
        logging.info("This turn, the weather was {}.  You gained {} food.".format(weather['word'], plusfood))

    def check_weather(self):
        roll = self.d20()
        logging.debug("Weather roll was a {}".format(roll))
        return {'value': roll, 'word': weather_map[roll] }
    
    def d20(self):
        return random.randint(1,20)
        
    def d20_interp(self, num):
        return num*5
