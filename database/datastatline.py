from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import DatabaseFactory

some_base = DatabaseFactory.Base

class DataStatline(some_base):
    __tablename__ = 'statline'
    id = Column(Integer, primary_key=True)
    airOuts = Column(Integer)
    atBats = Column(Integer)
    balls = Column(Integer)
    baseOnBalls = Column(Integer)
    battersFaced = Column(Integer)
    blownSaves = Column(Integer)
    catchersInterference = Column(Integer)
    caughtStealing = Column(Integer)
    completeGames = Column(Integer)
    doubles = Column(Integer)
    earnedRuns = Column(Integer)
    flyOuts = Column(Integer)
    gamesFinished = Column(Integer)
    gamesPitched = Column(Integer)
    gamesPlayed = Column(Integer)
    gamesStarted = Column(Integer)
    groundIntoDoublePlay = Column(Integer)
    groundIntoTriplePlay = Column(Integer)
    groundOuts = Column(Integer)
    hits = Column(Integer)
    hitBatsmen = Column(Integer)
    hitByPitch = Column(Integer)
    holds = Column(Integer)
    homeRuns = Column(Integer)
    inheritedRunners = Column(Integer)
    inheritedRunnersScored = Column(Integer)
    inningsPitched = Column(Integer)
    intentionalWalks = Column(Integer)
    leftOnBase = Column(Integer)
    losses = Column(Integer)
    note = Column(String)
    numberOfPitches = Column(Integer)
    outs = Column(Integer)
    pickoffs = Column(Integer)
    pitchesThrown = Column(Integer)
    rbi = Column(Integer)
    runs = Column(Integer)
    saveOpportunities = Column(Integer)
    sacBunts = Column(Integer)
    sacFlies = Column(Integer)
    saves = Column(Integer)
    shutouts = Column(Integer)
    stolenBases = Column(Integer)
    strikes = Column(Integer)
    strikeOuts = Column(Integer)
    triples = Column(Integer)
    totalBases = Column(Integer)
    wildPitches = Column(Integer)
    wins = Column(Integer)

    #gamelog = relationship("DataGamelog", uselist=False, backref="statline")

    def __init__(self, statline):
        self.hits = statline.categories["hits"]

#class User(Base): #statline
#    __tablename__ = 'user'

#    id = Column(Integer, primary_key=True)
#    name = Column(String)
#    mobile = relationship("Mobile", uselist=False, backref="owner")

#    def __init__(self, name):
#        self.name = name

