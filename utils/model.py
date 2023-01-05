import numpy as np
import os
import joblib


class Perceptron:
    def __init__(self, eta: float=None, epochs: int=None):
        self.weights = np.random.randn(3) * 1e-4 #small random weights
        is_training = (eta is not None) and (epochs is not None)
        if is_training:
            print(f"initial weights before training: \n{self.weights}")
        self.eta = eta
        self.epochs = epochs
             
    def _z_outcome(self, inputs, weights):
        # np.dot(4,6) = 24
        return np.dot(inputs,weights)
        
    def activation_function(self,z):
        # If z is greater than 0 is 1
        # if z is less than 0 it is 0
        return np.where(z>0,1,0)
    
    def fit(self,X, y):
        self.X = X
        self.y = y
        
        # np.c_[np.array([1,2,3]), np.array([4,5,6])] 
        # => array([[1, 4],[2, 5],[3, 6]])
        # -np.ones(4,1)
        # => array([[-1.],[-1.],[-1.],[-1.]]
        X_with_bias = np.c_[self.X , -np.ones((len(self.X),1))]
        print(f"X with bias: \n{X_with_bias}")
        
        for epoch in range(self.epochs):
            print("--"*10)
            print(f"for epoch >> {epoch}")
            print("--"*10)
            
            z = self._z_outcome(X_with_bias,self.weights)
            y_hat = self.activation_function(z)
            print(f"Predicted value after forward pass: \n{y_hat}")
            
            self.error = self.y - y_hat
            print(f"error: \n{self.error}")
            
            self.weights = self.weights + self.eta*np.dot(X_with_bias.T,self.error)
            print(f"updated weight after epoch: {epoch+1}/{self.epochs}: \n{self.weights}")
            print("##"*10)
    
    def predict(self, X):
        X_with_bias = np.c_[X,-np.ones((len(X),1))]
        z = self._z_outcome(X_with_bias,self.weights)
        return self.activation_function(z)
    
    def total_loss(self):
        total_loss = np.sum(self.error)
        print(f"total loss: {total_loss}\n")
        return total_loss
    
    def _create_dir_return_path(self,model_dir,filename):
        os.makedirs(model_dir,exist_ok=True)
        return os.path.join(model_dir,filename)
    
    def save(self,filename,model_dir=None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir,filename)
            joblib.dump(self,model_file_path)
        else:
            model_file_path = self._create_dir_return_path("model",filename)
            joblib.dump(self, model_file_path)
    
    def load(self,filepath):
        return joblib.load(filepath)