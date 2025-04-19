import torch

from petharbor.utils.logging_setup import get_logger

logger = get_logger()


def configure_device(device=None):
    """
    Configures the device to be used for computations, either CPU or CUDA.

    Parameters:
    device (str, optional): The device to be used. If None, the function will
                            automatically select CUDA if available, otherwise CPU.
                            If 'cpu', it will use the CPU even if CUDA is available.
                            If 'cuda' or 'cuda:<device_id>', it will use the specified
                            CUDA device if available, otherwise default to CPU.

    Returns:
    str: The device that will be used ('cpu' or 'cuda:<device_id>').
    """
    cuda_available = torch.cuda.is_available()

    if device is None:
        if cuda_available:
            device = f"cuda:{torch.cuda.current_device()}"
            logger.info(
                f"Using CUDA device: {torch.cuda.get_device_name()} (ID: {torch.cuda.current_device()})"
            )
        else:
            logger.warning("CUDA is not available, defaulting to CPU.")
            device = "cpu"
    elif device == "cpu":
        if cuda_available:
            logger.warning("CUDA is available, but using CPU.")
    elif device.startswith("cuda") or device.startswith("gpu"):
        if not cuda_available:
            logger.warning("Specified CUDA device is not available, defaulting to CPU.")
            device = "cpu"
    else:
        logger.warning(f"Unknown device specified: {device}, defaulting to CPU.")
        device = "cpu"

    return device
