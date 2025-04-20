from tensorflow.keras.models import Sequential, clone_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

def create_model(input_dim, hidden_units=16, output_dim=1):
    model = Sequential([
        Dense(hidden_units, activation='relu', input_shape=(input_dim,)),
        Dense(hidden_units, activation='relu'),
        Dense(output_dim)
    ])
    model.compile(optimizer=Adam(0.001), loss='mse', metrics=['mae'])
    return model

def combine_models_weights(model1, model2, r2_1, r2_2):
    w1, w2 = model1.get_weights(), model2.get_weights()
    combined = [(a*r2_1 + b*r2_2)/(r2_1 + r2_2) for a, b in zip(w1, w2)]
    new_model = clone_model(model1)
    new_model.set_weights(combined)
    new_model.compile(optimizer=Adam(0.001), loss='mse', metrics=['mae'])
    return new_model