#!/usr/bin/env python

import base64
import logging
import os
from ctypes import CDLL, byref, c_int, create_string_buffer
from io import BytesIO
from typing import Any, Optional, Union

import click
from PIL import Image, ImageDraw

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AusPostError(Exception):
    """Base exception class for Australia Post barcode generation errors."""

    pass


class InvalidFCCError(AusPostError):
    """Raised when an invalid FCC value is provided."""

    pass


class InvalidDPIDError(AusPostError):
    """Raised when an invalid DPID value is provided."""

    pass


def build_barcode(
    fcc_value: str, dpid_value: Union[str, int], customer_value: Optional[str] = None
) -> str:
    """
    Builds an Australia Post barcode based on the provided values.

    Args:
        fcc_value: The FCC (Format Control Code) value. Must be one of "11", "52",
            or "67".
        dpid_value: The DPID (Delivery Point Identifier) value. Must be 8 digits.
        customer_value: Optional customer value. If provided, must be a string.

    Returns:
        str: The generated barcode as a string.

    Raises:
        InvalidFCCError: If the FCC value is not supported.
        InvalidDPIDError: If the DPID value is not 8 digits.
        AusPostError: For other barcode generation errors.
    """
    fcc_values = ["11", "52", "67"]
    if str(fcc_value) not in fcc_values:
        raise InvalidFCCError(
            f"FCC [{fcc_value}] is not a supported Australia Post FCC type."
        )

    dpid_str = str(dpid_value)
    if len(dpid_str) != 8 or not dpid_str.isdigit():
        raise InvalidDPIDError("DPID must be 8 digits long.")

    try:
        aus_post = CDLL(os.path.join(os.path.dirname(__file__), "_c", "auspost.so"))
        barcode = create_string_buffer(b"\x01" * 67)
        fcc = create_string_buffer(b"\000" * 2)
        fcc.value = str(fcc_value).encode("ascii")  # Use ASCII for FCC
        dpid = create_string_buffer(b"\000" * 8)
        dpid.value = dpid_str.encode("ascii")  # Use ASCII for DPID
        customer = create_string_buffer(b"\000" * 10)

        if customer_value is not None:
            customer.value = str(customer_value).encode(
                "ascii"
            )  # Use ASCII for customer value

        length = c_int()
        aus_post.BuildBarcode(fcc, dpid, customer, barcode, byref(length))

        # Get the raw bytes up to the length specified by the C function
        raw_bytes = barcode.raw[: length.value]
        # Convert to string, treating each byte as a character
        return "".join(chr(b) for b in raw_bytes)
    except Exception as e:
        logger.error(f"Error generating barcode: {str(e)}")
        raise AusPostError(f"Failed to generate barcode: {str(e)}") from e


def write_barcode_to_image(barcode: str) -> Image.Image:
    """
    Creates a PIL Image object containing the barcode.

    Args:
        barcode: The barcode string to render.

    Returns:
        Image.Image: A PIL Image object containing the rendered barcode.
    """
    h_padding = 20
    x_padding = 60
    tad_height = 42
    bar_width = 5
    bar_qty = len(barcode)
    total_height = h_padding * 2 + tad_height
    total_width = x_padding * 2 + bar_width * 2 * bar_qty

    # Create image with explicit white background
    img = Image.new("RGB", (total_width, total_height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    line_types = {"0": (0, 0), "1": (0, 16), "2": (16, 0), "3": (16, 16)}

    for i in range(bar_qty):
        h_start = x_padding + i * bar_width * 2
        offset_t, offset_b = line_types.get(barcode[i], (0, 0))
        d.line(
            (h_start, h_padding + offset_t)
            + (h_start, total_height - h_padding - offset_b),
            fill=(0, 0, 0),  # Black color for bars
            width=bar_width,
        )

    return img


def write_barcode_to_image_file(barcode: str, out_file: str, **kwargs: Any) -> None:
    """
    Saves the barcode to an image file.

    Args:
        barcode: The barcode string to render.
        out_file: Path where the image should be saved.
        **kwargs: Additional arguments passed to PIL.Image.save()
    """
    try:
        print(f"Writing barcode to image file: {out_file}")
        img = write_barcode_to_image(barcode)
        # Use consistent PNG save settings
        save_kwargs: dict[str, Any] = {
            "format": "PNG",
            "optimize": False,  # Disable optimization for consistency
            "compress_level": 9,  # Maximum compression
            "dpi": (300, 300),  # Fixed DPI
        }
        save_kwargs.update(kwargs)
        img.save(out_file, **save_kwargs)
        print(f"Barcode successfully saved to {out_file}")
        logger.info(f"Barcode successfully saved to {out_file}")
    except Exception as e:
        logger.error(f"Error saving barcode to file: {str(e)}")
        raise AusPostError(f"Failed to save barcode to file: {str(e)}") from e


def write_barcode_to_image_base64(barcode: str) -> str:
    """
    Converts the barcode to a base64-encoded JPEG image.

    Args:
        barcode: The barcode string to render.

    Returns:
        str: Base64-encoded JPEG image data.
    """
    try:
        img = write_barcode_to_image(barcode)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error converting barcode to base64: {str(e)}")
        raise AusPostError(f"Failed to convert barcode to base64: {str(e)}") from e


@click.command()
@click.option(
    "--fcc",
    prompt="Enter the FCC code",
    type=click.Choice(["11", "52", "67"]),
    required=True,
    help="Format Control Code (11, 52, or 67)",
)
@click.option(
    "--dpid",
    prompt="Enter the DPID value",
    required=True,
    type=click.IntRange(10000000, 99999999),
    help="8-digit Delivery Point Identifier",
)
@click.option(
    "--cust-no",
    prompt="Enter the customer value if required",
    default="",
    help="Optional customer number",
)
@click.option(
    "--save-to",
    prompt="Save the image location and name",
    required=True,
    help="Path where the barcode image should be saved",
)
def write_image(fcc: str, dpid: int, cust_no: str, save_to: str) -> None:
    """
    CLI command to generate and save an Australia Post barcode.

    Args:
        fcc: Format Control Code
        dpid: Delivery Point Identifier
        cust_no: Customer number (optional)
        save_to: Output file path
    """
    try:
        barcode = build_barcode(fcc, dpid, cust_no if cust_no else None)
        write_barcode_to_image_file(barcode, save_to, dpi=(300, 300))
    except AusPostError as e:
        logger.error(f"Error generating barcode: {str(e)}")
        raise click.ClickException(str(e)) from e


if __name__ == "__main__":
    write_image()
