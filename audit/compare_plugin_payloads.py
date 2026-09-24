"""Compare decompressed record payloads, independent of compression and record order."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zlib

from inspect_weapon_records import subrecords


def inventory(path):
    raw = path.read_bytes()
    records = {}

    def walk(start, end, groups=()):
        pos = start
        while pos < end:
            assert pos + 24 <= end
            sig, size, flags, fid, vc, version, unknown = struct.unpack_from('<4sIIIIHH', raw, pos)
            if sig == b'GRUP':
                assert size >= 24 and pos + size <= end
                # Group label/type identify record membership; timestamp is metadata.
                walk(pos + 24, pos + size, groups + (raw[pos + 8:pos + 16].hex(),))
                pos += size
                continue
            finish = pos + 24 + size
            assert finish <= end
            payload = raw[pos + 24:finish]
            if flags & 0x40000:
                expected = struct.unpack_from('<I', payload)[0]
                payload = zlib.decompress(payload[4:])
                assert len(payload) == expected
            key = f'{sig.decode("ascii")}:{fid:08X}'
            assert key not in records, key
            records[key] = {'flags': flags & ~0x40000, 'version': version,
                            'unknown': unknown, 'groups': groups,
                            'subs': list(subrecords(payload)), 'payload': payload}
            pos = finish
        assert pos == end

    walk(0, len(raw))
    return records, hashlib.sha256(raw).hexdigest()


def compare(a, b):
    left, left_hash = inventory(a)
    right, right_hash = inventory(b)
    changed = []
    exact = 0
    for key in sorted(left.keys() & right.keys()):
        x, y = left[key], right[key]
        if x == y:
            exact += 1
            continue
        detail = {'record': key}
        for field in ('flags', 'version', 'unknown', 'groups'):
            if x[field] != y[field]:
                detail[field] = {'source': x[field], 'rebuilt': y[field]}
        if x['payload'] != y['payload']:
            detail['source_subrecords'] = len(x['subs'])
            detail['rebuilt_subrecords'] = len(y['subs'])
            # Multiset comparison separates reordered data from changed values.
            before, after = Counter(x['subs']), Counter(y['subs'])
            detail['removed'] = [{'type': k, 'size': len(v), 'count': n,
                                  'hex': v.hex() if len(v) <= 64 else None,
                                  'sha256': hashlib.sha256(v).hexdigest()}
                                 for (k, v), n in (before - after).items()]
            detail['added'] = [{'type': k, 'size': len(v), 'count': n,
                                'hex': v.hex() if len(v) <= 64 else None,
                                'sha256': hashlib.sha256(v).hexdigest()}
                               for (k, v), n in (after - before).items()]
            detail['order_only'] = before == after
        changed.append(detail)
    return {'source_sha256': left_hash, 'rebuilt_sha256': right_hash,
            'source_records': len(left), 'rebuilt_records': len(right),
            'missing': sorted(left.keys() - right.keys()), 'added': sorted(right.keys() - left.keys()),
            'exact_records': exact, 'differences': changed}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('rebuilt', type=Path)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    report = compare(args.source, args.rebuilt)
    args.report.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'differences'}, indent=2))
    print('Differing records:', len(report['differences']))
