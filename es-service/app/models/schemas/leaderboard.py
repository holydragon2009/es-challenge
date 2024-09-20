from app.models.common import SchemaBase


class LeaderboardBase(SchemaBase):
    score: int


class UpdateScoreRequest(LeaderboardBase):
    pass
