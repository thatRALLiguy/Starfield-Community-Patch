# Released plugin comparison: four weapons

Checked 2026-09-23 using the user's downloaded SFCP 1.0.0 ZIP and USFP 1.1.0 7z. DLC archives were not inspected; this pass is limited to the four base-game weapons from audit 01.

## Result

All four WEAP records exist in the downloaded SFCP plugin. Their KWDA keyword arrays match USFP exactly, including ordering. These records are missing from the older GitHub export, not from this release file.

| Weapon | FormID in Starfield.esm | SFCP keywords | USFP keywords | Exact keyword-array match |
|---|---|---:|---:|---|
| Grendel | 00028A02 | 16 | 16 | Yes |
| Kodama | 00253A16 | 16 | 16 | Yes |
| Shotty | 0026D960 | 16 | 16 | Yes |
| Maelstrom | 002984DF | 15 | 15 | Yes |

Every keyword in this comparison references master index 00, and both plugins identify Starfield.esm as their first master, so differing master orders do not invalidate these keyword comparisons.

The whole weapon payloads do NOT match. For example, USFP has a QUPA subrecord and three BFCB/BFCE occurrences in each of these weapons; SFCP has no QUPA and two BFCB/BFCE occurrences. This inspection does not decode those structures or attribute differences to particular game changes. A current vanilla comparison is still needed before deciding what to update.

The matching keyword arrays support the two changelogs' agreement about the automatic-keyword fix. No vanilla master was supplied or read, so this pass does not independently map keyword IDs to editor names, demonstrate which keyword was removed relative to vanilla, or prove gameplay behavior.

## Method and validation

Only the two main ESMs and the bundled USFP version history were extracted into audit/artifacts. The originals were not modified, and nothing was installed into the game. Extracted third-party files are ignored by Git locally.

The read-only inspect_weapon_records.py utility walks record/group boundaries, checks sizes, decompresses selected records when flagged, validates subrecord boundaries including extended sizes, and checks KSIZ against KWDA length. It found all four expected FormIDs once per plugin, with matching editor names. It traversed both plugins to their exact end boundaries. It is a targeted inspector, not a replacement for xEdit or a complete semantic plugin validator.

Raw keyword IDs, record offsets, master lists, and plugin SHA-256 hashes are saved in 04-weapon-plugin-evidence.json. Run `python audit/inspect_weapon_records.py` to reproduce extraction of that evidence from the local ESM copies.

Input archive hashes:

- SFCP: FAAF8384B6244EF9F7E559C7DF1EB125F62AA772EA287A3FD77169B031480DAD
- USFP: 82C7D13D6620C341DDE96C99DE9289790AD50536B5FB6F121AC4FC713B9F7416

## Next step

Recover and validate the GitHub source baseline from the supplied released SFCP plugin before adding fixes. Preserve this downloaded release as a reference. Do not copy entire USFP weapon records based on keyword agreement: other field differences still need attribution against current vanilla.
