import datajoint as dj

from . import get_schema_name


schema = dj.schema(get_schema_name('lab'))


# ------------------- GENERAL LAB INFORMATION --------------------


@schema
class Lab(dj.Lookup):
    definition = """
    lab             : varchar(24)  #  Abbreviated lab name 
    ---
    lab_name        : varchar(255)   # full lab name
    institution     : varchar(255)
    address         : varchar(255)
    time_zone       : varchar(64)
    """

    contents = [('SWC', 'Sainsbury Wellcome Centre', 'University College London',
                 '25 Howland Street London W1T 4JG', 'GMT+1')]


@schema
class Location(dj.Lookup):
    definition = """
    # location of animal housing or experimental rigs
    -> Lab
    location            : varchar(32)
    ---
    location_description=''    : varchar(255)
    """

    contents = [('SWC', 'room-0', 'room for experiment 0')]


@schema
class UserRole(dj.Lookup):
    definition = """
    user_role       : varchar(16)
    """


@schema
class User(dj.Lookup):
    definition = """
    user                : varchar(32)
    ---
    user_email=''       : varchar(128)
    user_cellphone=''   : varchar(32)
    """


@schema
class LabMembership(dj.Lookup):
    definition = """
    -> Lab
    -> User
    ---
    -> [nullable] UserRole
    """


@schema
class ProtocolType(dj.Lookup):
    definition = """
    protocol_type           : varchar(32)
    """


@schema
class Protocol(dj.Lookup):
    definition = """
    # protocol approved by some institutions like IACUC, IRB
    protocol                : varchar(16)
    ---
    -> ProtocolType
    protocol_description=''        : varchar(255)
    """


@schema
class Project(dj.Lookup):
    definition = """
    project                 : varchar(32)
    ---
    project_description=''         : varchar(1024)
    """


@schema
class ProjectUser(dj.Manual):
    definition = """
    -> Project
    -> User
    """


@schema
class Source(dj.Lookup):
    definition = """
    # source or supplier of animals
    source             : varchar(32)    # abbreviated source name
    ---
    source_name        : varchar(255)
    contact_details='' : varchar(255)
    source_description=''     : varchar(255)
    """


# ------------------- ARENA INFORMATION --------------------

@schema
class ArenaShape(dj.Lookup):
    definition = """
    arena_shape: varchar(32)
    """
    contents = zip(['square', 'circular', 'rectangular', 'linear'])


@schema
class Arena(dj.Lookup):
    """
    Coordinate frame convention:
    + x-dimension: x=0 is the left most point of the bounding box of the arena
    + y-dimension: y=0 is the bottom most point of the bounding box of the arena
    + z-dimension: z=0 is the lowest point of the arena (e.g. the ground)
    TODO: confirm/update this
    """
    definition = """
    arena_name: varchar(32)  # unique name of the arena (e.g. circular_2m)
    ---
    arena_description='': varchar(1000)
    -> ArenaShape
    arena_x_dim:    float # (m) x-dimension of the bounding box of this arena
    arena_y_dim:    float # (m) y-dimension of the bounding box of this arena
    arena_z_dim=0:  float # (m) z-dimension of this arena (e.g. wall height)
    """

    contents = [
        ('circle-2m', 'circular arena with 2-meter diameter', 'circular', 2, 2, 0.2)]


# ------------------- EQUIPMENTS --------------------


@schema
class Camera(dj.Lookup):
    definition = """  # Physical cameras, identified by unique serial number
    camera_id: int
    ---
    camera_serial_number: varchar(36)
    camera_description='': varchar(255)
    """

    contents = [(0, 'FrameTop', 'Overhead camera'),
                (1, 'FrameSide', 'Side camera')]


@schema
class FoodPatch(dj.Lookup):
    definition = """  # Physical food patch devices, identified by unique serial number
    food_patch_id: int
    ---
    food_patch_serial_number: varchar(36)
    food_patch_description: varchar(255)
    """

    contents = [(0, 'PatchEvents', '')]
