"""Handles the entire logic of the Presidio-anonymizer and text anonymizing."""
import logging

from presidio_anonymizer.entities import AnonymizerRequest, InvalidParamException


class AnonymizerEngine:
    """
    AnonymizerEngine class.

    Handles the entire logic of the Presidio-anonymizer. Gets the original text
    and replaces the PII entities with the desired transformations.
    """

    logger = logging.getLogger("presidio-anonymizer")

    def __init__(
        self,
    ):
        """Handle text replacement for PIIs with requested transformations.

        :param data: a map which contains the transformations, analyzer_results and text
        """

    def anonymize(self, engine_request: AnonymizerRequest) -> str:
        """Anonymize method to anonymize the given text.

        :return: the anonymized text
        """
        original_text = engine_request.get_text()
        last_replacement_point = len(original_text)
        output_text = engine_request.get_text()
        analyzer_results = (
            engine_request.get_analysis_results().to_sorted_unique_results(True)
        )
        for analyzer_result in analyzer_results:
            anonymizer_class = Anonymizer.subclasses.get_types().find(
                analyzer_result.entity_type
            )
            transformation_params_class = anonymizer_class.get_param_calss()
            transformation_params = engine_request.get_transformation_params(
                analyzer_result.entity_type
            )
            transformation_params_class(transformation_params).validate()
            self.logger.debug(
                f"for analyzer result {analyzer_result} received transformation "
                f"{str(transformation)}"
            )
            new_text = anonymizer_class().anonymize(
                original_text=original_text, **transformation_params
            )
            end_of_text = min(analyzer_result.end, last_replacement_point)
            self.__validate_position_over_text(analyzer_result, text_len)
            output_text = (
                output_text[: analyzer_result.start]
                + new_text
                + output_text[end_of_text:]
            )
            last_replacement_point = analyzer_result.start
        return output_text

    def __validate_position_over_text(self, analyzer_result, text_len):
        if text_len < analyzer_result.start or analyzer_result.end > text_len:
            raise InvalidParamException(
                f"Invalid analyzer result: '{analyzer_result}', "
                f"original text length is only {text_len}."
            )
