# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import requests


gemini_key              = environ.get('GOOGLE_API_KEY','') # GEMINI_KEY', '')
gemini_api_base         = environ.get('GEMINI_API_BASE','https://generativelanguage.googleapis.com/v1beta')
gemini_content_model    = environ.get('GEMINI_DEFAULT_CONTENT_MODEL', 'gemini-2.5-pro-exp-03-25')
gemini_embedding_model  = environ.get('GEMINI_DEFAULT_EMBEDDING_MODEL', 'text-embedding-004')

garbage = [
    {'category':'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_CIVIC_INTEGRITY', 'threshold': 'BLOCK_NONE'}
]


def continuation(text=None, contents=None, instruction=None, recorder=None, **kwargs):
    """A completions endpoint call.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 mandatory
            max_tokens      = number of tokens
            stop            = ['stop']  array of up to 4 sequences
    """
    instruction         = kwargs.get('system_instruction', instruction)
    system_instruction  = {'parts': [{'text': instruction}]} if instruction else None
    contents            = kwargs.get('contents', contents)

    # Create a structure that the idiots want.
    if text and not contents:
        contents = [{'parts': [{'text': text}], 'role': 'user'}]
    else:
        contents.append({'parts': [{'text': text}], 'role': 'user'})

    json_data = {
        'systemInstruction': system_instruction,
        'contents': contents,
        'safetySettings':  garbage,
        'generationConfig':{
             'stopSequences':   kwargs.get('stop_sequences', ['STOP','Title']),
             'responseMimeType': kwargs.get('mime_type','text/plain'),
            # 'responseSchema': {},
             'responseModalities': kwargs.get('modalities',['TEXT']),
             'temperature':     kwargs.get('temperature', 0.5),
             'maxOutputTokens': kwargs.get('max_tokens', 10000),
             'candidateCount':  kwargs.get('n', 1),  # not mandatory 1 now
             'topP':            kwargs.get('top_p', 0.9),
             'topK':            kwargs.get('top_k', 10),
            'enableEnhancedCivicAnswers': False,
            'thinkingConfig': {
                'includeThoughts': True,
                'thinkingBudget': 24576
                }
            #'cachedContent': '',
        },
    }
    try:
        response = requests.post(
            url=f'{gemini_api_base}/models/{kwargs.get("model", gemini_content_model)}:generateContent',
            params=f'key={gemini_key}',
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            answer = response.json()
            if answer.get('filters', None):
                raise Exception('Results filtered')
            else:
                if recorder:
                    log_message = {'query': json_data, 'response': answer}
                    recorder.log_event(log_message)
        else:
            print(f'Request status code: {response.status_code}')
            return None
        if recorder:
            rec = {'messages': json_data['contents'], 'response': answer['candidates']}
            recorder.record(rec)

    except Exception as e:
        print(f'Unable to generate continuation of the text, {e}')
        return None

    return [candidate['content']['parts'][0]['text'] for candidate in answer['candidates']]


def embed(input_list, **kwargs):
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {'texts': input_list} | kwargs
    try:
        response = requests.post(
            f'{gemini_api_base}/models/{kwargs.get("model", gemini_embedding_model)}:batchEmbedText',
            params=f'key={gemini_key}',
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            # embeddings_list = response.json()['embeddings']
            for count, candidate in enumerate(response.json()['embeddings']):
                item = {'index': count, 'embedding': candidate['value']}
                embeddings_list.append(item)
        else:
            print(f'Request status code: {response.status_code}')
        return embeddings_list
    except Exception as e:
        print('Unable to generate Embeddings response')
        print(f'Exception: {e}')
        return embeddings_list


if __name__ == '__main__':
    '''
    ['gemini-2.5-flash-preview-04-17', 'gemini-2.5-pro-exp-03-25', 'gemini-1.5-flash-latest',
    'gemini-2.0-flash-lite','gemini-2.0-flash','gemini-2.0-pro-exp-02-05',
    'gemini-2.0-flash-thinking-exp-01-21']
    '''
    kwa = {'model': 'gemini-2.5-flash-preview-04-17', 'n':2}
    instruction = 'You are an eloquent assistant'
    text = 'In one sentence, who was Gerhard Gentzen?'
    result = continuation(text, instruction=instruction, **kwa)
    print(result)
