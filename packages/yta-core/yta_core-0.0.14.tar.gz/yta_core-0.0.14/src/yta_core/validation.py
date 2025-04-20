"""
Module to include all the validation classes
that simplify the way we check if the provided
jsons are valid and accepted by our system or
not to build the Segment, Enhancement and/or
Shortcode components.
"""
from yta_core.configuration import Configuration
from yta_core.builder.utils import enum_name_to_class
from yta_core.builder import is_element_valid_for_method
from yta_core.builder.enums import Premade, TextPremade
from yta_core.shortcodes.parser import shortcode_parser, empty_shortcode_parser
from yta_core.enums.field import SegmentField, EnhancementField, ShortcodeField
from yta_core.enums.mode import SegmentMode, EnhancementMode, ShortcodeMode
from yta_core.enums.type import SegmentType, EnhancementType, ShortcodeType
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration
from yta_core.enums.component import Component
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from typing import Union


class BuilderValidator:
    """
    Class to validate everything related to segments,
    enhancements and shortcodes. A single source of
    validation.
    """

    @staticmethod
    def validate_segment_has_expected_fields(
        segment: dict
    ) -> None:
        """
        Check if the provided 'segment' dict has all the
        fields it must have as a Segment, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            segment,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_segment_has_valid_values(
        segment: dict
    ) -> None:
        """
        Check if the provided 'segment' dict has valid
        values for all the required fields.
        """
        return BuilderValidator._validate_component_has_valid_values(
            segment,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_has_expected_fields(
        enhancement: dict
    ) -> None:
        """
        Check if the provided 'enhancement' dict has all the
        fields it must have as an Enhancement, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            enhancement,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_has_expected_fields(
        shortcode: dict
    ) -> None:
        """
        Check if the provided 'shortcode' dict has all the
        fields it must have as a Shortcode, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            shortcode,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_has_expected_fields(
        element: dict,
        component: Component
    ) -> None:
        """
        Check if the provided 'element' dict, that must be
        a dict representing the 'component' passed as 
        parameter, has all the fields it must have, and 
        raises an Exception if not.

        This method will detect the parameters that exist
        in the provided 'element' but are not expected to
        be on it, and the ones that are expected to be but
        are not set on it.
        """
        component = Component.to_enum(component)
        ParameterValidator.validate_mandatory_dict('element', element)

        accepted_fields = {
            Component.SEGMENT: lambda: SegmentField.get_all_values(),
            Component.ENHANCEMENT: lambda: EnhancementField.get_all_values(),
            Component.SHORTCODE: lambda: ShortcodeField.get_all_values()
        }[component]()

        accepted_fields_str = ', '.join(accepted_fields)

        unaccepted_fields = [
            key
            for key in element.keys()
            if key not in accepted_fields
        ]
        unaccepted_fields_str = ', '.join(unaccepted_fields)
        
        missing_fields = [
            field
            for field in accepted_fields
            if field not in element
        ]
        missing_fields_str = ', '.join(missing_fields)

        if missing_fields:
            raise Exception(f'The next fields are mandatory and were not found in the element: "{missing_fields_str}". The mandatory fields are: "{accepted_fields_str}".')

        if unaccepted_fields:
            raise Exception(f'The next fields are not accepted in the provided element by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}".')
        
        return element
    
    @staticmethod
    def _validate_component_has_valid_values(
        element: dict,
        component: Component
    ) -> None:
        """
        Check if the provided 'element' dict, that must be
        a dict representing the 'component' passed as 
        parameter, has valid values for all its fields, and 
        raises an Exception if not.

        This method will detect the parameters that doesn't
        have valid values.
        """
        component = Component.to_enum(component)
        ParameterValidator.validate_mandatory_dict('element', element)

        # Validate 'audio_narration'
        ElementValidator.validate_voice_narration_fields(element)
        # Validate 'music'
        ElementValidator.validate_music_fields(element)
        # TODO: Validate other fields
    
    # MODE below
    @staticmethod
    def validate_segment_mode_field(
        mode: Union[SegmentMode, str, None]
    ):
        """
        Validate the provided 'mode' for a Segment
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_mode_field(
        mode: Union[EnhancementMode, str, None]
    ):
        """
        Validate the provided 'mode' for an Enhancement
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_mode_field(
        mode: Union[ShortcodeMode, str, None]
    ):
        """
        Validate the provided 'mode' for a Shortcode
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_mode_field(
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None],
        component: Component
    ):
        """
        Validate the provided 'mode' for the given
        'component'. The mode should be a SegmentMode,
        EnhancementMode or ShortcodeMode, or a string
        that fits one of these 3 enum classes.

        This method will raise an exception if the 
        'mode' provided is not valid for the given
        'component'.
        """
        component = Component.to_enum(component)

        # TODO: Do we accept 'None' value (?)
        return component.get_mode(mode)
    
    # MODE FOR TYPE below
    @staticmethod
    def validate_segment_mode_for_type(
        mode: Union[SegmentMode, str, None],
        type: Union[SegmentType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for a Segment.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_mode_for_type(
        mode: Union[EnhancementMode, str, None],
        type: Union[EnhancementType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for an Enhancement.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_mode_for_type(
        mode: Union[ShortcodeMode, str, None],
        type: Union[ShortcodeType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for an Shortcode.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.SHORTCODE
        )
    
    @staticmethod
    def _validate_component_mode_for_type(
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str],
        component: Component
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for the also provided
        'component'.
        """
        component = Component.to_enum(component)

        if not component.is_mode_accepted_for_type(mode, type):
            type = (
                type
                if PythonValidator.is_string(type) else
                type.value
            )

            raise Exception(f'The "{type}" type does not accept the provided "{mode}" mode.')

    # DURATION below
    @staticmethod
    def validate_segment_duration_field(
        duration: Union[SegmentStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for a
        Segment.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_duration_field(
        duration: Union[EnhancementStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for an
        Enhancement.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_duration_field(
        duration: Union[ShortcodeStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for a
        Shortcode.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_duration_field(
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str],
        component: Component
    ):
        """
        Validate that the provided 'duration' is valid for
        the given 'component'.
        """
        component = Component.to_enum(component)

        return component.get_duration(duration)
    
    # DURATION FOR TYPE below
    def validate_segment_duration_for_type(
        duration: Union[SegmentStringDuration, int, float, str],
        type: Union[SegmentType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for a Segment component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.SEGMENT
        )
    
    def validate_enhancement_duration_for_type(
        duration: Union[EnhancementStringDuration, int, float, str],
        type: Union[EnhancementType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for an Enhancement component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.ENHANCEMENT
        )
    
    def validate_shortcode_duration_for_type(
        duration: Union[ShortcodeStringDuration, int, float, str],
        type: Union[ShortcodeType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for a Shortcode component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_duration_for_type(
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str],
        component: Component
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for the also provided
        'component'.
        """
        component = Component.to_enum(component)

        if not component.is_duration_accepted_for_type(duration, type):
            type = (
                type
                if PythonValidator.is_string(type) else
                type.value
            )

            raise Exception(f'The "{type}" type does not accept the provided "{duration}" duration.')

    # START below
    @staticmethod
    def validate_segment_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for a Segment component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for an Enhancement component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for a Shortcode component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_start_field(
        start: Union[int, float, str, None],
        component: Component
    ):
        """
        Validate that the provided 'start' is valid
        for the given 'component'.
        """
        component = Component.to_enum(component)

        return component.get_start(start)

class SegmentJsonValidator:
    """
    Class to wrap the validation of a Segment
    that is still a raw json.
    """

    @staticmethod
    def validate(
        segment: dict
    ):
        """
        Validate a raw segment that has been read from
        a json file to check if it fits all the expected
        conditions, raising an Exception if not.
        """
        # 1. Validate that contains all the expected fields
        validate_segment_has_expected_fields(segment)

        # 2. Validate segment fields values are valid
        validate_segment_has_valid_values(segment)

        # 2. Validate that the 'type' is valid
        validate_segment_type_is_valid(segment)

        # 3. Validate that 'text' has no shortcodes
        validate_segment_text_has_no_shortcodes(segment)

        # 4. Validate that 'text_to_narrate' doesn't have
        # invalid shortcodes
        validate_segment_text_to_narrate_has_no_invalid_shortcodes(segment)

        # 5. Validate that 'duration' is a valid string or
        # a positive numeric value
        validate_segment_duration_is_valid_string_or_positive_number(segment)

        # 6. Validate that 'duration' is FILE_DURATION for
        # a valid type
        validate_segment_duration_is_valid_for_type(segment)

        # 7. Validate if the type has the mandatory fields
        validate_segment_has_extra_params_needed(segment)

        # 8. Validate that the segment enhancements are ok
        for enhancement in segment.get(SegmentField.ENHANCEMENTS.value, []):
            EnhancementJsonValidator.validate(enhancement)

        # 9. Validate segment mandatory conditions are met
        validate_segment_mets_mandatory_conditions(segment)

class EnhancementJsonValidator:
    """
    Class to wrap the validation of a Segment
    that is still a raw json.
    """

    @staticmethod
    def validate(
        enhancement: dict
    ):
        """
        Validate a raw enhancement that has been read
        from a json file to check if it fits all the
        expected conditions, raising an Exception if
        not.
        """
        # 1. Validate that contains all the expected fields
        validate_enhancement_has_all_fields(enhancement)

        # 2. Validate that the 'type' is valid
        validate_enhancement_type_is_valid(enhancement)

        # 3. Validate that 'text' has no shortcodes
        validate_enhancement_text_has_no_shortcodes(enhancement)

        # 4. Validate that 'text_to_narrate' doesn't have
        # invalid shortcodes
        validate_enhancement_text_to_narrate_has_no_invalid_shortcodes(enhancement)

        # 5. Validate that 'duration' is a valid string or
        # a positive numeric value
        validate_enhancement_duration_is_valid_string_or_positive_number(enhancement)

        # 6. Validate that 'duration' is FILE_DURATION for
        # a valid type
        validate_enhancement_duration_is_valid_for_type(enhancement)

        # 7. Validate that 'mode' is valid
        validate_enhancement_mode_is_valid_for_type(enhancement)

        # 8. Validate all the mandatory conditions are met
        Configuration.get_configuration_by_type(
            enhancement.get(EnhancementField.TYPE, None)
        ).validate_component_mandatory_conditions(enhancement)


# Validation methods below
def validate_enhancement_has_all_fields(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' contains
    all the expected keys, which are all the ones
    available through the EnhancementField Enum
    class, and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_has_expected_fields(enhancement)
    
def validate_enhancement_type_is_valid(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a valid
    type or raises an Exception if not.
    """
    EnhancementType.to_enum(enhancement.get(EnhancementField.TYPE.value, None))

def validate_enhancement_text_has_no_shortcodes(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has any 
    shortcode in its 'text' field and raises
    an Exception if so.
    """
    try:
        empty_shortcode_parser.parse(enhancement.get(EnhancementField.TEXT.value, ''))
    except Exception:
        raise Exception(f'The "enhancement" has some shortcodes in its "{EnhancementField.TEXT.value}" field and this is not allowed.')
    
def validate_enhancement_text_to_narrate_has_no_invalid_shortcodes(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has any
    invalid shortcode in its 'text_to_narrate'
    and raises an Exception if so.
    """
    try:
        # TODO: This has to be our general shortcode parser
        # TODO: I just faked it by now
        shortcode_parser = None
        shortcode_parser.parse(enhancement.get(EnhancementField.TEXT_TO_NARRATE.value, ''))
    except Exception:
        raise Exception(f'The "enhancement" has some invalid shortcodes in its "{EnhancementField.TEXT_TO_NARRATE.value}" field. Please, check the valid shortcodes.')
    
def validate_enhancement_duration_is_valid_string_or_positive_number(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'duration'
    field that is a valid string or a positive 
    number and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_duration_field(
        enhancement.get(EnhancementField.DURATION.value, None)
    )

def validate_enhancement_duration_is_valid_for_type(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'duration'
    field that is a valid string for its type or a
    positive number and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_duration_for_type(
        enhancement.get(EnhancementField.DURATION.value, None),
        enhancement.get(EnhancementField.TYPE.value, None)
    )
    
def validate_enhancement_mode_is_valid_for_type(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'mode' 
    field that is valid for its type.
    """
    BuilderValidator.validate_enhancement_mode_for_type(
        enhancement.get(EnhancementField.MODE.value, None),
        enhancement.get(EnhancementField.TYPE.value, None)
    )

def validate_segment_has_expected_fields(
    segment: dict
):
    """
    Check if the provided 'segment' contains all
    the expected keys, which are all the ones
    available through the SegmentField Enum class,
    and raises an Exception if not.
    """
    BuilderValidator.validate_segment_has_expected_fields(
        segment
    )

def validate_segment_has_valid_values(
    segment: dict
):
    """
    Check if the provided 'segment', which has been
    previously checked to confirm that it has the
    required fields, has valid values.
    """
    BuilderValidator.validate_segment_has_valid_values(
        segment
    )
    
def validate_segment_type_is_valid(
    segment: dict
):
    """
    Check if the provided 'segment' has a valid
    type or raises an Exception if not.
    """
    SegmentType.to_enum(segment.get(SegmentField.TYPE.value, None))

def validate_segment_text_has_no_shortcodes(
    segment: dict
):
    """
    Check if the provided 'segment' has any 
    shortcode in its 'text' field and raises
    an Exception if so.
    """
    try:
        empty_shortcode_parser.parse(segment.get(SegmentField.TEXT.value, ''))
    except Exception:
        raise Exception(f'The "segment" has some shortcodes in its "{SegmentField.TEXT.value}" field and this is not allowed.')
    
def validate_segment_text_to_narrate_has_no_invalid_shortcodes(
    segment: dict
):
    """
    Check if the provided 'segment' has any
    invalid shortcode in its 'text_to_narrate'
    and raises an Exception if so.
    """
    try:
        shortcode_parser.parse(segment.get(SegmentField.TEXT_TO_NARRATE.value, ''))
    except Exception:
        raise Exception(f'The "segment" has some invalid shortcodes in its "{SegmentField.TEXT_TO_NARRATE.value}" field. Please, check the valid shortcodes.')
    
def validate_segment_duration_is_valid_string_or_positive_number(
    segment: dict
):
    """
    Check if the provided 'segment' has a 'duration'
    field that is a valid string or a positive 
    number and raises an Exception if not.
    """
    BuilderValidator.validate_segment_duration_field(
        segment.get(SegmentField.DURATION.value, None)
    )

def validate_segment_duration_is_valid_for_type(
    segment: dict
):
    """
    Check if the provided 'segment' has a 'duration'
    field that is a valid string for its component
    type or raises an Exception if not.
    """
    BuilderValidator.validate_segment_duration_for_type(
        segment.get(SegmentField.DURATION.value, None),
        type = segment.get(SegmentField.TYPE.value, None)
    )
    
def validate_segment_has_extra_params_needed(
    segment: dict
):
    """
    Check if the provided 'segment' has the extra
    parameters that are needed according to its
    type and keywords (premades or text premades
    need extra parameters to be able to be built),
    or raises an Exception if not.
    """
    # TODO: Validate, if premade or effect, that 'extra_params' has
    # needed fields
    keywords = segment.get(SegmentField.KEYWORDS.value, None)
    if type == SegmentType.PREMADE.value:
        # TODO: This below was prepared for extra_params, I think
        # I don't have to ignore anything here... but we were
        # avoiding 'duration' because we obtain it from main fields
        if not is_element_valid_for_method(
            method = enum_name_to_class(keywords, Premade).generate,
            element = segment,
            #parameters_to_ignore = ['duration'],
            parameters_strictly_from_element = ['duration']
        ):
            # TODO: I don't tell anything about the parameters needed
            raise Exception('Some parameters are missing...')
    elif type == SegmentType.TEXT.value:
        # TODO: This below was prepared for extra_params, I think
        # I don't have to ignore anything here... but we were
        # avoiding 'text' and 'duration' because we obtain them
        # from main fields
        if not is_element_valid_for_method(
            method = enum_name_to_class(keywords, TextPremade).generate,
            element = segment,
            #parameters_to_ignore = ['output_filename', 'duration', 'text']
            parameters_to_ignore = ['output_filename'],
            parameters_strictly_from_element = ['duration', 'text']
        ):
            # TODO: I don't tell anything about the parameters needed
            raise Exception('Some parameters are missing...')
    # TODO: Validate for another types

def validate_segment_mets_mandatory_conditions(
    segment: dict
):
    """
    Check if the provided 'segment' mets all the
    mandatory conditions, that are those starting
    with 'do_' in the configuration dict and that
    have a True value, or raises an Exception if
    those mandatory conditions are not met.
    """
    Configuration.get_configuration_by_type(
        segment.get(SegmentField.TYPE.value, None)
    )().validate_component_mandatory_conditions(segment)



"""
TODO: I'm building a new validator based on the
new complex structure we want for the 'guion' to
be more descriptive and flexible.

More information here:
- https://www.notion.so/Esquema-guion-1aaf5a32d46280dabba1e33fc8b1e59c?pvs=4
"""
from yta_core.enums.field_v2 import _Field, VoiceNarrationField, MusicField
from yta_core.builder.music.enums import MusicEngine
from yta_audio.voice.enums import VoiceNarrationEngine, VoiceEmotion, VoiceSpeed, VoicePitch, NarrationLanguage # TODO: Names?
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.file.checker import FileValidator
from abc import ABC, abstractmethod


DEFAULT = 'default'
"""
The default value when handling element building
parameters. This value will be used by the system
to determine a valid value that is considered the
default one.
"""

class Field(ABC):
    """
    Abstract class to be used to implement the different
    type of fields we have and their validations.
    """

    def __init__(
        self,
        name: str,
        value: any
    ):
        self.name = name
        self.value = value

    @abstractmethod
    @property
    def is_valid(
        self
    ) -> bool:
        pass

    def validate(
        self
    ) -> None:
        if not self.is_valid:
            raise Exception(f'The parameter "{self.name}" is not valid.')

class VoiceNarrationFilenameField(Field):
    """
    The 'filename' field within the
    'voice_narration' dict field. It can be
    None, or a non-empty string that points
    to a real and valid audio file.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = VoiceNarrationField.FILENAME.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            FileValidator.file_is_audio_file(self.value)
        )

class VoiceNarrationTextField(Field):
    """
    The 'text' field within the 'voice_narration'
    dict field. It can be None or a non-empty
    string.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = VoiceNarrationField.TEXT.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            ParameterValidator.validate_string(self.name, self.value, do_accept_empty = False)
        )
    
class VoiceNarrationEngineField(Field):
    """
    The 'engine' field within the 'voice_narration'
    dict field. It can be None, 'default' or a
    non-empty string that is one of our accepted
    engines.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = VoiceNarrationField.ENGINE.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                VoiceNarrationEngine.is_valid_name(self.value.lower(), do_ignore_case = True)
            )
        )

class VoiceNarrationLanguageField(Field):
    """
    The 'language' field within the 'voice_narration'
    dict field. It can be None, 'default' or a
    non-empty string that is one of our accepted
    languages (for the given engine).
    """
    def __init__(
        self,
        value: any,
        engine: VoiceNarrationEngine
    ):
        self.name = VoiceNarrationField.ENGINE.value
        self.value = value
        self.engine: VoiceNarrationEngine = VoiceNarrationEngine.to_enum(engine)

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                NarrationLanguage.is_valid_name(self.value.lower(), do_ignore_case = True) and
                self.engine.is_language_valid(self.value)
            )
        )
    
class VoiceNarrationNarratorNameField(Field):
    """
    The 'narrator_name' field within the
    'voice_narration' dict field. It can be
    None, 'default' or a non-empty string 
    that is one of our accepted narrator 
    names.
    """

    def __init__(
        self,
        value: any,
        language: NarrationLanguage,
        engine: VoiceNarrationEngine
    ):
        self.name = VoiceNarrationField.NARRATOR_NAME.value
        self.value = value
        self.language: NarrationLanguage = NarrationLanguage.to_enum(language)
        self.engine: VoiceNarrationEngine = VoiceNarrationEngine.to_enum(engine)

    @property
    def is_valid(
        self
    ) -> bool:
        # TODO: I need a way to get the valid 'voice_narration'
        # narrator names to be checked here, that must be
        # loaded giving the narrator engine
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                self.engine.is_narrator_name_valid(self.language, self.value)
            )
        )
    
class VoiceNarrationSpeedField(Field):
    """
    The 'speed' field within the
    'voice_narration' dict field. It can be
    None, 'default' or a non-empty string 
    that is one of our accepted speed values.
    """

    def __init__(
        self,
        value: any,
        engine: VoiceNarrationEngine
    ):
        self.name = VoiceNarrationField.SPEED.value
        self.value = value
        self.engine: VoiceNarrationEngine = VoiceNarrationEngine.to_enum(engine)

    @property
    def is_valid(
        self
    ) -> bool:
        """
        Check if this speed field and value is valid
        for the given engine. This accepts 'None' as
        a valid value.
        
        TODO: Should I not accept 'None' here (?)
        """
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                # TODO: We should accept numeric values (?)
                VoiceSpeed.is_valid_name(self.value.lower(), do_ignore_case = True) and
                self.engine.is_speed_valid(self.value)
            )
        )
    
class VoiceNarrationEmotionField(Field):
    """
    The 'emotion' field within the
    'voice_narration' dict field. It can be
    None, 'default' or a non-empty string 
    that is one of our accepted emotion 
    values.
    """

    def __init__(
        self,
        value: any,
        engine: VoiceNarrationEngine
    ):
        self.name = VoiceNarrationField.EMOTION.value
        self.value = value
        self.engine: VoiceNarrationEngine = VoiceNarrationEngine.to_enum(engine)

    @property
    def is_valid(
        self
    ) -> bool:
        # TODO: I need a way to get the valid 'voice_narration'
        # emotion values to be checked here, that must be
        # loaded giving the narrator engine
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                VoiceEmotion.is_valid_name(self.value.lower(), do_ignore_case = True) and
                self.engine.is_emotion_valid(self.value)
            )
        )

class VoiceNarrationPitchField(Field):
    """
    The 'pitch' field within the
    'voice_narration' dict field. It can be
    None, 'default' or a non-empty string 
    that is one of our accepted pitch 
    values.
    """

    def __init__(
        self,
        value: any,
        engine: VoiceNarrationEngine
    ):
        self.name = VoiceNarrationField.PITCH.value
        self.value = value
        self.engine: VoiceNarrationEngine = VoiceNarrationEngine.to_enum(engine)

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                VoicePitch.is_valid_name(self.value.lower(), do_ignore_case = True) and
                self.engine.is_pitch_valid(self.value)
            )
        )
    
class MusicFilenameField(Field):
    """
    The 'filename' field within the 'music'
    dict field. It can be None, or a non-empty
    string that points to a real and valid
    audio file.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = MusicField.FILENAME.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            FileValidator.file_is_audio_file(self.value)
        )
    
class MusicUrlField(Field):
    """
    The 'url' field within the 'music' dict
    field. It can be None, or a non-empty
    string that points to a real and valid
    url.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = MusicField.URL.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            PythonValidator.is_url(self.value)
        )

class MusicEngineField(Field):
    """
    The 'engine' field within the 'music' dict
    field. It can be None, 'default' or a non-empty
    string that is one of our accepted engines.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = MusicField.ENGINE.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        # TODO: How to compare? to_enum (?)
        ACCEPTED_MUSIC_ENGINES = [
            engine.lower()
            for engine in MusicEngine.get_all()
        ]

        return (
            self.value is None or
            (
                PythonValidator.is_string(self.value) and
                self.value.lower() in ACCEPTED_MUSIC_ENGINES
            )
        )
    
class MusicKeywordsField(Field):
    """
    The 'keywords' field within the 'music' dict
    field. It can be None or a non-empty string.
    """

    def __init__(
        self,
        value: any
    ):
        self.name = MusicField.KEYWORDS.value
        self.value = value

    @property
    def is_valid(
        self
    ) -> bool:
        return (
            self.value is None or
            ParameterValidator.validate_string(self.name, self.value, do_accept_empty = False)
        )
    


class ElementValidator:
    """
    Class to wrap the validation methods for
    any kind of element we are trying to use
    in our app.
    """

    @staticmethod
    def validate_mandatory_fields(
        element: dict
    ) -> None:
        """
        Validate that the main structure is valid and
        all the mandatory fields are set (even if their
        value is None they must be set) in the provided
        'element'.
        """
        MANDATORY_FIELDS = [
            _Field.TYPE.value,
            _Field.VOICE_NARRATION.value,
            _Field.MUSIC.value,
            _Field.FILENAME.value,
            _Field.URL.value,
            _Field.KEYWORDS.value,
            _Field.TEXT.value,
            _Field.DURATION.value
        ]

        # TODO: Use Enum.get_all_values()
        ParameterValidator.validate_dict_has_keys('element', element, MANDATORY_FIELDS)

    @staticmethod
    def validate_voice_narration_fields(
        element: dict
    ):
        """
        Validate that the 'voice_narration' fields are
        set and valid for loading a voice narration from
        a file or for generating a new one.

        This method will raise an Exception if the 
        'voice_narration' field is provided but is not
        valid, but not if the 'voice_narration' is None.
        """
        voice_narration = element.get(_Field.VOICE_NARRATION.value, None)

        if voice_narration is not None:
            # Validate all fields are, at least, set
            ParameterValidator.validate_dict_has_keys('voice_narration', voice_narration, VoiceNarrationField.get_all_values())

            filename = voice_narration[VoiceNarrationField.FILENAME.value]
            text = voice_narration[VoiceNarrationField.TEXT.value]
            engine = voice_narration[VoiceNarrationField.ENGINE.value]
            language = voice_narration[VoiceNarrationField.LANGUAGE.value]
            narrator_name = voice_narration[VoiceNarrationField.NARRATOR_NAME.value]
            speed = voice_narration[VoiceNarrationField.SPEED.value]
            emotion = voice_narration[VoiceNarrationField.EMOTION.value]
            pitch = voice_narration[VoiceNarrationField.PITCH.value]

            # Validate the combination of fields values are valid
            if (
                filename is not None and
                not VoiceNarrationFilenameField(filename).is_valid
            ):
                raise Exception('The provided "voice_narration" "filename" field is not a valid audio file.')

            if (
                filename is None and
                (
                    not VoiceNarrationTextField(text).is_valid or
                    not VoiceNarrationEngineField(engine).is_valid or
                    not VoiceNarrationLanguageField(language, engine).is_valid or
                    not VoiceNarrationNarratorNameField(narrator_name, engine).is_valid or
                    not VoiceNarrationSpeedField(speed, engine).is_valid or
                    not VoiceNarrationEmotionField(emotion, engine).is_valid or
                    not VoiceNarrationPitchField(pitch, engine).is_valid
                )
            ):
                raise Exception('At least one of the "voice_narration" parameters needed is not valid.')
            
    @staticmethod
    def validate_music_fields(
        element: dict
    ):
        """
        Validate that the 'music' fields are set and
        valid for loading music from a file or for
        obtaining or creating the expected music.
        """
        music = element.get(_Field.MUSIC.value, None)

        if music is not None:
            # Validate all fields are, at least, set
            ParameterValidator.validate_dict_has_keys('music', music, MusicField.get_all_values())

            filename = music[MusicField.FILENAME.value]
            url = music[MusicField.URL.value]
            engine = music[MusicField.ENGINE.value]
            keywords = music[MusicField.KEYWORDS.value]

            # Validate the combination of fields values are valid
            if (
                filename is not None and
                not MusicFilenameField(filename).is_valid
            ):
                raise Exception('The provided "music" "filename" field is not a valid audio file.')

            if (
                filename is None and
                (
                    not MusicFilenameField(filename).is_valid or
                    not MusicUrlField(url).is_valid or
                    not MusicEngineField(engine).is_valid or
                    not MusicKeywordsField(keywords).is_valid
                )
            ):
                raise Exception('At least one of the "music" parameters needed is not valid.')
