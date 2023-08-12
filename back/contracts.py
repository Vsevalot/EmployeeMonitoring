from enum import Enum


class Permissions(Enum):
    create_manager = "managers:create"
    create_organisation_unit = "organisation_unit:create"
