# utils.py
import scipy.io as sio

def save_model(model, filename="model.mat"):
    """Save model weights to a .mat file."""
    model_dict = {
        "weights": model.weights.data,
        "bias": model.bias.data
    }
    sio.savemat(filename, model_dict)
    print(f"Model saved to {filename}")

def load_model(model, filename="model.mat"):
    """Load model weights from a .mat file."""
    model_dict = sio.loadmat(filename)
    model.weights.data = model_dict["weights"]
    model.bias.data = model_dict["bias"]
    print(f"Model loaded from {filename}")

    # utils.py
    def train(model, data, targets, optimizer, epochs=100, save_every=10):
        for epoch in range(epochs):
            total_loss = 0
            for x, y in zip(data, targets):
                # Forward pass
                output = model.forward(x)
                loss = (output - y) ** 2  # Mean Squared Error loss

                # Backward pass
                loss.backward()

                # Update weights
                optimizer.step()

                total_loss += loss.data

            if epoch % save_every == 0:
                save_model(model, f"model_epoch_{epoch}.mat")

            print(f"Epoch {epoch + 1}: Loss = {total_loss / len(data)}")

