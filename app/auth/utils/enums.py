from enum import Enum

class Role(str, Enum):
    ADMIN="ADMIN"
    AGENT="AGENT"
    CUSTOMER="CUSTOMER"