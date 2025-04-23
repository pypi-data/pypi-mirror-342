# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from ..adapters.gem_rest import prepared_gem_messages, formatted_gem_output


gemini_key          = environ.get("GOOGLE_API_KEY","")
default_model       = environ.get("GEMINI_DEFAULT_MODEL", "gemini-2.5-pro-exp-03-25")
embedding_model     = environ.get("GEMINI_DEFAULT_EMBEDDING_MODEL", "text-embedding-004")

garbage = [
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"},
    {"category":"HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"}
]

default_config = {
    'candidate_count': 1,
    'stop_sequences': ['STOP'],
    'max_output_tokens': 500,
    'temperature': 0.5,
    'top_p': 0.9,
    'top_k': 10,
    'response_mime_type': "text/plain",
    'safety_settings':   garbage,
    'response_modalities': ['TEXT']
}


def genai_get_client(**kwargs):
    """
    in the kwargs you can specify:

        api_key (str): API key to use for authentication.
        debug_config (DebugConfig): Config settings that control network behavior
            of the client. This is typically used when running test code.
        http_options (Union[HttpOptions, HttpOptionsDict]): Http options to use
            for the client.

    all the model parameters that were here in the previous version are now
    sent to the API in queries.
    """
    client = None
    try:
        from google import genai
        client = genai.Client(**kwargs)
    except ImportError:
        print("google-genai package is not installed")
    return client


def genai_complete(client, prompt="", recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are all optional
    """

    kwarg_config = kwargs.get('generation_config', default_config)

    gen_conf = {
        'candidate_count':      kwarg_config.get('n', default_config.get('candidate_count')),
        'stop_sequences':       kwarg_config.get('stop_sequences',    default_config.get('stop_sequences')),
        'max_output_tokens':    kwarg_config.get('max_tokens', default_config.get('max_output_tokens')),
        'temperature':          kwarg_config.get('temperature', default_config.get('temperature')),
        'top_p':                kwarg_config.get('top_p', default_config.get('top_p')),
        'top_k':                kwarg_config.get('top_k', default_config.get('top_k')),
        'response_mime_type':   kwarg_config.get('mime_type', default_config.get('response_mime_type')),
        'response_schema':      kwarg_config.get('schema', default_config.get('response_schema'))
    }

    generation_kwargs = {
        'model':                kwargs.get('model', default_model),
        'contents':             kwargs.get('contents', [prompt]),
        'config':               kwargs.get('generation_config', None)
    }

    try:
        completion = client.models.generate_content(**generation_kwargs)
        completion_dump = completion.text
        if recorder:
            log_message = {"query": generation_kwargs, "response": {"completion": completion_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    if recorder:
        rec = {"prompt": generation_kwargs["contents"], "completion": completion_dump}
        recorder.record(rec)

    return completion_dump


def genai_stream(client, prompt="", recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are
    """
    generation_kwargs = {
        'model': kwargs.get('model', default_model),
        'contents': kwargs.get('contents', [prompt]),
        'config': kwargs.get('generation_config', None)
    }
    result = ''
    for chunk in client.models.generate_content_stream(**generation_kwargs):
        result += chunk.text

    return result


def genai_get_chat_session(client, **kwargs):
    """ all parameters in kwargs.
    """
    chat_session = None
    chat_kwargs = {
        'model': kwargs.get('model', default_model),
        'config': kwargs.get('generation_config', default_config),
        'history': kwargs.get('history', None)
    }
    try:
        chat_session = client.chats.continuation(**chat_kwargs)
    except Exception as e:
        print("could not get chat session.")
    return chat_session


def genai_message(chat_session, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    kwarg_config = kwargs.get('generation_config', default_config)

    try:
        response = chat_session.send_message(**kwargs)
        msg_dump = response.text
        if recorder:
            log_message = {"query": kwargs, "response": {"message": msg_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None

    if recorder:
        rec = {'messages': kwargs['content'], 'response': msg_dump}
        recorder.record(rec)

    return msg_dump


if __name__ == "__main__":
    print("you launched main.")
