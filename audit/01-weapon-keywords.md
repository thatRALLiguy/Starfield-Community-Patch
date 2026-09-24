# Pilot audit: four automatic-weapon keywords

Checked: 2026-09-23. Scope: Grendel, Kodama, Shotty, and Maelstrom only.

Community Patch snapshot: `thatRALLiguy/Starfield-Community-Patch` at `0ad97d3eb087dafb91afbc4bbb1588598212cc87` (2024-09-30).

## Result

Resolved by binary inspection: all four weapon records are present in the user-supplied SFCP 1.0.0 release, and each keyword array exactly matches USFP 1.1.0. See 04-released-weapon-comparison.md and 04-weapon-plugin-evidence.json. The absence described below applies to GitHub's older source export.

Follow-up: the source export is stale. The entire spriggit directory has the identical Git tree SHA at the June 17, 2024 export and current upstream main. See 03-source-export-history.md. The four September changelog fixes therefore cannot be evaluated as missing from the distributed release merely because this older export omits them.

The two changelogs agree on the intended correction: remove WeaponTypeAutomatic from the four base weapons. However, the four corresponding weapon YAML records were not found in the fork's source tree. Treat this as a source/changelog discrepancy requiring verification, not proof that the distributed patch lacks the fix.

| Weapon | Starfield.esm FormID | SFCP 1.0.0 changelog | USFP 1.0.9 changelog | Fork source check |
|---|---|---|---|---|
| Grendel | 00028A02 | Remove base automatic keyword | Same intended fix, issue 36491 | No matching weapon file |
| Kodama | 00253A16 | Remove base automatic keyword | Same intended fix, issue 36491 | No matching weapon file |
| Shotty | 0026D960 | Remove base automatic keyword | Same intended fix, issue 36491 | No matching weapon file |
| Maelstrom | 002984DF | Remove base automatic keyword | Same intended fix, issue 36491 | No matching weapon file |

SFCP explains that receiver modifications provide the keyword and that the base keyword interfered with perk behavior for semi-automatic configurations. USFP documents the same four base-form corrections in its May 14, 2026 release. The live USFP changelog does not mark this entry as superseded by Bethesda.

## Evidence and limits

- Inspected the complete GitHub recursive tree (truncated=false), searched paths for all four names and normalized six-digit IDs, and independently listed spriggit/Weapons. The directory contains 18 ship weapon record files plus GroupRecordData.yaml; none of the four handheld weapons appears.
- Weapons/GroupRecordData.yaml contains only LastModified metadata. Root spriggit/RecordData.yaml contains no matching name or ID.
- The build workflow deserializes spriggit directly into StarfieldCommunityPatch.esm. This makes the missing source records worth checking against the distributed release.
- No USFP plugin, released SFCP plugin, or current vanilla master was examined. No field-level equivalence, current bug reproduction, or gameplay compatibility is established.
- No patch records were changed.

## Next bounded check

Inspect only these four records in the distributed SFCP plugin, current vanilla master, and USFP plugin. Confirm the FormID of WeaponTypeAutomatic, compare keyword lists, and check receiver behavior. If the distributed SFCP contains fixes absent from Git, first resolve which source is authoritative. Any eventual override should preserve current vanilla fields outside the intended fix.

## Sources

- [Pinned SFCP changelog](https://github.com/thatRALLiguy/Starfield-Community-Patch/blob/0ad97d3eb087dafb91afbc4bbb1588598212cc87/CHANGELOG.md), version 1.0.0, Item Fixes, issue 662.
- [Pinned weapon source directory](https://github.com/thatRALLiguy/Starfield-Community-Patch/tree/0ad97d3eb087dafb91afbc4bbb1588598212cc87/spriggit/Weapons).
- [Pinned build workflow](https://github.com/thatRALLiguy/Starfield-Community-Patch/blob/0ad97d3eb087dafb91afbc4bbb1588598212cc87/.github/workflows/build-release.yml).
- [USFP version history](https://www.afkmods.com/Unofficial%20Starfield%20Patch%20Version%20History.html), version 1.0.9, issue 36491; accessed 2026-09-23.
