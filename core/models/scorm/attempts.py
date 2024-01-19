from pydantic import BaseModel


class Comments(BaseModel):
    childArray: list = []


class LearnerPreference(BaseModel):
    audio_level: str = "1"
    language: str = ""
    delivery_speed: str = "1"
    audio_captioning: str = "0"


class Score(BaseModel):
    scaled: str = ""
    raw: str = ""
    min: str = ""
    max: str = ""


class Cmi(BaseModel):
    completion_status: str = "incomplete"
    completion_threshold: str = ""
    credit: str = "credit"
    entry: str = ""
    exit: str = "suspend"
    launch_data: str = ""
    learner_id: str = ""
    learner_name: str = ""
    location: str = ""
    max_time_allowed: str = ""
    mode: str = "normal"
    progress_measure: str = ""
    scaled_passing_score: str = ""
    session_time: str = ""
    success_status: str = "unknown"
    suspend_data: str = ""
    time_limit_action: str = "continue,no message"
    total_time: str = ""
    comments_from_learner: Comments = Comments()
    comments_from_lms: Comments = Comments()
    interactions: Comments = Comments()
    learner_preference: LearnerPreference = LearnerPreference()
    objectives: Comments = Comments()
    score: Score = Score()


class Nav(BaseModel):
    request: str = ""


class Adl(BaseModel):
    nav: Nav = Nav()


class CreateExitAttempt(BaseModel):
    cmi: Cmi = Cmi()
    adl: Adl = Adl()
