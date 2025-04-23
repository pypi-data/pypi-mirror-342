from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MonHW(_message.Message):
    __slots__ = ["pin_sel", "pin_bank", "pin_dir", "pin_val", "noise_per_ms", "agc_cnt", "a_status", "a_power", "flags", "reserved0", "used_mask", "vp", "jam_ind", "reserved1", "pin_irq", "pull_h", "pull_l"]
    PIN_SEL_FIELD_NUMBER: _ClassVar[int]
    PIN_BANK_FIELD_NUMBER: _ClassVar[int]
    PIN_DIR_FIELD_NUMBER: _ClassVar[int]
    PIN_VAL_FIELD_NUMBER: _ClassVar[int]
    NOISE_PER_MS_FIELD_NUMBER: _ClassVar[int]
    AGC_CNT_FIELD_NUMBER: _ClassVar[int]
    A_STATUS_FIELD_NUMBER: _ClassVar[int]
    A_POWER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    USED_MASK_FIELD_NUMBER: _ClassVar[int]
    VP_FIELD_NUMBER: _ClassVar[int]
    JAM_IND_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    PIN_IRQ_FIELD_NUMBER: _ClassVar[int]
    PULL_H_FIELD_NUMBER: _ClassVar[int]
    PULL_L_FIELD_NUMBER: _ClassVar[int]
    pin_sel: int
    pin_bank: int
    pin_dir: int
    pin_val: int
    noise_per_ms: int
    agc_cnt: int
    a_status: int
    a_power: int
    flags: int
    reserved0: int
    used_mask: int
    vp: _containers.RepeatedScalarFieldContainer[int]
    jam_ind: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    pin_irq: int
    pull_h: int
    pull_l: int
    def __init__(self, pin_sel: _Optional[int] = ..., pin_bank: _Optional[int] = ..., pin_dir: _Optional[int] = ..., pin_val: _Optional[int] = ..., noise_per_ms: _Optional[int] = ..., agc_cnt: _Optional[int] = ..., a_status: _Optional[int] = ..., a_power: _Optional[int] = ..., flags: _Optional[int] = ..., reserved0: _Optional[int] = ..., used_mask: _Optional[int] = ..., vp: _Optional[_Iterable[int]] = ..., jam_ind: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., pin_irq: _Optional[int] = ..., pull_h: _Optional[int] = ..., pull_l: _Optional[int] = ...) -> None: ...
