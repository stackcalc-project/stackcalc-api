import sys
from enum import StrEnum

from pydantic import BaseModel


class Flag(StrEnum):
    OFF = "off"
    ON = "on"


class Detail(StrEnum):
    OFF = "off"
    APPROXIMATE = "approx"
    EXACT = "exact"


class TimeUnit(StrEnum):
    SECOND = "s"
    MINUTE = "min"
    HOUR = "h"


class LengthUnit(StrEnum):
    METER = "m"
    FEET = "ft"
    INCH = "in"
    CENTIMETER = "cm"
    MILLIMETER = "mm"


class WeighUnit(StrEnum):
    KILOGRAM = "kg"
    POUND = "lb"
    OUNCE = "oz"
    GRAM = "g"


class Units(BaseModel):
    time_unit: TimeUnit = TimeUnit.SECOND
    length_unit: LengthUnit = LengthUnit.MILLIMETER
    weight_unit: WeighUnit = WeighUnit.GRAM


class Agent(StrEnum):
    HUMAN = "human"
    ROBOT = "robot"


class HumanOptions(BaseModel):
    pass


class RobotOptions(BaseModel):
    pass


class LayerOptions(BaseModel):
    opt_rest_layer: Flag = Flag.ON
    opt_full_layers: Flag = Flag.ON
    opt_full_layer_threshold: float = 0.8


class GroupingOptions(BaseModel):
    opt_item_grouping: Flag = Flag.OFF
    opt_family_grouping: Flag = Flag.OFF


class StabilityOptions(BaseModel):
    opt_weight_stability: Detail = Detail.APPROXIMATE
    opt_static_stability: Detail = Detail.APPROXIMATE
    opt_dynamic_stability: Detail = Detail.APPROXIMATE


class PostprocessingOptions(BaseModel):
    opt_center: Flag = Flag.OFF
    opt_beautify: Flag = Flag.OFF


class Strategy(StrEnum):
    MONO = "mono"
    RAINBOW = "rainbow"
    MIXED = "mixed"


class MonoOptions(StabilityOptions, PostprocessingOptions):
    opt_item_quantity_eq_nof_bins: Flag = Flag.ON


class RainbowOptions(GroupingOptions, StabilityOptions, PostprocessingOptions):
    opt_item_quantity_eq_nof_layers: Flag = Flag.ON


class MixedOptions(LayerOptions, GroupingOptions, StabilityOptions, PostprocessingOptions):
    opt_max_support_distance: int = 5
    opt_min_support_ratio: float = 0.7
    opt_min_support_corner: int = 50


class BinDescr(BaseModel):
    id: str
    width: float
    depth: float
    height: float
    capacity: float = float("inf")
    quantity: int = sys.maxsize


class ItemDescr(BaseModel):
    id: str
    width: float
    depth: float
    height: float
    weight: float = 0
    quantity: int = sys.maxsize


class Problem(BaseModel):
    units: Units
    agent: Agent
    agent_options: HumanOptions | RobotOptions
    strategy: Strategy
    strategy_options: MonoOptions | RainbowOptions | MixedOptions
    bins: BinDescr
    items: ItemDescr | list[ItemDescr]


class MonoProblem(Problem):
    strategy: Strategy = Strategy.MONO
    strategy_options: MonoOptions | RainbowOptions | MixedOptions = MonoOptions()


class RainbowProblem(Problem):
    strategy: Strategy = Strategy.RAINBOW
    strategy_options: MonoOptions | RainbowOptions | MixedOptions = RainbowOptions()


class MixedProblem(Problem):
    strategy: Strategy = Strategy.MIXED
    strategy_options: MonoOptions | RainbowOptions | MixedOptions = MixedOptions()


class Solution(BaseModel):
    pass


class Job(BaseModel):
    id: str
    status: str
    progress: int
    result: str | None
