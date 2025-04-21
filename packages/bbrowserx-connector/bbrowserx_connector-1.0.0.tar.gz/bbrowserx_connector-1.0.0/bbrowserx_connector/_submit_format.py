from enum import Enum
from pydantic import BaseModel


class SubmitType(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class Keys(Enum):
    ANNDATA = "anndata"
    MATRIX = "matrix"
    BARCODES = "barcodes"
    FEEATURES = "features"


class Formats(Enum):
    H5AD = "H5AD"
    RDS = "RDS"
    MTX_10X = "MTX_10X"
    H5_10X = "H5_10X"
    TSV = "TSV"
    PARSE_BIOSCIENCE = "PARSE_BIOSCIENCE"


class SubmitFormat(BaseModel):
    name: str

    def _parse_path(self, key, value):
        return {
            "key": key,
            "value": value
        }


class OneFile(SubmitFormat):
    file_path: str

    def _parse(self, _format: str, key: str = Keys.MATRIX.value):
        return {
            "name": self.name,
            "submission_type": SubmitType.SINGLE.value,
            "files": [
                self._parse_path(key, self.file_path)
            ],
            "format": _format,
        }


class MultipleFiles(SubmitFormat):
    matrix_path: str
    barcodes_path: str
    features_path: str

    def _parse(self, _format: str):
        return {
            "name": self.name,
            "submission_type": SubmitType.MULTIPLE.value,
            "files": [
                self._parse_path(Keys.MATRIX.value, self.matrix_path),
                self._parse_path(Keys.BARCODES.value, self.barcodes_path),
                self._parse_path(Keys.FEEATURES.value, self.features_path),
            ],
            "format": _format,
        }


class H5ADFormat(OneFile):
    def parse(self):
        return self._parse(_format=Formats.H5AD.value, key=Keys.ANNDATA.value)


class RDSFormat(OneFile):
    def parse(self):
        return self._parse(_format=Formats.RDS.value)


class H510XFormat(OneFile):
    def parse(self):
        return self._parse(_format=Formats.H5_10X.value)


class TSVFormat(OneFile):
    def parse(self):
        return self._parse(_format=Formats.TSV.value)


class MTX10XFormat(MultipleFiles):
    def parse(self):
        return self._parse(_format=Formats.MTX_10X.value)


class ParseBioFormat(MultipleFiles):
    def parse(self):
        return self._parse(_format=Formats.PARSE_BIOSCIENCE.value)
