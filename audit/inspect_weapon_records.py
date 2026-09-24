"""Read-only, bounded ESM inspection; does not deserialize or rebuild plugins."""
import hashlib
import json
import struct
import zlib
from collections import Counter
from pathlib import Path

TARGETS = {0x028A02: 'Grendel', 0x253A16: 'Kodama', 0x26D960: 'Shotty', 0x2984DF: 'Maelstrom'}


def subrecords(data):
    pos = 0
    extended = None
    while pos < len(data):
        assert pos + 6 <= len(data), ('subrecord header', pos, len(data))
        tag, size = struct.unpack_from('<4sH', data, pos)
        pos += 6
        if tag == b'XXXX':
            assert size == 4 and extended is None
            extended = struct.unpack_from('<I', data, pos)[0]
            pos += 4
            continue
        if extended is not None:
            size, extended = extended, None
        assert pos + size <= len(data), (tag, pos, size, len(data))
        yield tag.decode('ascii'), data[pos:pos + size]
        pos += size
    assert pos == len(data) and extended is None


def inspect(path):
    raw = path.read_bytes()
    counts = Counter()
    found = {}
    masters = []

    def walk(start, end):
        pos = start
        while pos < end:
            assert pos + 24 <= end, ('record header', pos, end)
            tag = raw[pos:pos + 4]
            size = struct.unpack_from('<I', raw, pos + 4)[0]
            if tag == b'GRUP':
                assert size >= 24 and pos + size <= end
                walk(pos + 24, pos + size)
                pos += size
                continue
            flags, formid = struct.unpack_from('<II', raw, pos + 8)
            finish = pos + 24 + size
            assert finish <= end, ('record end', pos, finish, end)
            counts[tag.decode('ascii')] += 1
            if tag == b'TES4' or (tag == b'WEAP' and formid in TARGETS):
                body = raw[pos + 24:finish]
                if flags & 0x40000:
                    expected = struct.unpack_from('<I', body)[0]
                    body = zlib.decompress(body[4:])
                    assert len(body) == expected
                subs = list(subrecords(body))
                if tag == b'TES4':
                    masters.extend(v.rstrip(b'\0').decode('utf-8') for k, v in subs if k == 'MAST')
                else:
                    assert formid not in found
                    kw = [v for k, v in subs if k == 'KWDA']
                    assert len(kw) == 1 and len(kw[0]) % 4 == 0
                    ids = struct.unpack('<' + 'I' * (len(kw[0]) // 4), kw[0])
                    declared = [struct.unpack('<I', v)[0] for k, v in subs if k == 'KSIZ']
                    assert declared == [len(ids)], ('keyword count', declared, ids)
                    found[formid] = {
                        'name': TARGETS[formid], 'form_id': f'{formid:08X}',
                        'editor_id': next(v.rstrip(b'\0').decode('utf-8') for k, v in subs if k == 'EDID'),
                        'offset': pos, 'keyword_ids': [f'{x:08X}' for x in ids],
                        'keyword_count': len(ids),
                        'subrecord_counts': dict(Counter(k for k, v in subs)),
                        'payload_sha256': hashlib.sha256(body).hexdigest(),
                    }
            pos = finish
        assert pos == end

    walk(0, len(raw))
    assert masters and masters[0].lower() == 'starfield.esm', masters
    return {'path': path.relative_to(Path(__file__).resolve().parents[1]).as_posix(), 'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'masters': masters, 'record_counts': dict(counts),
            'weapons': list(found.values()), 'missing_targets': [TARGETS[x] for x in TARGETS if x not in found]}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    results = [inspect(p) for p in sorted((root / 'artifacts').rglob('*.esm'))]
    (root / '04-weapon-plugin-evidence.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    for result in results:
        print(json.dumps({k: result[k] for k in ('path', 'masters', 'missing_targets', 'weapons')}, indent=2))
