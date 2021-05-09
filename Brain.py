from tensorflow.keras.layers import (
    Dense,
    Activation,
    Conv2D,
    Flatten,
    Dropout,
    BatchNormalization,
    MaxPooling2D,
)
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
import numpy as np


class ReplayBuffer(object):
    def __init__(self, max_size, input_shape):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.float32)
        self.action_memory = np.zeros((self.mem_size, 2), dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.uint8)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        states_ = self.new_state_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal


def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    model = Sequential()
    model.add(Flatten(input_shape=(*input_dims,)))
    model.add(Dense(fc1_dims, activation="sigmoid"))
    # model.add(Dense(fc2_dims, activation='relu'))
    model.add(Dense(n_actions, activation="sigmoid"))

    model.compile(optimizer=Adam(lr=lr), loss="mean_squared_error")

    return model


class Brain(object):
    def __init__(
        self,
        alpha,
        gamma,
        n_actions,
        epsilon,
        batch_size,
        replace,
        input_dims,
        eps_dec=0.996,
        eps_min=0.01,
        mem_size=10000,
        q_eval_fname="q_eval.h5",
        q_target_fname="q_next.h5",
    ):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = eps_dec
        self.eps_min = eps_min
        self.batch_size = batch_size
        self.replace = replace
        self.q_target_model_file = q_target_fname
        self.q_eval_model_file = q_eval_fname
        self.learn_step = 0
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(alpha, n_actions, input_dims, 32, 128)
        self.q_next = build_dqn(alpha, n_actions, input_dims, 32, 128)

    def replace_target_network(self):
        if self.replace is not None and self.learn_step % self.replace == 0:
            self.q_next.set_weights(self.q_eval.get_weights())
            print("UPDATING TARGET NETWORK")

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            actions = np.random.logistic(size=len(self.action_space))
        else:
            state = np.array([observation], copy=False, dtype=np.float32)
            actions = self.q_eval(state)
            # action = np.argmax(actions)

        return actions

    def learn(self):
        if self.memory.mem_cntr > self.batch_size:
            state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)

            self.replace_target_network()

            q_eval = self.q_eval.predict(state)

            q_next = self.q_next.predict(new_state)

            q_target = q_eval[:]
            indices = np.arange(self.batch_size)
            q_target[indices, action] = reward + self.gamma * np.max(q_next, axis=1) * (1 - done)
            self.q_eval.train_on_batch(state, q_target)

            self.epsilon = (
                self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min
            )
            self.learn_step += 1

    def save_models(self):
        self.q_eval.save(self.q_eval_model_file)
        self.q_next.save(self.q_target_model_file)
        print("... saving models ...")

    def load_models(self):
        self.q_eval = load_model(self.q_eval_model_file)
        self.q_nexdt = load_model(self.q_target_model_file)
        print("... loading models ...")

    def get_weights(self):
        return self.q_next.get_weights()

    def set_weights(self, weights):
        # Todo: change indexes to params i.e. self.n_weights_layer1 = input_size*layer1_size
        weights_layer1 = [
            np.array(np.reshape(weights[: 32 * 48], (48, 32))),
            np.array(weights[32 * 48 : 32 * 48 + 32]),
        ]
        weights_layer2 = [
            np.array(np.reshape(weights[32 * 48 + 32 : 32 * 48 + 32 + 32 * 3], (32, 3))),
            np.array(weights[32 * 48 + 32 + 32 * 3 :]),
        ]
        self.q_eval.layers[1].set_weights(weights_layer1)
        self.q_eval.layers[2].set_weights(weights_layer2)
        self.q_next.layers[1].set_weights(weights_layer1)
        self.q_next.layers[2].set_weights(weights_layer2)
