OLD_CHECKPOINT_FILE = "baseline_siamese-00-19901"
NEW_CHECKPOINT_FILE = "baseline_siamese-00-19901"

import tensorflow as tf
vars_to_rename = {
    # "lstm/basic_lstm_cell/weights": "lstm/basic_lstm_cell/kernel",
    # "lstm/basic_lstm_cell/biases": "lstm/basic_lstm_cell/bias",
    # "lstm/basic_lstm_cell/weights": "lstm/basic_lstm_cell/weights",
    # "lstm/basic_lstm_cell/biases": "lstm/basic_lstm_cell/biases",
    "lstm/BasicLSTMCell/Linear/Matrix": "lstm/basic_lstm_cell/kernel",
    "lstm/BasicLSTMCell/Linear/Bias": "lstm/basic_lstm_cell/bias",
}
new_checkpoint_vars = {}
reader = tf.train.NewCheckpointReader(OLD_CHECKPOINT_FILE)
for old_name in reader.get_variable_to_shape_map():
  print(old_name)
  if "lstm_cell/weights" in old_name:
    new_name = old_name.replace("lstm_cell/weights", "lstm_cell/kernel")
    new_name = old_name.replace("lstm_cell/biases", "lstm_cell/bias")
  elif "embedding_var/word_emb_mat" in old_name:
    new_name = old_name.replace("embedding_var/word_emb_mat", "embedding_var/word_emb_mat/Adam")
  else:
    new_name = old_name

  new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))
exit()
init = tf.global_variables_initializer()
saver = tf.train.Saver(new_checkpoint_vars)

with tf.Session() as sess:
  sess.run(init)
  saver.save(sess, NEW_CHECKPOINT_FILE)
