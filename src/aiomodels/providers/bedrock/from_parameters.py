from types_aiobotocore_bedrock_runtime.type_defs import InferenceConfigurationTypeDef

from aiomodels.parameters.parameters import Parameters


class FromParameters:
    @staticmethod
    def from_parameters(parameters: Parameters) -> InferenceConfigurationTypeDef:
        inference_config: InferenceConfigurationTypeDef = {}

        if parameters.temperature is not None:
            inference_config["temperature"] = parameters.temperature
        if parameters.top_p is not None:
            inference_config["topP"] = parameters.top_p
        if parameters.max_tokens is not None:
            inference_config["maxTokens"] = parameters.max_tokens
        if parameters.stop is not None:
            inference_config["stopSequences"] = parameters.stop

        return inference_config
