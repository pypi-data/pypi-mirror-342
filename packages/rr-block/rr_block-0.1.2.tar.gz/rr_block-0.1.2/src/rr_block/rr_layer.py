import torch
import torch.nn as nn


class RR(nn.Module):
    """
    Remix and Reactivate Layer.

    Args:
        dim (int): Number of input and output dimensions.
        activations (list): List of activation functions to apply.
    """

    def __init__(self, inout_dim: int, activations: list[nn.Module]):
        super().__init__()
        self.linear = nn.Linear(inout_dim, inout_dim)
        self.activations = activations

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the forward pass of the layer, each time it passes through one of the activations.

        Args:
            x (torch.Tensor): The input tensor. Shape should be compatible
                              with inout_dim.

        Returns:
            torch.Tensor: The output tensor. Shape will be related to
                          inout_dim.
        """
        for activation in self.activations:
            x = activation(x)
        return x

    def extra_repr(self) -> str:
        """
        Returns a string representation of the layer's parameters.
        """
        return (
            f"RR(inout_dim={self.linear.in_features}, activations={self.activations})"
        )
