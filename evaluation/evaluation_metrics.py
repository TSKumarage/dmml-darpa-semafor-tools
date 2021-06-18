from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import decimal

from matplotlib import pyplot


# Generate program metrics
class EvalMetrics:

    def __init__(self, analytic, save_path=""):
        self.analytic = analytic
        self.save_path = save_path

    def calculate_program_metrics(self, far, pd):

        pd_at_far = 0.0
        pd_at_eer = 0.0
        far_at_eer = 0.0

        for i in range(len(far)):
            if far[i] >= 0.1:
                pd_at_far = pd[i - 1]
                break

        for i in range(len(far)):
            if pd[i] >= 1 - far[i]:
                pd_at_eer = (pd[i - 1] + pd[i]) / 2
                far_at_eer = (far[i - 1] + far[i]) / 2
                break

        print("pD @ 0.1 FAR = %.3f" % (pd_at_far))
        print("pD @ EER = %.3f" % (pd_at_eer))
        print("FAR @ EER = %.3f" % (far_at_eer))

    def float_range(self, start, stop, step):

        while start < stop:
            yield float(start)
            start += decimal.Decimal(step)

    def evaluate_analytic(self, predict_prob, target):
        lr_auc = roc_auc_score(target, predict_prob)

        # summarize scores
        print("\n")
        print(" ----- Program Metrics Report -----")
        print()
        print('Classifier: ROC AUC=%.3f' % (lr_auc))

        # calculate roc curves
        lr_fpr, lr_tpr, _ = roc_curve(target, predict_prob)

        self.calculate_program_metrics(lr_fpr, lr_tpr)

        eq_fpr = list(self.float_range(0, 1, 1 / 1000))
        eq_tpr = [item for item in eq_fpr]

        # plot the roc curve for the model
        pyplot.plot(lr_fpr, lr_tpr, marker='.', label=self.analytic)
        pyplot.plot(eq_fpr, eq_tpr, marker='.', label='Random Chance')
        # axis labels

        pyplot.xlabel('Probability of False Alarm')
        pyplot.ylabel('Probability of Detection')
        # show the legend
        pyplot.legend()
        # show the plot
        pyplot.show()
        pyplot.savefig(self.save_path + '/' + self.analytic + "_ROC.pdf")
