from ninja import Schema
import enum

class MeasurementPreference(str, enum.Enum):
    FEET = 'Feet'
    METERS = 'Meters'

class AthleteSchema(Schema):
    id: int
    username: str
    measurement_preference: MeasurementPreference
    ftp: int
    weight: float
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str

    


class ConnectSchema(Schema):
    code: str
    
class MessageSchema(Schema):
    message: str
    success: bool