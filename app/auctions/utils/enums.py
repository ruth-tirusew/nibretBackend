from enum import Enum

class StatusEnum(str,Enum):
    PENDING='PENDING'
    ACTIVE='ACTIVE'
    COMPLETED='COMPLETED'
    CANCELLED='CANCELLED'