from enum import Enum

class PropertyType(str, Enum):
    PLOT_LAND = "Plot Land"
    SINGLE_FAMILY = "Single Family"
    APARTMENT = "Apartment"
    PENTHOUSE = "Penthouse"
    TOWNHOUSE = "Townhouse"
    VILLA = "Villa"
    COMMERCIAL = "Commercial"
    CONDOMINIUM = "Condominium"
    OFFICE_SPACE = "Office Space"
    WAREHOUSE = "Warehouse"
    LUXURY_APARTMENT = "Luxury Apartment"


class OwnerType(str, Enum):
    REGULAR="REGULAR"
    PREMIUM="PREMIUM"