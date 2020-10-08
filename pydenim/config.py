from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    n_rows: int
    n_cols: int
    starting_organism_count: int
