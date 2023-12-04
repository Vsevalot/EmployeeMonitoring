from enum import Enum

PARTICIPANT_READ_ORGANISATION = "participants:read?scope=organisation_unit"


class Permissions(Enum):
    create_manager = "managers:create"
    create_organisation_unit = "organisation_unit:create"
