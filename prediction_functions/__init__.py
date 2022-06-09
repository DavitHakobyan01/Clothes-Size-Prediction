import pickle
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

MODEL_DIR = r'.\models'

def predict_shoe_size(gender: str, age: float, height: float, weight: float,
                      model_name='voting_classifier_without_age_feature'):
    """
    :param gender: Gender of the person ('Իգական', 'Արական')
    :param age: Age of the person
    :param height: Height of the person  (cm)
    :param weight: Weight of the person (kg)
    :param model_name: ML model which should be used to predict shoe size.
    Models are in .\\models\\shoe_size_pred_models directory

    :return: Top 3 highest predicted probabilities of shoe size
    """
    with open(fr'{MODEL_DIR}\shoe_size_pred_models\{model_name}.pkl', 'rb') as f:
        model = pickle.load(f)

    if '_without_age_feature' in model_name:
        sample = pd.DataFrame([[gender, height, weight]], columns=['sex', 'height', 'weight'])
    elif '_without_gender_feature' in model_name:
        sample = pd.DataFrame([[age, height, weight]], columns=['age', 'height', 'weight'])
    else:
        sample = pd.DataFrame([[gender, age, height, weight]], columns=['sex', 'age', 'height', 'weight'])

    probabilities = pd.DataFrame(model.predict_proba(sample).reshape(-1, 1), columns=['Shoe'],
                                 index=[int(i) for i in model.classes_]).sort_values(by='Shoe', ascending=False).iloc[:3]
    return (probabilities * 100).round(2).to_dict()


def predict_jeans_size(gender: str, age: float, height: float, weight: float,
                       model_name='voting_classifier'):
    """
    :param gender: Gender of the person ('Իգական', 'Արական')
    :param age: Age of the person
    :param height: Height of the person (cm)
    :param weight: Weight of the person (kg)
    :param model_name: ML model which should be used to predict jeans size.
    Models are in .\\models\\jeans_size_pred_models directory

    :return: Top 3 highest predicted probabilities of jeans size
    """
    with open(fr'{MODEL_DIR}\jeans_size_pred_models\{model_name}.pkl', 'rb') as f:
        model = pickle.load(f)

    if '_without_age_feature' in model_name:
        sample = pd.DataFrame([[gender, height, weight]], columns=['sex', 'height', 'weight'])
    elif '_without_gender_feature' in model_name:
        sample = pd.DataFrame([[age, height, weight]], columns=['age', 'height', 'weight'])
    else:
        sample = pd.DataFrame([[gender, age, height, weight]], columns=['sex', 'age', 'height', 'weight'])

    jeans_sizes = {
        0: 'XS (34-35)', 1: 'S (36-37)', 2: 'M (38-39)', 3: 'L (40-41)',
        4: 'XL (42-43)', 5: 'XXL (44-45)', 6: '3XL (46>)'
    }
    classes = [jeans_sizes[i] for i in model.classes_ if i in jeans_sizes.keys()]
    probabilities = pd.DataFrame(model.predict_proba(sample).reshape(-1, 1), columns=['Jeans'],
                                 index=classes).sort_values(by='Jeans', ascending=False).iloc[:3]
    return (probabilities * 100).round(2).to_dict()


def predict_shirt_size(gender: str, age: float, height: float, weight: float,
                       model_name='voting_classifier_without_gender_feature'):
    """
    :param gender: Gender of the person ('Իգական', 'Արական')
    :param age: Age of the person
    :param height: Height of the person (cm)
    :param weight: Weight of the person (kg)
    :param model_name: ML model which should be used to predict shirt size
    Models are in .\\models\\shirt_size_pred_models directory

    :return: Top 3 highest predicted probabilities of shirt size
    """
    with open(fr'{MODEL_DIR}\shirt_size_pred_models\{model_name}.pkl', 'rb') as f:
        model = pickle.load(f)

    if '_without_age_feature' in model_name:
        sample = pd.DataFrame([[gender, height, weight]], columns=['sex', 'height', 'weight'])
    elif '_without_gender_feature' in model_name:
        sample = pd.DataFrame([[age, height, weight]], columns=['age', 'height', 'weight'])
    else:
        sample = pd.DataFrame([[gender, age, height, weight]], columns=['sex', 'age', 'height', 'weight'])

    shirt_sizes = {0: 'XS', 1: 'S', 2: 'M', 3: 'L', 4: 'XL', 5: 'XXL'}
    classes = [shirt_sizes[i] for i in model.classes_ if i in shirt_sizes.keys()]
    probabilities = pd.DataFrame(model.predict_proba(sample).reshape(-1, 1), columns=['Shirt'],
                                 index=classes).sort_values(by='Shirt', ascending=False).iloc[:3]
    return (probabilities * 100).round(2).to_dict()


def predict_clothes_sizes(gender: str, age: float, height: float, weight: float,
                          models_names=None):
    """
    :param gender: Gender of the person ('Իգական', 'Արական')
    :param age: Age of the person
    :param height: Height of the person (cm)
    :param weight: Weight of the person (kg)
    :param models_names: ML models which should be used to predict clothes_sizes order: shoe, jeans, shirt
    Models are in .\\models\\shirt_size_pred_models directory

    :return: Top 3 highest predicted probabilities of clothes sizes
    """
    if models_names is None:
        models_names = ['voting_classifier_without_age_feature',
                        'voting_classifier',
                        'voting_classifier_without_gender_feature']

    shoe_sizes = predict_shoe_size(gender, age, height, weight, models_names[0])
    jeans_sizes = predict_jeans_size(gender, age, height, weight, models_names[1])
    shirt_sizes = predict_shirt_size(gender, age, height, weight, models_names[2])

    json = {
        'Shoe': shoe_sizes['Shoe'],
        'Jeans': jeans_sizes['Jeans'],
        'Shirt': shirt_sizes['Shirt']
    }
    return json

