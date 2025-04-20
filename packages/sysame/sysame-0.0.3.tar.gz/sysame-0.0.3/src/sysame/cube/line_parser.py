# -*- coding: utf-8 -*-
"""
Module for parsing Cube linefile into structured dataframes.
"""

##### IMPORTS #####
# Standard imports
import re
import ast
from collections import Counter
from warnings import warn
from copy import deepcopy
from typing import Dict, List, Union, Optional, Any, Tuple

# Third party imports
import pandas as pd  # type: ignore

# Local imports

##### CONSTANTS #####


##### CLASSES #####
class Node:
    """
    Simple node class for representing network nodes.

    Parameters
    ----------
    string : str or int
        String representation of the node.
    **kwargs : dict
        Additional attributes to be assigned to the node.

    Attributes
    ----------
    id : int
        Node identifier, absolute value from string.
    stopping : bool
        Whether the node is a stopping point.
    _string : str
        Internal storage of the original string representation.
    """

    def __init__(self, string: Union[str, int], **kwargs: Any) -> None:
        self._string = str(string)
        self.id = abs(int(self._string.strip()))
        self.__dict__.update(**kwargs)

        if self._string.strip().startswith("-"):
            self.stopping = False
        else:
            self.stopping = True

    @property
    def attrs(self) -> Dict[str, Any]:
        """
        Returns a dictionary with user-defined attributes.

        Returns
        -------
        Dict[str, Any]
            Dictionary of custom attributes excluding internal ones.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if "_" not in k and "id" != k and "ID" != k and "stopping" != k
        }

    def __repr__(self) -> str:
        """
        Object's summary representation.

        Returns
        -------
        str
            String representation of the node.
        """
        return f"{'-' if not self.stopping else ''}{self.id}, {self.attrs}"

    def __str__(
        self,
        node_attrs: Optional[List[str]] = None,
        exclude_node_attrs: Optional[List[str]] = None,
    ) -> str:
        """
        String representation of the node.

        Parameters
        ----------
        node_attrs : list of str, optional
            List of node attributes to include.
        exclude_node_attrs : list of str, optional
            List of node attributes to omit.

        Returns
        -------
        str
            String representation of the node with selected attributes.
        """
        txt_node = f"{'-' if not self.stopping else ''}{self.id}"

        if self.attrs:
            if node_attrs:
                attrs = {k: v for k, v in self.attrs.items() if k in node_attrs}
            else:
                attrs = self.attrs

            if exclude_node_attrs:
                attrs = {k: v for k, v in attrs.items() if k not in exclude_node_attrs}

            formatted_attrs = [f"{k}={v}" for k, v in attrs.items()]

            txt_attrs = ", ".join(formatted_attrs)

            if txt_attrs:
                txt_node = ", ".join([txt_node, txt_attrs])

        return txt_node

    def copy(self) -> "Node":
        """
        Create a deep copy of the node.

        Returns
        -------
        Node
            A new instance that is a deep copy of this node.
        """
        return deepcopy(self)


class Line:
    """
    Simple line class representing a sequence of nodes.

    A line is a sequence of nodes with its own properties.

    Parameters
    ----------
    nodes : list of Node
        List of node objects that form the line.
    **kwargs : dict
        Additional attributes to be assigned to the line.

    Attributes
    ----------
    nodes : list of Node
        List of nodes that form the line.
    name : str
        Name of the line (set via kwargs).
    unquoted : list of str
        Class variable that defines values that should not be quoted.
    NodeLabel : str
        Label to identify nodes in string representation.
    """

    # Class variables
    unquoted = ["T", "F"]
    NodeLabel = "N"  # Or 'NODE'

    def __init__(self, nodes: List[Node], **kwargs: Any) -> None:
        """
        Initialize a line object.

        Parameters
        ----------
        nodes : List[Node]
            List of node objects that form the line.
        **kwargs : dict
            Additional attributes to be assigned to the line.
        """
        self.nodes = nodes  # a list of node objects
        self.name = kwargs.get("NAME", "")  # Use NAME if present, empty string if not

        # Remove NAME from kwargs to avoid duplication
        if "NAME" in kwargs:
            del kwargs["NAME"]

        self.__dict__.update(**kwargs)

    @property
    def attrs(self) -> Dict[str, Any]:
        """
        Returns a dictionary with user-defined attributes.

        Returns
        -------
        Dict[str, Any]
            Dictionary of line attributes excluding nodes and internal ones.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if "nodes" != k and not k.startswith("_")
        }

    @property
    def stops(self) -> List[Node]:
        """
        Returns a list of the nodes that are actual stops.

        Returns
        -------
        List[Node]
            List of nodes marked as stopping points.
        """
        return [node for node in self.nodes if node.stopping]

    def __repr__(self) -> str:
        """
        Object's summary representation.

        Returns
        -------
        str
            String summary of the line including node count and attributes.
        """
        txt = (
            f"Line with {len(self.nodes)} nodes (of which {len(self.stops)} are stops)."
        )
        txt += f"\n{self.attrs}"
        return txt

    def __str__(
        self,
        line_attrs: Optional[List[str]] = None,
        exclude_line_attrs: Optional[List[str]] = None,
        node_attrs: Optional[List[str]] = None,
        exclude_node_attrs: Optional[List[str]] = None,
    ) -> str:
        """
        String representation of the line.

        Parameters
        ----------
        line_attrs : list of str, optional
            List of line attributes to include.
        exclude_line_attrs : list of str, optional
            List of line attributes to omit.
        node_attrs : list of str, optional
            List of node attributes to include.
        exclude_node_attrs : list of str, optional
            List of node attributes to omit.

        Returns
        -------
        str
            String representation of the line with selected attributes.
        """
        # String attributes are quoted, with exceptions
        formatted_attrs = []

        if line_attrs:
            l_attrs = {k: v for k, v in self.attrs.items() if k in line_attrs}
        else:
            l_attrs = self.attrs

        if exclude_line_attrs:
            l_attrs = {k: v for k, v in l_attrs.items() if k not in exclude_line_attrs}

        for k, v in l_attrs.items():
            if isinstance(v, str) and v not in self.unquoted:
                f = repr(v)  # This will enclose in the right quotes
            else:
                f = v
            formatted_attrs.append(f"{k}={f}")

        txt_attrs = ", ".join(formatted_attrs)

        # First nodes, and nodes after attributes, are labeled
        formatted_nodes = []
        first_node = True
        for n in self.nodes:
            n_str = (
                n.__str__()
                if node_attrs is None and exclude_node_attrs is None
                else n.__str__(node_attrs, exclude_node_attrs)
            )
            if first_node:
                formatted_nodes.append(f"{self.NodeLabel}={n_str}")
                first_node = False
            else:
                formatted_nodes.append(n_str)

            if node_attrs:
                n_attrs = {k: v for k, v in n.attrs.items() if k in node_attrs}
            else:
                n_attrs = n.attrs

            if exclude_node_attrs:
                n_attrs = {
                    k: v for k, v in n_attrs.items() if k not in exclude_node_attrs
                }

            if n_attrs:
                # node has attributes printed, reset the flag:
                first_node = True

        txt_nodes = ", ".join(formatted_nodes)

        txt = f"LINE {', '.join([txt_attrs, txt_nodes])}"
        txt = txt.replace(", TF=", ",\n\tTF=")  # prettify

        return txt

    def is_node(self, n: Union[Node, int]) -> bool:
        """
        Returns True if n is one of the line's nodes.

        Parameters
        ----------
        n : Node or int
            Node or node ID to check.

        Returns
        -------
        bool
            True if the node is part of the line, False otherwise.
        """
        if isinstance(n, Node):
            node_id = n.id
        else:
            node_id = n
        return node_id in [n.id for n in self.nodes]

    def is_stop(self, n: Union[Node, int]) -> bool:
        """
        Returns True if line stops at n.

        Parameters
        ----------
        n : Node or int
            Node or node ID to check.

        Returns
        -------
        bool
            True if the node is a stopping point on the line, False otherwise.
        """
        if isinstance(n, Node):
            node_id = n.id
        else:
            node_id = n
        return node_id in [n.id for n in self.stops]

    @property
    def stop_seq(self, sep: str = "_") -> str:
        """
        Returns a concatenation of line's stops.

        Parameters
        ----------
        sep : str, default="_"
            Separator to use between stop IDs.

        Returns
        -------
        str
            Concatenated string of stop IDs.
        """
        return sep.join([str(n.id) for n in self.stops])

    @staticmethod
    def from_string(string: str, potential_seps: Optional[List[str]] = None) -> "Line":
        """
        Parse a string representation into a line object.

        Parameters
        ----------
        string : str
            String to parse.
        potential_seps : Optional[List[str]], default=None
            List of potential separators to detect.

        Returns
        -------
        Line
            Parsed line object.

        Raises
        ------
        AssertionError
            If invalid node declarations are found.
        """
        if potential_seps is None:
            potential_seps = [" ", "\t", ","]

        # Guess the separator as the most common of potential separators:
        formatted = re.sub(r"[=,][\s\n\t]+", ",", string)  # clean
        # Accounts for multiple separators.
        seps_count = [len(re.findall(f"{sep}+", formatted)) for sep in potential_seps]
        sep = potential_seps[seps_count.index(max(seps_count))]

        # Clean:
        string = string.replace("\n", "")
        string = string.replace("\x1a", "")  # EOF windows >_<
        string = re.sub(r"\ALINE\s+", "", string)
        string = re.sub(r"[\s,]*\Z", "", string)
        if sep == " ":
            string = re.sub(f"{sep}*={sep}*", "=", string)

        # src for this amazing magic:
        # https://stackoverflow.com/a/16710842/2802352
        parts_pat = (
            f"""(?:["](?:\\.|[^"])*["]|['](?:\\.|[^'])*[']|[^{sep}"]|[^{sep}'])+"""
        )
        parts = re.findall(parts_pat, string)

        node_label_pat = r"\A\s*N(?:ODES)?\b"

        nodes = []
        line_attrs = {}
        node_attrs = {}

        n = None
        attrs_section = True

        while parts:
            p = parts.pop(0)

            # Clean:
            p = re.sub(r"[\s,]*\Z", "", p)
            k, _, v = [part.strip() for part in p.partition("=")]

            try:
                # For numbers
                v = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                v = str(v)

            if bool(re.search(f"{node_label_pat}\s*=\s*", p)):
                attrs_section = False

            if attrs_section:
                if k and v:
                    line_attrs.update({k: v})

            else:
                # Replace the node label
                p = re.sub(f"{node_label_pat}\s*=\s*", "", p)

                if "=" in p:
                    if bool(re.search(f"{node_label_pat}", k)):
                        msg = f'Node declaration in attribute "{k}: {v}"'
                        msg += f"in node {n}, line:\n{line_attrs}"
                        raise AssertionError(msg)

                    # Still has '=', must be an attribute:
                    if k and v:
                        node_attrs.update({k: v})

                else:
                    # It is a node:
                    if n:
                        # Add the previous node, with the attrs read so far
                        nodes.append(Node(n, **node_attrs))
                        node_attrs = {}  # reset

                    n = p  # Set the new node for future attrs to be read

        # Add the last node (if it is not empty)
        if n:
            nodes.append(Node(n, **node_attrs))

        ln = Line(nodes, **line_attrs)

        return ln

    def copy(self) -> "Line":
        """
        Create a deep copy of the line.

        Returns
        -------
        Line
            A new instance that is a deep copy of this line.
        """
        return deepcopy(self)


class LineFile:
    """
    Class representing a file of lines.

    A LineFile is a collection of line objects and comments.

    Parameters
    ----------
    content : list of (Line or str), optional
        List of line objects and comment strings.

    Attributes
    ----------
    content : list of (Line or str)
        List containing line objects and comment strings.
    """

    def __init__(self, content: Optional[List[Union[Line, str]]] = None) -> None:
        if content:
            self.content = content
        else:
            self.content = []

    def _warn_if_duplicates(self, additional_info: Optional[str] = None) -> None:
        """
        Raises a warning if there are lines with duplicated NAME in the LineFile.

        Parameters
        ----------
        additional_info : str, optional
            Additional information to include in the warning message.
        """
        if not self.name_unique:
            msg = "Several lines have the same NAME."
            if additional_info:
                msg += f" {additional_info}"
            warn(msg)

    @property
    def content_duplicates_renamed(self) -> List[Union[Line, str]]:
        """
        Returns the LineFile's content with duplicated NAMEs renamed.

        Returns
        -------
        list
            Copy of content with renamed lines.
        """
        renamed_content = []
        counts = Counter(self.line_names)
        suffixes = {k: 1 for k in counts}

        for x in self.content:
            if isinstance(x, Line):
                name = str(x.name)  # Treats int = str
                if counts[name] > 1:
                    x = x.copy()
                    newname = f"{name}_{suffixes[name]}"
                    suffixes[name] += 1
                    x.name = newname
            renamed_content.append(x)

        # re-test (recursive)
        ren_sys = LineFile(renamed_content)
        if not ren_sys.name_unique:
            renamed_content = ren_sys.content_duplicates_renamed

        return renamed_content

    def rename_duplicates(self) -> None:
        """
        Changes the LineFile's content to avoid lines with duplicated NAMEs.
        """
        self.content = self.content_duplicates_renamed

    @property
    def name_unique(self) -> bool:
        """
        Returns True if lines' property "NAME" is a unique identifier.

        Returns
        -------
        bool
            True if all line names are unique, False otherwise.
        """
        names = self.line_names
        if not names:
            return True
        _, count = Counter(names).most_common(1)[0]
        return not count > 1

    @property
    def comments(self) -> List[str]:
        """
        Returns the list of comments in the file.

        Returns
        -------
        list of str
            All comments in the file.
        """
        return [x for x in self.content if isinstance(x, str)]

    @property
    def lines(self) -> Dict[str, Line]:
        """
        Returns a dictionary of lines by NAME.

        Returns
        -------
        Dict[str, Line]
            Dictionary of lines with NAME as key.
        """
        msg = "Only the latest line is displayed for conflicting NAMEs."
        self._warn_if_duplicates(additional_info=msg)
        return {x.name: x for x in self.content if isinstance(x, Line)}

    @property
    def lines_duplicates_renamed(self) -> Dict[str, Line]:
        """
        Returns a dictionary of lines with duplicated NAMEs renamed.

        Returns
        -------
        Dict[str, Line]
            Dictionary of lines with NAME as key, duplicates renamed.
        """
        return {
            x.name: x for x in self.content_duplicates_renamed if isinstance(x, Line)
        }

    @property
    def line_names(self) -> List[str]:
        """
        Returns a list of line names as strings.

        Preserves order. May contain duplicates.

        Returns
        -------
        List[str]
            List of line names.
        """
        return [str(x.name) for x in self.content if isinstance(x, Line)]

    def __repr__(self) -> str:
        """
        Object's summary representation.

        Returns
        -------
        str
            String representation summarizing the LineFile.
        """
        self._warn_if_duplicates()
        # Using self.line_names avoids triggering further warnings:
        txt = f"LineFile with {len(self.line_names)} lines, "
        txt += f"and {len(self.comments)} comments."
        txt += "\nLines:\n"
        txt += ", ".join([str(k) for k in self.line_names])  # if int NAMEs
        txt += "\nComments:\n"
        txt += "\n".join(self.comments)
        return txt

    def __str__(
        self,
        sort: bool = False,
        comments: bool = True,
        rename_duplicates: bool = False,
        **kwargs: Any,
    ) -> str:
        """
        Representation as the file itself.

        Parameters
        ----------
        sort : bool, default=False
            If False, output is sorted with the same structure as input content.
            If True, comments are first, then all lines in NAME order.
        comments : bool, default=True
            Output comments only if True.
        rename_duplicates : bool, default=False
            Rename duplicated NAMEs if True.
        **kwargs : dict
            Additional keyword arguments to pass to the line.__str__ method.

        Returns
        -------
        str
            String representation of the LineFile.
        """
        if not rename_duplicates:
            self._warn_if_duplicates()

        if sort:
            lines = self.lines
            # Use only if there are duplicates. Makes code more compact:
            if rename_duplicates and not self.name_unique:
                lines = self.lines_duplicates_renamed

            # Use str() instead of .__str__() directly
            sorted_lines = [lines[ln].__str__(**kwargs) for ln in sorted(lines)]
            txt_lines = "\n".join(sorted_lines)

            if comments:
                txt_comments = "\n".join([c for c in self.comments])
                txt = "\n".join([txt_comments, txt_lines])
            else:
                txt = txt_lines

        else:
            content = self.content
            # Use only if there are duplicates. Makes code more compact:
            if rename_duplicates and not self.name_unique:
                content = self.content_duplicates_renamed

            if comments:
                txt_content = [
                    x.__str__(**kwargs) if not isinstance(x, str) else str(x)
                    for x in content
                ]
            else:
                txt_content = [
                    x.__str__(**kwargs) for x in content if not isinstance(x, str)
                ]

            txt = "\n".join(txt_content)

        return txt

    def copy(self) -> "LineFile":
        """
        Create a deep copy of the LineFile.

        Returns
        -------
        LineFile
            A new instance that is a deep copy of this LineFile.
        """
        return deepcopy(self)

    def save(
        self,
        path: str,
        sort: bool = False,
        comments: bool = True,
        node_attrs: Optional[List[str]] = None,
        exclude_node_attrs: Optional[List[str]] = None,
        line_attrs: Optional[List[str]] = None,
        exclude_line_attrs: Optional[List[str]] = None,
        rename_duplicates: bool = True,
    ) -> None:
        """
        Save the LineFile to a file.

        Parameters
        ----------
        path : str
            Path to the output file.
        sort : bool, default=False
            If True, sorts the output.
        comments : bool, default=True
            If True, includes comments in the output.
        node_attrs : list of str, optional
            List of node attributes to include.
        exclude_node_attrs : list of str, optional
            List of node attributes to omit.
        line_attrs : list of str, optional
            List of line attributes to include.
        exclude_line_attrs : list of str, optional
            List of line attributes to omit.
        rename_duplicates : bool, default=True
            If True, renames duplicate line names.
        """
        if not self.name_unique and rename_duplicates:
            msg = "Duplicated NAMES will be renamed."
            self._warn_if_duplicates(additional_info=msg)

        with open(path, "w", encoding="utf-8") as ofile:
            # Use the method directly instead of the str() built-in
            output = self.__str__(
                sort=sort,
                comments=comments,
                node_attrs=node_attrs,
                exclude_node_attrs=exclude_node_attrs,
                line_attrs=line_attrs,
                exclude_line_attrs=exclude_line_attrs,
                rename_duplicates=rename_duplicates,
            )
            ofile.write(output)

    def lines_by_attr(self, attr: str, val: Any) -> List[Line]:
        """
        Returns a list of lines having a specific value in an attribute.

        Parameters
        ----------
        attr : str
            Attribute name to check.
        val : Any
            Value to match.

        Returns
        -------
        List[Line]
            List of lines that match the criteria.
        """
        lines = [ln for ln in self.lines.values() if getattr(ln, attr) == val]
        return lines

    def lines_query(self, qry: str) -> List[Line]:
        """
        Returns a list of lines meeting a SQL-like query.

        This relies on pandas DataFrame query:
            https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.query.html

        Parameters
        ----------
        qry : str
            SQL-like query string.

        Returns
        -------
        List[Line]
            List of lines that match the query.
        """
        lns_names = self.df.query(qry)["NAME"].tolist()

        if lns_names:
            lns = [self.lines[n] for n in lns_names]
            return lns
        else:
            return []

    @property
    def df(self) -> pd.DataFrame:
        """
        Returns a dataframe with the attributes for each line.

        Returns
        -------
        pd.DataFrame
            DataFrame containing line attributes as columns.
        """
        # Assume lines start on 1:
        data = {i: ln.attrs for i, ln in enumerate(self.lines.values(), 1)}
        df = pd.DataFrame.from_records(data).T

        # stops and nodes are objects!
        additional_attrs = "stop_seq stops nodes".split()
        for attr in additional_attrs:
            df[attr] = [getattr(ln, attr) for ln in self.lines.values()]

        return df

    @staticmethod
    def _extract_blocks(
        string: str,
        block_pat: str = r"(?s)(?:(;.*?|\n\s*)\n|LINE\s+(.*?)(?=\n\s*LINE|\n\s*;|\Z))",
    ) -> List[Tuple[str, str]]:
        """
        Returns a list of tuples [(comment, line), (), ...] for each record.

        Parameters
        ----------
        string : str
            Input string to parse.
        block_pat : str, default regex pattern
            Regex pattern to extract blocks.

        Returns
        -------
        List[Tuple[str, str]]
            List of tuples containing (comment, line) pairs.
        """
        block_re = re.compile(block_pat)
        blocks = block_re.findall(string)
        return blocks

    @staticmethod
    def from_string(string: str) -> "LineFile":
        """
        Create a LineFile from a string.

        Parameters
        ----------
        string : str
            String representation of a line file.

        Returns
        -------
        LineFile
            Parsed LineFile object.
        """
        blocks = LineFile._extract_blocks(string)

        content: List[Union[str, Line]] = []
        for comment_txt, line_txt in blocks:
            if comment_txt:
                content.append(comment_txt)

            if line_txt:
                ln = Line.from_string(line_txt)
                content.append(ln)

        s = LineFile(content)

        return s

    @staticmethod
    def read_file(path: str) -> "LineFile":
        """
        Read a line file from disk.

        Parameters
        ----------
        path : str
            Path to the file.

        Returns
        -------
        LineFile
            Parsed LineFile object from the file.
        """
        with open(path, "r", encoding="utf-8") as ifile:
            content = ifile.read()

        s = LineFile.from_string(content)

        return s


##### FUNCTIONS #####
