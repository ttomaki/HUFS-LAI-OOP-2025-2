# main.py
"""
Problem 6 — 지표 계산기 (상속과 추상화)
- ML 성능 지표를 계산하는 추상 클래스와 구체 클래스들 구현
- 상속, 추상화, 다형성 학습
"""

from abc import ABC, abstractmethod


class Metric(ABC):
    def __init__(self, name: str) -> None:
        """
        지표 이름을 저장하는 기본 생성자.
        """
        self.name = name

    @abstractmethod
    def compute(self, y_true: list[int], y_pred: list[int]) -> float:
        """
        실제값과 예측값을 받아 지표를 계산하는 추상 메서드.
        구체 클래스에서 반드시 구현해야 합니다.
        """
        pass

    def evaluate(self, y_true: list[int], y_pred: list[int]) -> str:
        """
        지표를 계산하고 결과를 문자열로 반환.
        """
        score = self.compute(y_true, y_pred)
        return f"{self.name}: {score:.3f}"


class Accuracy(Metric):
    def __init__(self) -> None:
        """
        정확도 지표 초기화.
        """
        super().__init__("Accuracy")

    def compute(self, y_true: list[int], y_pred: list[int]) -> float:
        """
        정확도 계산: (맞은 예측 수) / (전체 예측 수)
        """
        if len(y_true) == 0:
            return 0.0

        correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        return correct / len(y_true)


class Precision(Metric):
    def __init__(self, positive_class: int = 1) -> None:
        """
        정밀도 지표 초기화.
        """
        super().__init__("Precision")
        self.positive_class = positive_class

    def compute(self, y_true: list[int], y_pred: list[int]) -> float:
        """
        정밀도 계산: TP / (TP + FP)
        """
        if len(y_true) == 0:
            return 0.0

        tp = sum(1 for t, p in zip(y_true, y_pred)
                if t == self.positive_class and p == self.positive_class)
        fp = sum(1 for t, p in zip(y_true, y_pred)
                if t != self.positive_class and p == self.positive_class)

        if tp + fp == 0:
            return 0.0

        return tp / (tp + fp)


class Recall(Metric):
    def __init__(self, positive_class: int = 1) -> None:
        """
        재현율 지표 초기화.
        """
        super().__init__("Recall")
        self.positive_class = positive_class

    def compute(self, y_true: list[int], y_pred: list[int]) -> float:
        """
        재현율 계산: TP / (TP + FN)
        """
        if len(y_true) == 0:
            return 0.0

        tp = sum(1 for t, p in zip(y_true, y_pred)
                if t == self.positive_class and p == self.positive_class)
        fn = sum(1 for t, p in zip(y_true, y_pred)
                if t == self.positive_class and p != self.positive_class)

        if tp + fn == 0:
            return 0.0

        return tp / (tp + fn)


if __name__ == "__main__":
    # Demo runs only when executed directly
    def run_demo():
        print("📊 ML Metrics Calculator Demo")
        print("=" * 40)

        # 테스트 데이터
        y_true = [1, 0, 1, 1, 0, 1, 0, 0]
        y_pred = [1, 0, 0, 1, 0, 1, 1, 0]

        print(f"\n📋 Test Data:")
        print(f"y_true: {y_true}")
        print(f"y_pred: {y_pred}")

        # 지표 객체 생성
        accuracy = Accuracy()
        precision = Precision(positive_class=1)
        recall = Recall(positive_class=1)

        print(f"\n🔍 Inheritance Check:")
        print(f"accuracy isinstance Metric: {isinstance(accuracy, Metric)}")
        print(f"precision isinstance Metric: {isinstance(precision, Metric)}")
        print(f"recall isinstance Metric: {isinstance(recall, Metric)}")

        print(f"\n📈 Individual Metrics:")
        print(f"Accuracy: {accuracy.compute(y_true, y_pred):.3f}")
        print(f"Precision: {precision.compute(y_true, y_pred):.3f}")
        print(f"Recall: {recall.compute(y_true, y_pred):.3f}")

        print(f"\n📝 Formatted Results:")
        print(accuracy.evaluate(y_true, y_pred))
        print(precision.evaluate(y_true, y_pred))
        print(recall.evaluate(y_true, y_pred))

        print(f"\n🎯 Polymorphism Demo:")
        metrics = [accuracy, precision, recall]
        for metric in metrics:
            result = metric.evaluate(y_true, y_pred)
            print(f"  {result}")

        print(f"\n🧮 Detailed Calculation Example:")
        # 상세 계산 예시
        y_example = [1, 0, 1, 1]
        p_example = [1, 0, 0, 1]

        print(f"Example: y_true={y_example}, y_pred={p_example}")

        # 수동 계산
        correct = sum(1 for t, p in zip(y_example, p_example) if t == p)
        acc = correct / len(y_example)
        print(f"  Accuracy: {correct}/{len(y_example)} = {acc:.3f}")

        tp = sum(1 for t, p in zip(y_example, p_example) if t == 1 and p == 1)
        fp = sum(1 for t, p in zip(y_example, p_example) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(y_example, p_example) if t == 1 and p == 0)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        print(f"  TP={tp}, FP={fp}, FN={fn}")
        print(f"  Precision: {tp}/({tp}+{fp}) = {prec:.3f}")
        print(f"  Recall: {tp}/({tp}+{fn}) = {rec:.3f}")

        # 추상 클래스 테스트
        print(f"\n⚠️ Abstract Class Test:")
        try:
            metric = Metric("Test")
            print("ERROR: Should not be able to instantiate abstract class!")
        except TypeError as e:
            print(f"✅ Correctly prevented: {e}")

    run_demo()