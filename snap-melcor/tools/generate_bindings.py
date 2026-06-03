"""Generate Python bindings for MELCOR SNAP plugin components.

Parses Java BeanInfo and SelEditor source files from the SNAP-MELCOR-plugin
and produces two Python modules:

  snap_melcor/bindings/enums.py      — enum classes from *SelEditor.java
  snap_melcor/bindings/components.py — component wrappers from *BeanInfo.java

Usage:
    python tools/generate_bindings.py \
        --melcor-src /path/to/SNAP-MELCOR-plugin/src/cfnplugin/melcor \
        --out-dir snap_melcor/bindings
"""
from __future__ import annotations

import argparse
import keyword
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Editor class name → Python property type
# ---------------------------------------------------------------------------
# Rules applied in order; first match wins.
# Value is (python_type, notes)
EDITOR_TYPE_MAP: list[tuple[re.Pattern, str]] = [
    # Enum selectors
    (re.compile(r'\w+SelEditor$'), 'enum'),
    # String / name editors
    (re.compile(r'(LimitedLongStringEditor|MelcorComponentNameEditor'
                r'|CNamelistStringEditor|StringEditor)$'), 'string'),
    # Integer editors
    (re.compile(r'(IntNonMultiEdit|IntEdit|CNamelistIntEditor'
                r'|IntegerEditor)$'), 'int'),
    # Boolean / toggle editors
    (re.compile(r'(NLYNSelEditor|BooleanEditor|CheckBoxEditor)$'), 'bool'),
    # Optional real (active/inactive flag companion)
    (re.compile(r'CNamelistRealEditor$'), 'real_optional'),
    # Reference editors (required)
    (re.compile(r'\w+IdentEditor$'), 'reference'),
    # Reference editors (optional)
    (re.compile(r'\w+IdentEmptyEditor$'), 'reference_optional'),
    # Tabular function identifiers
    (re.compile(r'TabularFunctionIdent'), 'tabfunc_ref'),
    # Control function identifiers
    (re.compile(r'ControlFunctionIdent'), 'ctlfunc_ref'),
    # Default fallback
    (re.compile(r'.*'), 'real'),
]


def _editor_to_type(editor_class: str) -> str:
    """Map a Java editor class name to a Python property type string."""
    for pattern, ptype in EDITOR_TYPE_MAP:
        if pattern.match(editor_class):
            return ptype
    return 'real'


# ---------------------------------------------------------------------------
# Enum (SelEditor) parsing
# ---------------------------------------------------------------------------

_OPTVAL_RE = re.compile(
    r'int\[\]\s+optVal\s*=\s*\{([^}]+)\}', re.DOTALL)
_OPTSTR_RE = re.compile(
    r'String\[\]\s+optStr\s*=\s*\{([^}]+)\}', re.DOTALL)
_STRING_LITERAL_RE = re.compile(r'"([^"]*)"')
_INT_LITERAL_RE = re.compile(r'-?\d+')
_CLASS_NAME_RE = re.compile(r'public class\s+(\w+)\s+extends')


def _strip_editor_suffix(name: str) -> str:
    """Remove 'Editor' suffix to get enum class name."""
    if name.endswith('Editor'):
        return name[:-len('Editor')]
    return name


_PYTHON_BUILTINS = frozenset({'None', 'True', 'False'})


def _clean_enum_name(raw: str) -> str:
    """Convert a SelEditor option string to a valid Python identifier."""
    # Replace spaces, hyphens, slashes, dots, parens with underscores
    name = re.sub(r'[^A-Za-z0-9_]', '_', raw)
    # Collapse consecutive underscores
    name = re.sub(r'_+', '_', name).strip('_')
    # Ensure it doesn't start with a digit
    if name and name[0].isdigit():
        name = 'v_' + name
    # Escape Python keywords and built-in singletons
    if keyword.iskeyword(name) or name in _PYTHON_BUILTINS:
        name = name + '_'
    return name or 'unknown'


def parse_sel_editor(java_path: Path) -> dict | None:
    """Parse a *SelEditor.java file and return enum metadata dict or None."""
    text = java_path.read_text(encoding='utf-8', errors='replace')

    class_match = _CLASS_NAME_RE.search(text)
    if not class_match:
        return None
    java_class = class_match.group(1)
    enum_name = _strip_editor_suffix(java_class)

    optval_match = _OPTVAL_RE.search(text)
    optstr_match = _OPTSTR_RE.search(text)
    if not optval_match or not optstr_match:
        return None

    values = [int(v) for v in _INT_LITERAL_RE.findall(optval_match.group(1))]
    labels = _STRING_LITERAL_RE.findall(optstr_match.group(1))

    if not values or not labels or len(values) != len(labels):
        return None

    return {
        'java_class': java_class,
        'enum_name': enum_name,
        'values': values,
        'labels': labels,
    }


def generate_enum_class(meta: dict) -> list[str]:
    """Render Python source lines for one enum class."""
    enum_name = meta['enum_name']
    lines: list[str] = []
    lines.append(f'class {enum_name}(object):')
    lines.append(f'    """Enumeration of {enum_name} values."""')
    lines.append('')
    lines.append(f'    def __init__(self, name, value):')
    lines.append(f'        object.__init__(self)')
    lines.append(f'        self._name = name')
    lines.append(f'        self._value = value')
    lines.append('')
    lines.append(f'    def __eq__(self, other):')
    lines.append(f'        if type(self) != type(other):')
    lines.append(f'            return False')
    lines.append(f'        return self._name == other._name and self._value == other._value')
    lines.append('')
    lines.append(f'    def __repr__(self):')
    lines.append(f'        return "{{}}.{{}}".format(type(self).__name__, self._name)')
    lines.append('')
    lines.append(f'    @property')
    lines.append(f'    def value(self):')
    lines.append(f'        return self._value')
    lines.append('')
    lines.append(f'    @staticmethod')
    lines.append(f'    def _for_value(v):')
    lines.append(f'        """Return the {enum_name} instance for a given integer value."""')
    lines.append(f'        _MAP = {{')
    for val, label in zip(meta['values'], meta['labels']):
        pname = _clean_enum_name(label)
        lines.append(f'            {val}: {enum_name}.{pname}(),')
    lines.append(f'        }}')
    lines.append(f'        return _MAP.get(v, {enum_name}("unknown_{{}}".format(v), v))')
    lines.append('')
    for val, label in zip(meta['values'], meta['labels']):
        pname = _clean_enum_name(label)
        lines.append(f'    @staticmethod')
        lines.append(f'    def {pname}():')
        lines.append(f'        """Returns the {enum_name} value for {label!r}."""')
        lines.append(f'        return {enum_name}({pname!r}, {val})')
        lines.append('')
    lines.append('')
    return lines


def build_enums_module(sel_editor_dir: Path) -> str:
    """Parse all *SelEditor.java files and generate enums.py content."""
    metas = []
    for jfile in sorted(sel_editor_dir.glob('*SelEditor.java')):
        meta = parse_sel_editor(jfile)
        if meta:
            metas.append(meta)

    header = [
        '"""Auto-generated MELCOR enum classes.',
        '',
        'Generated from *SelEditor.java files in cfnplugin.melcor.editors.enums.',
        'Do not edit by hand — re-run tools/generate_bindings.py instead.',
        '"""',
        '',
        '',
    ]
    body: list[str] = []
    for meta in metas:
        body.extend(generate_enum_class(meta))

    # Patch: the _for_value staticmethod references class methods by name, but
    # those are defined after _for_value. Replace with lambda-based lazy map.
    return '\n'.join(header + body)


# ---------------------------------------------------------------------------
# Java class hierarchy parsing
# ---------------------------------------------------------------------------

_JAVA_CLASS_DEF_RE = re.compile(
    r'public\s+(?:abstract\s+)?class\s+(\w+)\s+extends\s+(\w+)')


def build_superclass_map(components_dir: Path) -> dict[str, str]:
    """Parse *.java (not BeanInfo) to build {ClassName: SuperclassName} map."""
    superclass_map: dict[str, str] = {}
    for jfile in components_dir.glob('*.java'):
        if jfile.name.endswith('BeanInfo.java'):
            continue
        try:
            text = jfile.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        for m in _JAVA_CLASS_DEF_RE.finditer(text):
            superclass_map[m.group(1)] = m.group(2)
    return superclass_map


# ---------------------------------------------------------------------------
# BeanInfo (component) parsing
# ---------------------------------------------------------------------------

_BEAN_CLASS_RE = re.compile(r'beanClass\s*=\s*(\w+)\.class')
_PROP_BLOCK_START_RE = re.compile(
    r'pd\[(\d+)\]\s*=\s*new\s+((?:Indexed)?PropertyDescriptor)\(')
_PROP_NAME_RE = re.compile(r'"(\w+)"')
_GETTER_SETTER_RE = re.compile(
    r'new\s+PropertyDescriptor\s*\(\s*"(\w+)"\s*,\s*\w+\s*,\s*"(\w+)"\s*,\s*"(\w+)"')
_DISPLAY_NAME_RE = re.compile(r'\.setDisplayName\("([^"]*)"\)')
_SHORT_DESC_RE = re.compile(r'\.setShortDescription\("([^"]*)"\)')
_EDITOR_CLASS_RE = re.compile(r'\.setPropertyEditorClass\((\w+)\.class\)')
_HIDDEN_RE = re.compile(r'\.setHidden\(true\)')
_PROP_COUNT_RE = re.compile(r'PropertyDescriptor\s+pd\[\]\s*=\s*new\s+PropertyDescriptor\[(\d+)\]')


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case, preserving consecutive caps."""
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    s2 = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def _safe_prop_name(name: str) -> str:
    """Ensure a property name is a valid Python identifier (not a keyword)."""
    if keyword.iskeyword(name) or name in _PYTHON_BUILTINS:
        return name + '_'
    if not name.isidentifier():
        return re.sub(r'[^A-Za-z0-9_]', '_', name)
    return name


def parse_bean_info(java_path: Path) -> dict | None:
    """Parse a *BeanInfo.java file and return component metadata dict or None."""
    text = java_path.read_text(encoding='utf-8', errors='replace')

    # Class name
    class_match = _CLASS_NAME_RE.search(text)
    if not class_match:
        return None
    bi_class = class_match.group(1)
    if not bi_class.endswith('BeanInfo'):
        return None
    comp_class = bi_class[:-len('BeanInfo')]

    # Bean target class (the actual component class, not BeanInfo)
    bean_match = _BEAN_CLASS_RE.search(text)
    bean_class = bean_match.group(1) if bean_match else comp_class

    # Find the getPropertyDescriptors method body
    pd_start = text.find('getPropertyDescriptors()')
    if pd_start == -1:
        return {'class': comp_class, 'bean_class': bean_class, 'properties': []}
    pd_body = text[pd_start:]

    # Split into per-property blocks on pd[N] = new ...Descriptor(
    blocks = re.split(r'(?=pd\[\d+\]\s*=\s*new\s+(?:Indexed)?PropertyDescriptor)', pd_body)

    properties: list[dict] = []
    for block in blocks:
        pm = _PROP_BLOCK_START_RE.match(block.strip())
        if not pm:
            continue
        is_indexed = 'IndexedPropertyDescriptor' in pm.group(2)
        if is_indexed:
            continue  # skip indexed properties

        # Extract property name
        name_match = _PROP_NAME_RE.search(block.split('=')[1].split(')')[0])
        if not name_match:
            continue
        prop_name = name_match.group(1)

        # Skip internal/meta properties
        if prop_name in ('ident', 'majorCreationVersion', 'majorVersion',
                         'minorCreationVersion', 'minorVersion'):
            continue

        # Custom getter/setter
        gs_match = _GETTER_SETTER_RE.search(block)
        getter = gs_match.group(2) if gs_match else f'get{prop_name[0].upper()}{prop_name[1:]}'
        setter = gs_match.group(3) if gs_match else f'set{prop_name[0].upper()}{prop_name[1:]}'

        # Attributes
        display_match = _DISPLAY_NAME_RE.search(block)
        display_name = display_match.group(1) if display_match else prop_name

        desc_match = _SHORT_DESC_RE.search(block)
        description = desc_match.group(1) if desc_match else ''

        editor_match = _EDITOR_CLASS_RE.search(block)
        editor_class = editor_match.group(1) if editor_match else None

        hidden = bool(_HIDDEN_RE.search(block))

        prop_type = _editor_to_type(editor_class) if editor_class else 'real'

        # Determine enum class name if applicable
        enum_class = None
        if prop_type == 'enum' and editor_class:
            enum_class = _strip_editor_suffix(editor_class)

        properties.append({
            'name': prop_name,
            'getter': getter,
            'setter': setter,
            'display_name': display_name,
            'description': description[:200],  # truncate long descriptions
            'editor_class': editor_class,
            'prop_type': prop_type,
            'enum_class': enum_class,
            'hidden': hidden,
        })

    return {'class': comp_class, 'bean_class': bean_class, 'properties': properties}


def _prop_getter_body(prop: dict, class_name: str) -> list[str]:
    """Generate the getter body for a property."""
    ptype = prop['prop_type']
    getter = prop['getter']
    lines = []
    if ptype == 'enum':
        enum_cls = prop['enum_class'] or 'object'
        lines.append(f'        raw = self.java_object.{getter}()')
        lines.append(f'        return EnumProperty(True, True, '
                     f'{enum_cls}._for_value(raw))')
    elif ptype == 'string':
        lines.append(f'        return StringProperty(True, True, '
                     f'self.java_object.{getter}(), ref_allowed=True)')
    elif ptype in ('int',):
        lines.append(f'        return IntegerProperty(True, True, '
                     f'self.java_object.{getter}())')
    elif ptype == 'bool':
        lines.append(f'        return BooleanProperty(True, True, '
                     f'self.java_object.{getter}())')
    elif ptype in ('real', 'real_optional'):
        lines.append(f'        return RealProperty(True, True, '
                     f'self.java_object.{getter}())')
    elif ptype in ('reference', 'reference_optional',
                   'tabfunc_ref', 'ctlfunc_ref'):
        lines.append(f'        raw = self.java_object.{getter}()')
        lines.append(f'        return str(raw) if raw is not None else None')
    else:
        lines.append(f'        return self.java_object.{getter}()')
    return lines


def _prop_setter_body(prop: dict) -> list[str]:
    """Generate the setter body for a property."""
    ptype = prop['prop_type']
    setter = prop['setter']
    lines = []
    if ptype == 'enum':
        lines.append(f'        java_value = value.value if hasattr(value, "value") else int(value)')
        lines.append(f'        self.java_object.{setter}(java_value)')
    elif ptype == 'string':
        lines.append(f'        self.java_object.{setter}(str(value))')
    elif ptype in ('int',):
        lines.append(f'        self.java_object.{setter}(int(value))')
    elif ptype == 'bool':
        lines.append(f'        self.java_object.{setter}(bool(value))')
    elif ptype in ('real', 'real_optional'):
        lines.append(f'        real = self.java_object.{prop["getter"]}()')
        lines.append(f'        real.convert(float(value))')
        lines.append(f'        self.java_object.{setter}(real.getValue())')
    elif ptype in ('reference', 'reference_optional',
                   'tabfunc_ref', 'ctlfunc_ref'):
        lines.append(f'        self.java_object.{setter}(value)')
    else:
        lines.append(f'        self.java_object.{setter}(value)')
    return lines


def _sanitize_docstring(text: str) -> str:
    """Make a Java description safe to embed in a Python triple-quoted string."""
    # Collapse Java escape sequences to plain text
    text = text.replace('\\n', ' ').replace('\\r', '').replace('\\"', '"')
    text = text.replace('\\\\', '\\')
    # Replace any remaining triple-quote sequences
    text = text.replace('"""', "'''")
    # Strip trailing backslashes to avoid `\"""` terminating early
    text = text.rstrip('\\')
    return text.strip()


def _prop_schema_entry(prop: dict) -> str:
    """Render a schema dict entry for this property (used in _SCHEMA)."""
    desc = _sanitize_docstring(prop["description"])[:120]
    disp = _sanitize_docstring(prop["display_name"])
    return (f'        {prop["name"]!r}: {{'
            f'"display": {disp!r}, '
            f'"type": {prop["prop_type"]!r}, '
            f'"description": {desc!r}'
            f'}},')


def generate_component_class(
    meta: dict,
    known_enums: set[str],
    known_classes: set[str],
    superclass_map: dict[str, str],
) -> list[str]:
    """Render Python source lines for one component wrapper class."""
    comp_class = meta['class']
    props = [p for p in meta['properties'] if not p['hidden']]

    # Determine Python base class: use the mapped Java superclass if known
    java_super = superclass_map.get(comp_class, '')
    if java_super and java_super in known_classes:
        py_base = java_super
    else:
        py_base = 'SnapComponent'

    lines: list[str] = []
    lines.append(f'class {comp_class}({py_base}):')
    lines.append(f'    """MELCOR {comp_class} component wrapper."""')
    lines.append('')
    lines.append(f'    def __init__(self, med_model, java_object):')
    lines.append(f'        {py_base}.__init__(self, med_model, java_object)')
    lines.append('')

    # Schema dict for MCP introspection
    lines.append(f'    _SCHEMA = {{')
    for prop in props:
        lines.append(_prop_schema_entry(prop))
    lines.append(f'    }}')
    lines.append('')

    for prop in props:
        pname = _safe_prop_name(prop['name'])
        ptype = prop['prop_type']
        enum_cls = prop.get('enum_class')

        # Validate enum class exists
        if ptype == 'enum' and enum_cls not in known_enums:
            ptype = 'real'  # fall back gracefully

        # Getter
        safe_desc = _sanitize_docstring(prop["description"])[:80]
        safe_disp = _sanitize_docstring(prop["display_name"])
        lines.append(f'    @property')
        lines.append(f'    def {pname}(self):')
        lines.append(f'        """[{safe_disp}] {safe_desc}"""')
        lines.append(f'        try:')
        for body_line in _prop_getter_body(prop, comp_class):
            lines.append(f'    {body_line}')
        lines.append(f'        except Exception:')
        lines.append(f'            return None')
        lines.append('')

        # Setter
        lines.append(f'    @{pname}.setter')
        lines.append(f'    def {pname}(self, value):')
        lines.append(f'        """Set {pname} ({ptype})."""')
        lines.append(f'        try:')
        for body_line in _prop_setter_body(prop):
            lines.append(f'    {body_line}')
        lines.append(f'        except Exception as exc:')
        lines.append(f'            raise ValueError('
                     f'"Cannot set {pname!r}: {{}}".format(exc)) from exc')
        lines.append('')

    lines.append('')
    return lines


def _topo_sort(
    metas: list[dict],
    superclass_map: dict[str, str],
    known_classes: set[str],
) -> list[dict]:
    """Return metas sorted so base classes appear before derived classes."""
    by_name = {m['class']: m for m in metas}
    order: list[dict] = []
    visited: set[str] = set()

    def visit(name: str):
        if name in visited or name not in by_name:
            return
        visited.add(name)
        parent = superclass_map.get(name)
        if parent and parent in known_classes:
            visit(parent)
        order.append(by_name[name])

    for m in metas:
        visit(m['class'])

    return order


def build_components_module(
    components_dir: Path,
    known_enums: set[str],
) -> str:
    """Parse all *BeanInfo.java files and generate components.py content."""
    metas = []
    for jfile in sorted(components_dir.glob('*BeanInfo.java')):
        meta = parse_bean_info(jfile)
        if meta:
            metas.append(meta)

    superclass_map = build_superclass_map(components_dir)
    known_classes = {m['class'] for m in metas}

    # Topological sort: base classes before derived
    metas = _topo_sort(metas, superclass_map, known_classes)

    header = [
        '"""Auto-generated MELCOR component wrapper classes.',
        '',
        'Generated from *BeanInfo.java files in cfnplugin.melcor.components.',
        'Do not edit by hand — re-run tools/generate_bindings.py instead.',
        '"""',
        'from __future__ import annotations',
        '',
        'try:',
        '    from snap.codes.properties import (',
        '        SnapComponent, ModelElement, RealProperty, BooleanProperty,',
        '        IntegerProperty, StringProperty, EnumProperty,',
        '    )',
        'except ImportError:',
        '    # Stub bases for schema-only usage without SNAP installed',
        '    class _Base:',
        '        def __init__(self, *a, **kw): pass',
        '    SnapComponent = ModelElement = RealProperty = BooleanProperty = _Base',
        '    IntegerProperty = StringProperty = EnumProperty = _Base',
        '',
        'try:',
        '    from snap_melcor.bindings.enums import *',
        'except ImportError:',
        '    pass',
        '',
        '',
    ]

    body: list[str] = []
    for meta in metas:
        body.extend(generate_component_class(
            meta, known_enums, known_classes, superclass_map))

    # Build __all__ list
    all_names = [f'    {m["class"]!r},' for m in metas]
    all_block = ['__all__ = ['] + all_names + [']', '']

    return '\n'.join(header + all_block + body)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--melcor-src',
        required=True,
        type=Path,
        help='Path to cfnplugin/melcor in the SNAP-MELCOR-plugin source tree',
    )
    parser.add_argument(
        '--out-dir',
        required=True,
        type=Path,
        help='Output directory for generated Python modules',
    )
    args = parser.parse_args()

    melcor_src: Path = args.melcor_src
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    enums_dir = melcor_src / 'editors' / 'enums'
    components_dir = melcor_src / 'components'

    if not enums_dir.is_dir():
        print(f'ERROR: enums dir not found: {enums_dir}', file=sys.stderr)
        sys.exit(1)
    if not components_dir.is_dir():
        print(f'ERROR: components dir not found: {components_dir}', file=sys.stderr)
        sys.exit(1)

    print(f'Parsing SelEditor files in {enums_dir}...')
    enums_src = build_enums_module(enums_dir)
    enums_out = out_dir / 'enums.py'
    enums_out.write_text(enums_src, encoding='utf-8')
    enum_count = enums_src.count('\nclass ')
    print(f'  Wrote {enum_count} enum classes → {enums_out}')

    # Collect known enum names for validation
    known_enums: set[str] = set(re.findall(r'^class (\w+)\(object\):', enums_src, re.M))

    print(f'Parsing BeanInfo files in {components_dir}...')
    components_src = build_components_module(components_dir, known_enums)
    components_out = out_dir / 'components.py'
    components_out.write_text(components_src, encoding='utf-8')
    comp_count = components_src.count('\nclass ')
    print(f'  Wrote {comp_count} component classes → {components_out}')

    # Write __init__.py
    init_out = out_dir / '__init__.py'
    if not init_out.exists():
        init_out.write_text(
            '"""Auto-generated MELCOR Python bindings."""\n'
            'from snap_melcor.bindings.enums import *\n'
            'from snap_melcor.bindings.components import *\n',
            encoding='utf-8',
        )
        print(f'  Wrote {init_out}')

    print('Done.')


if __name__ == '__main__':
    main()
