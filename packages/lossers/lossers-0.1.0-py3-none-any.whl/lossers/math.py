from torch.nn import functional as F_

smooth_l1_loss = F_.smooth_l1_loss
l1_loss = F_.l1_loss
huber_loss = F_.huber_loss
l2_loss = F_.mse_loss
# inputs: y_pred, y_true
kl_div = F_.kl_div
