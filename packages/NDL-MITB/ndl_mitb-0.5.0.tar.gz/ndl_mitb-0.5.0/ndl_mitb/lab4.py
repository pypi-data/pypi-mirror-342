import numpy as np
import matplotlib.pyplot as plt

class GRBF_XOR:
    def __init__(self):
        self.inputs = np.array([[0,0],[0,1],[1,0],[1,1]])
        self.outputs = np.array([0,1,1,0])
        self.w1 = np.array([1,1])
        self.w2 = np.array([0,0])

    def gaussian(self, x, w):
        return np.exp(-np.linalg.norm(x - w) ** 2)

    def evaluate(self):
        print("Input\tFirst Function\tSecond Function")
        for i in self.inputs:
            v1, v2 = self.gaussian(i, self.w1), self.gaussian(i, self.w2)
            print(f"{i} \t{v1:.4f} \t\t{v2:.4f}")

    def plot_features(self):
        f1, f2 = [], []
        inputs = np.array([[0,0],[1,1],[0,1],[1,0]])
        for i in inputs:
            f1.append(self.gaussian(i, self.w1))
            f2.append(self.gaussian(i, self.w2))

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.scatter(f1[:2], f2[:2], marker="x", label="Output: 0")
        ax.scatter(f1[2:], f2[2:], marker="o", label="Output: 1")
        ax.plot(np.linspace(0,1,10), -np.linspace(0,1,10)+1, label="y = -x + 1", color="gray")
        ax.set_xlabel("Hidden Function 1")
        ax.set_ylabel("Hidden Function 2")
        ax.set_xlim(left=-0.1)
        ax.set_ylim(bottom=-0.1)
        ax.legend()
        plt.title("Feature Space for XOR using GRBF")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    # Create GRBF_XOR object
    model = GRBF_XOR()
    model.evaluate()
    model.plot_features()
