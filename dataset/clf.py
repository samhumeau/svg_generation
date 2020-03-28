from sklearn import tree
from sklearn.tree.export import export_text

classes_indexes = {key: val for val, key in enumerate(['exposed', 'call15', 'planConsult', 'fastConsult', 'confined'])}
base_features_names = [
    '!!data.age',
    '!!data.breathingProblems',
    '!!data.fever',
    '!!data.cough',
    'hasMorbidityOrPregnancy(data)',
    'hasBeenExposed(data)',
    'hasDiarrheaOrFatigue(data)'
]

extended_features_names = [
    '(!!data.breathingProblems or !!data.fever or !!data.cough)',
    '(!!data.breathingProblems and !!data.fever and !!data.cough)'
]

def compute_extended_features(features):
    return [
        min(1, features[1] + features[2] + features[3]),
        features[1] * features[2] * features[3]
    ]



data = []
classes = []
with open('./tree.tsv', 'r') as f:
    for line in f:
        split = line.rstrip().split('\t')
        features = [1 if val == "Oui" else 0 for val in split[:-1]]
        extended_features = compute_extended_features(features)
        data.append(features + extended_features)
        classes.append(classes_indexes[split[-1]])


clf = tree.DecisionTreeClassifier(criterion='gini')
clf = clf.
res = export_text(clf, feature_names=base_features_names + extended_features_names)
res = res.replace('---', 'if ').replace(' >  0.50', ' is true:').replace('<= 0.50', 'is false:')
print(res)
