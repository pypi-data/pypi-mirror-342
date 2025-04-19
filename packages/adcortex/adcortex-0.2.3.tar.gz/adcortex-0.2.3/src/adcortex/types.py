"""Types for ADCortex API.

This module defines data classes and enumerations used by the ADCortex API client.
"""

from enum import Enum
from typing import Any, Dict, List

import pycountry
from pydantic import BaseModel, field_validator, Field


class Platform(BaseModel):
    """
    Contains platform-related metadata.

    Attributes:
        varient (str): varient for experimentation
    """
    name: str
    varient: str = "default"


class Gender(str, Enum):
    """
    Gender enumeration.

    Attributes:
        male: Represents the male gender.
        female: Represents the female gender.
        other: Represents any gender not covered by male or female.
    """

    male = "male"
    female = "female"
    other = "other"


class Role(str, Enum):
    """
    Role enumeration.

    Attributes:
        user: Indicates that the message sender is a user.
        ai: Indicates that the message sender is an AI.
    """

    user = "user"
    ai = "ai"


class Interest(str, Enum):
    """
    Interest enumeration.

    Attributes:
        flirting: Indicates an interest in flirting.
        gaming: Indicates an interest in gaming.
        sports: Indicates an interest in sports.
        music: Indicates an interest in music.
        travel: Indicates an interest in travel.
        technology: Indicates an interest in technology.
        art: Indicates an interest in art.
        cooking: Indicates an interest in cooking.
        all: Represents all interests.
    """

    flirting = "flirting"
    gaming = "gaming"
    sports = "sports"
    music = "music"
    travel = "travel"
    technology = "technology"
    art = "art"
    cooking = "cooking"
    all = "all"


class Language(Enum):
    ar = "ar"  # Arabic
    bg = "bg"  # Bulgarian
    ca = "ca"  # Catalan
    cs = "cs"  # Czech
    da = "da"  # Danish
    de = "de"  # German
    el = "el"  # Greek
    en = "en"  # English
    es = "es"  # Spanish
    et = "et"  # Estonian
    fa = "fa"  # Persian
    fi = "fi"  # Finnish
    fr = "fr"  # French
    gl = "gl"  # Galician
    gu = "gu"  # Gujarati
    he = "he"  # Hebrew
    hi = "hi"  # Hindi
    hr = "hr"  # Croatian
    hu = "hu"  # Hungarian
    hy = "hy"  # Armenian
    id = "id"  # Indonesian
    it = "it"  # Italian
    ja = "ja"  # Japanese
    ka = "ka"  # Georgian
    ko = "ko"  # Korean
    ku = "ku"  # Kurdish
    lt = "lt"  # Lithuanian
    lv = "lv"  # Latvian
    mk = "mk"  # Macedonian
    mn = "mn"  # Mongolian
    mr = "mr"  # Marathi
    ms = "ms"  # Malay
    my = "my"  # Burmese
    nb = "nb"  # Norwegian Bokmål
    nl = "nl"  # Dutch
    pl = "pl"  # Polish
    pt = "pt"  # Portuguese
    ro = "ro"  # Romanian
    ru = "ru"  # Russian
    sk = "sk"  # Slovak
    sl = "sl"  # Slovenian
    sq = "sq"  # Albanian
    sr = "sr"  # Serbian
    sv = "sv"  # Swedish
    th = "th"  # Thai
    tr = "tr"  # Turkish
    uk = "uk"  # Ukrainian
    ur = "ur"  # Urdu
    vi = "vi"  # Vietnamese


class UserInfo(BaseModel):
    """
    Stores user information for ADCortex API.

    Attributes:
        user_id (str): Unique identifier for the user.
        age (int): User's age.
        gender (str): User's gender (must be one of the Gender enum values).
        location (str): User's location (ISO 3166-1 alpha-2 code).
        language (str): Preferred language (must be "english").
        interests (List[Interest]): List of user's interests.
    """

    user_id: str
    age: int
    gender: str
    location: str
    language: str
    interests: List[Interest]

    @field_validator("age")
    def validate_age(cls, value):
        """
        Validate that age is greater than 0.
        """
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value

    @field_validator("gender")
    def validate_gender(cls, value):
        """
        Validate that the provided gender is one of the defined Gender enum values.
        """
        if value not in Gender.__members__:
            raise ValueError(
                f"Gender must be one of: {', '.join(Gender.__members__.keys())}."
            )
        return value

    @field_validator("language")
    def validate_language(cls, value):
        """
        Validate that the provided gender is one of the defined Gender enum values.
        """
        if value not in Language.__members__:
            raise ValueError(
                f"Language must be one of: {', '.join(Language.__members__.keys())}."
            )
        return value

    @field_validator("interests")
    def validate_interests(cls, value):
        """
        Validate that the provided interests list contains valid Interest enum values.
        """
        for interest in value:
            if not isinstance(interest, Interest):
                raise ValueError(
                    f"Interest '{interest}' must be an Interest enum value. Valid values are: {', '.join(Interest.__members__.keys())}."
                )
        return value

    @field_validator("location")
    def validate_country(cls, value):
        """
        Validate that the provided country code is a valid ISO 3166-1 alpha-2 code.
        """
        country = pycountry.countries.get(alpha_2=value.upper())
        return value if country else None


class SessionInfo(BaseModel):
    """
    Stores session details including user.

    Attributes:
        session_id (str): Unique identifier for the session.
        character_name (str): Name of the character (assistant).
        character_metadata (str): Additional metadata for the character as a string.
        user_info (UserInfo): User information.
        platform (Platform): Platform information.
    """

    session_id: str
    character_name: str
    character_metadata: str
    user_info: UserInfo
    platform: Platform


class Message(BaseModel):
    """
    Represents a single message in a conversation.

    Attributes:
        role (Role): The role of the message sender (either user or AI).
        content (str): The content of the message.
        timestamp (float): The timestamp of when the message was created.
    """

    role: Role
    content: str
    # timestamp: float  # Add timestamp field


class Ad(BaseModel):
    """
    Represents an advertisement fetched via the ADCortex API.

    Attributes:
        idx (int): Identifier for the advertisement.
        ad_title (str): Title of the advertisement.
        ad_description (str): Description of the advertisement.
        placement_template (str): Template used for ad placement.
        link (str): URL link to the advertised product or service.
    """

    ad_title: str
    ad_description: str
    placement_template: str
    link: str


class AdResponse(BaseModel):
    """
    Schema for validating ADCortex API responses.

    Attributes:
        ads (List[Ad]): List of ads returned by the API.
    """
    ads: List[Ad]
