import pytest
import torch
import torch.nn as nn

from rr_block import RR


@pytest.fixture
def default_layer():
    """Provides a default instance of RR for tests."""
    dim = 64
    return RR(inout_dim=dim, activations=[nn.ReLU(), nn.Sigmoid()])


@pytest.fixture
def default_input():
    """Provides default input data."""
    batch_size = 4
    dim = 64
    return torch.randn(batch_size, dim)


def test_layer_creation():
    """Tests if the layer can be instantiated correctly."""
    dim = 32
    try:
        layer = RR(inout_dim=dim, activations=[nn.ReLU(), nn.Sigmoid()])
        assert isinstance(layer, RR), "Layer should be an instance of RR"
        assert isinstance(layer, nn.Module), "Layer should be a PyTorch Module"
        assert layer.linear.in_features == dim, "Input features should match"
        assert layer.linear.out_features == dim, "Output features should match"
        assert len(layer.activations) == 2, "Should have two activations"
        assert isinstance(
            layer.activations[0], nn.ReLU
        ), "First activation should be ReLU"
        assert isinstance(
            layer.activations[1], nn.Sigmoid
        ), "Second activation should be Sigmoid"
    except Exception as e:
        pytest.fail(f"Layer instantiation failed: {e}")


def test_forward_pass_shape(default_layer, default_input):
    """Tests the output shape after a forward pass."""
    layer = default_layer
    input_data = default_input

    # Ensure input matches layer's expected input features
    assert (
        input_data.shape[1] == layer.linear.in_features
    ), f"Input shape mismatch. Expected {layer.linear.in_features}, got {input_data.shape[1]}"

    # Perform forward pass
    try:
        output = layer(input_data)
    except Exception as e:
        pytest.fail(f"Forward pass failed: {e}")

    # Check output type
    assert isinstance(output, torch.Tensor), "Output should be a torch.Tensor"

    # Check output shape
    expected_batch_size = input_data.shape[0]
    expected_output_features = layer.linear.out_features
    expected_shape = (expected_batch_size, expected_output_features)

    assert (
        output.shape == expected_shape
    ), f"Output shape mismatch. Expected {expected_shape}, got {output.shape}"


@pytest.mark.parametrize(
    "batch_size, dim, activations",
    [
        (1, 64, [nn.ReLU()]),
        (2, 128, [nn.ReLU(), nn.Sigmoid()]),
        (4, 256, [nn.Tanh()]),
        (8, 512, [nn.ReLU(), nn.Sigmoid(), nn.Tanh()]),
        (16, 512, [nn.ReLU(), nn.Sigmoid(), nn.Tanh(), nn.LeakyReLU()]),
    ],
)
def test_forward_various_shapes(batch_size, dim, activations):
    """Tests forward pass with various input shapes and activations."""
    layer = RR(inout_dim=dim, activations=activations)
    input_data = torch.randn(batch_size, dim)
    try:
        output = layer(input_data)
    except Exception as e:
        pytest.fail(
            f"Forward pass failed for batch_size {batch_size} and dim {dim}: {e} with activations {activations}"
        )

    expected_shape = (batch_size, dim)
    assert (
        output.shape == expected_shape
    ), f"Output shape mismatch for batch_size {batch_size} and dim {dim}. Expected {expected_shape}, got {output.shape}"


def test_gradient_flow(default_layer, default_input):
    """Tests if gradients can flow back through the layer."""
    layer = default_layer
    input_data = default_input.clone().requires_grad_(True)

    params_require_grad = [p for p in layer.parameters() if p.requires_grad]
    assert (
        len(params_require_grad) > 0
    ), "Layer should have trainable parameters for this test"

    # Perform forward pass
    output = layer(input_data)

    # Create a dummy loss (e.g., sum of outputs)
    # Ensure the loss is a scalar
    loss = output.sum()

    # Perform backward pass
    try:
        loss.backward()
    except Exception as e:
        pytest.fail(f"Backward pass failed: {e}")

    # Check if input gradient exists (if input required grad)
    assert (
        input_data.grad is not None
    ), "Input gradient should exist after backward pass"
    assert input_data.grad.shape == input_data.shape, "Input gradient shape mismatch"

    # Check if layer parameters have gradients (if they require grad)
    for param in params_require_grad:
        assert (
            param.grad is not None
        ), f"Parameter {param.name if hasattr(param, 'name') else 'unnamed'} should have a gradient"
        assert not torch.all(
            param.grad == 0
        ), f"Gradient for parameter {param.name if hasattr(param, 'name') else 'unnamed'} should not be all zeros (usually)"


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA device not available")
def test_forward_pass_gpu(default_layer, default_input):
    """Tests the forward pass on a GPU device, if available."""
    device = torch.device("cuda")
    layer = default_layer.to(device)
    input_data = default_input.to(device)

    try:
        output = layer(input_data)
    except Exception as e:
        pytest.fail(f"Forward pass on GPU failed: {e}")

    assert output.device.type == "cuda", "Output tensor should be on CUDA device"

    # Check output shape (as before)
    expected_shape = (input_data.shape[0], layer.linear.out_features)
    assert (
        output.shape == expected_shape
    ), f"Output shape mismatch on GPU. Expected {expected_shape}, got {output.shape}"


def test_scriptability(default_layer):
    """Tests if the layer can be JIT-scripted."""
    layer = default_layer
    try:
        scripted_layer = torch.jit.script(layer)
        assert scripted_layer is not None
        input_data = torch.randn(2, layer.linear.in_features)
        output_script = scripted_layer(input_data)
        output_orig = layer(input_data)
        assert torch.allclose(output_script, output_orig)
    except Exception as e:
        pytest.fail(f"torch.jit.script(layer) failed: {e}")


def test_repr(default_layer):
    """Tests the string representation of the layer."""
    layer = default_layer
    representation = repr(layer)
    assert isinstance(representation, str)
    assert "RR" in representation
    assert f"inout_dim={layer.linear.in_features}" in representation
    assert f"activations={layer.activations})" in representation
