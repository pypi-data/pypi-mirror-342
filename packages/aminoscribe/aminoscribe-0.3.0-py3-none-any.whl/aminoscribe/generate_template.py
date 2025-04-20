import numpy as np

# Globals
aa_to_mean = {
    'C': -0.28974021809519707,
    'S': -0.0035002010654761493,
    'A': -0.03108840476998101,
    'G': 0.06698305168494242,
    'T': -0.2957685855135865,
    'V': -0.30156827132970515,
    'N': -0.1491754438521338,
    'Q': -0.29759999726556324,
    'M': -0.3476622691937972,
    'I': -0.384734702909101,
    'L': -0.40732718322660594,
    'Y': -0.5151876113404014,
    'W': -0.5086544951426771,
    'F': -0.39973706243275675,
    'P': -0.3176054339184605,
    'H': -0.3546616920759566,
    'R': -0.4626488736914648,
    'K': -0.322363089090543,
    'D': 0.4787410087108259,
    'E': 0.26795968917348334
}

aa_to_std = {
    'C': 0.0878836937602983,
    'S': 0.0031622776601683794,
    'A': 0.0031622776601683794,
    'G': 0.0031622776601683794,
    'T': 0.07013493083186818,
    'V': 0.08433398152006277,
    'N': 0.031023313546838776,
    'Q': 0.0031622776601683794,
    'M': 0.02154807770604568,
    'I': 0.0031622776601683794,
    'L': 0.0031622776601683794,
    'Y': 0.0031622776601683794,
    'W': 0.0031622776601683794,
    'F': 0.0031622776601683794,
    'P': 0.04203324905756604,
    'H': 0.0031622776601683794,
    'R': 0.02313273013244223,
    'K': 0.07874032269860308,
    'D': 0.07433504559998479,
    'E': 0.08112084580409262}

window_size = 20
window_indices = np.arange(window_size)
window_function = np.array(-0.00944976 * window_indices**2 + 0.179545 * window_indices + 0.148364,
                           dtype=np.float64)

# Pulls from Gaussian, unless platonian is true
def get_score(amino_acid, platonian=False, rng=None):
    if platonian:
        return aa_to_mean[amino_acid]
    rng = rng or np.random.default_rng()
    return rng.normal(aa_to_mean[amino_acid], aa_to_std[amino_acid])


def predict_current(scores):
    window_score = np.dot(scores, window_function)
    return window_score


def template_from_sequence(seq, platonian=False, rng=None):
    backwards_sliding_indices = range(len(seq) - window_size, -1, -1)
    scores = [get_score(aa, platonian=platonian, rng=rng) for aa in seq]
    squiggle = np.array([predict_current(scores[i:i+window_size])
                        for i in backwards_sliding_indices], dtype=np.float64)
    return squiggle
