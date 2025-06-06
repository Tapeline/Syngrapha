from dataclasses import dataclass

value_object = dataclass(frozen=True, slots=True)
