#!/usr/bin/env python
import pytest

from martens import martens


@pytest.mark.parametrize("file_path", [
    './tests/test_data/file_example_XLSX_10.xlsx',
    './tests/test_data/file_example_XLS_10.xls',
])
def test_total_ages_women(file_path):
    total_ages_women = martens.SourceFile(file_path=file_path) \
        .dataset.headings_lower.filter(lambda gender: gender == 'Female') \
        .long_apply(lambda age: sum(age))
    assert total_ages_women == 263


@pytest.mark.parametrize("file_path", ['./tests/test_data/file_example_XLS_10.xls'])
def test_chart_generator(file_path):
    data = martens.SourceFile(file_path=file_path) \
        .dataset.headings_lower \
        .group_by(['gender', 'country'], count='count') \
        .mutate(lambda country: {'Great Britain': 1, 'France': 2, 'United States': 3}[country],'country_order') \
        .mutate(lambda gender: {'Male': 1, 'Female': 2}[gender], 'gender_order') \
        .pivot_chart_constructor(x_name='country', colour='gender', y_name='count', colour_sort_keys=['gender_order'], x_sort_keys=['country_order'])
    print(data)
