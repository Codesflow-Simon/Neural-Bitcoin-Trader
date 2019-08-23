import tensorflow as tf
import numpy as np
from dataset import environment
import sys

# DNN sizes
n_inputs = 27
n_hidden = 4
n_output = 3
initalister = tf.initializers.variance_scaling()

learning_rate = 0.01

# Building DNN
X = tf.placeholder(tf.float32, shape=[None, n_inputs], name='input')
hidden = tf.layers.dense(X, n_hidden, activation=tf.nn.elu,
                         kernel_initializer=initalister)
logits = tf.layers.dense(hidden, n_output,
                         kernel_initializer=initalister)
output = tf.nn.softmax(logits)
action = tf.random.categorical(tf.math.log(output), num_samples=1)

# Want 1 to be target
y = tf.one_hot(action[0], depth=3)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(
    labels=y, logits=logits)
optimizer = tf.train.AdamOptimizer(learning_rate)

# Calculation and storage of gradients
grads_and_vars = optimizer.compute_gradients(cross_entropy)
gradients = [grad for grad, variable in grads_and_vars]
gradient_placeholders = []
grads_and_vars_feed = []
for grad, variable in grads_and_vars:
    gradient_placeholder = tf.placeholder(tf.float32, shape=grad.shape, name='gradient')
    gradient_placeholders.append(gradient_placeholder)
    grads_and_vars_feed.append((gradient_placeholder, variable))

training_op = optimizer.apply_gradients(grads_and_vars_feed)
init = tf.global_variables_initializer()
saver = tf.train.Saver()


def discount_rewards(rewards, gamma):
    discounted_rewards = np.empty(len(rewards))
    cumulative_rewards = 0
    for step in reversed(range(len(rewards))):
        cumulative_rewards = rewards[step] + cumulative_rewards * gamma
        discounted_rewards[step] = cumulative_rewards
    return discounted_rewards


def discount_and_normalise_rewards(all_rewards, gamma):
    all_discounted_rewards = [discount_rewards(
        rewards, gamma)for rewards in all_rewards]
    flat_rewards = np.concatenate(all_discounted_rewards)
    rewards_mean = flat_rewards.mean()
    rewards_std = flat_rewards.std()
    return [(discounted_rewards - rewards_mean)/rewards_std
            for discounted_rewards in all_discounted_rewards]


n_iterations = 100       # Training iterations
n_max_steps = 10         # Max steps per episode
n_games_per_update = 10  # Train the policy every x episodes
save_iterations = 10     # save the model every 10 iterations
gamma = 0.93             # discount factor
env = environment()

with tf.Session() as sess:
    init.run()
    for iteration in range(n_iterations):
        all_rewards = []   # all sequences of raw rewards for each episode
        all_gradients = [] # gradients saves at each step per episode

        position = 0
        for game in range(n_games_per_update):
            current_rewards = []
            current_gradients = []
            obs, d = env.reset()

            for step in range(n_max_steps):
                action_val, gradients_val, recomended_position = sess.run(
                    [action, gradients, action[0]-1],
                    feed_dict={X: obs}
                )
                if recomended_position != position:
                    bias = -0.1
                else:
                    bias = 0
                position = recomended_position
                obs, d = env.next_step()
                reward = d * position + bias
                current_rewards.append(d)
                current_gradients.append(gradients_val)

            all_rewards.append(current_rewards)
            all_gradients.append(current_gradients)


        all_rewards = discount_and_normalise_rewards(all_rewards, gamma)
        feed_dict = {}
        _b, _d = env.reset()
        for var_index, grad_placeholder in enumerate(gradient_placeholders):
            # Multiply the gradients by the action scores
            mean_gradients = np.mean(
                [reward * all_gradients[game_index][step][var_index]
                for game_index, rewards in enumerate(all_rewards)
                for step, reward in enumerate(rewards)],
                axis=0
            )
            feed_dict[grad_placeholder] = mean_gradients
        sess.run(training_op, feed_dict=feed_dict)
        if iteration % save_iterations ==0:
            saver.save(sess, './train/checkpoints/policy.ckpt')
