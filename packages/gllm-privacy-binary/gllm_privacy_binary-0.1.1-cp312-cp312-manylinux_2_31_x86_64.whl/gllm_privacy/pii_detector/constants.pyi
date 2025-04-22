from _typeshed import Incomplete
from enum import StrEnum
from presidio_analyzer import RecognizerResult as PresidioRecognizerResult

RecognizerResult = PresidioRecognizerResult

class Entities(StrEnum):
    """Supported entities for PII detection."""
    KTP = 'ID_KTP'
    NPWP = 'ID_NPWP'
    PROJECT = 'PROJECT'
    ORGANIZATION_NAME = 'ORGANIZATION'
    EMPLOYEE_ID = 'EMPLOYEE_ID'
    FAMILY_CARD_NUMBER = 'FAMILY_CARD_NUMBER'
    FACEBOOK_ACCOUNT = 'FACEBOOK_ACCOUNT'
    LINKEDIN_ACCOUNT = 'LINKEDIN_ACCOUNT'
    BANK_ACCOUNT = 'BANK_ACCOUNT'
    ID_BPJS_NUMBER = 'ID_BPJS_NUMBER'
    EMAIL_ADDRESS = 'EMAIL_ADDRESS'
    PERSON = 'PERSON'
    PHONE_NUMBER = 'PHONE_NUMBER'
    IBAN_CODE = 'IBAN_CODE'
    CREDIT_CARD = 'CREDIT_CARD'
    CRYPTO = 'CRYPTO'
    IP_ADDRESS = 'IP_ADDRESS'
    LOCATION = 'LOCATION'
    DATE_TIME = 'DATE_TIME'
    NRP = 'NRP'
    MEDICAL_LICENSE = 'MEDICAL_LICENSE'
    URL = 'URL'
    MONEY = 'MONEY'
    US_BANK_NUMBER = 'US_BANK_NUMBER'
    US_DRIVER_LICENSE = 'US_DRIVER_LICENSE'
    US_ITIN = 'US_ITIN'
    US_PASSPORT = 'US_PASSPORT'
    US_SSN = 'US_SSN'
    OTHER_NAME = 'OTHER_NAME'
    GOD = 'GOD'
    FACILITY = 'FACILITY'
    PRODUCT = 'PRODUCT'
    EVENT = 'EVENT'
    TIME = 'TIME'
    NUMBER = 'NUMBER'
    MEASUREMENT = 'MEASUREMENT'

GLLM_PRIVACY_ENTITIES: Incomplete

class ProsaNERConstant:
    """Defines constants used in the Prosa NER integration.

    This class encapsulates various constants that are utilized throughout the Prosa Named Entity Recognition (NER)
    integration process. These include API headers, API payload keys and values, entity recognition response keys,
    and default values for entity recognition processing.

    Attributes:
        HEADER_CONTENT_TYPE_KEY (str): Key for the content type header.
        HEADER_CONTENT_TYPE_VAL (str): Value for the 'Content-Type' header, typically 'application/json'.
        HEADER_USER_AGENT (str): Key for the user agent header.
        HEADER_USER_AGENT_VAL (str): Value for User-Agent HTTP header for request.
        ID_LANGUAGE (str): Language code for Indonesian language, used in language-specific operations.
        VERSION_CUSTOM_NER (str): Version identifier for the custom NER being used.
        PAYLOAD_VERSION_KEY (str): Key for specifying the version in the API payload.
        PAYLOAD_VERSION_VAL (str): Value for the API version, typically 'v1'.
        PAYLOAD_TEXT_KEY (str): Key for the text to be analyzed in the API payload.
        RESPONSE_TIMEOUT (int): Timeout value for the API response, in seconds.
        ENTITY_TYPE_KEY (str): Key for the entity type in entity dictionaries.
        START_KEY (str): Key for the start index of an entity in the text.
        START_IDX_KEY (str): Key for the start index of an entity in the text returned by Prosa.
        END_KEY (str): Key for the end index of an entity in the text.
        SCORE_KEY (str): Key for the confidence score of the entity recognition.
        DEFAULT_SCORE (float): Default score assigned to recognized entities if not provided.
        RECOGNITION_METADATA_KEY (str): Key for additional metadata associated with recognized entities.
        NAME_KEY (str): Key for the entity's name within the recognition metadata.
        ENTITY_KEY (str): Key for accessing entity string from the API response.
    """
    HEADER_CONTENT_TYPE_KEY: str
    HEADER_CONTENT_TYPE_VAL: str
    HEADER_X_API_KEY_KEY: str
    HEADER_USER_AGENT: str
    HEADER_USER_AGENT_VAL: str
    ID_LANGUAGE: str
    VERSION_CUSTOM_NER: str
    PAYLOAD_VERSION_KEY: str
    PAYLOAD_VERSION_VAL: str
    PAYLOAD_TEXT_KEY: str
    RESPONSE_TIMEOUT: int
    ENTITY_TYPE_KEY: str
    START_KEY: str
    START_IDX_KEY: str
    END_KEY: str
    LENGTH_KEY: str
    SCORE_KEY: str
    DEFAULT_SCORE: float
    RECOGNITION_METADATA_KEY: str
    NAME_KEY: str
    ENTITY_KEY: str

PROSA_ENTITY_MAP: Incomplete
DEFAULT_PROSA_SUPPORTED_PII_ENTITIES: Incomplete
