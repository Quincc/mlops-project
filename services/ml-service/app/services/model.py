MODEL_VERSION = 'demo-model-1.0.0'


def predict_score(feature1: float, feature2: float, feature3: float) -> float:
    return round(feature1 * 0.6 + feature2 * 0.3 - feature3 * 0.1, 4)
