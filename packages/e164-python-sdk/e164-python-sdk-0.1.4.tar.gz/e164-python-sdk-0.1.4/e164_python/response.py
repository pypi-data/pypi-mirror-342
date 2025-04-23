from typing import Optional

class Response:
    def __init__(
        self,
        prefix: Optional[str] = None,
        calling_code: Optional[str] = None,
        iso3: Optional[str] = None,
        tadig: Optional[str] = None,
        mccmnc: Optional[str] = None,
        type: Optional[str] = None,
        location: Optional[str] = None,
        operator_brand: Optional[str] = None,
        operator_company: Optional[str] = None,
        total_length_min: Optional[str] = None,
        total_length_max: Optional[str] = None,
        weight: Optional[str] = None,
        source: Optional[str] = None,
    ):
        self.prefix: Optional[str] = prefix
        self.calling_code: Optional[str] = calling_code
        self.iso3: Optional[str] = iso3
        self.tadig: Optional[str] = tadig
        self.mccmnc: Optional[str] = mccmnc
        self.type: Optional[str] = type
        self.location: Optional[str] = location
        self.operator_brand: Optional[str] = operator_brand
        self.operator_company: Optional[str] = operator_company
        self.total_length_min: Optional[str] = total_length_min
        self.total_length_max: Optional[str] = total_length_max
        self.weight: Optional[str] = weight
        self.source: Optional[str] = source

    def __repr__(self) -> str:
        attributes = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items() if value is not None)
        return f"Response({attributes})"

    @classmethod
    def from_dict(cls, data: dict) -> 'Response':
        return cls(
            prefix=data.get('prefix'),
            calling_code=data.get('calling_code'),
            iso3=data.get('iso3'),
            tadig=data.get('tadig'),
            mccmnc=data.get('mccmnc'),
            type=data.get('type'),
            location=data.get('location'),
            operator_brand=data.get('operator_brand'),
            operator_company=data.get('operator_company'),
            total_length_min=data.get('total_length_min'),
            total_length_max=data.get('total_length_max'),
            weight=data.get('weight'),
            source=data.get('source'),
        )

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if value is not None}
