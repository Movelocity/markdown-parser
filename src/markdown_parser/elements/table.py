"""Table parser for markdown."""

import re
from typing import List, Optional, Tuple
from ..models import Table, TableRow, TableCell
from .text import parse_inline_elements
from ..regex_patterns import TABLE_SEPARATOR_PATTERN


def parse_table(lines: List[str], start_idx: int) -> Optional[Tuple[Table, int]]:
    """Parse a table starting from the given line index.
    
    Returns the table element and the index of the next line after the table.
    """
    if start_idx >= len(lines):
        return None
    
    # Use the existing table detection logic
    tables = locate_markdown_tables(lines[start_idx:])
    
    if not tables or tables[0][0] != 0:
        return None
    
    table_start, table_end = tables[0]
    table_lines = lines[start_idx:start_idx + table_end + 1]
    
    # Parse the table structure
    if len(table_lines) < 2:
        return None
    
    header_line = table_lines[0]
    separator_line = table_lines[1]
    data_lines = table_lines[2:] if len(table_lines) > 2 else []
    
    # Parse header
    header_cells = _parse_table_row(header_line)
    if not header_cells:
        return None
    
    # Parse alignments from separator
    alignments = _parse_alignments(separator_line)
    
    # Ensure alignments match header columns
    while len(alignments) < len(header_cells):
        alignments.append(None)
    
    # Create header row
    header = TableRow(cells=[
        TableCell(
            content=parse_inline_elements(cell),
            alignment=alignments[i] if i < len(alignments) else None
        )
        for i, cell in enumerate(header_cells)
    ])
    
    # Parse data rows
    rows = []
    for line in data_lines:
        cells = _parse_table_row(line)
        if cells:
            # Pad with empty cells if needed
            while len(cells) < len(header_cells):
                cells.append('')
            
            row = TableRow(cells=[
                TableCell(
                    content=parse_inline_elements(cell),
                    alignment=alignments[i] if i < len(alignments) else None
                )
                for i, cell in enumerate(cells[:len(header_cells)])
            ])
            rows.append(row)
    
    table = Table(
        header=header,
        alignments=alignments[:len(header_cells)],
        rows=rows
    )
    
    return table, start_idx + table_end + 1


def _parse_table_row(line: str) -> List[str]:
    """Parse a table row into cells."""
    line = line.strip()
    if not line:
        return []
    
    # Split by pipe
    parts = line.split('|')
    
    # Remove empty first/last parts if line starts/ends with pipe
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    
    # Clean up each cell
    return [part.strip() for part in parts]


def _parse_alignments(separator_line: str) -> List[Optional[str]]:
    """Parse column alignments from separator line."""
    cells = _parse_table_row(separator_line)
    alignments = []
    
    for cell in cells:
        cell = cell.strip()
        if cell.startswith(':') and cell.endswith(':'):
            alignments.append('center')
        elif cell.endswith(':'):
            alignments.append('right')
        elif cell.startswith(':'):
            alignments.append('left')
        else:
            alignments.append(None)
    
    return alignments


def is_separator_line(line: str, expected_columns: Optional[int] = None) -> bool:
    """Check if a line is a valid table separator."""
    line_stripped = line.strip()
    if not line_stripped:
        return False
    
    parts = line_stripped.split('|')
    # Remove empty first/last parts
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    
    n_cols = len(parts)
    # Check column count
    if expected_columns is not None and n_cols != expected_columns:
        return False
    if n_cols < 1:
        return False
    
    # Verify each part is a valid separator
    for part in parts:
        clean_part = part.strip().replace(' ', '')
        if not TABLE_SEPARATOR_PATTERN.match(clean_part):
            return False
    
    return True


def locate_markdown_tables(lines: List[str]) -> List[Tuple[int, int]]:
    """Locate all tables in the given lines.
    
    Returns list of (start_line, end_line) tuples.
    """
    tables = []
    state = "outside"
    current_start = None
    current_cols = None
    n = len(lines)
    i = 0
    
    while i < n:
        line = lines[i].rstrip('\n')
        line_stripped = line.strip()
        
        if state == "outside":
            if not line_stripped:
                i += 1
                continue
            
            if '|' in line:
                # Check if it's a separator line
                if is_separator_line(line):
                    i += 1
                    continue
                
                # Parse header row
                parts = line_stripped.split('|')
                if parts and not parts[0].strip():
                    parts = parts[1:]
                if parts and not parts[-1].strip():
                    parts = parts[:-1]
                n_cols = len(parts)
                
                if n_cols < 1:
                    i += 1
                    continue
                
                # Enter header state
                current_start = i
                current_cols = n_cols
                state = "header"
                i += 1
            else:
                i += 1
        
        elif state == "header":
            if not line_stripped:
                state = "outside"
                i += 1
                continue
            
            # Check for separator line
            if is_separator_line(line, current_cols):
                state = "inside"
                i += 1
            else:
                state = "outside"
                continue
        
        elif state == "inside":
            if not line_stripped:
                tables.append((current_start, i - 1))
                state = "outside"
                i += 1
                continue
            
            # Check table row
            parts = line_stripped.split('|')
            if parts and not parts[0].strip():
                parts = parts[1:]
            if parts and not parts[-1].strip():
                parts = parts[:-1]
            n_cols = len(parts)
            
            if n_cols == current_cols:
                i += 1
            else:
                tables.append((current_start, i - 1))
                state = "outside"
                continue
    
    # Handle table at end of file
    if state == "inside":
        tables.append((current_start, n - 1))
    
    return tables 