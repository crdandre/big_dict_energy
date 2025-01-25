import unicodedata
import re
from pathlib import Path
from typing import Any, Dict, List, Union

def serialize_paths(obj: Any) -> Any:
    """Convert Path objects to strings recursively in any data structure."""
    if isinstance(obj, dict):
        return {k: serialize_paths(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_paths(item) for item in obj]
    elif isinstance(obj, Path):
        return str(obj)
    return obj

def normalize_text_fields(obj: Any) -> Any:
    """Normalize text fields and convert Path objects to strings recursively."""
    if isinstance(obj, dict):
        return {k: normalize_text_fields(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_text_fields(item) for item in obj]
    elif isinstance(obj, str):
        return normalize_unicode(obj)
    elif isinstance(obj, Path):
        return str(obj)
    return obj

def normalize_unicode(text: str) -> str:
    """Normalize Unicode characters for LLM processing while preserving mathematical meaning."""
    # Define mathematical symbols to preserve as escape sequences
    math_symbols = {
        '±': '\u00b1',
        '°': '\u00b0',
        '≥': '\u2265',
        '≤': '\u2264',
        # Basic mathematical symbols
        '→': '\u2192',
        '←': '\u2190', 
        '↔': '\u2194',
        '≠': '\u2260',
        '∞': '\u221E',
        '∑': '\u2211',
        '∏': '\u220F',
        '√': '\u221A',
        '∫': '\u222B',
        # Greek letters
        'π': '\u03C0',
        'μ': '\u03BC',
        'α': '\u03B1',
        'β': '\u03B2',
        'γ': '\u03B3',
        'δ': '\u03B4',
        'ε': '\u03B5',
        'θ': '\u03B8',
        'λ': '\u03BB',
        'σ': '\u03C3',
        'τ': '\u03C4',
        'φ': '\u03C6',
        'ω': '\u03C9',
        # Additional mathematical symbols
        'Δ': '\u0394',
        '×': '\u00D7',
        '÷': '\u00F7',
        '≈': '\u2248',
        '≡': '\u2261',
        '∝': '\u221D',
        '∂': '\u2202',
        '∇': '\u2207',
        '∈': '\u2208',
        '∉': '\u2209',
        '∋': '\u220B',
        '∌': '\u220C',
        '∩': '\u2229',
        '∪': '\u222A'
    }
    
    # First convert any direct symbols to escape sequences
    for symbol, escape_seq in math_symbols.items():
        text = text.replace(symbol, escape_seq)
    
    # Then normalize remaining Unicode to ASCII where possible
    normalized = unicodedata.normalize('NFKD', text)
    
    # Keep only non-combining characters, except preserve our escape sequences
    result = []
    i = 0
    while i < len(normalized):
        if normalized[i:i+6].startswith('\\u'):  # Check for escape sequence
            result.append(normalized[i:i+6])
            i += 6
        elif not unicodedata.combining(normalized[i]):
            result.append(normalized[i])
        i += 1
    
    return ''.join(result)