class Settings:
    time = 0
    dollars = 0

    WIDTH = 24  # number of columns of the game
    HEIGHT = 24  # number of rows of the game
    PEOPLE_SPEED = 2  # number of turns it takes to a people to move 1px
    PEOPLE_GENERATION = 3  # a new people is generated every x turns
    NUMBER_OF_INITIAL_PEOPLES = 10  # number of people at the begining of the game
    WAIT_OF_PEOPLE_MIN = 25  # number of turns a people will wait before leaving the building
    WAIT_OF_PEOPLE_MAX = 50
    SPEED = 1 / 50  # higher = faster
    SEED = 0  # random generation seed

    # currentTimeoutId what does this do??
    locked = False