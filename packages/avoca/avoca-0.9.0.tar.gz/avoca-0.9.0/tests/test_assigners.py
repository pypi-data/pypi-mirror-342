"""Test for the zscore function."""

import pandas as pd
import pytest

from avoca.qa_class.abstract import AbstractQA_Assigner
from avoca.qa_class.zscore import ExtremeValues, XY_Correlations
from avoca.testing.df import (
    df_around_zero,
    df_full_nan,
    df_nan_training,
    df_one_extreme,
    df_regular,
    df_with_inf,
    empty_index,
)


@pytest.fixture(
    params=[
        (ExtremeValues, {}),
        (XY_Correlations, {}),
        (ExtremeValues, {"use_log_normal": True}),
    ]
)
def assigner(
    request: tuple[pytest.FixtureRequest, dict[str, any]],
) -> AbstractQA_Assigner:
    """Fixture to create assigners for testing."""
    assigner_type, kwargs = request.param
    return assigner_type(variable="test_var", compounds=["compA", "compB"], **kwargs)


def test_simple(assigner: AbstractQA_Assigner):
    assigner.fit(df_regular)
    flagged = assigner.assign(df_one_extreme)

    index_2 = pd.Index([2], dtype="int64")

    comparison_output = {
        ExtremeValues: empty_index,
        # Also b is outside of the correlation cloud
        XY_Correlations: index_2,
    }

    pd.testing.assert_index_equal(flagged["compA"], index_2)
    pd.testing.assert_index_equal(flagged["compB"], comparison_output[type(assigner)])


def test_nan_values_given_fit(assigner: AbstractQA_Assigner):
    assigner.fit(df_nan_training)
    flagged = assigner.assign(df_regular)

    # Nothing should be flagged
    pd.testing.assert_index_equal(flagged["compA"], empty_index)
    pd.testing.assert_index_equal(flagged["compB"], empty_index)


def test_only_nan_values_given_fit(assigner: AbstractQA_Assigner):
    assigner.fit(df_full_nan)
    flagged = assigner.assign(df_regular)

    # Nothing should be flagged
    pd.testing.assert_index_equal(flagged["compA"], empty_index)
    pd.testing.assert_index_equal(flagged["compB"], empty_index)


def test_fitting_nans(assigner: AbstractQA_Assigner):
    assigner.fit(df_regular)

    flagged = assigner.assign(df_nan_training)
    flagged_allnans = assigner.assign(df_full_nan)

    # Nothing should be flagged
    pd.testing.assert_index_equal(flagged["compA"], empty_index)
    pd.testing.assert_index_equal(flagged["compB"], empty_index)
    pd.testing.assert_index_equal(flagged_allnans["compA"], empty_index)
    pd.testing.assert_index_equal(flagged_allnans["compB"], empty_index)


def test_zero_values(assigner: AbstractQA_Assigner):
    """Test that zero values are not flagged."""

    assigner.fit(df_around_zero)
    flagged = assigner.assign(df_around_zero)

    # Nothing should be flagged
    pd.testing.assert_index_equal(flagged["compA"], empty_index)
    pd.testing.assert_index_equal(flagged["compB"], empty_index)


def test_inf_values(assigner: AbstractQA_Assigner):
    """Test that inf values are flagged."""

    assigner.fit(df_with_inf)
    flagged = assigner.assign(df_with_inf)

    # Nothing should be flagged
    pd.testing.assert_index_equal(flagged["compA"], empty_index)
    pd.testing.assert_index_equal(flagged["compB"], empty_index)