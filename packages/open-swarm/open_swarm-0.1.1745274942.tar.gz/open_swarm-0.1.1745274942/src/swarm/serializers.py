from rest_framework import serializers
from swarm.models import ChatMessage
import logging

logger = logging.getLogger(__name__)
print_logger = logging.getLogger('print_debug')

class MessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["system", "user", "assistant", "tool"])
    # Content is CharField, allows null/blank by default
    content = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)

    # Removed validate_content

    def validate(self, data):
        """Validate message structure based on role."""
        print_logger.debug(f"MessageSerializer.validate received data: {data}")
        role = data.get('role')
        content = data.get('content', None)
        name = data.get('name')

        # Role validation
        if 'role' not in data:
             raise serializers.ValidationError({"role": ["This field is required."]})

        # Content requiredness validation (based on role)
        content_required = role in ['system', 'user', 'assistant', 'tool']
        content_present = 'content' in data

        if content_required:
            if not content_present:
                 raise serializers.ValidationError({"content": ["This field is required."]})
            # Null/Blank checks are handled by field definition (allow_null/allow_blank)
            # Type check will happen in ChatCompletionRequestSerializer.validate_messages

        # Name validation for tool role
        if role == 'tool' and not name:
             raise serializers.ValidationError({"name": ["This field is required for role 'tool'."]})

        print_logger.debug(f"MessageSerializer.validate PASSED for data: {data}")
        return data

class ChatCompletionRequestSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=255)
    messages = MessageSerializer(many=True, min_length=1)
    stream = serializers.BooleanField(default=False)
    params = serializers.JSONField(required=False, allow_null=True)

    def validate(self, data):
        """Perform object-level validation."""
        model_value = self.initial_data.get('model')
        logger.debug(f"Top-level validate checking model type. Got: {type(model_value)}, value: {model_value}")
        if model_value is not None and not isinstance(model_value, str):
             raise serializers.ValidationError({"model": ["Field 'model' must be a string."]})
        # Messages validation (including content type) happens in validate_messages
        return data

    def validate_messages(self, value):
        """
        Validate the messages list itself and perform raw type checks.
        'value' here is the list *after* MessageSerializer has run on each item.
        We need to inspect `self.initial_data` for the raw types.
        """
        if not value:
            raise serializers.ValidationError("Messages list cannot be empty.")

        # Access raw message data from initial_data for type checking
        raw_messages = self.initial_data.get('messages', [])
        if not isinstance(raw_messages, list):
             # This case is handled by ListField implicitly, but good to be explicit
             raise serializers.ValidationError("Expected a list of message items.")

        errors = []
        for i, raw_msg in enumerate(raw_messages):
             msg_errors = {}
             if not isinstance(raw_msg, dict):
                 # If the item itself isn't a dict, add error and skip further checks for it
                 errors.append({f"item_{i}": "Each message must be a dictionary."})
                 continue

             # *** Check raw content type here ***
             content = raw_msg.get('content', None)
             if 'content' in raw_msg and content is not None and not isinstance(content, str):
                  msg_errors['content'] = ["Content must be a string or null."] # Match test assertion

             # Add other raw checks if needed (e.g., role type)

             if msg_errors:
                  errors.append(msg_errors) # Append errors for this specific message index

        if errors:
             # Raise a single validation error containing all message-specific errors
             raise serializers.ValidationError(errors)

        # Return the processed 'value' which passed MessageSerializer validation
        return value

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

