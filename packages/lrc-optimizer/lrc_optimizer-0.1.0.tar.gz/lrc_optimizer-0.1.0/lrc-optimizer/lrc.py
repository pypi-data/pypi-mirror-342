import torch
class LearningEfficiencyTracker:
    def __init__(self):
        self.lrc_history = []
        self.total_lrc = 0.0

    def compute_LRC(self, model, optimizer, loss_fn, data_loader):
        total_lrc = 0.0
        num_batches = 0

        for inputs, targets in data_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, targets)

            # Get gradient of loss w.r.t. outputs
            loss_derivative = torch.autograd.grad(loss, outputs, create_graph=True)[0]

            # Task complexity: variance of input
            task_complexity = torch.var(inputs)

            # Adaptability: sum of learning rates
            adaptability = sum([group['lr'] for group in optimizer.param_groups])

            # LRC = |dL/dŷ| × C(t) × A(t)
            lrc = loss_derivative * task_complexity * adaptability
            total_lrc += lrc.abs().sum()
            num_batches += 1

        avg_lrc = total_lrc / num_batches if num_batches > 0 else 0.0
        self.lrc_history.append(avg_lrc)
        self.total_lrc += avg_lrc
        return avg_lrc

    def get_integrated_learning_efficiency(self):
        return self.total_lrc

    def get_average_learning_efficiency(self):
        return sum(self.lrc_history) / len(self.lrc_history) if self.lrc_history else 0.0
