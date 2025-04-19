#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Helper functions """

import logging
import os
from .constants import NAME

log = logging.getLogger(NAME)

def gather_environ(keys: dict[dict]) -> dict[dict]:
    """
    Return a dict of environment variables correlating to the keys dict.
    The variables have to be set in ALL_UPPER_CASE.

    Every environment variable found will be echoed on log.info(). Keys with
    `redact` set to `True` will have their value redacted in the log.

    `boolean` keys will use :py:func:`strtobool` to convert a string to boolean.

    The env separator for the type `list` is `<space>` and the key/value separator
    for the type `filter` (which is stored as a dictionary) is the first `=` sign.
    So a `filter` with the value `a=b=c=d` will be stored as `{'a': 'b=c=d'}`.

    Deprecated keys will issue a `log.warning` and will be stored, if `replaced_by`
    is set, on the key documented as `replaced_by`. Make sure to use the same `<type>`
    for both new and deprecated keys, as this is not checked. Setting both keys will
    issue another warning and will drop the deprecated key.

    Hidden keys will not issue any `log.info` if they are unset and the default
    is used.

    The keys must be in the following format:

        keys = {
            'key_one': {
                'default': ['one', 2],
                'type': "list",
            },
            'key_two':{
                'hidden': True,
                'default': False,
                'type': "boolean",
            },
            'key_three': {
                'default': {},
                'type': "filter",
            },
            'key_four': {
                'default': None,
                'redact': True,
                'type': 'string',
            },
            'key_five': {
                'default': 12,
                'type': 'int',
            },
            'key_six': {
                'default': 'INFO',
                'type': 'enum',
                'values': [
                    'DEBUG',
                    'INFO',
                    'WARNING',
                    'ERROR'
                ],
            },
            'key_seven': {
                'default': '12',
                'deprecated': True,
                'replaced_by': 'key_five',
                'type': 'int',
            }
        }


    :param keys: dict[Any, dict]
        The environ keys to use, each of them correlating to
        `int`, `list`, `string`, `boolean`, `enum` or `filter`
    :return: dict[Any, dict]: A dict of the found environ values
    """
    environs = {}

    # Check the environment variables
    for key, key_attributes in keys.items():
        if os.environ.get(key.upper()):
            environs.update({key: os.environ[key.upper()]})

            if key_attributes['type'] == 'list':
                environs[key] = environs[key].split(' ')

            if key_attributes['type'] == 'filter':
                filters = environs[key].split('=', 1)
                try:
                    environs[key] = {filters[0]: filters[1]}
                except IndexError:
                    log.warning(f"`{environs[key]}` not understood for {key.upper()}. Ignoring.")
                    del environs[key]
                    continue

            if key_attributes['type'] == 'int':
                try:
                    environs[key] = int(environs[key])
                except ValueError:
                    log.warning(f"`{environs[key]}` not understood for {key.upper()}. Ignoring.")
                    del environs[key]
                    continue

            if key_attributes['type'] == 'boolean':
                try:
                    environs[key] = bool(strtobool(environs[key]))
                except ValueError:
                    log.warning(f"`{environs[key]}` not understood for {key.upper()}. Ignoring.")
                    del environs[key]
                    continue

            if key_attributes['type'] == 'enum':
                if not environs[key] in key_attributes['values']:
                    log.warning(f"`{environs[key]}` not understood for {key.upper()}. Ignoring.")
                    del environs[key]
                    continue

            log.info(
                redact(
                    message=f'{key.upper()} is interpreted as `{environs[key]}`.',
                    param=environs[key],
                    replace=key_attributes.get('redact', False)
                )
            )

    environs = _handle_deprecations(environs=environs, keys=keys)
    environs = _fill_missing_environs(environs=environs, keys=keys)
    return environs

def _fill_missing_environs(environs: dict, keys: dict) -> dict:
    """
    Fills out the missing environment variables with the values stored in the keys

    :param environs: The already gathered environment variables
    :param keys: The environ keys to use
    :return: A dict of found environ values. For the unset environment variables,
             it returns the default set in the `keys`
    """
    for key, key_attributes in keys.items():
        if not key in environs and not key_attributes.get('deprecated', False) :
            display = key_attributes['default']

            if key_attributes['type'] == 'list':
                display = ' '.join(display)

            if key_attributes['type'] == 'filter':
                display = '='.join(display)

            if not key_attributes.get('hidden', False):
                log.info(f'{key.upper()} is using default value: `{display}`')
            environs[key] = key_attributes['default']
    return environs

def _handle_deprecations(environs: dict, keys: dict) -> dict:
    """
    Handles deprecated environment variables

    :param environs: The already gathered environment variables
    :param keys: The environ keys to use
    :return: A dict environ values, after deprecation processing
    """
    for key, key_attributes in keys.items():
        if key in environs and key_attributes.get('deprecated', False) :
            message = f"{key.upper()} is deprecated and will be removed in a next version."
            if key_attributes.get('replaced_by'):
                message += f" Use {key_attributes['replaced_by'].upper()} instead."
                log.warning(message)
                if key_attributes['replaced_by'] in environs:
                    log.warning(
                        f"{key.upper()} and {key_attributes['replaced_by'].upper()} are both set."
                        f" Dropping {key.upper()}."
                    )
                    del environs[key]
                else:
                    environs[key_attributes['replaced_by']] = environs[key]
                    del environs[key]
            else:
                log.warning(message)

    return environs

def short_msg(msg: str, chars=150) -> str:
    """
    Truncates the message to `chars` characters and adds two dots at the end.

    :param msg: The string to truncate
    :param chars: The max number of characters before adding `..`
    :return: The truncated `msg`. It will return back the `msg` if the length is < `chars`
    """
    return (str(msg)[:chars] + '..') if len(str(msg)) > chars else str(msg)

def strtobool(value: str) -> bool:
    """
    Converts a string to a boolean

    :param value: The string to check if it represents true or false
    :return: The corresponding boolean value
    """
    str_to_bool_map = {
        'y': True,
        'yes': True,
        't': True,
        'true': True,
        'on': True,
        '1': True,
        'n': False,
        'no': False,
        'f': False,
        'false': False,
        'off': False,
        '0': False
    }

    try:
        return str_to_bool_map[str(value).lower()]
    except KeyError as exc:
        raise ValueError(f'"{value}" is not a valid bool value') from exc

def redact(message: str, param: str, replace=False, replace_value='xxxREDACTEDxxx') -> str:
    """
    Replaces in `message` the `param` string with `replace_value`

    :param message: The string to parse
    :param param: The substring to be replaced
    :param replace: A boolean informing if the `param` should be replaced or not
    :param replace_value: The value to replace `param` with
    :return: str: The modified string
    """
    if replace:
        return message.replace(param, replace_value)
    return message

def key_to_title(key: str) -> str:
    """ converts a string key in form 'a_is_b' to a title in form 'A Is B ' """
    parsed = ""
    keys = key.split('_')
    for k in keys:
        parsed += f'{k.capitalize()} '
    return parsed[:-1]
