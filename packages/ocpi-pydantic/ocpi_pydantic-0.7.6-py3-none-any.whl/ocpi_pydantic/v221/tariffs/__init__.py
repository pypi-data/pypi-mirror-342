from decimal import Decimal
from typing import Annotated

from ocpi_pydantic.v221.locations.location import OcpiEnergyMix
from pydantic import AwareDatetime, BaseModel, Field, HttpUrl

from ocpi_pydantic.v221.base import OcpiDisplayText, OcpiPrice
from ocpi_pydantic.v221.enum import OcpiDayOfWeekEnum, OcpiReservationRestrictionTypeEnum, OcpiTariffDimensionTypeEnum, OcpiTariffTypeEnum



class OcpiPriceComponent(BaseModel):
    '''
    OCPI 11.4.2. PriceComponent class
    '''
    type: OcpiTariffDimensionTypeEnum = Field(description='Type of tariff dimension.')
    price: Decimal = Field(description='Price per unit (excl. VAT) for this tariff dimension.')
    vat: Annotated[float | None, Field(
        description='''
        Applicable VAT percentage for this tariff dimension. If omitted, no VAT
        is applicable. Not providing a VAT is different from 0% VAT, which would
        be a value of 0.0 here.
        ''',
    )] = None
    step_size: int = Field(
        description='''
        Minimum amount to be billed. This unit will be billed in this step_size
        blocks. Amounts that are less then this step_size are rounded up to
        the given step_size. For example: if type is TIME and step_size
        has a value of 300, then time will be billed in blocks of 5 minutes. If 6
        minutes were used, 10 minutes (2 blocks of step_size) will be billed.
        ''',
    )



class OcpiTariffRestrictions(BaseModel):
    '''
    OCPI 11.4.6. TariffRestrictions class

    These restrictions are not for the entire Charging Session. They only describe if and when a TariffElement becomes active or
    inactive during a Charging Session.

    When more than one restriction is set, they are to be threaded as a logical AND. So all need to be valid before this tariff is active.
    '''
    start_time: Annotated[str | None, Field(
        min_length=5,
        max_length=5,
        description='''
        Start time of day in local time, the time zone is defined in the `time_zone` field of
        the Location, for example 13:30, valid from this time of the day. Must be in 24h
        format with leading zeros. Hour/Minute separator: ":" Regex: `([0-1][0-
        9]|2[0-3]):[0-5][0-9]`
        ''',
    )] = None
    end_time: Annotated[str | None, Field(
        min_length=5,
        max_length=5,
        description='''
        End time of day in local time, the time zone is defined in the `time_zone` field of
        the Location, for example 19:45, valid until this time of the day. Same syntax as
        `start_time`. If end_time < start_time then the period wraps around to the next
        day. To stop at end of the day use: 00:00.
        ''',
    )] = None
    start_date: Annotated[str | None, Field(
        min_length=10,
        max_length=10,
        description='''
        Start date in local time, the time zone is defined in the `time_zone` field of the
        Location, for example: 2015-12-24, valid from this day (inclusive). Regex:
        `([12][0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])`
        ''',
    )] = None
    end_date: Annotated[str | None, Field(
        min_length=10,
        max_length=10,
        description='''
        End date in local time, the time zone is defined in the `time_zone` field of the
        Location, for example: 2015-12-27, valid until this day (exclusive). Same syntax
        as `start_date`.
        ''',
    )] = None
    min_kwh: Annotated[float | None, Field(
        description='''
        Minimum consumed energy in kWh, for example 20, valid from this amount of
        energy (inclusive) being used.
        ''',
    )] = None
    max_kwh: Annotated[float | None, Field(
        description='''
        Maximum consumed energy in kWh, for example 50, valid until this amount of
        energy (exclusive) being used.
        ''',
    )] = None
    min_current: Annotated[float | None, Field(
        description='''
        Sum of the minimum current (in Amperes) over all phases, for example 5. When
        the EV is charging with more than, or equal to, the defined amount of current,
        this TariffElement is/becomes active. If the charging current is or becomes lower,
        this TariffElement is not or no longer valid and becomes inactive. This describes
        NOT the minimum current over the entire Charging Session. This restriction can
        make a TariffElement become active when the charging current is above the
        defined value, but the TariffElement MUST no longer be active when the
        charging current drops below the defined value.
        ''',
    )] = None
    max_current: Annotated[float | None, Field(
        description='''
        Sum of the maximum current (in Amperes) over all phases, for example 20.
        When the EV is charging with less than the defined amount of current, this
        TariffElement becomes/is active. If the charging current is or becomes higher,
        this TariffElement is not or no longer valid and becomes inactive. This describes
        NOT the maximum current over the entire Charging Session. This restriction can
        make a TariffElement become active when the charging current is below this
        value, but the TariffElement MUST no longer be active when the charging
        current raises above the defined value.
        ''',
    )] = None
    min_power: Annotated[float | None, Field(
        description='''
        Minimum power in kW, for example 5. When the EV is charging with more than,
        or equal to, the defined amount of power, this TariffElement is/becomes active. If
        the charging power is or becomes lower, this TariffElement is not or no longer
        valid and becomes inactive. This describes NOT the minimum power over the
        entire Charging Session. This restriction can make a TariffElement become
        active when the charging power is above this value, but the TariffElement MUST
        no longer be active when the charging power drops below the defined value.
        ''',
    )] = None
    min_power: Annotated[float | None, Field(
        description='''
        Maximum power in kW, for example 20. When the EV is charging with less than
        the defined amount of power, this TariffElement becomes/is active. If the
        charging power is or becomes higher, this TariffElement is not or no longer valid
        and becomes inactive. This describes NOT the maximum power over the entire
        Charging Session. This restriction can make a TariffElement become active
        when the charging power is below this value, but the TariffElement MUST no
        longer be active when the charging power raises above the defined value.
        ''',
    )] = None
    min_duration: Annotated[int | None, Field(
        description='''
        Minimum duration in seconds the Charging Session MUST last (inclusive).
        When the duration of a Charging Session is longer than the defined value, this
        TariffElement is or becomes active. Before that moment, this TariffElement is not
        yet active.
        ''',
    )] = None
    max_duration: Annotated[int | None, Field(
        description='''
        Maximum duration in seconds the Charging Session MUST last (exclusive).
        When the duration of a Charging Session is shorter than the defined value, this
        TariffElement is or becomes active. After that moment, this TariffElement is no
        longer active.
        ''',
    )] = None
    day_of_week: Annotated[list[OcpiDayOfWeekEnum], Field(description='Which day(s) of the week this TariffElement is active.')] = []
    reservation: Annotated[OcpiReservationRestrictionTypeEnum | None, Field(
        description='''
        When this field is present, the TariffElement describes reservation costs. A
        reservation starts when the reservation is made, and ends when the driver
        starts charging on the reserved EVSE/Location, or when the reservation
        expires. A reservation can only have: FLAT and TIME TariffDimensions, where
        `TIME` is for the duration of the reservation.
        ''',
    )] = None




class OcpiTariffElement(BaseModel):
    '''
    OCPI 11.4.4. TariffElement class
    '''
    price_components: list[OcpiPriceComponent] = Field(description='List of price components that describe the pricing of a tariff.')
    restrictions: Annotated[OcpiTariffRestrictions | None, Field(description='Restrictions that describe the applicability of a tariff.')] = None



class OcpiTariff(BaseModel):
    '''
    OCPI 11.3.1. Tariff Object
    '''
    country_code: str = Field(min_length=2, max_length=2, description="""ISO-3166 alpha-2 country code of the CPO that 'owns' this Tariff.""")
    party_id: str = Field(
        min_length=3, max_length=3, description="""
        ID of the CPO that 'owns' this Traiff (following the ISO-15118
        standard).
        """,
    )
    id: str = Field(
        max_length=36,
        description='''
        Uniquely identifies the tariff within the CPO’s platform (and suboperator
        platforms).
        ''',
    )
    currency: str = Field(max_length=3, description='ISO-4217 code of the currency of this tariff.')
    type: Annotated[OcpiTariffTypeEnum | None, Field(
        description='''
        Defines the type of the tariff. This allows for distinction in case of given Charging
        Preferences. When omitted, this tariff is valid for all sessions.
        ''',
    )] = None
    tariff_alt_text: Annotated[list[OcpiDisplayText], Field(description='List of multi-language alternative tariff info texts.')] = []
    tariff_alt_url: Annotated[HttpUrl | None, Field(
        description='''
        URL to a web page that contains an explanation of the tariff information in
        human readable form.
        ''',
    )] = None
    min_price: Annotated[OcpiPrice | None, Field(
        description='''
        When this field is set, a Charging Session with this tariff will at least cost this
        amount. This is different from a `FLAT` fee (Start Tariff, Transaction Fee), as a
        `FLAT` fee is a fixed amount that has to be paid for any Charging Session. A
        minimum price indicates that when the cost of a Charging Session is lower than
        this amount, the cost of the Session will be equal to this amount. (Also see note
        below)
        ''',
    )] = None
    max_price: Annotated[OcpiPrice | None, Field(
        description='''
        When this field is set, a Charging Session with this tariff will NOT cost more than
        this amount. (See note below)
        ''',
    )] = None
    elements: list[OcpiTariffElement] = Field(description='List of Tariff Elements.')
    start_date_time: Annotated[AwareDatetime | None, Field(
        description='''
        The time when this tariff becomes active, in UTC, `time_zone` field of the
        Location can be used to convert to local time. Typically used for a new tariff that
        is already given with the location, before it becomes active. (See note below)
        ''',
    )] = None
    end_date_time: Annotated[AwareDatetime | None, Field(
        description='''
        The time after which this tariff is no longer valid, in UTC, `time_zone` field if the
        Location can be used to convert to local time. Typically used when this tariff is
        going to be replaced with a different tariff in the near future. (See note below)
        ''',
    )] = None
    energy_mix: Annotated[OcpiEnergyMix | None, Field(description='Details on the energy supplied with this tariff.')] = None
    last_updated: AwareDatetime = Field(description='Timestamp when this Tariff was last updated (or created).')
