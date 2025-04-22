from _typeshed import Incomplete
from gllm_privacy.pii_detector.recognizer.config import CAHYA_BERT_CONFIGURATION as CAHYA_BERT_CONFIGURATION
from presidio_analyzer import AnalysisExplanation, EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts as NlpArtifacts
from transformers import TokenClassificationPipeline as TokenClassificationPipeline

manager: Incomplete
logger: Incomplete

class TransformersRecognizer(EntityRecognizer):
    """Wrapper for a transformers model, if needed to be used within Presidio Analyzer.

    The class loads models hosted on HuggingFace - https://huggingface.co/
    and loads the model and tokenizer into a TokenClassification pipeline.
    Samples are split into short text chunks, ideally shorter than max_length input_ids of the individual model,
    to avoid truncation by the Tokenizer and loss of information

    A configuration object should be maintained for each dataset-model combination and translate
    entities names into a standardized view. A sample of a configuration file is attached in
    the example.

    Attributes:
        model_path (str | None, optional): String referencing a HuggingFace uploaded model to be used
                for inference. Defaults to None.
        pipeline (TokenClassificationPipeline | None, optional): Instance of a TokenClassificationPipeline
                including a Tokenizer and a Model. Defaults to None.
        supported_entities (list[str] | None, optional): List of entities to run inference on. Defaults to None.
    """
    model_path: Incomplete
    pipeline: Incomplete
    is_loaded: bool
    aggregation_mechanism: Incomplete
    ignore_labels: Incomplete
    model_to_presidio_mapping: Incomplete
    entity_mapping: Incomplete
    default_explanation: Incomplete
    chunk_length: Incomplete
    id_entity_name: Incomplete
    id_score_reduction: Incomplete
    supported_language: str
    def __init__(self, model_path: str | None = None, pipeline: TokenClassificationPipeline | None = None, supported_entities: list[str] | None = None) -> None:
        """Initialize the TransformersRecognizer.

        Args:
            model_path (str | None, optional): Path to the model to be used for inference. Defaults to None.
            pipeline (TokenClassificationPipeline | None, optional): Instance of a TokenClassificationPipeline
                including a Tokenizer and a Model. Defaults to None.
            supported_entities (list[str] | None, optional): List of entities to run inference on. Defaults to None.
        """
    def load(self) -> None:
        """Initialize the recognizer assets if needed."""
    def load_transformer(self, **kwargs) -> None:
        '''Load external configuration parameters and set default values.

        Args:
            **kwargs: Default values for class attributes and modify pipeline behavior.
                DATASET_TO_PRESIDIO_MAPPING (dict): Defines mapping entity strings from dataset format to
                    Presidio format.
                MODEL_TO_PRESIDIO_MAPPING (dict): Defines mapping entity strings from chosen model format to
                    Presidio format.
                SUB_WORD_AGGREGATION (str): Define how to aggregate sub-word tokens into full words and spans as defined
                    in HuggingFace https://huggingface.co/transformers/v4.8.0/main_classes/pipelines.html
                CHUNK_SIZE (int): Number of characters in each chunk of text.
                LABELS_TO_IGNORE (list[str]): List of entities to skip evaluation. Defaults to ["O"].
                DEFAULT_EXPLANATION (str): String format to use for prediction explanations.
                ID_ENTITY_NAME (str): Name of the ID entity.
                ID_SCORE_REDUCTION (float): Score multiplier for ID entities.
        '''
    def get_supported_entities(self) -> list[str]:
        """Return supported entities by this model.

        Returns:
            list[str]: List of the supported entities.
        """
    def analyze(self, text: str, entities: list[str], nlp_artifacts: NlpArtifacts = None) -> list[RecognizerResult]:
        """Analyze text using transformers model to produce NER tagging.

        Args:
            text (str): The text for analysis.
            entities (list[str]): The list of entities this recognizer is able to detect.
            nlp_artifacts (NlpArtifacts, optional): Not used by this recognizer.

        Returns:
            list[RecognizerResult]: The list of Presidio RecognizerResult constructed from the recognized
                transformers detections.
        """
    def build_transformers_explanation(self, original_score: float, explanation: str, pattern: str) -> AnalysisExplanation:
        """Create explanation for why this result was detected.

        Args:
            original_score (float): Score given by this recognizer.
            explanation (str): Explanation string.
            pattern (str): Regex pattern used.

        Returns:
            AnalysisExplanation: Structured explanation and scores of a NER model prediction.
        """
    @staticmethod
    def split_long_text(text: str, start_pos: int, max_length: int) -> list[tuple[int, int]]:
        """Split a long text into chunks at word boundaries.

        Args:
            text (str): Text to split
            start_pos (int): Starting position in the original text
            max_length (int): Maximum length of each chunk

        Returns:
            list of (start, end) position tuples for each chunk
        """
