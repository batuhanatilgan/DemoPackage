from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Param

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Input Image"

class OverlayInputImage(Input):
    name: Literal["overlayImage"] = "overlayImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
            title = "Overlay Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image"

class OutputInfo(Output):
    name: Literal["outputInfo"] = "outputInfo"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Process Info"

class BrightnessValue(Config):
    name: Literal["BrightnessValue"] = "BrightnessValue"
    value: float = Field(default=1.0, ge=0.0, le=3.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Brightness Level"

class OptionManual(Config):
    name: Literal["OptionManual"] = "OptionManual"
    example: BrightnessValue
    value: Literal["Manual"] = "Manual"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Manual Mode"

class PresetLow(Config):
    name: Literal["PresetLow"] = "PresetLow"
    value: Literal["Low"] = "Low"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Low"

class PresetHigh(Config):
    name: Literal["PresetHigh"] = "PresetHigh"
    value: Literal["High"] = "High"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "High"

class PresetSelection(Config):
    name: Literal["PresetSelection"] = "PresetSelection"
    value: Union[PresetLow, PresetHigh]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Select Preset"

class OptionPreset(Config):
    name: Literal["OptionPreset"] = "OptionPreset"
    example: PresetSelection
    value: Literal["Preset"] = "Preset"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Preset Mode"

class ConfigAdjustmentMode(Config):
    name: Literal["ConfigAdjustmentMode"] = "ConfigAdjustmentMode"
    value: Union[OptionManual, OptionPreset]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Adjustment Mode"

class BrightnessInputs(Inputs):
    inputImage: InputImage

class BrightnessConfigs(Configs):
    adjustmentMode: ConfigAdjustmentMode

class BrightnessOutputs(Outputs):
    outputImage: OutputImage

class BrightnessRequest(Request):
    inputs: Optional[BrightnessInputs]
    configs: BrightnessConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class BrightnessResponse(Response):
    outputs: BrightnessOutputs

class BrightnessExecutor(Config):
    name: Literal["Brightness"] = "Brightness"
    value: Union[BrightnessRequest, BrightnessResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Brightness Adjuster"
        json_schema_extra = {"target": {"value": 0}}

class OpacityValue(Config):
    name: Literal["OpacityValue"] = "OpacityValue"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Opacity (0.0-1.0)"

class OptionOpacity(Config):
    name: Literal["OptionOpacity"] = "OptionOpacity"
    example: OpacityValue
    value: Literal["Opacity"] = "Opacity"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Opacity Blend"

class MethodAdd(Config):
    name: Literal["MethodAdd"] = "MethodAdd"
    value: Literal["Add"] = "Add"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Add"

class MethodMultiply(Config):
    name: Literal["MethodMultiply"] = "MethodMultiply"
    value: Literal["Multiply"] = "Multiply"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Multiply"

class MethodSelection(Config):
    name: Literal["MethodSelection"] = "MethodSelection"
    value: Union[MethodAdd, MethodMultiply]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Select Method"

class OptionMethod(Config):
    name: Literal["OptionMethod"] = "OptionMethod"
    example: MethodSelection
    value: Literal["Method"] = "Method"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Method Blend"

class ConfigBlendMode(Config):
    name: Literal["ConfigBlendMode"] = "ConfigBlendMode"
    value: Union[OptionOpacity, OptionMethod]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Blending Mode"

class MixerInputs(Inputs):
    inputImage: InputImage
    overlayInputImage: OverlayInputImage

class MixerConfigs(Configs):
    blendMode: ConfigBlendMode

class MixerOutputs(Outputs):
    outputImage: OutputImage
    outputInfo: OutputInfo

class MixerRequest(Request):
    inputs: Optional[MixerInputs]
    configs: MixerConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class MixerResponse(Response):
    outputs: MixerOutputs

class MixerExecutor(Config):
    name: Literal["Mixer"] = "Mixer"
    value: Union[MixerRequest, MixerResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Mixer"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BrightnessExecutor, MixerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Select Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"