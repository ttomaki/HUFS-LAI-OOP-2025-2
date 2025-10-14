#!/usr/bin/env python3
"""
Assignment 2 Auto-Grader
========================

자동 채점 시스템: 모든 문제들을 테스트하고 점수를 매깁니다.

Usage:
    python grader.py

Features:
- 각 문제별 세부 테스트
- 예외 상황 처리 테스트
- 상세한 피드백과 점수
- 전체 점수 요약
"""

import sys
import traceback
import importlib.util
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple
import random


class TestResult:
    """테스트 결과를 저장하는 클래스"""

    def __init__(
        self,
        name: str,
        passed: bool,
        points: int,
        max_points: int,
        message: str = "",
        details: dict = None,
    ):
        self.name = name
        self.passed = passed
        self.points = points
        self.max_points = max_points
        self.message = message
        self.details = details or {}

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        result = f"{status} {self.name} ({self.points}/{self.max_points} pts)"
        if self.message:
            result += f" {self.message}"
        return result


class Grader:
    """자동 채점 시스템"""

    def __init__(self):
        self.results: List[TestResult] = []
        self.current_problem = ""

    def test(
        self, name: str, test_func: Callable, points: int = 1, verbose: bool = True
    ) -> TestResult:
        """단일 테스트 실행"""
        try:
            test_details = test_func()
            result = TestResult(name, True, points, points, "", test_details)
            if verbose:
                print(f"  ✅ {name}")
                if test_details:
                    self._print_test_details(test_details, success=True)
        except AssertionError as e:
            details = getattr(e, "details", {})
            result = TestResult(
                name, False, 0, points, f"Assertion failed: {e}", details
            )
            if verbose:
                print(f"  ❌ {name}: {e}")
                if details:
                    self._print_test_details(details, success=False)
        except Exception as e:
            result = TestResult(name, False, 0, points, f"Error: {e}")
            if verbose:
                print(f"  ❌ {name}: {e}")

        self.results.append(result)
        return result

    def _print_test_details(self, details: dict, success: bool = True):
        """테스트 세부 정보 출력"""
        if not details:
            return

        indent = "    "
        if "input" in details:
            print(f"{indent}📥 Input: {details['input']}")
        if "expected" in details:
            print(f"{indent}🎯 Expected: {details['expected']}")
        if "actual" in details:
            print(f"{indent}📤 Actual: {details['actual']}")
        if "test_cases" in details:
            print(f"{indent}🔍 Test cases:")
            for i, case in enumerate(details["test_cases"]):
                status = "✅" if case.get("passed", success) else "❌"
                print(f"{indent}  {status} Case {i+1}: {case}")

    def assert_with_details(self, condition: bool, message: str, **details):
        """상세 정보를 포함한 assertion"""
        if not condition:
            error = AssertionError(message)
            error.details = details
            raise error
        return details

    def import_module(self, module_path: str, module_name: str = None):
        """모듈을 동적으로 import"""
        if module_name is None:
            module_name = Path(module_path).stem

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def problem_header(self, problem_num: int, title: str):
        """문제 시작 헤더 출력"""
        self.current_problem = f"Problem {problem_num}"
        print(f"\n{'='*60}")
        print(f"Problem {problem_num}: {title}")
        print("=" * 60)

    def test_problem1(self):
        """Problem 1: Accumulator 클래스 테스트"""
        self.problem_header(1, "Accumulator (stateful counter)")

        try:
            # Import the module
            main_module = self.import_module("problem1/main.py")
            Accumulator = main_module.Accumulator

            # Basic functionality tests
            self.test(
                "Basic initialization", lambda: self._test_p1_init(Accumulator), 2
            )
            self.test(
                "Add method functionality", lambda: self._test_p1_add(Accumulator), 3
            )
            self.test(
                "Total property (read-only)",
                lambda: self._test_p1_total_property(Accumulator),
                3,
            )
            self.test(
                "Reset functionality", lambda: self._test_p1_reset(Accumulator), 2
            )
            self.test(
                "Multiple instances independence",
                lambda: self._test_p1_independence(Accumulator),
                3,
            )
            self.test("Edge cases", lambda: self._test_p1_edge_cases(Accumulator), 2)

        except Exception as e:
            print(f"  ❌ Failed to import Problem 1: {e}")
            self.results.append(TestResult("Problem 1 Import", False, 0, 15, str(e)))

    def _test_p1_init(self, Accumulator):
        test_cases = []

        # Test case 1: Default initialization
        acc1 = Accumulator()
        result1 = acc1.total
        expected1 = 0.0
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            "Default initialization should be 0.0",
            input="Accumulator()",
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": "Accumulator()",
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Custom initialization
        acc2 = Accumulator(10.5)
        result2 = acc2.total
        expected2 = 10.5
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            "Custom initialization should work",
            input="Accumulator(10.5)",
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": "Accumulator(10.5)",
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        return {"test_cases": test_cases}

    def _test_p1_add(self, Accumulator):
        acc = Accumulator()

        # Test case 1: First add
        result1 = acc.add(3.0)
        self.assert_with_details(
            result1 == 3.0,
            "add() should return new total",
            input="acc.add(3.0)",
            expected=3.0,
            actual=result1,
        )

        self.assert_with_details(
            acc.total == 3.0,
            "total should be updated",
            input="acc.total after add(3.0)",
            expected=3.0,
            actual=acc.total,
        )

        # Test case 2: Second add
        result2 = acc.add(4.5)
        self.assert_with_details(
            result2 == 7.5,
            "add() should accumulate correctly",
            input="acc.add(4.5) after add(3.0)",
            expected=7.5,
            actual=result2,
        )

        self.assert_with_details(
            acc.total == 7.5,
            "total should be cumulative",
            input="acc.total after add(3.0) + add(4.5)",
            expected=7.5,
            actual=acc.total,
        )

        return {
            "test_cases": [
                {
                    "input": "add(3.0)",
                    "expected": 3.0,
                    "actual": result1,
                    "passed": result1 == 3.0,
                },
                {
                    "input": "add(4.5)",
                    "expected": 7.5,
                    "actual": result2,
                    "passed": result2 == 7.5,
                },
            ]
        }

    def _test_p1_total_property(self, Accumulator):
        acc = Accumulator(5.0)
        assert acc.total == 5.0, "total property should return current value"

        # Test read-only property
        try:
            acc.total = 100.0
            assert False, "total property should be read-only"
        except (AssertionError, AttributeError):
            pass  # Expected behavior

    def _test_p1_reset(self, Accumulator):
        acc = Accumulator(10.0)
        acc.add(5.0)
        assert acc.total == 15.0, "Setup check"

        acc.reset()
        assert acc.total == 0.0, "reset() should set total to 0.0"

    def _test_p1_independence(self, Accumulator):
        acc1 = Accumulator(10.0)
        acc2 = Accumulator(20.0)

        acc1.add(5.0)
        acc2.add(3.0)

        assert acc1.total == 15.0, "acc1 should be independent"
        assert acc2.total == 23.0, "acc2 should be independent"

        acc1.reset()
        assert acc1.total == 0.0, "acc1 reset should not affect acc2"
        assert acc2.total == 23.0, "acc2 should be unchanged"

    def _test_p1_edge_cases(self, Accumulator):
        acc = Accumulator()

        # Negative numbers
        acc.add(-5.0)
        assert acc.total == -5.0, "Should handle negative numbers"

        # Zero
        acc.add(0.0)
        assert acc.total == -5.0, "Adding zero should not change total"

        # Large numbers
        acc.add(1e6)
        assert acc.total == 1e6 - 5.0, "Should handle large numbers"

    def test_problem2(self):
        """Problem 2: textops 패키지 테스트"""
        self.problem_header(2, "textops (clean & tokenize)")

        try:
            # Test individual modules first
            filters = self.import_module("problem2/textops/clean/filters.py")
            word = self.import_module("problem2/textops/tokenize/word.py")

            self.test(
                "clean_text basic functionality",
                lambda: self._test_p2_clean_basic(filters.clean_text),
                3,
            )
            self.test(
                "clean_text edge cases",
                lambda: self._test_p2_clean_edge(filters.clean_text),
                3,
            )
            self.test(
                "word_tokens basic functionality",
                lambda: self._test_p2_tokens_basic(word.word_tokens),
                2,
            )
            self.test(
                "word_tokens edge cases",
                lambda: self._test_p2_tokens_edge(word.word_tokens),
                2,
            )

            # Test package imports
            sys.path.append("problem2")
            try:
                import textops

                self.test(
                    "Package re-export",
                    lambda: self._test_p2_package_import(textops),
                    3,
                )
                self.test(
                    "__all__ definition",
                    lambda: self._test_p2_all_definition(textops),
                    2,
                )
            finally:
                sys.path.remove("problem2")

        except Exception as e:
            print(f"  ❌ Failed to import Problem 2: {e}")
            self.results.append(TestResult("Problem 2 Import", False, 0, 15, str(e)))

    def _test_p2_clean_basic(self, clean_text):
        test_cases = []

        # Test case 1: Basic cleaning
        input1 = "  Hello,   WORLD!  "
        result1 = clean_text(input1)
        expected1 = "hello world"
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            f"Basic text cleaning failed",
            input=input1,
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": input1,
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Preserve apostrophes and hyphens
        input2 = "ROCK-'N'-ROLL!!"
        result2 = clean_text(input2)
        expected2 = "rock-'n'-roll"
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            f"Should preserve apostrophes and hyphens",
            input=input2,
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": input2,
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        return {"test_cases": test_cases}

    def _test_p2_clean_edge(self, clean_text):
        test_cases = []

        # Test case 1: Only punctuation
        input1 = "..."
        result1 = clean_text(input1)
        expected1 = ""
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            "Only punctuation should result in empty string",
            input=input1,
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": input1,
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Whitespace collapse
        input2 = " A  B\tC\nD "
        result2 = clean_text(input2)
        expected2 = "a b c d"
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            "Should collapse all whitespace",
            input=input2,
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": input2,
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        # Test case 3: Empty string
        input3 = ""
        result3 = clean_text(input3)
        expected3 = ""
        passed3 = result3 == expected3

        self.assert_with_details(
            passed3,
            "Empty string should remain empty",
            input=input3,
            expected=expected3,
            actual=result3,
        )
        test_cases.append(
            {
                "input": input3,
                "expected": expected3,
                "actual": result3,
                "passed": passed3,
            }
        )

        return {"test_cases": test_cases}

    def _test_p2_tokens_basic(self, word_tokens):
        test_cases = []

        # Test case 1: Multiple words
        input1 = "hello world"
        result1 = word_tokens(input1)
        expected1 = ["hello", "world"]
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            "Should split on spaces",
            input=input1,
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": input1,
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Single word
        input2 = "single"
        result2 = word_tokens(input2)
        expected2 = ["single"]
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            "Single word should return list with one item",
            input=input2,
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": input2,
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        return {"test_cases": test_cases}

    def _test_p2_tokens_edge(self, word_tokens):
        test_cases = []

        # Test case 1: Empty string
        input1 = ""
        result1 = word_tokens(input1)
        expected1 = []
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            "Empty string should return empty list",
            input=input1,
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": input1,
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Single space
        input2 = " "
        result2 = word_tokens(input2)
        expected2 = []
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            "Whitespace-only should return empty list",
            input=input2,
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": input2,
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        # Test case 3: Multiple spaces
        input3 = "   "
        result3 = word_tokens(input3)
        expected3 = []
        passed3 = result3 == expected3

        self.assert_with_details(
            passed3,
            "Multiple whitespace should return empty list",
            input=input3,
            expected=expected3,
            actual=result3,
        )
        test_cases.append(
            {
                "input": input3,
                "expected": expected3,
                "actual": result3,
                "passed": passed3,
            }
        )

        return {"test_cases": test_cases}

    def _test_p2_package_import(self, textops):
        # Test that functions are available at package level
        assert hasattr(
            textops, "clean_text"
        ), "clean_text should be available at package level"
        assert hasattr(
            textops, "word_tokens"
        ), "word_tokens should be available at package level"

        # Test functionality through package
        result = textops.clean_text("  TEST  ")
        assert result == "test", "Package-level clean_text should work"

        result = textops.word_tokens("hello world")
        assert result == ["hello", "world"], "Package-level word_tokens should work"

    def _test_p2_all_definition(self, textops):
        assert hasattr(textops, "__all__"), "__all__ should be defined"
        assert "clean_text" in textops.__all__, "clean_text should be in __all__"
        assert "word_tokens" in textops.__all__, "word_tokens should be in __all__"
        assert len(textops.__all__) == 2, "__all__ should contain exactly 2 items"

    def test_problem3(self):
        """Problem 3: tokenstats 모듈 테스트"""
        self.problem_header(3, "tokenstats (module + __main__ demo)")

        try:
            main_module = self.import_module("problem3/main.py")

            self.test(
                "count_tokens functionality",
                lambda: self._test_p3_count_tokens(main_module.count_tokens),
                3,
            )
            self.test(
                "top_k functionality", lambda: self._test_p3_top_k(main_module.top_k), 4
            )
            self.test(
                "top_k edge cases",
                lambda: self._test_p3_top_k_edge(main_module.top_k),
                3,
            )

            if hasattr(main_module, "merge_freqs"):
                self.test(
                    "merge_freqs functionality",
                    lambda: self._test_p3_merge_freqs(main_module.merge_freqs),
                    3,
                )
            else:
                self.results.append(
                    TestResult(
                        "merge_freqs (optional)",
                        True,
                        2,
                        3,
                        "Not implemented (optional)",
                    )
                )

        except Exception as e:
            print(f"  ❌ Failed to import Problem 3: {e}")
            self.results.append(TestResult("Problem 3 Import", False, 0, 13, str(e)))

    def _test_p3_count_tokens(self, count_tokens):
        test_cases = []

        # Test case 1: Mixed tokens
        input1 = ["a", "b", "a"]
        result1 = count_tokens(input1)
        expected1 = {"a": 2, "b": 1}
        passed1 = result1 == expected1

        self.assert_with_details(
            passed1,
            f"Token counting failed",
            input=input1,
            expected=expected1,
            actual=result1,
        )
        test_cases.append(
            {
                "input": input1,
                "expected": expected1,
                "actual": result1,
                "passed": passed1,
            }
        )

        # Test case 2: Empty list
        input2 = []
        result2 = count_tokens(input2)
        expected2 = {}
        passed2 = result2 == expected2

        self.assert_with_details(
            passed2,
            "Empty list should return empty dict",
            input=input2,
            expected=expected2,
            actual=result2,
        )
        test_cases.append(
            {
                "input": input2,
                "expected": expected2,
                "actual": result2,
                "passed": passed2,
            }
        )

        # Test case 3: All same tokens
        input3 = ["same", "same", "same"]
        result3 = count_tokens(input3)
        expected3 = {"same": 3}
        passed3 = result3 == expected3

        self.assert_with_details(
            passed3,
            "All same tokens should work",
            input=input3,
            expected=expected3,
            actual=result3,
        )
        test_cases.append(
            {
                "input": input3,
                "expected": expected3,
                "actual": result3,
                "passed": passed3,
            }
        )

        return {"test_cases": test_cases}

    def _test_p3_top_k(self, top_k):
        freqs = {"a": 2, "b": 2, "c": 1}
        result = top_k(freqs, 2)

        # Should be sorted by frequency desc, then token asc for ties
        assert len(result) == 2, "Should return exactly k items"
        assert result[0][1] >= result[1][1], "Should be sorted by frequency descending"

        # Check tie-breaking (a and b both have frequency 2, a comes first alphabetically)
        high_freq_tokens = [token for token, freq in result if freq == 2]
        if len(high_freq_tokens) > 1:
            assert high_freq_tokens == sorted(
                high_freq_tokens
            ), "Ties should be broken alphabetically"

    def _test_p3_top_k_edge(self, top_k):
        freqs = {"a": 1, "b": 2}

        result = top_k(freqs, 0)
        assert result == [], "k=0 should return empty list"

        result = top_k(freqs, -1)
        assert result == [], "Negative k should return empty list"

        result = top_k(freqs, 10)
        assert len(result) == 2, "k > dict size should return all items"

    def _test_p3_merge_freqs(self, merge_freqs):
        result = merge_freqs([{"a": 1}, {"a": 2, "b": 1}])
        assert result == {"a": 3, "b": 1}, f"Expected {{'a': 3, 'b': 1}}, got {result}"

        result = merge_freqs([])
        assert result == {}, "Empty list should return empty dict"

        result = merge_freqs([{"x": 5}])
        assert result == {"x": 5}, "Single dict should be returned as-is"

    def test_problem4(self):
        """Problem 4: dsops 패키지 테스트"""
        self.problem_header(4, "dsops (dataset utilities)")

        try:
            sys.path.append("problem4")
            try:
                import dsops

                self.test("Package import", lambda: self._test_p4_import(dsops), 2)
                self.test(
                    "train_test_split basic",
                    lambda: self._test_p4_split_basic(dsops.train_test_split),
                    4,
                )
                self.test(
                    "train_test_split reproducibility",
                    lambda: self._test_p4_split_seed(dsops.train_test_split),
                    3,
                )
                self.test(
                    "train_test_split edge cases",
                    lambda: self._test_p4_split_edge(dsops.train_test_split),
                    3,
                )
                self.test(
                    "label_distribution",
                    lambda: self._test_p4_label_dist(dsops.label_distribution),
                    3,
                )
            finally:
                sys.path.remove("problem4")

        except Exception as e:
            print(f"  ❌ Failed to import Problem 4: {e}")
            self.results.append(TestResult("Problem 4 Import", False, 0, 15, str(e)))

    def _test_p4_import(self, dsops):
        assert hasattr(
            dsops, "train_test_split"
        ), "train_test_split should be available"
        assert hasattr(
            dsops, "label_distribution"
        ), "label_distribution should be available"
        assert hasattr(dsops, "__all__"), "__all__ should be defined"

    def _test_p4_split_basic(self, train_test_split):
        test_cases = []

        data = [1, 2, 3, 4, 5]
        train, test = train_test_split(data, 0.4, seed=42)

        # Test case 1: Total length preservation
        total_len = len(train) + len(test)
        expected_len = len(data)
        passed1 = total_len == expected_len

        self.assert_with_details(
            passed1,
            "Total length should be preserved",
            input=f"train_test_split({data}, 0.4, seed=42)",
            expected=f"len(train) + len(test) = {expected_len}",
            actual=f"len(train) + len(test) = {total_len}",
        )
        test_cases.append(
            {
                "input": "length preservation",
                "expected": expected_len,
                "actual": total_len,
                "passed": passed1,
            }
        )

        # Test case 2: Test set size
        test_len = len(test)
        expected_test_len = 2  # 40% of 5 = 2
        passed2 = test_len == expected_test_len

        self.assert_with_details(
            passed2,
            f"Test set should have {expected_test_len} items for ratio 0.4",
            input="len(test) after split",
            expected=expected_test_len,
            actual=test_len,
        )
        test_cases.append(
            {
                "input": "test set size",
                "expected": expected_test_len,
                "actual": test_len,
                "passed": passed2,
            }
        )

        # Test case 3: No data loss
        combined = set(train + test)
        original = set(data)
        passed3 = combined == original

        self.assert_with_details(
            passed3,
            "No data should be lost",
            input="set(train + test) vs set(original)",
            expected=original,
            actual=combined,
        )
        test_cases.append(
            {
                "input": "data preservation",
                "expected": original,
                "actual": combined,
                "passed": passed3,
            }
        )

        return {"test_cases": test_cases}

    def _test_p4_split_seed(self, train_test_split):
        data = list(range(10))

        # Same seed should give same results
        train1, test1 = train_test_split(data, 0.3, seed=123)
        train2, test2 = train_test_split(data, 0.3, seed=123)

        assert train1 == train2, "Same seed should give same train set"
        assert test1 == test2, "Same seed should give same test set"

        # Different seed should give different results (with high probability)
        train3, test3 = train_test_split(data, 0.3, seed=456)
        assert (
            train1 != train3 or test1 != test3
        ), "Different seeds should give different results"

    def _test_p4_split_edge(self, train_test_split):
        # Empty list
        train, test = train_test_split([], 0.5)
        assert train == [] and test == [], "Empty input should return empty lists"

        # test_ratio = 0.0
        train, test = train_test_split([1, 2, 3], 0.0)
        assert test == [], "test_ratio=0.0 should give empty test set"
        assert len(train) == 3, "All items should be in train set"

        # test_ratio = 1.0
        train, test = train_test_split([1, 2, 3], 1.0)
        assert train == [], "test_ratio=1.0 should give empty train set"
        assert len(test) == 3, "All items should be in test set"

        # Invalid ratio
        try:
            train_test_split([1, 2, 3], -0.1)
            assert False, "Negative ratio should raise ValueError"
        except ValueError:
            pass

        try:
            train_test_split([1, 2, 3], 1.1)
            assert False, "Ratio > 1.0 should raise ValueError"
        except ValueError:
            pass

    def _test_p4_label_dist(self, label_distribution):
        result = label_distribution(["cat", "dog", "cat"])
        assert result == {
            "cat": 2,
            "dog": 1,
        }, f"Expected {{'cat': 2, 'dog': 1}}, got {result}"

        result = label_distribution([])
        assert result == {}, "Empty list should return empty dict"

        result = label_distribution(["same", "same", "same"])
        assert result == {"same": 3}, "All same labels should work"

    def test_problem5(self):
        """Problem 5: cachekit 패키지 테스트"""
        self.problem_header(5, "cachekit (simple memory cache)")

        try:
            sys.path.append("problem5")
            try:
                import cachekit

                self.test(
                    "Package structure", lambda: self._test_p5_structure(cachekit), 2
                )
                self.test(
                    "Cache basic operations",
                    lambda: self._test_p5_cache_basic(cachekit.Cache),
                    4,
                )
                self.test(
                    "Cache edge cases",
                    lambda: self._test_p5_cache_edge(cachekit.Cache),
                    3,
                )
                self.test("Version info", lambda: self._test_p5_version(cachekit), 1)
            finally:
                sys.path.remove("problem5")

        except Exception as e:
            print(f"  ❌ Failed to import Problem 5: {e}")
            self.results.append(TestResult("Problem 5 Import", False, 0, 10, str(e)))

    def _test_p5_structure(self, cachekit):
        assert hasattr(cachekit, "Cache"), "Cache class should be available"
        assert hasattr(cachekit, "VERSION"), "VERSION should be available"
        assert hasattr(
            cachekit, "print_version_info"
        ), "print_version_info should be available"
        assert hasattr(cachekit, "__all__"), "__all__ should be defined"

    def _test_p5_cache_basic(self, Cache):
        c = Cache()

        # Basic put/get
        c.put("a", 1)
        assert c.get("a") == 1, "Should be able to store and retrieve values"

        # Length
        assert len(c) == 1, "Length should be 1 after adding one item"

        # Default value
        assert c.get("missing", 42) == 42, "Should return default for missing key"
        assert c.get("missing") is None, "Should return None as default"

        # Overwrite
        c.put("a", 999)
        assert c.get("a") == 999, "Should be able to overwrite values"
        assert len(c) == 1, "Length should still be 1 after overwriting"

        # Clear
        c.clear()
        assert len(c) == 0, "Length should be 0 after clear"
        assert c.get("a") is None, "Should not find items after clear"

    def _test_p5_cache_edge(self, Cache):
        c = Cache()

        # Empty cache
        assert len(c) == 0, "New cache should be empty"
        assert c.get("anything") is None, "Empty cache should return None"

        # Multiple items
        c.put("x", 1)
        c.put("y", 2)
        c.put("z", 3)
        assert len(c) == 3, "Should handle multiple items"

        # Different value types
        c.put("string", "hello")
        c.put("list", [1, 2, 3])
        c.put("none", None)

        assert c.get("string") == "hello", "Should handle string values"
        assert c.get("list") == [1, 2, 3], "Should handle list values"
        assert c.get("none") is None, "Should handle None values"

    def _test_p5_version(self, cachekit):
        assert isinstance(cachekit.VERSION, str), "VERSION should be a string"
        assert len(cachekit.VERSION) > 0, "VERSION should not be empty"

        # print_version_info should not raise an error
        cachekit.print_version_info()

    def test_problem6(self):
        """Problem 6: 지표 계산기 (상속과 추상화) - 12 points"""
        self.problem_header(6, "지표 계산기 (상속과 추상화)")

        try:
            # Import the module
            problem6_path = Path("problem6/main.py")
            if not problem6_path.exists():
                self.results.append(TestResult("Problem 6 file missing", False, 0, 12, "problem6/main.py not found"))
                return

            spec = importlib.util.spec_from_file_location("problem6", problem6_path)
            problem6 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(problem6)

            # Test Metric abstract class
            self.test(
                "Metric abstract class",
                lambda: self._test_p6_metric_abstract(problem6.Metric),
                2
            )

            # Test Accuracy class
            self.test(
                "Accuracy class implementation",
                lambda: self._test_p6_accuracy_class(problem6.Accuracy, problem6.Metric),
                3
            )

            # Test Precision class
            self.test(
                "Precision class implementation",
                lambda: self._test_p6_precision_class(problem6.Precision, problem6.Metric),
                3
            )

            # Test Recall class
            self.test(
                "Recall class implementation",
                lambda: self._test_p6_recall_class(problem6.Recall, problem6.Metric),
                3
            )

            # Test polymorphism
            self.test(
                "Polymorphism behavior",
                lambda: self._test_p6_polymorphism(problem6.Accuracy, problem6.Precision, problem6.Recall),
                1
            )

        except Exception as e:
            print(f"  ❌ Failed to import Problem 6: {e}")
            self.results.append(TestResult("Problem 6 Import", False, 0, 12, str(e)))

    def _test_p6_metric_abstract(self, Metric):
        """Test Metric abstract class"""
        test_cases = []

        # Test abstract class cannot be instantiated
        try:
            metric = Metric("Test")
            self.assert_with_details(
                False,
                "Should not be able to instantiate abstract class",
                input="Metric('Test')",
                expected="TypeError",
                actual="No error (unexpected)"
            )
        except TypeError:
            # This is expected
            test_cases.append({
                "input": "Metric('Test')",
                "expected": "TypeError",
                "actual": "TypeError (correct)",
                "passed": True
            })

        # Test ABC structure
        import abc
        abc_inheritance = issubclass(Metric, abc.ABC)
        self.assert_with_details(
            abc_inheritance,
            "Metric should inherit from ABC",
            input="issubclass(Metric, abc.ABC)",
            expected=True,
            actual=abc_inheritance
        )
        test_cases.append({
            "input": "ABC inheritance check",
            "expected": True,
            "actual": abc_inheritance,
            "passed": abc_inheritance
        })

        return {"test_cases": test_cases}

    def _test_p6_accuracy_class(self, Accuracy, Metric):
        """Test Accuracy class"""
        test_cases = []
        accuracy = Accuracy()

        # Test inheritance
        inheritance_ok = isinstance(accuracy, Metric)
        self.assert_with_details(
            inheritance_ok,
            "Accuracy should inherit from Metric",
            input="isinstance(Accuracy(), Metric)",
            expected=True,
            actual=inheritance_ok
        )
        test_cases.append({
            "input": "Accuracy inheritance",
            "expected": True,
            "actual": inheritance_ok,
            "passed": inheritance_ok
        })

        # Test accuracy calculation
        y_true = [1, 0, 1, 1, 0, 1, 0, 0]
        y_pred = [1, 0, 0, 1, 0, 1, 1, 0]
        expected_acc = 6 / 8  # 6 correct out of 8
        acc_score = accuracy.compute(y_true, y_pred)
        acc_ok = abs(acc_score - expected_acc) < 0.01

        self.assert_with_details(
            acc_ok,
            "Accuracy should be (correct predictions) / (total predictions)",
            input=f"compute({y_true}, {y_pred})",
            expected=f"{expected_acc:.3f}",
            actual=f"{acc_score:.3f}"
        )
        test_cases.append({
            "input": f"compute({y_true}, {y_pred})",
            "expected": f"{expected_acc:.3f}",
            "actual": f"{acc_score:.3f}",
            "passed": acc_ok
        })

        # Test evaluate method
        eval_result = accuracy.evaluate(y_true, y_pred)
        eval_ok = "Accuracy: 0.750" in eval_result
        self.assert_with_details(
            eval_ok,
            "Accuracy evaluate should format correctly",
            input=f"evaluate({y_true}, {y_pred})",
            expected="'Accuracy: 0.750'",
            actual=eval_result
        )
        test_cases.append({
            "input": "evaluate() format",
            "expected": "'Accuracy: 0.750'",
            "actual": eval_result,
            "passed": eval_ok
        })

        return {"test_cases": test_cases}

    def _test_p6_precision_class(self, Precision, Metric):
        """Test Precision class"""
        test_cases = []
        precision = Precision(positive_class=1)

        # Test inheritance
        inheritance_ok = isinstance(precision, Metric)
        self.assert_with_details(
            inheritance_ok,
            "Precision should inherit from Metric",
            input="isinstance(Precision(positive_class=1), Metric)",
            expected=True,
            actual=inheritance_ok
        )
        test_cases.append({
            "input": "Precision inheritance",
            "expected": True,
            "actual": inheritance_ok,
            "passed": inheritance_ok
        })

        # Test precision calculation
        y_true = [1, 0, 1, 1, 0, 1, 0, 0]
        y_pred = [1, 0, 0, 1, 0, 1, 1, 0]
        # TP=3 (indices 0,3,5), FP=1 (index 6), Precision = 3/(3+1) = 0.75
        expected_prec = 3 / 4
        prec_score = precision.compute(y_true, y_pred)
        prec_ok = abs(prec_score - expected_prec) < 0.01

        self.assert_with_details(
            prec_ok,
            "Precision should be TP / (TP + FP)",
            input=f"compute({y_true}, {y_pred})",
            expected=f"{expected_prec:.3f}",
            actual=f"{prec_score:.3f}"
        )
        test_cases.append({
            "input": f"compute({y_true}, {y_pred})",
            "expected": f"{expected_prec:.3f}",
            "actual": f"{prec_score:.3f}",
            "passed": prec_ok
        })

        # Test evaluate method
        eval_result = precision.evaluate(y_true, y_pred)
        eval_ok = "Precision: 0.750" in eval_result
        self.assert_with_details(
            eval_ok,
            "Precision evaluate should format correctly",
            input=f"evaluate({y_true}, {y_pred})",
            expected="'Precision: 0.750'",
            actual=eval_result
        )
        test_cases.append({
            "input": "evaluate() format",
            "expected": "'Precision: 0.750'",
            "actual": eval_result,
            "passed": eval_ok
        })

        return {"test_cases": test_cases}

    def _test_p6_recall_class(self, Recall, Metric):
        """Test Recall class"""
        test_cases = []
        recall = Recall(positive_class=1)

        # Test inheritance
        inheritance_ok = isinstance(recall, Metric)
        self.assert_with_details(
            inheritance_ok,
            "Recall should inherit from Metric",
            input="isinstance(Recall(positive_class=1), Metric)",
            expected=True,
            actual=inheritance_ok
        )
        test_cases.append({
            "input": "Recall inheritance",
            "expected": True,
            "actual": inheritance_ok,
            "passed": inheritance_ok
        })

        # Test recall calculation
        y_true = [1, 0, 1, 1, 0, 1, 0, 0]
        y_pred = [1, 0, 0, 1, 0, 1, 1, 0]
        # TP=3 (indices 0,3,5), FN=1 (index 2), Recall = 3/(3+1) = 0.75
        expected_rec = 3 / 4
        rec_score = recall.compute(y_true, y_pred)
        rec_ok = abs(rec_score - expected_rec) < 0.01

        self.assert_with_details(
            rec_ok,
            "Recall should be TP / (TP + FN)",
            input=f"compute({y_true}, {y_pred})",
            expected=f"{expected_rec:.3f}",
            actual=f"{rec_score:.3f}"
        )
        test_cases.append({
            "input": f"compute({y_true}, {y_pred})",
            "expected": f"{expected_rec:.3f}",
            "actual": f"{rec_score:.3f}",
            "passed": rec_ok
        })

        # Test evaluate method
        eval_result = recall.evaluate(y_true, y_pred)
        eval_ok = "Recall: 0.750" in eval_result
        self.assert_with_details(
            eval_ok,
            "Recall evaluate should format correctly",
            input=f"evaluate({y_true}, {y_pred})",
            expected="'Recall: 0.750'",
            actual=eval_result
        )
        test_cases.append({
            "input": "evaluate() format",
            "expected": "'Recall: 0.750'",
            "actual": eval_result,
            "passed": eval_ok
        })

        return {"test_cases": test_cases}

    def _test_p6_polymorphism(self, Accuracy, Precision, Recall):
        """Test polymorphism"""
        # Test polymorphic behavior
        accuracy = Accuracy()
        precision = Precision(positive_class=1)
        recall = Recall(positive_class=1)

        y_true = [1, 0, 1, 1]
        y_pred = [1, 0, 0, 1]

        # Test that all metrics can be used polymorphically
        metrics = [accuracy, precision, recall]
        results = []
        for metric in metrics:
            result = metric.evaluate(y_true, y_pred)
            results.append(result)

        poly_ok = len(results) == 3 and all(":" in r for r in results)
        self.assert_with_details(
            poly_ok,
            "All metrics should work polymorphically",
            input="[m.evaluate(y_true, y_pred) for m in metrics]",
            expected="3 results with ':' format",
            actual=f"{len(results)} results: {results}"
        )

        return {
            "test_cases": [{
                "input": "polymorphic evaluation",
                "expected": "3 results with ':' format",
                "actual": f"{len(results)} results: {results}",
                "passed": poly_ok
            }]
        }

    def run_all_tests(self):
        """모든 테스트 실행"""
        print("🎯 Assignment 2 Auto-Grader")
        print("=" * 60)

        # Run all problem tests
        self.test_problem1()
        self.test_problem2()
        self.test_problem3()
        self.test_problem4()
        self.test_problem5()
        self.test_problem6()

        # Summary
        self.print_summary()

    def print_summary(self):
        """결과 요약 출력"""
        print(f"\n{'='*60}")
        print("📊 GRADING SUMMARY")
        print("=" * 60)

        total_points = 0
        max_total = 0
        problem_scores = {}

        # Calculate scores by problem
        for result in self.results:
            total_points += result.points
            max_total += result.max_points

            # Extract problem number from result name or use current_problem
            problem = "Unknown"
            if "Problem" in result.name:
                problem = result.name.split()[0] + " " + result.name.split()[1]

            if problem not in problem_scores:
                problem_scores[problem] = {"earned": 0, "total": 0}

            problem_scores[problem]["earned"] += result.points
            problem_scores[problem]["total"] += result.max_points

        # Print problem-by-problem scores
        for problem, scores in problem_scores.items():
            if scores["total"] > 0:
                percentage = (scores["earned"] / scores["total"]) * 100
                print(
                    f"{problem}: {scores['earned']}/{scores['total']} pts ({percentage:.1f}%)"
                )

        # Overall score
        print("-" * 40)
        overall_percentage = (total_points / max_total) * 100 if max_total > 0 else 0
        print(f"TOTAL: {total_points}/{max_total} pts ({overall_percentage:.1f}%)")

        # Grade assignment
        if overall_percentage >= 90:
            grade = "A"
        elif overall_percentage >= 80:
            grade = "B"
        elif overall_percentage >= 70:
            grade = "C"
        elif overall_percentage >= 60:
            grade = "D"
        else:
            grade = "F"

        print(f"GRADE: {grade}")

        # Failed tests details
        failed_tests = [r for r in self.results if not r.passed and r.max_points > 0]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"  • {result.name}: {result.message}")


if __name__ == "__main__":
    grader = Grader()
    grader.run_all_tests()
