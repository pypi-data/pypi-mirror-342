import zipfile
import os

from zeta.converter.base import BaseConverter, ConvertData
from zeta.utils.logging import zetaLogger
from zeta.sdk.asset import AssetUtils
from zeta.sdk.uid import generate_uid


class NoopConverter(BaseConverter):
    def extract(self) -> ConvertData:
        # Make the USDZ extract no-op.
        data = ConvertData()
        data.root_layer = self._filename
        data.usdz_asset = self._filename

        # Capture thumbnail
        thumbnail_path = os.path.join(self._tmp_path, f"{generate_uid()}.jpeg")
        if not self._capture_thumbnail(self._filename, thumbnail_path):
            zetaLogger.error("Failed to capture thumbnail")

        if AssetUtils.is_asset_file_valid(thumbnail_path):
            data.thumbnail_path = thumbnail_path

        return data

    def get_stage_path(self, asset_path) -> str:
        return self._filename


class UsdzConverter(BaseConverter):
    def _unzip_uszd(self, zip_file_path, extract_to_dir):
        # Ensure the extraction directory exists
        if not os.path.exists(extract_to_dir):
            os.makedirs(extract_to_dir)

        if zip_file_path in self._usdz_unziped:
            return

        # Extract the outer zip file
        print(f"Extracting nested zip file: {zip_file_path} to {extract_to_dir}, {self._usdz_unziped}")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to_dir)
            self._usdz_unziped.add(zip_file_path)

        # Walk through the extracted files to find nested zip files
        usdz_to_extract = set()
        for root, _, files in os.walk(extract_to_dir):
            for file in files:
                if file.endswith(".usdz"):
                    # Nested zip file found
                    nested_zip_path = os.path.join(root, file)
                    usdz_to_extract.add(nested_zip_path)

        for usdz_path in usdz_to_extract:
            self._unzip_uszd(usdz_path, extract_to_dir)


    def get_stage_path(self, asset_path) -> str:
        self._usdz_unziped = set()
        self._unzip_uszd(self._filename, asset_path)

        return self._filename


# if __name__ == "__main__":
#     converter = UsdzConverter(tmp_path=f"/tmp/{generate_uid()}",
#                               usdz_filename="/code/zeta/assets/usdz/honda-e.usdz")
#     update = converter.extract()
#     print(update.root_layer)
#     print(update.assets)