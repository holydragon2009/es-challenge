from app.models.domain.rmodel import RWModel


class RWSchema(RWModel):
    class Config(RWModel.Config):
        orm_mode = True
