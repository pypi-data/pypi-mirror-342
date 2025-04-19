# railcif

Generate parsing code for Common Interchange Format files, commonly used
when working with UK train data.

## How do I use it?

Take your data:

```
RL708524001032025270220250704201770 8524HEBDEN BRIDGE   HBD00000     8524  30WY      13HEBDEN BRIDGE                            HEBDEN BRIDGE   HEBDEN BRIDGE                                               HEBDEN BRIDGE                                           0 NNNNNN0009006S0000000000000
RL708524007052024100420240704201770 8524HEBDEN BRIDGE   HBD00000     8524  30WY      13HEBDEN BRIDGE                            HEBDEN BRIDGE   HEBDEN BRIDGE                                               HEBDEN BRIDGE                                           0 NNNNNN0009006S0000000000000
RL708524009042024290320240704201770 8524HEBDEN BRIDGE   HBD00000     8524  30WY      13HEBDEN BRIDGE                            HEBDEN BRIDGE   HEBDEN BRIDGE                                               HEBDEN BRIDGE                                           0 NNNNNN0009006S0000000000000
RL708524021032025020320250704201770 8524HEBDEN BRIDGE   HBD00000     8524  30WY      13HEBDEN BRIDGE                            HEBDEN BRIDGE   HEBDEN BRIDGE                                               HEBDEN BRIDGE                                           0 NNNNNN0009006S0000000000000
RL708524026022025271120240704201770 8524HEBDEN BRIDGE   HBD00000     8524  30WY      13HEBDEN BRIDGE                            HEBDEN BRIDGE   HEBDEN BRIDGE  
...
```

And a description of the data:

```py
from traincif import CifRecord, Field


def parse_date_ddmmyyyy(byte_string: bytes) -> date:
    """Parses a ddmmyyyy byte string into a date object."""
    return datetime.datetime.strptime(byte_string.decode(), "%d%m%Y").date()


class LocationRecord(CifRecord):
    """
    Parses a Location record (type 'L') from the Fares Data Feed LOC file.
    Based on RSPS5045 Section 4.20.2.
    """
    
    update_marker: Annotated[str, Field(1)]
    """
    In a ‘changes only’ update file, indicates whether the record is to be
    inserted, amended or deleted (‘I’/’A’/’D’). For a full file refresh all
    update markers in the file will be set to ‘R’.
    """

    record_type: Annotated[Literal['L'], Field(1, discriminant=True)]
    """Record type discriminant. Contains ‘L’.”"""

    uic_code: Annotated[str, Field(7)]
    """A unique code which identifies this location."""

    end_date: Annotated[date, Field(8, parse_date_ddmmyyyy)]
    """
    Last date for which this record can be used. Format is ddmmyyyy.
    A high date (31122999) is used to indicate records which have no defined
    end date.
    """

    start_date: Annotated[date, Field(8, parse_date_ddmmyyyy)]
    """First date for which this record can be used. Format is ddmmyyyy."""

    quote_date: Annotated[date, Field(8, parse_date_ddmmyyyy)]
    """First date on which this record can be queried. Format is ddmmyyyy."""

    admin_area_code: Annotated[str, Field(3)]
    """Administrative area code (e.g. ‘70 ‘ = Britain)."""

    nlc_code: Annotated[str, Field(4)]
    """
    National location code, for British locations only. No value is output in
    this field for non-GB locations.
    """

    description: Annotated[str, Field(16)]
    """Location description."""

    crs_code: Annotated[str, Field(3)]
    """
    Where present, gives the location code as used by the Central
    Reservations System (superseded by NRS). Contains spaces for locations
    with no CRS code.
    """

    resv_code: Annotated[str, Field(5)]
    """The international reservation code."""

    ers_country: Annotated[str, Field(2)]
    """
    Along with the ERS Code this forms a reference to the location for use by
    Eurostar Reservation System.
    """

    ers_code: Annotated[str, Field(3)]
    """
    Along with the ERS Country this forms a reference to the location for use
    by Eurostar Reservation System.
    """

    fare_group: Annotated[str, Field(6)]
    """
    LOC-FARE-GROUP is always populated for BR locations. It is the same as
    LOC-NLC for locations which are not a member of a fare group, otherwise it
    contains a group NLC code, e.g. ‘1072’ = London.
    """

    county: Annotated[str, Field(2)]
    """
    Used to decide if a location is in Scotland, England & Wales or elsewhere.
    County codes on the mainland are all numeric values. Other values are ‘NI’
    (Northern Ireland), ‘IR’ (Ireland), ‘CI’ (Channel Islands).
    """

    pte_code: Annotated[str, Field(2)]
    """
    Code for the transport authority associated with the location (e.g. ‘GM’ =
    Greater Manchester). Note: this field is obsolete and will be set to space
    for all new locations.
    """

    zone_no: Annotated[str, Field(4)]
    """
    NLC code that matches a Zone location where the ZONE-IND = 1 to 6. Other
    values are not used. Spaces are permitted.
    """

    zone_ind: Annotated[str, Field(2)]
    """
    The Zone number. Permitted values are 1, 2, 3, 4, 5, 6, R, U and space.
    Where ZONE-IND is not space, then ZONE-NO is an NLC code, representing
    a travelcard location.
    """

    region: Annotated[str, Field(1)]
    """
    Identifies the region using a code ‘0’ = non-BR or LUL, ‘1’ = ER, ‘2’ = LMR,
    ‘3’ = SCR, ‘4’ = SR, ‘5’ = WR and ‘6’ = LUL.
    """

    hierarchy: Annotated[str, Field(1)]
    """
    Where the location fits in the hierarchy of location types (e.g. major
    station, minor station). Note – this field is obsolete and will set to space
    for all new locations.
    """

    cc_desc_out: Annotated[str, Field(41)]
    """
    Location description for credit card size tickets for the outward journey
    from this location.
    """

    cc_desc_rtn: Annotated[str, Field(16)]
    """
    Location description for credit card size tickets for the return journey to
    this location.
    """

    atb_desc_out: Annotated[str, Field(60)]
    """
    Location description for ATB (airline) size tickets for the outward journey
    from this location.
    """

    atb_desc_rtn: Annotated[str, Field(30)]
    """
    Location description for ATB (airline) size tickets for the return journey
    to this location.
    """

    special_facilities: Annotated[str, Field(26)]
    """
    Indicates the facilities available at the location, each character represents
    a special facility.
    """

    lul_direction_ind: Annotated[str, Field(1)]
    """
    Values ‘0’, ‘1’, ‘2’, ‘3’ or space. Used for LUL magnetic stripe encoding.
    """

    lul_uts_mode: Annotated[str, Field(1)]
    """
    Used to indicate which transport modes are encoded in the ticket (LUL
    magnetic stripe encoding).
    """

    lul_zone_1: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_zone_2: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_zone_3: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_zone_4: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_zone_5: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_zone_6: Annotated[str, Field(1)]
    """
    Value = ‘Y’ or ‘N’, used for LUL magnetic stripe encoding. Please note that
    this information is supplied from the source system, and is not validated
    by DTD.
    """

    lul_uts_london_stn: Annotated[str, Field(1)]
    """
    Values are ‘0’ or ‘1’. Indicates whether the station is a London station. Used
    for LUL magnetic stripe encoding. Please note that this information is
    supplied from the source system, and is not validated by DTD.
    """

    uts_code: Annotated[str, Field(3)]
    """Location code for UTS. Used for LUL magnetic stripe encoding."""

    uts_a_code: Annotated[str, Field(3)]
    """Alternative UTS code. Used for LUL magnetic stripe encoding."""

    uts_ptr_bias: Annotated[str, Field(1)]
    """Used for LUL magnetic stripe encoding."""

    uts_offset: Annotated[str, Field(1)]
    """Used for LUL magnetic stripe encoding."""

    uts_north: Annotated[str, Field(3)]
    """Used for LUL magnetic stripe encoding."""

    uts_east: Annotated[str, Field(3)]
    """Used for LUL magnetic stripe encoding."""

    uts_south: Annotated[str, Field(3)]
    """Used for LUL magnetic stripe encoding."""

    uts_west: Annotated[str, Field(3)]
    """Used for LUL magnetic stripe encoding."""
```

And parse it:

```
>>> iter = LocationRecord.parse_from_file(open("some_file.txt", "rb"))
>>> for record in iter:
...     print(record)
... 
LocationRecord(update_marker='R', record_type=None, uic_code='7085240', end_date=datetime.date(2025, 3, 1), start_date=datetime.date(2025, 2, 27), quote_date=datetime.date(2017, 4, 7), admin_area_code='70', nlc_code='8524', description='HEBDEN BRIDGE', crs_code='HBD', resv_code='00000', ers_country='', ers_code='', fare_group='8524', county='30', pte_code='WY', zone_no='', zone_ind='', region='1', hierarchy='3', cc_desc_out='HEBDEN BRIDGE', cc_desc_rtn='HEBDEN BRIDGE', atb_desc_out='HEBDEN BRIDGE', atb_desc_rtn='HEBDEN BRIDGE', special_facilities='', lul_direction_ind='0', lul_uts_mode='', lul_zone_1='N', lul_zone_2='N', lul_zone_3='N', lul_zone_4='N', lul_zone_5='N', lul_zone_6='N', lul_uts_london_stn='0', uts_code='009', uts_a_code='006', uts_ptr_bias='S', uts_offset='0', uts_north='000', uts_east='000', uts_south='000', uts_west='000')
...
```

Where multiple records exist within one file, you can use `Field(discriminant=True)`
and `RecordUnion` to parse all of them at once:

```
from traincif import RecordUnion

iter = RecordUnion(LocationRecord, ...).parse_from_file(open("RJFAF357.LOC"))
for record in iter:
    ...
```

## Reference

All fields must be `typing.Annotated`, so the parser knows the length of the field.

A field may be one of:

- int
- str
- bytes
- None

> [!INFO]
> Note that strings are stripped of leading and trailing whitespace, but
> bytes aren't.

## Licensing

MIT or WTFPL, depending on how much of a prude you are

> [!IMPORTANT]
> This repository contains data from National Rail Enquiries feeds:
>
> > tests/RJFAF357.LOC
>
> Such data is not under the same license as the rest of this repository.
> 
> See https://opendata.nationalrail.co.uk/terms
>
> Data from https://nationalrail.co.uk/