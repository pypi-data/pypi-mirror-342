"""
A Python module written in C for fast parsing of genomic files and genomic
context analysis. With the classes it provides you can easily parse GTF and
FASTA files, and perform various operations on them. The module is written in C
for speed and memory efficiency, and is meant to be used in bioinformatics
applications.
"""

from __future__ import annotations
from collections.abc import Sequence, Iterable, Callable
from typing import Iterator, Literal, Self, overload, Any, TextIO, Mapping, Iterable

class GtfDict(Mapping[str, Any]):
    """
    A mapping object that is guaranteed to have all the necessary keys as
    specified per the GTF specification. You can access those keys via the
    attributes, or by using the mapping interface. With the couple of methods
    provided, you can easily compare, check for overlaps, containment, and more.
    """

    seqname: str | None
    """The name of the sequence being annotated"""
    source: str | None
    """Where this annotation comes from"""
    feature: str | None
    """What this annotation is meant to represent"""
    start: int | None
    """The start nt"""
    end: int | None
    """The end nt"""
    score: float | None
    """A score associated with the sequence"""
    reverse: bool | None
    """On which strand the sequence is located"""
    frame: int | None
    """Indicates which base of the feature is the first base of a codon"""
    @overload
    def __init__(
        self,
        seqname: str | None = None,
        source: str | None = None,
        feature: str | None = None,
        start: int | None = None,
        end: int | None = None,
        score: float | None = None,
        reverse: bool | None = None,
        frame: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Creates a new GtfDict instance. Additional provided keyword arguments
        will be added to the GtfDict.

        Args:
            seqname (str | None, optional): The name of the sequence being annotated. Defaults to None.
            source (str | None, optional): Where this annotation comes from. Defaults to None.
            feature (str | None, optional): What this annotation is meant to represent. Defaults to None.
            start (int | None, optional): The start nt. Defaults to None.
            end (int | None, optional): The end nt. Defaults to None.
            score (float | None, optional): A score associated with the sequence. Usually left empty. Defaults to None.
            reverse (bool | None, optional): On which strand the sequence is located. Defaults to None.
            frame (int | None, optional): Indicates which base of the feature is the first base of a codon. Defaults to None.
        """
        ...

    @overload
    def __init__(self, toConvert: Mapping[str, Any]) -> None:
        """Creates a new GtfDict instance from a provided mapping.
        The mapping must contain all necessary keys as specified per the GTF
        specification.

        Args:
            toConvert (Mapping): The mapping to use for the GtfDict
        """
        ...

    def __eq__(self, check: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks seqname, feature, start, end and reverse

        Args:
            check (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether the objects are equal
        """
        ...

    def __ne__(self, check: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks seqname, feature, start, end and reverse

        Args:
            check (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether the objects are not equal
        """
        ...

    def __lt__(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks if self is before other

        Args:
            other (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether self is before other
        """
        ...

    def __le__(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks if self is mostly before other with a possible 1 nt overlap

        Args:
            other (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether self is mostly before other with a possible 1 nt overlap
        """
        ...

    def __gt__(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks if self is after other

        Args:
            other (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether self is after other
        """
        ...

    def __ge__(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Checks if self is mostly after other with a possible 1 nt overlap

        Args:
            other (GtfDict | Mapping[str, Any]): The object to compare to

        Returns:
            bool: Whether self is mostly after other with a possible 1 nt overlap
        """
        ...

    def overlaps(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Returns true if the provided entry's sequence overlaps with this.
        seqname must equal for both, and reverse must also equal or be
        None in either sequence

        Args:
            other (GtfDict | Mapping[str, Any]): The sequence to check for overlap

        Returns:
            bool: Whether the sequences overlap
        """
        ...

    def contains(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Returns true if sequence's sequence is inside the other's sequence's
        sequence. seqname must equal for both entries, and reverse must also equal
        or be None in either entry

        Args:
            other (GtfDict | Mapping[str, Any]): The sequence to check for containment

        Returns:
            bool: Whether the sequence contains the other sequence
        """
        ...

    def __contains__(self, other: "GtfDict" | Mapping[str, Any]) -> bool:
        """Returns true if sequence's sequence is inside the other's sequence's
        sequence. seqname must equal for both entries, and reverse must also equal
        or be None in either entry

        Args:
            other (GtfDict | Mapping[str, Any]): The sequence to check for containment

        Returns:
            bool: Whether the sequence contains the other sequence
        """
        ...

    def __len__(self) -> int:
        """Returns the length of the sequence

        Returns:
            int: The length of the sequence
        """
        ...

    def __str__(self) -> str:
        """Returns GTF representation of the sequence

        Returns:
            str: A valid GTF entry
        """
        ...

    def keys(self) -> list[str]:
        """Returns the keys of the GtfDict

        Returns:
            list[str]: The keys of the GtfDict
        """
        ...

    def values(self) -> list[Any]:
        """Returns the values of the GtfDict

        Returns:
            list[Any]: The values of the GtfDict
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """Returns the value of the provided key

        Args:
            key (str): The key to get the value for

        Returns:
            Any: The value of the key
        """
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        """Sets the value of the provided key

        Args:
            key (str): The key to set the value for
            value (Any): The value to set
        """
        ...

    def __delitem__(self, key: str) -> None:
        """Deletes the provided key

        Args:
            key (str): The key to delete
        """
        ...

    def __iter__(self) -> Iterator[str]:
        """Returns an iterable of the GtfDict

        Returns:
            Iterator[str]: An iterator of the GtfDict
        """
        ...

    def pop(self, key: str) -> Any:
        """Removes the key and returns the value

        Args:
            key (str): The key to remove

        Returns:
            Any: The value of the key
        """
        ...

    def get(self, key: str, default: Any = None) -> Any:
        """Returns the value of the key or the default value if the key is not
        found

        Args:
            key (str): The key to get the value for
            default (Any, optional): The default value to return. Defaults to None.

        Returns:
            Any: The value of the key or the default value
        """
        ...

    def items(self) -> list[tuple[str, Any]]:
        """Returns the items of the GtfDict

        Returns:
            list[tuple[str, Any]]: The items of the GtfDict
        """
        ...

    def update(self, other: "GtfDict" | Mapping[str, Any]) -> None:
        """Updates the GtfDict with the provided dict

        Args:
            other (GtfDict | Mapping[str, Any]): The dict to update with
        """
        ...

    def __hash__(self) -> int:
        """Returns a hash of the GtfDict

        Raises:
            TypeError: If one of the stored values is unhashable, this can only happen with attributes

        Returns:
            int: A hash of the GtfDict
        """
        ...

    def __repr__(self) -> str:
        """Returns a representation of the GtfDict
        This is equivalent to str(dict(self))

        Returns:
            str: A representation of the GtfDict
        """
        ...

class GeneList(list[GtfDict]):
    """A subclass of a list that holds only GtfDicts.
    It's worth noting that the list can be converted to a set.
    """

    @overload
    def __init__(self, *args: GtfDict) -> None:
        """Creates a GeneList from provided GtfDicts"""
        ...

    @overload
    def __init__(self, obj: Sequence[GtfDict]) -> None:
        """Converts a list to a GeneList."""
        ...

    @overload
    def __init__(self, obj: Iterator[GtfDict]) -> None:
        """Creates a GeneList from an iterator of GtfDicts"""
        ...

    def find_closest_bound(self, sequence: GtfDict) -> GtfDict | None:
        """Finds the entry that most closely bounds the provided sequence.
        The entry with the closest bound is the one that has the smallest
        hausdorff distance to the provided sequence.

        Args:
            sequence (GtfDict): The sequence to find the closest bounding entry for

        Returns:
            GtfDict | None: The entry that most closely bounds the provided sequence
        """
        ...

    def __str__(self) -> str:
        """Returns a GTF file representation of the GeneList

        Returns:
            str: A GTF file representation of the GeneList
        """
        ...

    def sq_split(self) -> dict[str | None, "GeneList"]:
        """Splits the GeneList into separate GeneLists based on seqname.
        This is very useful for optimizing operations on the GeneList.

        Returns:
            dict[str | None, GeneList]: A dictionary containing GeneLists split by seqname
        """
        ...

    def find(
        self,
        *args: Callable[[GtfDict], bool],
        **kwargs: Any | Callable[[Any], bool],
    ) -> "GeneList":
        """Finds all entries that match the provided conditions
        You can provide three types of arguments:
        1. A function that takes a GtfDict and returns a boolean
        2. A keyword argument that will be used to filter the GeneList
        3. A keyword argument that is a function that takes an a value held under the given key and returns a boolean

        Returns:
            GeneList: A GeneList containing all entries that match the provided conditions
        """
        ...

    def column(self, key: str, pad: bool = True) -> list[Any]:
        """Returns a list of values for the provided key

        Args:
            key (str): The key to get the values for
            pad (bool, optional): Whether to pad the list with None values for missing keys. Defaults to True. If False, missing keys will cause an exception.

        Returns:
            list[Any]: A list of values for the provided key
        """
        ...

    def __iadd__(self, value: "GeneList") -> Self: ...
    @overload
    def __add__(self, value: "GeneList") -> "GeneList": ...
    @overload
    def __add__(self, value: Sequence[Any]) -> list[Any]: ...

class GtfFile(Iterable[GtfDict]):
    """
    An iterable GTF parser. It reads a GTF file and returns GtfDicts.
    Once entered, it spawns a GtfReader instance that can be iterated over.
    """

    def __init__(self, filename: str) -> None:
        """Creates a new GtfFile instance

        Args:
            filename (str): The name of the file to read
        """
        ...

    def __iter__(self) -> "GtfReader":
        """Prepares the reader for iteration and returns this instance"""
        ...

    def __enter__(self) -> "GtfFile": ...
    def __exit__(self, *args, **kwargs) -> None: ...

class GtfReader(Iterator[GtfDict]):
    """
    A reader instance that iteratively returns GtfDicts from a file object.
    It can be used standalone, but it's usually spawned by a GtfFile instance.
    Please note that standalone instances of GtfReader parse slower than those
    spawned by GtfFile due to limits imposed by the Python layer.
    """

    def __init__(self, file: TextIO) -> None:
        """Creates a new GtfReader instance

        Args:
            file (TextIO): The file object to read from
        """
        ...

    def __next__(self) -> GtfDict: ...

class FastaBuff(Sequence[str]):
    """
    A class that holds a FASTA DNA sequence in an optimal binary format.
    Approximately twice as memory efficient than a string representation.
    It should function approximately the same as a string.
    """

    @overload
    def __init__(self, seq: str, RNA: bool = False) -> None:
        """Initializes the FastaBuff with the provided sequence. The sequence
        must be a valid FASTA sequence containing only IUPAC codes.

        Args:
            seq (str): A sequence of valid genetic IUPAC codes
            RNA (bool, optional): Whether the sequence is meant to represent an RNA sequence. Determines whether T or U is used. Defaults to False.
        """
        ...

    @overload
    def __init__(self, seq: bytes, RNA: bool = False) -> None:
        """Initializes the FastaBuff with a previous FastaBuff dump in form of
        bytes.

        Args:
            seq (bytes): The bytes representation of the sequence
            RNA (bool, optional): Whether the sequence is meant to represent an RNA sequence. Determines whether T or U is used. Defaults to False.
        """
        ...

    @overload
    def __init__(self, seq: TextIO, RNA: bool = False) -> None:
        """Initializes the FastaBuff with a file object containing a FASTA
        sequence.

        Args:
            seq (TextIO): The file object containing the FASTA sequence
            RNA (bool, optional): Whether the sequence is meant to represent an RNA sequence. Determines whether T or U is used. Defaults to False.
        """
        ...

    def __str__(self) -> str:
        """Returns the stored sequence

        Returns:
            str: The stored sequence
        """
        ...

    def __repr__(self) -> str: ...
    def __eq__(self, value: Any) -> bool: ...
    def __ne__(self, value: Any) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int | slice) -> str: ...
    def __setitem__(self, key: int, value: str) -> None: ...
    def __contains__(self, seq: str | "FastaBuff") -> bool: ...
    def dump(self) -> bytes:
        """Returns the bytes representation of the buffer.
        This operation discards some information, leaving only a binary
        representation of the sequence. The exact length of the sequence is
        lost, leading to a potential gap(. character) being additionally
        encoded, but the sequence is still valid.

        Returns:
            bytes: The binary representation of the sequence
        """
        ...

    def index(self, seq: str | "FastaBuff", start: int = 0) -> int | None:
        """Returns the index of the provided sequence

        Args:
            seq (str | FastaBuff): The sequence to find
            start (int, optional): The index to start searching from. Defaults to 0.

        Returns:
            int | None: The index of the sequence or None if not found
        """
        ...

    def count(self, seq: str | "FastaBuff") -> int:
        """Counts the occurrences of the provided sequence

        Args:
            seq (str | FastaBuff): The sequence to count

        Returns:
            int: The number of occurrences of the sequence
        """
        ...

    def get_annotated(self, entry: GtfDict | Mapping) -> str:
        """Returns the annotated sequence of the provided entry

        Args:
            entry (GtfDict): The annotation to apply

        Returns:
            str: The annotated sequence
        """
        ...

    def find(self, seq: str | "FastaBuff") -> list[int]:
        """Finds all occurrences of the provided sequence

        Args:
            seq (str | FastaBuff): The sequence to find

        Returns:
            list[int]: A list of indexes where the sequence was found
        """
        ...

@overload
def parseFASTA(
    file: str | TextIO, binary: Literal[False] = True, echo: TextIO | None = None
) -> list[tuple[str, str]]: ...
def parseFASTA(
    file: str | TextIO, binary: Literal[True] = True, echo: TextIO | None = None
) -> list[tuple[str, FastaBuff]]:
    """Parses raw FASTA data and returns a list of all entries. You may either
    pass raw file data as file, or a file object.

    Args:
        file (str | TextIO): The file to parse
        binary (bool): Whether to parse the sequence as a FastaBuff. Defaults to True.
        echo (TextIO | None, optional): The IO to output echo into. Defaults to None.

    Returns:
        list[tuple[str, FastaBuff | str]]: A list containing title, sequence tuples
    """
    ...

def parseGTF(file: str | TextIO, echo: TextIO | None = None) -> GeneList:
    """Parses raw GTF, GFF2 and GFF3 data and returns a list containing parsed
    GtfDicts. You may either pass raw file data as file, or a file object.

    Args:
        file (str | TextIO): The file to parse
        echo (TextIO | None, optional): The IO to output echo into. Defaults to None.

    Returns:
        GeneList: A list containing parsed GtfDicts
    """
    ...
