'''Provides a few methods to write fgbio-metric-like files from classes
decorated by the :py:mod:`~attr` module.'''

import logging
from pathlib import Path
from typing import Any, List, Tuple

import attr


def _to_tuples(obj: Any, print_all: bool = True) -> List[Tuple[str, str]]:
    '''Returns a list of name/value tuples for each attribute in the object.

    The object must be decorated by the :py:mod:`~attr` module.  If the object contains an
    attribute whose class is also decorated by the :py:mod:`~attr` module, that attribuet will be
    replaced by the attributes in the latter class.  The name returned for each sub-attribute will
    be pre-pended with the original fields name seperated by an underscore.

    Args:
        obj: an object who is decorated by the :py:mod:`~attr` module.
    '''
    cls = obj.__class__
    attribute_names = [a.name for a in attr.fields(cls)
                       if print_all or 'print' not in a.metadata or a.metadata['print']]
    raw_values = [(name, getattr(obj, name)) for name in attribute_names]
    values: List[Tuple[str, str]] = []
    for name, raw_value in raw_values:
        if isinstance(raw_value, (str, int, float)):
            values.append((name, str(raw_value)))
        else:
            values.extend([(f'{name}_{sub_name}', sub_value)
                           for sub_name, sub_value in _to_tuples(raw_value, print_all=False)])

    return values


def write_metric(output: Path, obj: Any) -> None:
    '''Writes the given metric to a file.

    Args:
        output: path to the output metric file.
        obj: an object who is decorated by the :py:mod:`~attr` module.
    '''
    write_metrics(output, [obj])


def write_metrics(output: Path, objs: List[Any]) -> None:
    '''Writes the given metrics to a file.

    Args:
        output: path to the output metric file.
        objs: one or more objects who are decorated by the :py:mod:`~attr` module.
    '''
    if len(objs) == 0:
        logging.warning(f'No metrics given, so the output will be empty: {output}')
    with open(output, 'w') as fh:
        # TODO: check that all objects have the same type/names?
        expected_names = None
        for i, obj in enumerate(objs):
            metric = _to_tuples(obj)
            names = [name for name, _ in metric]
            if i == 0:
                fh.write('\t'.join([name for name, value in metric]) + '\n')
                expected_names = names
            else:
                assert len(expected_names) == len(names)
                for left, right in zip(expected_names, names):
                    assert left == right
            fh.write('\t'.join([value for name, value in metric]) + '\n')
