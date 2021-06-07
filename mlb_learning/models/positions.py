from .position import Position

class Positions:
    PITCHER = Position("pitcher")
    BATTER = Position("batter")

    def is_batter(position):
        return position == Positions.BATTER

    def is_pitcher(position):
        return position == Positions.PITCHER