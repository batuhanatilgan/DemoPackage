from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    BrightnessExecutor,
    BrightnessResponse,
    BrightnessOutputs,
    OutputImage,
    MixerExecutor,
    MixerResponse,
    MixerOutputs,
    OutputInfo
)


def build_response(context):
    executor_name = context.__class__.__name__

    if executor_name == "Brightness":
        return build_response_brightness(context)
    elif executor_name == "Mixer":
        return build_response_mixer(context)
    else:
        return {}


def build_response_brightness(context):
    output_img = OutputImage(value=context.outputImage)
    brightness_outputs = BrightnessOutputs(outputImage=output_img)
    brightness_response = BrightnessResponse(outputs=brightness_outputs)
    brightness_executor = BrightnessExecutor(value=brightness_response)
    config_executor = ConfigExecutor(value=brightness_executor)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)


def build_response_mixer(context):
    output_img = OutputImage(value=context.outputImage)
    output_info = OutputInfo(value=context.outputInfo)
    mixer_outputs = MixerOutputs(
        outputImage=output_img,
        processInfo=output_info
    )
    mixer_response = MixerResponse(outputs=mixer_outputs)
    mixer_executor = MixerExecutor(value=mixer_response)
    config_executor = ConfigExecutor(value=mixer_executor)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)